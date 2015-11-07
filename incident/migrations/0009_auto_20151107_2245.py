# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0008_auto_20151107_2114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inciupdatephoto',
            name='inci_update',
        ),
#         migrations.AddField(
#             model_name='dispatch',
#             name='is_approved',
#             field=models.BooleanField(default=False),
#         ),
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
    ]
