# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0003_auto_20151016_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispatch',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 17, 6, 58, 8, 502018), verbose_name='time dispatched'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 17, 6, 58, 8, 500304), verbose_name='time reported'),
        ),
        migrations.AlterField(
            model_name='inciupdate',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 17, 6, 58, 8, 501355), verbose_name='time updated'),
        ),
    ]
