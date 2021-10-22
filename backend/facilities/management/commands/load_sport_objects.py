import csv
import json
from typing import Type

from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from density.models import PopulationHex, PopulationHexBig, PopulationHexSmall
from facilities.models import (
    Facility,
    Department,
    SportsArea,
    SportsAreaType,
    SportType,
)
from sport_density.models import HexIntersections, BigHexIntersections


def load_zone_types():
    with open(f"{settings.BASE_DIR}/data/sports_areas_type.csv", newline="") as file:
        reader = csv.reader(file, quotechar='"')
        next(reader, None)
        zone_types = []
        for row in reader:
            zone_types.append(SportsAreaType(id=row[0], name=row[1]))
        SportsAreaType.objects.bulk_create(zone_types)


def load_sport_types():
    with open(f"{settings.BASE_DIR}/data/sports.csv", newline="") as file:
        reader = csv.reader(file, quotechar='"')
        next(reader, None)
        sport_types = []
        for row in reader:
            sport_types.append(SportsAreaType(id=row[0], name=row[1]))
        SportType.objects.bulk_create(sport_types)


def load_departments():
    with open(f"{settings.BASE_DIR}/data/departments.csv", newline="") as file:
        reader = csv.reader(file, quotechar='"')
        next(reader, None)
        departments = []
        for row in reader:
            departments.append(Department(id=row[0], name=row[1]))
        Department.objects.bulk_create(departments)


def parse_float(val):
    if not val:
        return None
    return int(float(val))


def load_facilities():
    with open(f"{settings.BASE_DIR}/data/facilities.csv", newline="") as file:
        reader = csv.reader(file, quotechar='"')
        next(reader, None)
        facilities = []
        for row in reader:
            facilities.append(
                Facility(
                    id=row[0],
                    name=row[1],
                    department_id=int(row[2]),
                    availability=row[3],
                    placement=Point(x=float(row[4]), y=float(row[5])),
                    sports=json.loads(row[6]),
                )
            )
        Facility.objects.bulk_create(facilities)


def load_sports_areas():
    with open(f"{settings.BASE_DIR}/data/areas.csv", newline="") as file:
        reader = csv.reader(file, quotechar='"')
        next(reader, None)
        areas = []
        for row in reader:
            areas.append(
                SportsArea(
                    id=row[0],
                    facility_id=row[1],
                    name=row[2],
                    type_id=row[3],
                    square=float(row[4]),
                    sports=json.loads(row[5]),
                )
            )
        SportsArea.objects.bulk_create(areas)


def load_hex(model: Type[PopulationHex], filename: str):
    with open(f"{settings.BASE_DIR}/data/{filename}", newline="") as file:
        reader = csv.reader(file, quotechar='"')
        next(reader, None)
        hexes = []
        for row in reader:
            hexes.append(model(polygon=row[1], population=row[2]))
        model.objects.bulk_create(hexes)


def load_hex_intersections(model, filename):
    with open(f"{settings.BASE_DIR}/data/{filename}", newline="") as file:
        reader = csv.reader(file, quotechar='"')
        next(reader, None)

        for row in reader:
            intersection = model.objects.create(polygon=row[1])

            facilities = json.loads(row[2])
            intersection.facilities.add(*facilities)


def clear_tables():
    SportsAreaType.objects.all().delete()
    SportType.objects.all().delete()
    Department.objects.all().delete()
    Facility.objects.all().delete()
    SportsArea.objects.all().delete()
    PopulationHexBig.objects.all().delete()
    PopulationHexSmall.objects.all().delete()
    HexIntersections.objects.all().delete()
    BigHexIntersections.objects.all().delete()


class Command(BaseCommand):
    def handle(self, *args, **options):
        clear_tables()
        load_zone_types()
        load_sport_types()
        load_departments()
        load_facilities()
        load_sports_areas()
        load_hex(PopulationHexSmall, "population_density.csv")
        load_hex(PopulationHexBig, "population_density_big.csv")
        load_hex_intersections(HexIntersections, "hex_facility_intersection.csv")
        load_hex_intersections(BigHexIntersections, "big_hex_facility_intersection.csv")
