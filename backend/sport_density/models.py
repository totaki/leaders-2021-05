from django.contrib.gis.db import models

from facilities.models import Facility


class HexIntersections(models.Model):
    polygon = models.PolygonField()
    facilities = models.ManyToManyField(Facility, related_name='hexes')

    class Meta:
        db_table = 'sport_density_hex_intersections'