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
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FacilityFilter
    pagination_class = LimitOffsetPagination

    @action(detail=True)
    def report(self, request, pk=None):
        facility = (
            self.queryset.prefetch_related("areas")
            .select_related("department")
            .get(pk=pk)
        )
        serializer = FacilityDetailSerializer(facility)
        return Response(serializer.data)


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
