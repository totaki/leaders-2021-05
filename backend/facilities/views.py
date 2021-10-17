from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Sum
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from facilities.filters import FacilityFilter
from facilities.models import (
    Department,
    Facility,
    SportType,
    SportsAreaType,
    SportsArea,
)
from facilities.serializers import (
    DepartmentSerializer,
    FacilitySerializer,
    SportTypeSerializer,
    SportsAreaTypeSerializer,
    SportsAreaSerializer,
    FacilityDetailSerializer,
)


class DepartmentsViewSet(ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class FacilitiesViewSet(ReadOnlyModelViewSet):
    queryset = (
        Facility.objects.prefetch_related("areas")
        .annotate(square=Sum("areas__square"))
        .all()
    )
    serializer_class = FacilitySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FacilityFilter
    pagination_class = LimitOffsetPagination

    @action(detail=True)
    def report(self, request, pk=None):
        facility = self.queryset.select_related("department").get(pk=pk)
        serializer = FacilityDetailSerializer(facility)
        return Response(serializer.data)

    def get_queryset(self):
        if self.action == "list":
            return self.queryset.annotate(
                area_types=ArrayAgg("areas__type", distinct=True)
            )
        return super(FacilitiesViewSet, self).get_queryset()


class SportTypesViewSet(ReadOnlyModelViewSet):
    queryset = SportType.objects.all()
    serializer_class = SportTypeSerializer


class SportsAreaTypesViewSet(ReadOnlyModelViewSet):
    queryset = SportsAreaType.objects.all()
    serializer_class = SportsAreaTypeSerializer


class SportsAreasViewSet(ReadOnlyModelViewSet):
    queryset = SportsArea.objects.all()
    serializer_class = SportsAreaSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["facility", "type"]
    pagination_class = LimitOffsetPagination
