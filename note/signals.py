from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.signals import request_started
from django.urls import reverse

from note.models import Note


@receiver(pre_save, sender=Note)
def add_slug_to_note(sender, instance, **kwargs):
    if instance and not instance.slug:
        instance.slug = slugify(instance.title)
