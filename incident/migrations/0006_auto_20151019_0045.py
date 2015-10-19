# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0005_auto_20151019_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispatch',
            name='time',
            field=models.DateTimeField(verbose_name='time dispatched', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='incident',
            name='time',
            field=models.DateTimeField(verbose_name='time reported', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='inciupdate',
            name='time',
            field=models.DateTimeField(verbose_name='time updated', default=django.utils.timezone.now),
        ),
    ]
