import simplejson
import requests
from django.shortcuts import render

# Create your views here.

def superadmin_dashboard(request):
	template = "superadmin/index.html"
	context = {
		"page_title": "Dashboard"
	}
	return render(request, template, context)

def superadmin_merchant_list(request):
	template = "superadmin/merchant/merchant_list.html"
	context = {
		"page_title": "Merchant List"
	}
	return render(request, template, context)


def superadmin_merchant_details(request, merchant_id):
	merchant_details_url = "http://kulsofttech.info/mycakebox/API/api_merchant_details.php?merchant_id=1&key=QAZ5I3O6Zh58j9Up"
	merchant_details_response = requests.get(merchant_details_url)
	for item in merchant_details_response.json():
		merchant_name = item['m_name']
		merchant_phone = item['mobile']
		merchant_alt_phone = item['alternate_mobile']
		merchant_address = item['address']
		merchant_email = item['username']
		merchant_joining_date = item['date_of_joining']
		merchant_wallet_balance = item['wallet_balance']
		merchant_referral_code = item['referal_code']

	template = "superadmin/merchant/merchant_details.html"
	context = {
		"page_title": "Merchant Details",
		"merchant_name": merchant_name,
		"merchant_phone": merchant_phone,
		"merchant_alt_phone": merchant_alt_phone,
		"merchant_address": merchant_address,
		"merchant_joining_date": merchant_joining_date,
		"merchant_email": merchant_email,
		"merchant_wallet_balance": merchant_wallet_balance,
		"merchant_referral_code": merchant_referral_code,
	}
	return render(request, template, context)

def superadmin_booking_details(request, booking_id):
	booking_details_url = "http://kulsofttech.info/mycakebox/API/api_merchant_individual_booking.php?merchant_id=1&booking_id=39&key=QAZ5I3O6Zh58j9Up"
	booking_details_response = requests.get(booking_details_url)
	print booking_details_response.json()
	for item in booking_details_response.json():
		print item

	template = "superadmin/booking/booking_details.html"
	context = {
			"page_title": "Booking Details"
	}
	return render(request, template, context)
