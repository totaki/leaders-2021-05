from typing import List

import numpy as np
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Sum, Count, F, Q

from facilities.models import Facility


def get_areas_filter(sport_ids=None, area_type=None, availability=None, department=None):
    areas_filter = None
    filters = []
    if sport_ids:
        filters.append(Q(facilities__areas__sports__contains=sport_ids))
    if area_type is not None:
        filters.append(Q(facilities__areas__type=area_type))
    if availability is not None:
        filters.append(Q(facilities__availability=availability))
    if department is not None:
        filters.append(Q(facilities__department=department))

    if filters:
        areas_filter = filters[0]
        for filter_ in filters:
            areas_filter &= filter_
    return areas_filter


def calculate_bins(values, quantiles):
    values = [value for value in values if value]
    if not values:
        return []
    return list(np.quantile(values, quantiles))


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

    def color_bins_by_square(self, areas_filter, quantiles=None) -> List[int]:
        if not quantiles:
            quantiles = np.linspace(0, 1, 11)
        squares = self.annotate_areas(areas_filter).values_list('square', flat=True)
        return calculate_bins(squares, quantiles)

    def color_bins_by_square_per_person(self, areas_filter, quantiles=None) -> List[int]:
        if not quantiles:
            quantiles = np.linspace(0, 1, 11)
        squares = (
            self.populated()
            .annotate_areas(areas_filter)
            .annotate_square_by_person()
            .values_list('square_by_person', flat=True)
        )
        return calculate_bins(squares, quantiles)


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


class ColorBins(models.Model):
    sport_id = models.PositiveIntegerField()
    availability = models.PositiveIntegerField()
    is_big_hexes = models.BooleanField(default=True)
    bins = ArrayField(models.IntegerField(), size=20)

    class Meta:
        abstract = True


class SquareColorBins(models.Model):
    sport_id = models.PositiveIntegerField()
    availability = models.PositiveIntegerField()
    is_big_hexes = models.BooleanField(default=True)
    bins = ArrayField(models.IntegerField(), size=20)

    class Meta:
        db_table = 'sport_density_square_color_bins'


class SquarePerPersonColorBins(models.Model):
    sport_id = models.PositiveIntegerField(null=True)
    availability = models.PositiveIntegerField(null=True)
    is_big_hexes = models.BooleanField(default=True)
    bins = ArrayField(models.FloatField(), size=20)

    class Meta:
        db_table = 'sport_density_square_per_person_color_bins'
