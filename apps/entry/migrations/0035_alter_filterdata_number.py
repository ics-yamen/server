# Generated by Django 3.2.9 on 2021-12-07 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0034_attribute_widget_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filterdata',
            name='number',
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
    ]
