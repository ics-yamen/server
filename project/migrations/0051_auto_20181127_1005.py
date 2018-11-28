# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-27 09:54
from __future__ import unicode_literals

from django.db import migrations, models


def create_default_roles(apps, schema_editor):
    ProjectMembership = apps.get_model('project', 'ProjectMembership')
    ProjectRole = apps.get_model('project', 'ProjectRole')

    co, _ = ProjectRole.objects.update_or_create(
        title='Clairvoyant One',
        defaults={
            'lead_permissions': 15,
            'entry_permissions': 15,
            'setup_permissions': 3,
            'export_permissions': 1,
            'assessment_permissions': 15,
            'level': 1,
            'is_creator_role': True,
            'is_default_role': False,
        },
    )

    admin, _ = ProjectRole.objects.update_or_create(
        title='Admin',
        defaults={
            'lead_permissions': 15,
            'entry_permissions': 15,
            'setup_permissions': 1,
            'export_permissions': 1,
            'assessment_permissions': 15,
            'level': 100,
            'is_creator_role': False,
            'is_default_role': False,
        },
    )

    analyst, _ = ProjectRole.objects.update_or_create(
        title='Analyst',
        defaults={
            'lead_permissions': 15,
            'entry_permissions': 15,
            'setup_permissions': 0,
            'export_permissions': 1,
            'assessment_permissions': 15,
            'level': 200,
            'is_creator_role': False,
            'is_default_role': True,
        },
    )

    sourcer, _ = ProjectRole.objects.update_or_create(
        title='Sourcer',
        defaults={
            'lead_permissions': 15,
            'entry_permissions': 0,
            'setup_permissions': 0,
            'export_permissions': 0,
            'assessment_permissions': 0,
            'level': 300,
            'is_creator_role': False,
            'is_default_role': False,
        },
    )

    reader, _ = ProjectRole.objects.update_or_create(
        title='Reader',
        defaults={
            'lead_permissions': 1,
            'entry_permissions': 1,
            'setup_permissions': 0,
            'export_permissions': 1,
            'assessment_permissions': 0,
            'level': 400,
            'is_creator_role': False,
            'is_default_role': False,
        },
    )

    # All old admin users who are creators should now be
    # clairvoyant one.
    ProjectMembership.objects.filter(
        role=admin,
        project__created_by=models.F('member'),
    ).update(role=co)


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0050_auto_20181127_0954'),
    ]

    operations = [
        migrations.RunPython(create_default_roles),
    ]
