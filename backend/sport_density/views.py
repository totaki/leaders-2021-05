from abc import ABC

from django.db.models import Sum, Count, F, Case, When
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.filters import TMSTileFilter, InBBoxFilter

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

    def get_queryset(self):
        if self.action == "sport_density":
            return self.queryset.annotate(
                square=Sum("facilities__areas__square"),
                areas_count=Count("facilities__areas"),
            )
        if self.action == "population_density":
            return self.queryset.filter(flats__gt=0)
        if self.action == "list":
            return self.queryset.annotate(
                square=Sum("facilities__areas__square"),
                areas_count=Count("facilities__areas"),
            ).annotate(
                square_by_person=Case(
                    When(flats=0, then=None),
                    default=F("square") * 4.5 / F("flats"),
                )
            )
        return self.queryset

    @action(detail=False, url_path="sport-density")
    def sport_density(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=False, url_path="population-density")
    def population_density(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SmallHexViewSet(BaseHexViewSet):
    queryset = DataHexSmall.objects.all()
    serializer_class = DetailDataHexSmallSerializer

    def get_serializer_class(self):
        if self.action == "sport_density":
            return DataHexSmallSerializer
        if self.action == "population_density":
            return BaseDataHexSmallSerializer
        return self.serializer_class


class BigHexViewSet(BaseHexViewSet):
    queryset = DataHexBig.objects.all()
    serializer_class = DetailDataHexBigSerializer

    def get_serializer_class(self):
        if self.action == "sport_density":
            return DataHexBigSerializer
        if self.action == "population_density":
            return BaseDataHexBigSerializer
        return self.serializer_class


class HexIntersectionViewSet(ReadOnlyModelViewSet):
    queryset = DataHexSmall.objects.all()
    serializer_class = BaseHexIntersectionsSerializer
    filter_backends = [TMSTileFilter, InBBoxFilter]
    bbox_filter_field = "polygon"
    bbox_filter_include_overlapping = True
    pagination_class = LimitOffsetPagination
