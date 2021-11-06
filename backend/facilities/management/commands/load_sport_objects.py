import csv
import json
from typing import Tuple, List

from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from facilities.models import (
    Facility,
    Department,
    SportsArea,
    SportsAreaType,
    SportType,
)
from sport_density.models import DataHexSmall, DataHexBig, get_areas_filter, SquareColorBins, \
    SquarePerPersonColorBins


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


def read_data_hex_csv(filename) -> Tuple[int, str, List[int], int]:
    with open(f"{settings.BASE_DIR}/data/{filename}", newline="") as file:
        reader = csv.reader(file, quotechar='"')
        next(reader, None)

        for row in reader:
            yield int(row[0]), row[1], json.loads(row[2]), int(float(row[3]))


def load_data_hexes(model, filename):
    for id_, polygon, facilities, population in read_data_hex_csv(filename):
        intersection = model.objects.create(id=id_, polygon=polygon, population=population)
        intersection.facilities.add(*facilities)


def load_color_bins():
    if SquareColorBins.objects.all().exists():
        return
    sport_ids = list(SportType.objects.all().values_list('id', flat=True))
    sport_ids.append(None)
    availabilities = list(range(1, 5))
    availabilities.append(None)
    for sport_id in sport_ids:
        for availability in availabilities:
            by_square, by_square_per_person = calculate_color_bins_for_hexes([sport_id], availability)
            save_color_bins(sport_id, availability, by_square, by_square_per_person)
            if by_square:
                by_square = calculate_color_bins_for_hexes_by_square([sport_id], availability, is_big_hexes=False)
            if by_square_per_person:
                by_square_per_person = calculate_color_bins_for_hexes_by_square_per_person(
                    [sport_id], availability, is_big_hexes=False
                )
            save_color_bins(sport_id, availability, by_square, by_square_per_person, is_big_hexes=False)


def save_color_bins(sport_id, availability, bins_by_square, bins_by_square_per_person, is_big_hexes=True):
    SquareColorBins.objects.create(
        sport_id=sport_id,
        availability=availability,
        bins=bins_by_square,
        is_big_hexes=is_big_hexes
    )
    SquarePerPersonColorBins.objects.create(
        sport_id=sport_id,
        availability=availability,
        bins=bins_by_square_per_person,
        is_big_hexes=is_big_hexes
    )


def calculate_color_bins_for_hexes_by_square(
        sport_ids, availability, is_big_hexes=True, area_type=None
):
    areas_filter = get_areas_filter(
        sport_ids=sport_ids, availability=availability, area_type=area_type
    )
    if is_big_hexes:
        bins_by_square = DataHexBig.objects.color_bins_by_square(areas_filter)
    else:
        bins_by_square = DataHexSmall.objects.color_bins_by_square(areas_filter)
    return bins_by_square


def calculate_color_bins_for_hexes_by_square_per_person(
        sport_ids, availability, is_big_hexes=True, area_type=None
):
    areas_filter = get_areas_filter(
        sport_ids=sport_ids, availability=availability, area_type=area_type
    )
    if is_big_hexes:
        bins_by_square_per_person = DataHexBig.objects.color_bins_by_square_per_person(areas_filter)
    else:
        bins_by_square_per_person = DataHexSmall.objects.color_bins_by_square_per_person(areas_filter)
    return bins_by_square_per_person


def calculate_color_bins_for_hexes(sport_ids, availability, is_big_hexes=True, area_type=None):
    bins_by_square = calculate_color_bins_for_hexes_by_square(
        sport_ids, availability, is_big_hexes, area_type
    )
    bins_by_square_per_person = calculate_color_bins_for_hexes_by_square_per_person(
        sport_ids, availability, is_big_hexes, area_type
    )
    return bins_by_square, bins_by_square_per_person


def clear_tables():
    SportsAreaType.objects.all().delete()
    SportType.objects.all().delete()
    Department.objects.all().delete()
    Facility.objects.all().delete()
    SportsArea.objects.all().delete()
    DataHexSmall.objects.all().delete()
    DataHexBig.objects.all().delete()
    # SquareColorBins.objects.all().delete()
    # SquarePerPersonColorBins.objects.all().delete()


class Command(BaseCommand):
    def handle(self, *args, **options):
        clear_tables()
        load_zone_types()
        load_sport_types()
        load_departments()
        load_facilities()
        load_sports_areas()
        load_data_hexes(DataHexSmall, "data_hexes_small.csv")
        load_data_hexes(DataHexBig, "data_hexes_big.csv")
        # load_color_bins()
