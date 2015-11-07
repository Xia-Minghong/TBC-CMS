# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0009_auto_20151107_2245'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='inciupdate',
            name='photo_url',
            field=models.URLField(default=b'', max_length=500),
        ),
    ]
