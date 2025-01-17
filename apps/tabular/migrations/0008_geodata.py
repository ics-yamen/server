# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-29 09:24
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tabular', '0007_auto_20181028_1012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Geodata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='pending', max_length=30)),
                ('field', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='geodata', to='tabular.Field')),
            ],
        ),
    ]
