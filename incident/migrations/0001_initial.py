# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('contact', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Dispatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('resource', models.TextField()),
                ('time', models.DateTimeField(verbose_name='time dispatched')),
                ('agency', models.ForeignKey(to='incident.Agency')),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
        migrations.CreateModel(
            name='InciUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('updated_severity', models.IntegerField()),
                ('description', models.TextField()),
                ('time', models.DateTimeField(verbose_name='time updated')),
                ('agency', models.ForeignKey(to='incident.Agency')),
                ('incident', models.ForeignKey(to='incident.Incident')),
            ],
        ),
        migrations.AddField(
            model_name='dispatch',
            name='incident',
            field=models.ForeignKey(to='incident.Incident'),
        ),
        migrations.AddField(
            model_name='agency',
            name='dispatched_by',
            field=models.ManyToManyField(through='incident.Dispatch', related_name='dispatch+', to='incident.Incident'),
        ),
        migrations.AddField(
            model_name='agency',
            name='update_to',
            field=models.ManyToManyField(through='incident.InciUpdate', related_name='update+', to='incident.Incident'),
        ),
    ]
