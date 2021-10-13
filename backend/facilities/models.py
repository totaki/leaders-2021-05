from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField


class AvailabilityType(models.IntegerChoices):
    city = 1
    area = 2
    district = 3
    step_availability = 4


class Department(models.Model):
    name = models.CharField(max_length=200)


class Facility(models.Model):
    name = models.CharField(max_length=400)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True
    )
    availability = models.PositiveSmallIntegerField(choices=AvailabilityType.choices)
    placement = models.PointField()


class SportType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'facilities_sport_type'


class SportsAreaType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'facilities_sports_area_type'


class SportsArea(models.Model):
    name = models.CharField(max_length=400)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    type = models.ForeignKey(SportsAreaType, on_delete=models.CASCADE)
    sports = ArrayField(models.PositiveSmallIntegerField(), size=20)

    class Meta:
        db_table = 'facilities_sports_area'
