from __future__ import unicode_literals
import requests
import simplejson
from django.db import models
from merchant.models import MerchantAccount, Customer
from rider.models import Rider
from django.conf import settings
from django.core.urlresolvers import reverse
# Create your models here.

DELIVERY_TYPE = (
		("Normal", "Normal"),
		("Jet", "Jet"),
		("Superjet", "Superjet"),
	)

STATUS_CHOICES = (
		("Pending", "Pending"),
		("Confirmed", "Confirmed"),
		("Shipped","Shipped"),
		("Complete", "Complete"),
		("Cancelled", "Cancelled"),
		("Ready to Pick", "Ready to Pick"),
	)

try:
	tax_rate = settings.DEFAULT_TAX_RATE
except Exception, e:
	print str(e)
	raise NotImplementedError(str(e))

class Booking(models.Model):
	booking_id = models.CharField(max_length=10, default='ABC', unique=True)
	merchant = models.ForeignKey(MerchantAccount, null=True, blank=True)
	customer = models.ForeignKey(Customer, null=True, blank=True)
	rider = models.ForeignKey(Rider, null=True, blank=True)
	cake_cost = models.CharField(max_length=100)
	cake_weight = models.CharField(max_length=100)
	instructions = models.TextField(default="")
	origin = models.TextField(default="")
	origin_locality = models.CharField(max_length=100, default="")
	pickup_date = models.CharField(max_length=50, default=0)
	pickup_time = models.CharField(max_length=50, default=0)
	drop_date = models.CharField(max_length=50, default=0)
	drop_time = models.CharField(max_length=50, default=0)
	destination = models.TextField(default="")
	destination_locality = models.CharField(max_length=100, default="")
	duration = models.CharField(max_length=100)
	distance = models.CharField(max_length=100)
	approx_total = models.CharField(max_length=50, default=0)
	discount_total = models.CharField(max_length=50, default=0)
	sub_total = models.CharField(max_length=50, default=0)
	final_total = models.CharField(max_length=50)
	approve = models.BooleanField(default=False)
	delivery_type = models.CharField(max_length=120, choices=DELIVERY_TYPE, default="Normal")
	status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Pending")
	notify_merchant = models.BooleanField(default=False)
	notify_rider = models.BooleanField(default=False)

	def __unicode__(self):
		return self.booking_id

	def save(self, *args, **kwargs):
		if self.rider is not None and self.notify_rider == True:
			print "Sending SMS"
			complete_origin_address = str(self.origin) + str(self.origin_locality)
			complete_destination_address = str(self.destination) + str(self.destination_locality)
			sms_payload = {
				"TemplateName": "Notify rider about delivery ",
				"From": "MCBRID",
				"To": self.rider.phone_number,
				"VAR1": self.booking_id,
				"VAR2": complete_origin_address,
				"VAR3": self.merchant.phone_number,
				"VAR4": complete_destination_address,
				"VAR5": self.customer.get_full_name(),
				"VAR6": self.customer.get_full_name(),
				"VAR7": self.customer.phone_number,
				"VAR8": self.pickup_date,
				"VAR9": self.drop_date,
			}
			sms_response = requests.request("POST", settings.TRANSACTIONAL_SMS_URL, data=sms_payload)
			print "SMS sent"
			self.notify_rider = False
		if self.approve == True and self.notify_merchant == True:
			print "Sending SMS To Baker"
			"""Bit.ly URL"""
			bitly_url = "https://api-ssl.bitly.com/v3/shorten"
			bitly_param = {
				"access_token" : "f0917bc54386679c3ada6ba6ca2fe72edeb3d9ca",
				"longUrl" : settings.DOMAIN_NAME + "/merchant/bookings/booking_detail/" + self.booking_id
			}
			bitly_response = requests.request("GET", bitly_url, headers=None, params=bitly_param)
			bitly_response_content = simplejson.loads(bitly_response.text)
			sms_payload = {
				"TemplateName": "Approve MCB order",
				"From": "MCBMRC",
				"To": self.merchant.phone_number,
				"VAR1": self.merchant,
				"VAR2": self.booking_id,
				"VAR3": self.rider.first_name,
				"VAR4": self.rider.phone_number,
				"VAR5": bitly_response_content['data']['url'],
			}
			sms_response = requests.request("POST", settings.TRANSACTIONAL_SMS_URL, data=sms_payload)
			print "SMS sent"
			self.notify_merchant = False
				
		super(Booking, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse("booking_details", kwargs={"booking_id": self.booking_id})


	def get_final_amount(self):
		instance = Booking.objects.get(id=self.id)
		two_places = Decimal(10) ** -2
		sub_total_dec = instance.sub_total
		discount_total_dec = instance.discount_total
		tax_total_dec = Decimal(tax_rate_dec * sub_total_dec).quantize(two_places)
		instance.tax_total = tax_total_dec
		instance.final_total = sub_total_dec - discount_total_dec + tax_total_dec
		instance.save()
		return instance.final_total
	