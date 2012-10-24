from django.contrib import admin
from image_grab.models import *

class VendorAdmin(admin.ModelAdmin):
	list_display = ['name', 'domain_name', 'facebook_id', 'facebook_url', 'profile_image_url']

admin.site.register(Vendor, VendorAdmin)