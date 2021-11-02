from django.contrib.gis.db import models
from django.db.models import Sum, Count, F

from facilities.models import Facility


class HexesQuerySet(models.QuerySet):
    def annotate_areas(self, areas_filter=None):
        return self.annotate(
            square=Sum("facilities__areas__square", filter=areas_filter),
            areas_count=Count("facilities__areas", filter=areas_filter),
        )

    def annotate_square_by_person(self):
        return self.annotate(square_by_person=F("square") / F("population"))

    def populated(self):
        return self.filter(population__gt=0)


class DataHexSmall(models.Model):
    polygon = models.PolygonField()
    population = models.PositiveIntegerField()
    facilities = models.ManyToManyField(Facility, related_name='hexes')
    objects = HexesQuerySet.as_manager()

    class Meta:
        db_table = 'sport_density_data_hex_small'


class DataHexBig(models.Model):
    polygon = models.PolygonField()
    population = models.PositiveIntegerField()
    facilities = models.ManyToManyField(Facility, related_name='big_hexes')
    objects = HexesQuerySet.as_manager()

    class Meta:
        db_table = 'sport_density_data_hex_big'
