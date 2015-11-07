# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0007_auto_20151106_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='InciUpdatePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.FileField(upload_to=b'inci_update_photos')),
                ('inci_update', models.ForeignKey(to='incident.InciUpdate')),
            ],
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
