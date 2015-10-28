# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('system_log', '0002_auto_20151029_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syslog',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 17, 18, 2, 51189, tzinfo=utc), verbose_name=b'time generated'),
        ),
    ]
