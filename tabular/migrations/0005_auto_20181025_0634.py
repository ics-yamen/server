# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-25 06:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabular', '0004_auto_20181024_1303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='field',
            options={'ordering': ['ordering']},
        ),
        migrations.AddField(
            model_name='field',
            name='ordering',
            field=models.IntegerField(default=1),
        ),
    ]