from django_filters import rest_framework as filters

from facilities.models import Facility, AvailabilityType


class FacilityFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    area_name = filters.CharFilter(field_name="areas__name", lookup_expr='icontains')
    area_type = filters.BaseInFilter(field_name="area_types", lookup_expr='contains')
    availability = filters.MultipleChoiceFilter(field_name="availability", choices=AvailabilityType.choices)

    class Meta:
        model = Facility
        fields = ['name', 'department', 'availability', 'area_name', 'area_type']  #, 'sports'