from django.contrib.gis.db import models
from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.postgres.fields import ArrayField
from django.db.models import Sum, Func, F


class AvailabilityType(models.IntegerChoices):
    city = 1
    area = 2
    district = 3
    step_availability = 4


class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Facility(models.Model):
    name = models.CharField(max_length=400)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    availability = models.PositiveSmallIntegerField(choices=AvailabilityType.choices)
    placement = models.PointField()
    sports = ArrayField(models.PositiveSmallIntegerField(), size=70)


class SportType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = "facilities_sport_type"


class SportsAreaType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = "facilities_sports_area_type"


class SportsAreaQuerySet(models.QuerySet):
    def get_stats(self):
        return self.aggregate(
            total_sport_square=Sum("square"),
            area_types=ArrayAgg("type"),
        )

    def get_all_sports(self):
        return (
            self.annotate(all_sports=Func(F("sports"), function="unnest"))
            .values_list("all_sports", flat=True)
            .distinct()
        )

    def get_sports_coverage(self):
        return (
            self.values('type')
            .annotate(Sum('square'))
        )


class SportsArea(models.Model):
    name = models.CharField(max_length=400)
    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name="areas"
    )
    type = models.ForeignKey(SportsAreaType, on_delete=models.CASCADE)
    sports = ArrayField(models.PositiveSmallIntegerField(), size=20)
    square = models.FloatField(null=True)
    objects = SportsAreaQuerySet.as_manager()

    class Meta:
        db_table = "facilities_sports_area"
