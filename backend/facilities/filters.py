from django import forms
from django_filters import rest_framework as filters

from facilities.models import Facility, AvailabilityType


class NoValidationMultipleChoiceField(forms.MultipleChoiceField):
    def validate(self, value):
        return True


class SportsFilter(filters.Filter):
    field_class = NoValidationMultipleChoiceField

    def __init__(self, *args, **kwargs):
        self.conjoined = kwargs.pop('conjoined', False)
        super().__init__(*args, **kwargs)

    def filter(self, qs, values):
        return qs.filter(areas__sports__contains=[int(value) for value in values])


class FacilityFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    area_name = filters.CharFilter(field_name="areas__name", lookup_expr="icontains")
    area_type = filters.BaseInFilter(field_name="area_types", lookup_expr="contains")
    availability = filters.MultipleChoiceFilter(
        field_name="availability", choices=AvailabilityType.choices
    )
    sports = SportsFilter()

    class Meta:
        model = Facility
        fields = [
            "name",
            "department",
            "availability",
            "area_name",
            "area_type",
            "sports",
        ]
