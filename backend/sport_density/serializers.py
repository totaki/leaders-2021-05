from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from sport_density.models import HexIntersections


class HexIntersectionsSerializer(ModelSerializer):
    square = serializers.FloatField()
    areas_count = serializers.IntegerField()

    class Meta:
        model = HexIntersections
        fields = ['id', 'polygon', 'square', 'areas_count']


class BaseHexIntersectionsSerializer(ModelSerializer):

    class Meta:
        model = HexIntersections
        fields = "__all__"
