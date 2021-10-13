from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

from rest_framework.viewsets import ReadOnlyModelViewSet
from facilities.models import Department, Facility, SportType, SportsAreaType, SportsArea
from facilities.serializers import DepartmentSerializer, FacilitySerializer, SportTypeSerializer, \
    SportsAreaTypeSerializer, SportsAreaSerializer


class DepartmentsViewSet(ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class FacilitiesViewSet(ReadOnlyModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department', 'availability']
    pagination_class = LimitOffsetPagination


class SportTypesViewSet(ReadOnlyModelViewSet):
    queryset = SportType.objects.all()
    serializer_class = SportTypeSerializer


class SportsAreaTypesViewSet(ReadOnlyModelViewSet):
    queryset = SportsAreaType.objects.all()
    serializer_class = SportsAreaTypeSerializer


class SportsAreasViewSet(ReadOnlyModelViewSet):
    queryset = SportsArea.objects.all()
    serializer_class = SportsAreaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['facility', 'type']
    pagination_class = LimitOffsetPagination
