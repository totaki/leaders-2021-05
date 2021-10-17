from django_filters import rest_framework as filters

from facilities.models import Facility


class FacilityFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    area_name = filters.CharFilter(field_name="areas__name", lookup_expr='icontains')

    class Meta:
        model = Facility
        fields = ['name', 'department', 'availability', 'area_name']  #, 'sports', 'area_type'