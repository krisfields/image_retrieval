from django.contrib import admin
from image_grab.models import *

class VendorAdmin(admin.ModelAdmin):
	list_display = ['domain_name', 'name', 'facebook_id', 'facebook_link', 'profile_image']
	search_fields = ['domain_name', 'name']

	def profile_image(self, obj):
		if obj.profile_image_url:
			return '<a href="%s">%s</a>' % (obj.profile_image_url, obj.profile_image_url)
		else:
			return obj.profile_image_url
	profile_image.allow_tags = True
	profile_image.short_description = 'Profile image url'

	def facebook_link(self, obj):
		if obj.facebook_url:
			return '<a href="%s">%s</a>' % (obj.facebook_url, obj.facebook_url)
		else:
			return obj.facebook_url
	facebook_link.allow_tags = True
	facebook_link.short_description = 'Facebook url'

admin.site.register(Vendor, VendorAdmin)