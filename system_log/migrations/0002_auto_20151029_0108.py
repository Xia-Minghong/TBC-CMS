# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('system_log', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syslog',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 17, 8, 1, 994430, tzinfo=utc), verbose_name=b'time generated'),
        ),
    ]
