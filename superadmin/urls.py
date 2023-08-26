from django.conf.urls import include, url
from . import views
from views import *
# (?P<id>\d+)
urlpatterns = [
		# url(r'^superadmin/login$', views.superadmin_login, name='superadmin_login'),
		# url(r'^superadmin/logout$', views.superadmin_logout, name='superadmin_logout'),
		url(r'^superadmin/dashboard$', views.superadmin_dashboard, name='superadmin_dashboard'),
		url(r'^superadmin/merchant/merchant_list$', views.superadmin_merchant_list, name='superadmin_merchant_list'),
		url(r'^superadmin/merchant/merchant_details/(?P<merchant_id>\w+)$', views.superadmin_merchant_details, name='superadmin_merchant_details'),
		url(r'^superadmin/booking/booking_details/(?P<booking_id>\w+)$', views.superadmin_booking_details, name='superadmin_booking_details'),
	]