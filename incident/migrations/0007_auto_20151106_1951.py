# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0002_auto_20151019_0037'),
        ('incident', '0006_auto_20151019_0045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incident',
            name='dispatches',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='updates',
        ),
        migrations.AddField(
            model_name='incident',
            name='agencies_through_dispatch',
            field=models.ManyToManyField(related_name='_agencies_through_dispatch_+', through='incident.Dispatch', to='agency.Agency'),
        ),
        migrations.AddField(
            model_name='incident',
            name='agencies_through_inci_update',
            field=models.ManyToManyField(related_name='_agencies_through_inci_update_+', through='incident.InciUpdate', to='agency.Agency'),
        ),
#         migrations.AddField(
#             model_name='incident',
#             name='latitude',
#             field=models.CharField(default=b'0', max_length=50),
#         ),
#         migrations.AddField(
#             model_name='incident',
#             name='longitude',
#             field=models.CharField(default=b'0', max_length=50),
#         ),
        migrations.AlterField(
            model_name='incident',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='status',
            field=models.CharField(default=b'initiated', max_length=20, choices=[(b'initiated', b'initiated'), (b'approved', b'approved'), (b'dispatched', b'dispatched'), (b'rejected', b'rejected'), (b'closed', b'closed')]),
        ),
        migrations.AlterField(
            model_name='incident',
            name='type',
            field=models.CharField(max_length=50, choices=[(b'haze', b'Haze'), (b'fire', b'Fire'), (b'crash', b'Crash'), (b'dengue', b'Dengue')]),
        ),
#         migrations.AddField(
#             model_name='dispatch',
#             name='is_approved',
#             field=models.BooleanField(default=False),
#         ),
    ]
