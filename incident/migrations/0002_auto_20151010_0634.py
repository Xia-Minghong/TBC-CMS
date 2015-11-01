# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0001_initial'),
        ('incident', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispatch',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('resource', models.TextField()),
                ('time', models.DateTimeField(verbose_name='time dispatched')),
                ('agency', models.ForeignKey(to='agency.Agency')),
                ('incident', models.ForeignKey(to='incident.Incident')),
            ],
        ),
        migrations.CreateModel(
            name='InciUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('updated_severity', models.IntegerField()),
                ('description', models.TextField()),
                ('time', models.DateTimeField(verbose_name='time updated')),
                ('agency', models.ForeignKey(to='agency.Agency')),
                ('incident', models.ForeignKey(to='incident.Incident')),
            ],
        ),
        migrations.AddField(
            model_name='incident',
            name='dispatches',
            field=models.ManyToManyField(to='agency.Agency', related_name='dispatch+', through='incident.Dispatch'),
        ),
        migrations.AddField(
            model_name='incident',
            name='updates',
            field=models.ManyToManyField(to='agency.Agency', related_name='updatekeys+', through='incident.InciUpdate'),
        ),
    ]
