# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv

from django.db import models, migrations
from DataManager.sqlgenerator.CountryAndAirportDataGenerator import AirportCity

__author__ = 'Magda'


def get_airports():
    airports = []
    city_names = set()
    with open('./data/airports2.csv', 'r', encoding="UTF-8") as csvfile:
        airport_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in airport_reader:
            airport = AirportCity(row[2], row[3])
            if airport.city not in city_names:
                airports.append(airport)
                city_names.add(airport.city)

    return airports

def add_cities(apps, schema_editor):
    City = apps.get_model("DataManager", "City")
    Country = apps.get_model("DataManager", "Country")
    db_alias = schema_editor.connection.alias

    airports = set(get_airports())

    cities = []
    for airport in airports:
        country = Country.objects.get(name=airport.country)
        cities.append(City(name=airport.city, country=country, forms=airport.city))

    City.objects.using(db_alias).bulk_create(cities)


def remove_cities(apps, schema_editor):
        City = apps.get_model("DataManager", "City")
        db_alias = schema_editor.connection.alias

        airports = set(get_airports())

        for airport in airports:
            City.objects.using(db_alias).get(name=airport.city).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('DataManager', '0002_data'),
    ]

    operations = [
        migrations.RunPython(add_cities, remove_cities),
    ]
