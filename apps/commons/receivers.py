# Reusable actions
from django.db import models
from django.db.transaction import on_commit
from django.dispatch import receiver

from lead.models import (
    LeadPreview,
    LeadPreviewAttachment,
)
from unified_connector.models import ConnectorLeadPreviewAttachment


# Lead
@receiver(models.signals.post_delete, sender=LeadPreview)
@receiver(models.signals.post_delete, sender=LeadPreviewAttachment)
# Unified Connector
@receiver(models.signals.post_delete, sender=ConnectorLeadPreviewAttachment)
def cleanup_file_on_instance_delete(sender, instance, **kwargs):
    files = []
    for field in instance._meta.get_fields():
        if isinstance(field, models.FileField):
            field_name = field.name
            field_value = getattr(instance, field_name)
            if not field_value:
                continue
            storage, path = field_value.storage, field_value.name
            files.append([storage, path])
    on_commit(lambda: [storage.delete(path) for storage, path in files])
