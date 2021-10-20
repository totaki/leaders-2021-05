# Generated by Django 3.2.8 on 2021-10-16 10:38

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('density', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PopulationHexBig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('population', models.FloatField()),
            ],
            options={
                'db_table': 'density_population_hex_big',
            },
        ),
        migrations.RenameModel(
            old_name='PopulationHex',
            new_name='PopulationHexSmall',
        ),
        migrations.AlterModelTable(
            name='populationhexsmall',
            table='density_population_hex_small',
        ),
    ]
