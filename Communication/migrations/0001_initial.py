# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMediaReport',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('timestamp', models.DateTimeField(verbose_name='time published')),
                ('socialMediaText', models.TextField()),
                ('incident', models.ForeignKey(to='incident.Incident')),
            ],
        ),
    ]
