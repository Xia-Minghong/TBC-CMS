# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InciUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('updated_severity', models.IntegerField()),
                ('description', models.TextField()),
                ('time', models.DateTimeField(verbose_name='time updated')),
                ('updated_by', models.CharField(max_length=20)),
                ('incident', models.ForeignKey(to='incident.Incident')),
            ],
        ),
    ]
