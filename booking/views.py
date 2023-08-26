import operator
import urllib
import logging
import datetime
import requests
import simplejson
import math
import googlemaps
from datetime import datetime
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
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core import serializers
from booking.models import Booking
from booking.utils import *
from merchant.utils import *
from merchant.models import *

# Create your views here.

	# Views for RESTful Android app
# def merchant_login(request):
# 	if request.user.is_authenticated:
# 		return HttpResponseRedirect(reverse("merchant_dashboard"))
# 	else:
# 		if request.method == "POST":
# 			if "username" not in request.POST:
# 				username = None
# 			else:
# 				username = request.POST["username"]

# 			if "password" not in request.POST:
# 				password = None
# 			else:
# 				password = request.POST["password"]

# 			data = {
# 				"username": username,
# 				"password": password,
# 				"client_id": settings.ANDROID_CLIENT_ID,
# 				"client_secret": settings.ANDROID_CLIENT_SECRET,
# 				"grant_type": "password"
# 			}
# 			response = requests.post('https://cakemporos-logistics.herokuapp.com/api/user/oauth/token', data = data)
# 			if response.status_code == 200:
# 				user = User.objects.get(username=username)
# 				merchant_account = MerchantAccount.objects.get(merchant=user)
# 				if user.check_password(password):
# 					for key, value in response.json().iteritems():
# 						if key == "access_token":
# 							merchant_account.access_token = value
# 							merchant_account.save()
# 						elif key == "refresh_token" :
# 							merchant_account.refresh_token = value
# 							merchant_account.save()
# 					messages.success(request, "Successfully Logged In. Welcome Back!")
# 					user = authenticate(username=username, password=password)
# 					login(request, user)
# 					return HttpResponseRedirect(reverse("merchant_dashboard"))
# 			else:
# 				return HttpResponseRedirect(reverse("merchant_login"))
# 		template = "merchant/login.html"
# 		context = {
# 			"page_title" : "Login"
# 		}
# 		return render(request, template, context)

# def merchant_logout(request):
# 	logout(request)
# 	return HttpResponseRedirect("/merchant/login")

# @login_required(login_url='/merchant/login')
# def merchant_dashboard(request):
# 	template = "merchant/index.html"
# 	context = {
# 	"page_title" : "Dashboard - Book Delivery in minutes"
# 	}
# 	return render(request, template, context)

# def merchant_quickbook(request):
# 	user = request.user
# 	merchant_account = MerchantAccount.objects.get(merchant=user)
# 	data = {
# 		"refresh_token" : merchant_account.refresh_token,
# 		"client_id" : settings.ANDROID_CLIENT_ID,
# 		"client_secret": settings.ANDROID_CLIENT_SECRET,
# 		"grant_type": "refresh_token"
# 	}
# 	print data
# 	refresh_header = {
# 	"Content-Type" : "application/json"
# 	}
# 	refresh_response = requests.post('https://cakemporos-logistics.herokuapp.com/api/user/oauth/token', data = data)
# 	print refresh_response.json()
# 	if refresh_response.status_code == 200:
# 		for key, value in refresh_response.json().iteritems():
# 			if key == "access_token":
# 				merchant_account.access_token = value
# 				merchant_account.save()
# 			elif key == "refresh_token" :
# 				merchant_account.refresh_token = value
# 				merchant_account.save()
# 	quick_headers = {
# 		"Content-Type" : "application/json",
# 		"x-access-token": merchant_account.access_token
# 	}
# 	quick_book = {}
# 	quick_book['status'] = "PENDING"
# 	quick_book['cakeType'] = "Normal"
# 	quick_book['cost'] = "723"
# 	quick_book['pickUpDate'] = "12/01/2017 21:53:00"
# 	quick_book['dropDate'] = "12/01/2017 23:00:00"
# 	quick_book['altPhone'] = "9988998899"
# 	quick_book['weight'] = "ONE"
# 	quick_book['address'] = "Sminu Apt"
# 	quick_book['locality'] = {
# 		"name" : "IC Colony, Borivali",
# 		"_id" : "5831a2d330b46c142050f5bd"
# 	}
# 	quick_book['customer'] = {

# 		"address" : "Swastik Residence",
# 		"firstName": "Shashank",
# 		"lastName": "Srivastava",
# 		"phone":"9766526943"
# 		}
# 	quick_book['customer']['locality'] = {
# 			"name" : "Anand Nagar, Thane",
# 			"_id" : "5831a2d430f33c1420094730"
# 		}
# 	quick_book['dropAltPhone'] = "9096081092"
# 	quick_response = requests.post("https://cakemporos-logistics.herokuapp.com/api/user/baker/order/", data=simplejson.dumps(quick_book), headers=quick_headers)
# 	print quick_response.status_code
# 	print quick_response.text
# 	return HttpResponse(JsonResponse(quick_response.json()))





