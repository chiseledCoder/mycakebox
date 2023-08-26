import operator
import urllib
import logging
import datetime
import requests
import simplejson
import googlemaps
import math
from decimal import Decimal
from datetime import datetime, date
from django.http import JsonResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect, Http404, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core import serializers
from .models import MerchantAccount, Customer
from .forms import LoginForm
from booking.models import Booking
from booking.utils import *
from merchant.utils import *
from django.core import serializers
from django_datatables_view.base_datatable_view import BaseDatatableView
# Create your views here.

def merchant_logout(request):
	logout(request)
	return HttpResponseRedirect('%s'%(reverse("mybaker_login")))

def merchant_login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/merchant/dashboard")
	
	form = LoginForm(request.POST or None)
	btn = "Login"
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		login(request, user)
		messages.success(request, "Successfully Logged In. Welcome Back!")
		return HttpResponseRedirect("/merchant/dashboard")
	context = {
		"form": form,
		"submit_btn": btn,
	}
	return render(request, "merchant/login.html", context)

@login_required(login_url='/merchant/login')
def merchant_dashboard(request):
	merchant = get_object_or_404(MerchantAccount, merchant=request.user)
	bookings = Booking.objects.filter(merchant=merchant)
	total_bookings_count = Booking.objects.filter(merchant=merchant).count()
	upcoming_bookings = Booking.objects.filter(merchant=merchant).exclude(status="Complete")
	upcoming_bookings_count = Booking.objects.filter(merchant=merchant).exclude(status="Complete").count()
	complete_bookings_count = Booking.objects.filter(merchant=merchant, status="Complete").count()
	template = "merchant/index.html"
	context = {
		"page_title" : "Dashboard - Book Cake Delivery in minutes",
		"merchant": merchant,
		"bookings": bookings,
		"total_bookings_count": total_bookings_count,
		"upcoming_bookings" : upcoming_bookings,
		"upcoming_bookings_count": upcoming_bookings_count,
		"complete_bookings_count": complete_bookings_count,
	}
	return render(request, template, context)

@login_required(login_url='/merchant/login')
def get_customer_data(request, cust_id):
	if request.is_ajax:
		get_customer = get_object_or_404(Customer, customer_id=cust_id)
		cust_data = {}
		cust_data['customer_first_name'] = get_customer.first_name
		cust_data['customer_last_name'] = get_customer.last_name
		cust_data['customer_phone'] = get_customer.phone_number
		cust_data['customer_address'] = get_customer.address
		cust_data['customer_locality'] = get_customer.locality
		return HttpResponse(JsonResponse(cust_data))
	return HttpResponse(JsonResponse(cust_data))

@login_required(login_url='/merchant/login')
def merchant_booking_list(request):
	template = "merchant/booking/booking_list.html"
	context = {
		"site_title": "Merchant Booking List"
	}
	return render(request, template, context)

class BookingListByMerchantJson(BaseDatatableView):
	columns = ['booking id', 'customer', 'customer phone', 'drop address', 'rider', 'pickup date', 'drop date', 'status', 'action']
	order_columns = ['booking_id', 'customer']
	max_display_length = 500

	def get_initial_queryset(self):
		merchant = get_object_or_404(MerchantAccount, merchant=self.request.user)
		return Booking.objects.all().filter(merchant=merchant)

	def render_column(self, row, column):
		if column == 'booking id':
			return row.booking_id
		elif column == 'customer':
			return row.customer.get_full_name()
		elif column == 'customer phone':
			return row.customer.phone_number
		elif column == 'drop address':
			return '%s , %s' %(row.destination, row.destination_locality)
		elif column == 'pickup date':
			return row.pickup_date
		elif column == 'drop date':
			return row.drop_date
		elif column == 'status':
			return row.status
		elif column == 'action':
			booking_id = row.booking_id
			return '<a href="/merchant/booking/booking_details/'+booking_id+'"> View More</a>'
		else:
			return super(BookingListByMerchantJson, self).render_column(row, column)

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(BookingListByMerchantJson, self).dispatch(request, *args, **kwargs)

