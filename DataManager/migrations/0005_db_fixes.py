# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DataManager','0004_delete_offer')
    ]

    operations = [
        # run database fixes
        migrations.RunSQL(
            sql=' '.join(open('DataManager/sql/update_forms.sql', encoding='UTF-8').readlines()),
        ),

    ]