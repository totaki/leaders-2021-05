from django.db.models import Sum, Count
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.filters import TMSTileFilter, InBBoxFilter

from sport_density.models import HexIntersections, BigHexIntersections
from sport_density.serializers import (
    HexIntersectionsSerializer,
    BaseHexIntersectionsSerializer,
    BigHexIntersectionsSerializer,
)


class SmallHexViewSet(ReadOnlyModelViewSet):
    queryset = HexIntersections.objects.all().annotate(
        square=Sum("facilities__areas__square"),
        areas_count=Count("facilities__areas"),
    )
    serializer_class = HexIntersectionsSerializer
    filter_backends = [TMSTileFilter, InBBoxFilter]
    bbox_filter_field = "polygon"
    bbox_filter_include_overlapping = True
    pagination_class = LimitOffsetPagination


class BigHexViewSet(ReadOnlyModelViewSet):
    queryset = BigHexIntersections.objects.all().annotate(
        square=Sum("facilities__areas__square"),
        areas_count=Count("facilities__areas"),
    )
    serializer_class = BigHexIntersectionsSerializer
    filter_backends = [TMSTileFilter, InBBoxFilter]
    bbox_filter_field = "polygon"
    bbox_filter_include_overlapping = True
    pagination_class = LimitOffsetPagination


class HexIntersectionViewSet(ReadOnlyModelViewSet):
    queryset = HexIntersections.objects.all()
    serializer_class = BaseHexIntersectionsSerializer
    filter_backends = [TMSTileFilter, InBBoxFilter]
    bbox_filter_field = "polygon"
    bbox_filter_include_overlapping = True
    pagination_class = LimitOffsetPagination
