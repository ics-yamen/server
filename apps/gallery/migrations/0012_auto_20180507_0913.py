# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-07 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_auto_20180410_0405'),
        ('gallery', '0011_auto_20180405_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='permitted_user_groups',
        ),
        migrations.RemoveField(
            model_name='file',
            name='permitted_users',
        ),
        migrations.AddField(
            model_name='file',
            name='projects',
            field=models.ManyToManyField(blank=True, to='project.Project'),
        ),
    ]