# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0004_auto_20151017_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispatch',
            name='time',
            field=models.DateTimeField(verbose_name='time dispatched', default=datetime.datetime(2015, 10, 19, 0, 38, 38, 528757, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='incident',
            name='contact',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='incident',
            name='time',
            field=models.DateTimeField(verbose_name='time reported', default=datetime.datetime(2015, 10, 19, 0, 38, 38, 527234, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='inciupdate',
            name='time',
            field=models.DateTimeField(verbose_name='time updated', default=datetime.datetime(2015, 10, 19, 0, 38, 38, 528122, tzinfo=utc)),
        ),
    ]
