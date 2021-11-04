from abc import ABC
from collections import Counter

import h3
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.filters import TMSTileFilter, InBBoxFilter

from facilities.models import SportsArea
from sport_density.models import DataHexSmall, DataHexBig
from sport_density.serializers import (
    DataHexSmallSerializer,
    BaseHexIntersectionsSerializer,
    DataHexBigSerializer,
    BaseDataHexSmallSerializer,
    BaseDataHexBigSerializer,
    DetailDataHexBigSerializer,
    DetailDataHexSmallSerializer,
)


class BaseHexViewSet(ReadOnlyModelViewSet, ABC):
    filter_backends = [TMSTileFilter, InBBoxFilter]
    bbox_filter_field = "polygon"
    bbox_filter_include_overlapping = True
    pagination_class = LimitOffsetPagination
    h3_resolution = 8

    def get_queryset(self):
        if self.action == "sport_density":
            return self.queryset.annotate_areas()
        if self.action == "hexes_report":
            return self.queryset
        if self.action == "population_density" or self.action == 'list':
            return self.queryset.populated()

        return (
            self.queryset
            .populated()
            .annotate_areas()
            .annotate_square_by_person()
        )

    def filter_queryset(self, queryset):
        if self.action == "hexes_report":
            hex_ids = self.request.query_params.getlist("ids", [])
            hex_ids = [int(hex_id) for hex_id in hex_ids]
            return super().filter_queryset(queryset.filter(pk__in=hex_ids))
        if self.action in ("list", "sport_density"):
            sport_ids = self.request.query_params.getlist("sports", [])
            area_type = self.request.query_params.get("area_type", None)
            availability = self.request.query_params.get("availability", None)
            department = self.request.query_params.get("department", None)
            areas_filter = None
            filters = []
            if sport_ids:
                filters.append(Q(facilities__areas__sports__contains=sport_ids))
            if area_type is not None:
                filters.append(Q(facilities__areas__type=area_type))
            if availability is not None:
                filters.append(Q(facilities__availability=availability))
            if department is not None:
                filters.append(Q(facilities__department=department))

            if filters:
                areas_filter = filters[0]
                for filter_ in filters:
                    areas_filter &= filter_

            return super().filter_queryset(
                self.queryset
                .populated()
                .annotate_areas(areas_filter=areas_filter)
                .annotate_square_by_person()
            )
        return super().filter_queryset(queryset)

    @action(detail=False, url_path="sport-density")
    def sport_density(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=False, url_path="population-density")
    def population_density(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=False, url_path="hexes-report")
    def hexes_report(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if not qs:
            return Response([])
        hexes = []
        total_population = 0
        for hex_ in qs:
            total_population += hex_.population
            hex_ = h3.geo_to_h3(
                hex_.polygon.centroid.x, hex_.polygon.centroid.y, self.h3_resolution
            )
            hexes.append(hex_)
        total_square = h3.hex_area(self.h3_resolution) * len(hexes)

        areas = self.get_areas()

        all_sports = list(set(areas.get_all_sports()))
        area_types_coverage = {}
        for row in areas.get_sports_coverage():
            area_types_coverage[row["type"]] = row["square__sum"]
        sports_counter = Counter(all_sports)
        areas_stats = areas.get_stats()
        area_types_counter = Counter(areas_stats["area_types"])
        polygon = h3.h3_set_to_multi_polygon(hexes, geo_json=True)
        return Response(
            {
                "polygon": {
                    "type": "MultiPolygon",
                    "coordinates": polygon,
                },
                "total_square": total_square,
                "area_types_counter": area_types_counter,
                "total_sport_square": areas_stats["total_sport_square"],
                "sports_counts": sports_counter,
                "area_types_coverage": area_types_coverage,
            }
        )


class SmallHexViewSet(BaseHexViewSet):
    queryset = DataHexSmall.objects.all()
    serializer_class = DetailDataHexSmallSerializer
    h3_resolution = 9

    def get_serializer_class(self):
        if self.action == "sport_density":
            return DataHexSmallSerializer
        if self.action == "population_density":
            return BaseDataHexSmallSerializer
        return self.serializer_class

    def get_areas(self):
        return SportsArea.objects.filter(
            facility__hexes__id__in=self.request.query_params.getlist("ids")
        ).distinct()


class BigHexViewSet(BaseHexViewSet):
    queryset = DataHexBig.objects.all()
    serializer_class = DetailDataHexBigSerializer
    h3_resolution = 8

    def get_serializer_class(self):
        if self.action == "sport_density":
            return DataHexBigSerializer
        if self.action == "population_density":
            return BaseDataHexBigSerializer
        return self.serializer_class

    def get_areas(self):
        return SportsArea.objects.filter(
            facility__big_hexes__id__in=self.request.query_params.getlist("ids")
        ).distinct()


class HexIntersectionViewSet(ReadOnlyModelViewSet):
    queryset = DataHexSmall.objects.all()
    serializer_class = BaseHexIntersectionsSerializer
    filter_backends = [TMSTileFilter, InBBoxFilter]
    bbox_filter_field = "polygon"
    bbox_filter_include_overlapping = True
    pagination_class = LimitOffsetPagination
