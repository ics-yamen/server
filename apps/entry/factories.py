import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from gallery.factories import FileFactory
from django.core.files.base import ContentFile


from .models import (
    Entry,
    Attribute,
    EntryComment,
    EntryAttachment
)


class EntryFactory(DjangoModelFactory):
    entry_type = fuzzy.FuzzyChoice(Entry.TagType)
    excerpt = fuzzy.FuzzyText(length=100)
    image = factory.SubFactory(FileFactory)

    class Meta:
        model = Entry

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        entry = model_class(*args, **kwargs)
        if getattr(entry, 'project', None) is None:  # Use lead's project if project is not provided
            entry.project = entry.lead.project
        if getattr(entry, 'analysis_framework', None) is None:  # Use lead's project's AF if AF is not provided
            entry.analysis_framework = entry.lead.project.analysis_framework
        entry.save()
        return entry

    @factory.post_generation
    def verified_by(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for verified_by_user in extracted:
                self.verified_by.add(verified_by_user)


class EntryAttributeFactory(DjangoModelFactory):
    widget_version = 1

    class Meta:
        model = Attribute


class EntryCommentFactory(DjangoModelFactory):
    class Meta:
        model = EntryComment


class EntryAttachmentFactory(DjangoModelFactory):
    class Meta:
        model = EntryAttachment

    file = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
    )
    file_preview = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
    )
