from django.contrib.gis.db import models

from facilities.models import Facility


class DataHexSmall(models.Model):
    polygon = models.PolygonField()
    population = models.PositiveIntegerField()
    facilities = models.ManyToManyField(Facility, related_name='hexes')

    class Meta:
        db_table = 'sport_density_data_hex_small'


class DataHexBig(models.Model):
    polygon = models.PolygonField()
    population = models.PositiveIntegerField()
    facilities = models.ManyToManyField(Facility, related_name='big_hexes')

    class Meta:
        db_table = 'sport_density_data_hex_big'
