from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from ckeditor.fields import RichTextField
from profanity.validators import validate_is_profane

from core.helpers.model_choices import HEX_CHOICES


class Note(models.Model):
	title = models.CharField(
		max_length=32, unique=True, blank=False 
	)
	content = RichTextField(blank=False)
	slug = models.SlugField(blank=True, null=False)

	create = models.DateTimeField(auto_now_add=True)
	modify = models.DateTimeField(auto_now=True)

	categories = models.ManyToManyField('note.Category', blank=True)

	def __str__(self):
		return self.title


@receiver(pre_save, sender=Note)
def add_slug_to_note(sender, instance, **kwargs):
    if instance and not instance.slug:
        instance.slug = slugify(instance.title)


class Category(models.Model):
	name = models.CharField(max_length=32)
	color = models.CharField(max_length=7, choices=HEX_CHOICES)

	def __str__(self):
		return self.name
