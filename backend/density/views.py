from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.filters import TMSTileFilter, InBBoxFilter

from density.models import PopulationHexBig, PopulationHexSmall
from density.serializers import PopulationHexSmallSerializer, PopulationHexBigSerializer


class BigHexViewSet(ReadOnlyModelViewSet):
    queryset = PopulationHexBig.objects.filter(population__gt=0)
    serializer_class = PopulationHexBigSerializer
    filter_backends = [TMSTileFilter, InBBoxFilter]
    bbox_filter_include_overlapping = True
    bbox_filter_field = 'polygon'
    pagination_class = LimitOffsetPagination


class SmallHexViewSet(ReadOnlyModelViewSet):
    queryset = PopulationHexSmall.objects.filter(population__gt=0)
    serializer_class = PopulationHexSmallSerializer
    filter_backends = [TMSTileFilter, InBBoxFilter]
    bbox_filter_field = 'polygon'
    bbox_filter_include_overlapping = True
    pagination_class = LimitOffsetPagination

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)
