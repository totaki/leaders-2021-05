from rest_framework.serializers import ModelSerializer

from facilities.models import (
    Department,
    Facility,
    SportType,
    SportsAreaType,
    SportsArea,
)


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = "__all__"


class SportTypeSerializer(ModelSerializer):
    class Meta:
        model = SportType
        fields = "__all__"


class SportsAreaTypeSerializer(ModelSerializer):
    class Meta:
        model = SportsAreaType
        fields = "__all__"


class SportsAreaSerializer(ModelSerializer):
    class Meta:
        model = SportsArea
        fields = "__all__"


class FacilityDetailSerializer(ModelSerializer):
    areas = SportsAreaSerializer(many=True, read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Facility
        fields = ("name", "availability", "areas", "department")
