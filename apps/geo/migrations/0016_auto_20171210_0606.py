# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-10 06:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
        ('geo', '0015_auto_20171210_0602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminlevel',
            name='geo_shape_file',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='gallery.File'),
        ),
    ]
