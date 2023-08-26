from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
# Create your models here.

FLAGS = (
		("GREEN", "GREEN"),
		("GREEN", "GREEN"),
		("RED", "RED"),
	)

class Rider(models.Model):
	
	rider_id = models.CharField(max_length=10, default='ABC', unique=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	locality = models.CharField(max_length=100)
	phone_number = models.CharField(max_length=15)
	alt_phone_number = models.CharField(max_length=15, blank=True, null=True)
	flag = models.CharField(max_length=100, choices=FLAGS, default="RED")
	slug = models.SlugField(unique=True, default="")

	def __unicode__(self):
		return "%s %s" %(self.first_name, self.last_name)

	def get_full_name(self):
		return "%s %s" %(self.first_name, self.last_name)

	def save(self, *args, **kwargs):
		self.slug = '-'.join((slugify(self.rider_id), slugify(self.first_name), slugify(self.last_name)))
		super(Rider, self).save(*args, **kwargs)