@login_required(login_url='/merchant/login')
def book_delivery(request):
	merchant = get_object_or_404(MerchantAccount, merchant=request.user)
	distance_data ={}
	if request.method == "POST" and request.is_ajax:
		if 'cost_of_cake' not in request.POST:
			cost_of_cake = 0
		else:
			cost_of_cake = request.POST['cost_of_cake']

		if 'weight_of_cake' not in request.POST:
			weight_of_cake = 0
		else:
			weight_of_cake = request.POST['weight_of_cake']

		if 'customer_first_name' not in request.POST:
			customer_first_name = 0
		else:
			customer_first_name = request.POST['customer_first_name']

		if 'customer_last_name' not in request.POST:
			customer_last_name = 0
		else:
			customer_last_name = request.POST['customer_last_name']

		if 'customer_address' not in request.POST:
			customer_address = 0
		else:
			customer_address = request.POST['customer_address']

		if 'customer_locality' not in request.POST:
			customer_locality = 0
		else:
			customer_locality = request.POST['customer_locality']

		if 'customer_phone' not in request.POST:
			customer_phone = 0
		else:
			customer_phone = request.POST['customer_phone']

		if 'customer_alt_phone' not in request.POST:
			customer_alt_phone = 0
		else:
			customer_alt_phone = request.POST['customer_alt_phone']

		if 'instruction' not in request.POST:
			instruction = 0
		else:
			instruction = request.POST['instruction']

		if 'booking_id' not in request.POST:
			booking_id = "ASDFFEKKDS"
		else:
			booking_id = request.POST['booking_id']

		if 'pickup_date' not in request.POST:
			pickup_date = "EKKDS"
		else:
			pickup_date = request.POST['pickup_date']

		if 'pickup_time' not in request.POST:
			pickup_time = "EKKDS"
		else:
			pickup_time = request.POST['pickup_time']

		if 'drop_date' not in request.POST:
			drop_date = "EKKDS"
		else:
			drop_date = request.POST['drop_date']

		if 'drop_time' not in request.POST:
			drop_time = "EKKDS"
		else:
			drop_time = request.POST['drop_time']

		url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins="+merchant.address+"&destinations="+customer_locality+"&key=AIzaSyCRcKLBQYizfeHi8fc1GzihE5TK4KTOYEY"
		googleResponse = urllib.urlopen(url)
		jsonResponse = simplejson.loads(googleResponse.read())

		try:
			customer = get_object_or_404(Customer, phone_number=customer_phone)
		except:
			customer = Customer.objects.create(customer_id=customer_id_generator())
			customer.first_name = customer_first_name
			customer.last_name = customer_last_name
			customer.address = customer_address
			customer.locality = customer_locality
			customer.phone_number = customer_phone
			customer.alt_phone_number = customer_alt_phone
			customer.save()

		try:
			booking = get_object_or_404(Booking, booking_id=booking_id)
		except:
			booking = Booking.objects.create(merchant=merchant, booking_id=booking_id_generator())
			booking.customer = customer
			booking.cake_cost = cost_of_cake
			booking.cake_weight = weight_of_cake
			booking.instruction = instruction
			booking.origin = merchant.address
			booking.origin_address = merchant.locality
			booking.destination = customer.address
			booking.destination_locality = jsonResponse['destination_addresses'][0]
			booking.duration = jsonResponse['rows'][0]['elements'][0]['duration']['text']
			booking.distance = jsonResponse['rows'][0]['elements'][0]['distance']['text']
			booking.pickup_date = pickup_date
			booking.drop_date = drop_date
			booking.save()

		merchant.customer.add(customer)
		merchant.save()
		approx_total_normal = 0
		approx_total_jet = 0 
		approx_total_superjet = 0 
		rate_normal = 0
		rate_jet = 0
		rate_superjet = 0
		first = booking.distance.split()
		if float(first[0]) <= 10.0:
			delivery_type = "Hyperlocal"
			if float(first[0]) < 3.0:
				approx_total_normal = 60
			else:
				approx_total_normal = 60+((float(first[0])-3.0)*12)
			rate_normal = "Rs. 60.0 for 3.0 km, Rs. 12.0/km afterthat upto 10.0 km."
		elif float(first[0]) > 10.0:
			delivery_type = "Long distance"
			approx_total_jet = 200
			if float(first[0]) < 5.0:
				approx_total_superjet = 250
			else:
				approx_total_superjet = 250+((float(first[0])-5.0)*15)
			rate_jet = "Rs. 200.0 flat (Public means of transport will be used)."
			rate_superjet = "Rs. 250.0 for 5.0 km, Rs. 15.0/km afterthat."

		distance_data['booking_id'] = booking.booking_id
		distance_data['cake_cost'] = booking.cake_cost
		distance_data['cake_weight'] = booking.cake_weight
		distance_data['customer'] = "%s %s" %(booking.customer.first_name, booking.customer.last_name)
		distance_data['customer_phone'] = "%s / %s" %(booking.customer.phone_number ,booking.customer.alt_phone_number)
		distance_data['origin'] = booking.origin
		distance_data['destination'] = booking.destination
		distance_data['pickupDateTime'] = booking.pickup_date
		distance_data['dropDateTime'] = booking.drop_date
		distance_data['distance'] = booking.distance
		distance_data['duration'] = booking.duration
		distance_data['instruction'] = booking.instruction
		distance_data['delivery_type'] = delivery_type
		distance_data['rate_normal'] = rate_normal
		distance_data['rate_jet'] = rate_jet
		distance_data['rate_superjet'] = rate_superjet
		distance_data['approx_total_normal'] = math.ceil(approx_total_normal)
		distance_data['approx_total_jet'] = math.ceil(approx_total_jet)
		distance_data['approx_total_superjet'] = math.ceil(approx_total_superjet)


		return HttpResponse(JsonResponse(distance_data))
	return HttpResponse(JsonResponse(distance_data))

