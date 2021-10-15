from django.contrib.gis.db import models


class PopulationHex(models.Model):
    polygon = models.PolygonField()
    population = models.FloatField()

    class Meta:
        db_table = 'density_population_hex'
