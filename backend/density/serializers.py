from rest_framework.serializers import ModelSerializer

from density.models import PopulationHexSmall, PopulationHexBig


class PopulationHexSmallSerializer(ModelSerializer):
    class Meta:
        model = PopulationHexSmall
        fields = "__all__"


class PopulationHexBigSerializer(ModelSerializer):
    class Meta:
        model = PopulationHexBig
        fields = "__all__"