@login_required(login_url='/merchant/login')
def confirm_booking_details(request):
	confirmation_data = {}
	if request.POST and request.is_ajax:
		if 'booking_id' not in request.POST:
			booking_id = "Normal"
		else:
			booking_id = request.POST['booking_id']

		if 'delivery_type' not in request.POST:
			delivery_type = "Normal"
		else:
			delivery_type = request.POST['delivery_type']

		if 'approx_total' not in request.POST:
			approx_total = "60"
		else:
			approx_total = request.POST['approx_total']

		booking = get_object_or_404(Booking, booking_id=booking_id)
		booking.delivery_type = delivery_type
		booking.approx_total = approx_total
		booking.save()
		confirmation_data['success'] = "True"
		messages.success(request, "Your booking id "+booking_id+" is submitted successfully.")
		return HttpResponse(JsonResponse(confirmation_data))
	confirmation_data['success'] = "False"
	return HttpResponse(JsonResponse(confirmation_data))

def cancel_booking(request, booking_id):
	booking = get_object_or_404(Booking, booking_id=booking_id)
	cancellation_data = {}
	if request.is_ajax:
		booking.instruction = "Booking cancelled by merchant"
		booking.status = "Cancelled"
		booking.save()
		cancellation_data['success'] = "True"
		return HttpResponse(JsonResponse(cancellation_data))
	cancellation_data['success'] = "False"
	return HttpResponse(JsonResponse(cancellation_data))


@login_required(login_url='/merchant/login')
def booking_details(request, booking_id):
	booking = get_object_or_404(Booking, booking_id=booking_id)
	gmaps = googlemaps.Client(key='AIzaSyCRcKLBQYizfeHi8fc1GzihE5TK4KTOYEY')

	# Geocoding an address
	geocode_result = gmaps.geocode("Rutu Park, Thane West, Thane, Maharashtra")

	# Look up an address with reverse geocoding
	reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

	# Request directions via public transit

	# directions_result = gmaps.directions("Rutu Park, Thane West, Thane, Maharashtra","Swastik Residency, Swastik Residency Road, Thane West, Thane, Maharashtra,", mode="driving")
	url = "https://maps.googleapis.com/maps/api/directions/json?origin=Rutu Park, Thane West, Thane, Maharashtra&destination=Swastik Residency, Swastik Residency Road, Thane West, Thane, Maharashtra&key=AIzaSyCRcKLBQYizfeHi8fc1GzihE5TK4KTOYEY"
	googleResponse = urllib.urlopen(url)
	jsonResponse = simplejson.loads(googleResponse.read())
	steps = []
	for item in jsonResponse['routes'][0]['legs'][0]['steps']:
		steps.append("via:enc:"+item['polyline']['points']+":|")
		
		
	template = "merchant/booking/booking_details.html"
	context = {
		"page_title": "Booking Details for " + str(booking_id),
		"booking_id": booking_id,
		"booking": booking,
		"steps" : steps
	}
	return render(request, template, context)

@login_required(login_url='/merchant/login')
def account_settings(request):
	template = "merchant/account_settings.html"
	context = {

	}
	return render(request, template, context)

@login_required(login_url='/merchant/login')
def documentation(request):
	template = "merchant/documentation.html"
	context = {

	}
	return render(request, template, context)

@login_required(login_url='/merchant/login')
def contact(request):
	template = "merchant/contact.html"
	context = {

	}
	return render(request, template, context)
	
