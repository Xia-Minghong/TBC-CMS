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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('init', 'initiated'), ('rej', 'rejected'), ('appr', 'approved'), ('disp', 'dispatched'), ('closed', 'closed')], max_length=20)),
                ('severity', models.IntegerField()),
                ('time', models.DateTimeField(verbose_name='time reported')),
                ('location', models.CharField(max_length=100)),
                ('contact', models.IntegerField()),
                ('type', models.CharField(choices=[('haze', 'haze'), ('fire', 'fire'), ('crash', 'crash'), ('dengue', 'dengue')], max_length=50)),
                ('description', models.TextField()),
            ],
        ),
    ]
