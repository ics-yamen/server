# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-30 04:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_group', '0007_usergroup_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergroup',
            name='display_picture',
        ),
    ]
