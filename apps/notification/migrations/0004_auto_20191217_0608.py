# Generated by Django 2.1.8 on 2019-12-17 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_auto_20181227_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('project_join_request', 'Join project request'), ('project_join_request_abort', 'Join project request abort'), ('project_join_response', 'Join project response'), ('entry_comment_add', 'Entry Comment Add'), ('entry_comment_modify', 'Entry Comment Modify'), ('entry_comment_reply_add', 'Entry Comment Reply Add'), ('entry_comment_reply_modify', 'Entry Comment Reply Modify'), ('entry_comment_resolved', 'Entry Comment Resolved')], max_length=48),
        ),
    ]
