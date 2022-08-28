from django.db import models
from ckeditor.fields import RichTextField

from core.helpers.model_choices import HEX_CHOICES


class Note(models.Model):
	title = models.CharField(max_length=32)
	content = RichTextField()
	categories = models.ManyToManyField('note.Category', blank=True)


	def __str__(self):
		return self.title


class Category(models.Model):
	name = models.CharField(max_length=32)
	color = models.CharField(max_length=7, choices=HEX_CHOICES)

	def __str__(self):
		return self.name
