from django.contrib import admin
from .models import MerchantAccount
# Register your models here.

class MerchantAccountAdmin(admin.ModelAdmin):
	list_display = [
		'merchant',
		'phone_number',
		'address'
	]
admin.site.register(MerchantAccount, MerchantAccountAdmin)