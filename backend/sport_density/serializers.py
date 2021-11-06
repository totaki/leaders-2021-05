from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from sport_density.models import DataHexSmall, DataHexBig, SquareColorBins, SquarePerPersonColorBins


class BaseDataHexSmallSerializer(ModelSerializer):
    class Meta:
        model = DataHexSmall
        fields = ['id', 'polygon', 'population']


class DataHexSmallSerializer(ModelSerializer):
    square = serializers.FloatField()
    areas_count = serializers.IntegerField()

    class Meta:
        model = DataHexSmall
        fields = ['id', 'polygon', 'population', 'square', 'areas_count']


class DetailDataHexSmallSerializer(DataHexSmallSerializer):
    square_by_person = serializers.FloatField()

    class Meta:
        model = DataHexSmall
        fields = ['id', 'polygon', 'population', 'square', 'areas_count', 'square_by_person']


class BaseDataHexBigSerializer(ModelSerializer):
    class Meta:
        model = DataHexBig
        fields = ['id', 'polygon', 'population']


class DataHexBigSerializer(ModelSerializer):
    square = serializers.FloatField()
    areas_count = serializers.IntegerField()

    class Meta:
        model = DataHexBig
        fields = ['id', 'polygon', 'population', 'square', 'areas_count']


class DetailDataHexBigSerializer(DataHexBigSerializer):
    square_by_person = serializers.FloatField()

    class Meta:
        model = DataHexBig
        fields = ['id', 'polygon', 'population', 'square', 'areas_count', 'square_by_person']


class BaseHexIntersectionsSerializer(ModelSerializer):

    class Meta:
        model = DataHexSmall
        fields = "__all__"


class SquareColorBinsSerializer(ModelSerializer):

    class Meta:
        model = SquareColorBins
        fields = ("sport_id", "availability", "area_type", "is_big_hexes", "bins")


class SquarePerPersonColorBinsSerializer(ModelSerializer):

    class Meta:
        model = SquarePerPersonColorBins
        fields = ("sport_id", "availability", "area_type", "is_big_hexes", "bins")
