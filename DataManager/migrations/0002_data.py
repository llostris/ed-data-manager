# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

__author__ = 'Magda'


class Migration(migrations.Migration):

    dependencies = [
        ('DataManager','0001_initial')
    ]

    operations = [
        # initialize Country table with data
        migrations.RunSQL(
            sql=open('DataManager/sql/country.sql', encoding='UTF-8').readlines(),
        ),
        # initialize Airline table with data
        migrations.RunSQL(
            sql=open('DataManager/sql/airline.sql', encoding='UTF-8').readlines(),
        ),
        # initialize City table with data
        # migrations.RunSQL(
        #     sql=open('DataManager/sql/city.sql', encoding='UTF-8').readlines(),
        # ),

    ]