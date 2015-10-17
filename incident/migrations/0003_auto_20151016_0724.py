# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0002_auto_20151010_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='status',
            field=models.CharField(max_length=20, choices=[('initiated', 'initiated'), ('rejected', 'rejected'), ('approved', 'approved'), ('dispatched', 'dispatched'), ('closed', 'closed')], default='initiated'),
        ),
    ]
