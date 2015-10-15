# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=20, choices=[('init', 'initiated'), ('rej', 'rejected'), ('appr', 'approved'), ('disp', 'dispatched'), ('closed', 'closed')])),
                ('severity', models.IntegerField()),
                ('time', models.DateTimeField(verbose_name='time reported')),
                ('location', models.CharField(max_length=100)),
                ('contact', models.IntegerField()),
                ('type', models.CharField(max_length=50, choices=[('haze', 'haze'), ('fire', 'fire'), ('crash', 'crash'), ('dengue', 'dengue')])),
                ('description', models.TextField()),
            ],
        ),
    ]
