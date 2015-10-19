# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='contact',
            field=models.CharField(max_length=50),
        ),
    ]
