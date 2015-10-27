# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DataManager', '0003_city_data'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Offer',
        ),
    ]
