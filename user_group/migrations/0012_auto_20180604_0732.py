# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-04 07:32
from __future__ import unicode_literals

from django.db import migrations


def migrate_added_by(apps, schema_editor):
    UserGroup = apps.get_model('user_group', 'UserGroup')
    GroupMembership = apps.get_model('user_group', 'GroupMembership')
    for group in UserGroup.objects.all():
        admin_ship = GroupMembership.objects.filter(
            group=group,
            role='admin'
        ).first()
        if admin_ship:
            admin = admin_ship.member
            for member in GroupMembership.objects.filter(group=group):
                member.added_by = admin
                member.save()


class Migration(migrations.Migration):

    dependencies = [
        ('user_group', '0011_groupmembership_added_by'),
    ]

    operations = [
        migrations.RunPython(migrate_added_by),
    ]
