# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-20 05:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ary', '0020_assessment_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='scorematrixscale',
            name='default',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scorescale',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
