from django.contrib import admin
from .models import Booking, Customer
# Register your models here.
class BookingAdmin(admin.ModelAdmin):
	list_display = (
		'booking_id',
		'merchant',
		'customer',
		'rider',
		'duration',
		'distance',
		'approx_total',
		'final_total',
		'approve',
		'delivery_type',
		'status'
		)
	list_filter = ['merchant', 'customer', 'rider']

admin.site.register(Booking, BookingAdmin)
admin.site.register(Customer)