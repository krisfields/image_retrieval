from django.contrib import admin
from image_grab.models import *

class VendorAdmin(admin.ModelAdmin):
	list_display = ['domain_name', 'name', 'facebook_id', 'facebook_url', 'profile_image_url']
	search_fields = ['domain_name', 'name']

admin.site.register(Vendor, VendorAdmin)