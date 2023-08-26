from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

STATUS = (
		("Enabled", "Enabled"),
		("Disabled", "Disabled"),
	)

# Create your models here.
class MerchantAccount(models.Model):
	"""docstring for MerchantAccount"""
	merchant = models.ForeignKey(User, blank=True, null=True)
	phone_number = models.CharField(max_length=15, default="")
	image = models.ImageField(upload_to='baker/images/', default="baker/default.jpg")
	customer = models.ManyToManyField('Customer', blank=True, null=True)
	address = models.CharField(max_length=100, blank=True, null=True)
	locality = models.CharField(max_length=100, blank=True, null=True)
	mou_signed_on = models.DateField('Date', default="2017-06-06")
	status = models.CharField(max_length=100, choices=STATUS, default="Disabled")
	slug = models.SlugField(unique=True, default="")
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return "Merchant - %s" %(self.merchant)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.merchant)
		super(MerchantAccount, self).save(*args, **kwargs)


class Customer(models.Model):
	customer_id = models.CharField(max_length=10, default='ABC', unique=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	locality = models.CharField(max_length=100)
	phone_number = models.CharField(max_length=15, default='9766526943', unique=True)
	alt_phone_number = models.CharField(max_length=15, blank=True, null=True)

	def __unicode__(self):
		return "%s %s - %s" %(self.first_name, self.last_name, self.phone_number)

	def get_full_name(self):
		return "%s %s"%(self.first_name, self.last_name)