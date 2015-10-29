# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='syslog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('time', models.DateTimeField(default=datetime.datetime(2015, 10, 28, 17, 4, 14, 391762, tzinfo=utc), verbose_name=b'time generated')),
                ('generator', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
    ]
