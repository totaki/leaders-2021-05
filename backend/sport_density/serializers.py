from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from sport_density.models import DataHexSmall, DataHexBig


class BaseDataHexSmallSerializer(ModelSerializer):
    class Meta:
        model = DataHexSmall
        fields = ['id', 'polygon', 'flats']


class DataHexSmallSerializer(ModelSerializer):
    square = serializers.FloatField()
    areas_count = serializers.IntegerField()

    class Meta:
        model = DataHexSmall
        fields = ['id', 'polygon', 'flats', 'square', 'areas_count']


class DetailDataHexSmallSerializer(DataHexSmallSerializer):
    square_by_person = serializers.FloatField()

    class Meta:
        model = DataHexSmall
        fields = ['id', 'polygon', 'flats', 'square', 'areas_count', 'square_by_person']


class BaseDataHexBigSerializer(ModelSerializer):
    class Meta:
        model = DataHexBig
        fields = ['id', 'polygon', 'flats']


class DataHexBigSerializer(ModelSerializer):
    square = serializers.FloatField()
    areas_count = serializers.IntegerField()

    class Meta:
        model = DataHexBig
        fields = ['id', 'polygon', 'flats', 'square', 'areas_count']


class DetailDataHexBigSerializer(DataHexBigSerializer):
    square_by_person = serializers.FloatField()

    class Meta:
        model = DataHexBig
        fields = ['id', 'polygon', 'flats', 'square', 'areas_count', 'square_by_person']


class BaseHexIntersectionsSerializer(ModelSerializer):

    class Meta:
        model = DataHexSmall
        fields = "__all__"
