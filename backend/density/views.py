from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.filters import TMSTileFilter

from density.models import PopulationHexBig
from density.serializers import PopulationHexSmallSerializer


class BigHexViewSet(ReadOnlyModelViewSet):
    queryset = PopulationHexBig.objects.all()
    serializer_class = PopulationHexSmallSerializer
    filter_backends = [TMSTileFilter]
    bbox_filter_include_overlapping = True
    bbox_filter_field = 'polygon'
    pagination_class = LimitOffsetPagination


class SmallHexViewSet(ReadOnlyModelViewSet):
    queryset = PopulationHexBig.objects.all()
    serializer_class = PopulationHexSmallSerializer
    filter_backends = [TMSTileFilter]
    filterset_fields = ['polygon']
    bbox_filter_include_overlapping = True
    pagination_class = LimitOffsetPagination
