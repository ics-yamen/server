# Generated by Django 3.2.25 on 2024-06-21 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0049_auto_20231121_0926_squashed_0054_auto_20231218_0552'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LeadPreviewImage',
            new_name='LeadPreviewAttachment'
        ),
    ]
