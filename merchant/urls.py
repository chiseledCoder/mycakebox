from django.conf.urls import include, url
from . import views
from views import *
# (?P<id>\d+)
urlpatterns = [
		url(r'^merchant/login$', views.merchant_login, name='merchant_login'),
		url(r'^merchant/logout$', views.merchant_logout, name='merchant_logout'),
		url(r'^merchant/dashboard$', views.merchant_dashboard, name='merchant_dashboard'),
		url(r'^merchant/customer/get_data/(?P<cust_id>\w+)$', views.get_customer_data, name='get_customer_data'),
		url(r'^merchant/booking/booking_list$', views.merchant_booking_list, name='merchant_booking_list'),
		url(r'^merchant/booking/booking_json', BookingListByMerchantJson.as_view(), name='booking_list_json'),
		url(r'^merchant/booking/book_delivery$', views.book_delivery, name='book_delivery'),
		url(r'^merchant/booking/confirm_booking_details$', views.confirm_booking_details, name='confirm_booking_details'),
		url(r'^merchant/booking/cancel_booking/(?P<booking_id>\w+)$', views.cancel_booking, name='cancel_booking'),
		url(r'^merchant/booking/booking_details/(?P<booking_id>\w+)/$', views.booking_details, name='booking_details'),	
		url(r'^merchant/account/settings$', views.account_settings, name='account_settings'),
		url(r'^merchant/help/documentation$', views.documentation, name='documentation'),
		url(r'^merchant/help/contact$', views.contact, name='contact'),	
	]