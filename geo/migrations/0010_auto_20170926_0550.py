# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 05:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geo', '0009_auto_20170926_0533'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='region',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='region_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='region',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='region',
            name='modified_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='region_modified', to=settings.AUTH_USER_MODEL),
        ),
    ]
