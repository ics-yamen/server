# Generated by Django 3.2.25 on 2024-06-21 11:49

from django.db import migrations,models


class Migration(migrations.Migration):

    dependencies = [
        ('unified_connector', '0008_connectorlead_text_extraction_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connectorleadpreviewimage',
            old_name='image',
            new_name='file',
        ),
        migrations.AlterField(
            model_name='connectorleadpreviewimage',
            name='file',
            field=models.FileField(upload_to='connector-lead/attachments/')
        ),
        migrations.RenameModel(
            old_name='ConnectorLeadPreviewImage',
            new_name='ConnectorLeadPreviewAttachment'
        ),
    ]
