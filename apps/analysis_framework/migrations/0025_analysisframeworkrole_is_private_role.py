# Generated by Django 2.1.9 on 2019-07-15 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_framework', '0024_auto_20190712_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysisframeworkrole',
            name='is_private_role',
            field=models.BooleanField(default=False),
        ),
    ]
