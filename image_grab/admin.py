from django.contrib import admin
from image_grab.models import *

class VendorAdmin(admin.ModelAdmin):
	list_display = ['domain_name', 'profile_image', 'name', 'facebook_id', 'facebook_link', 'profile_image_link']
	search_fields = ['domain_name', 'name']

	def profile_image(self, obj):
		if obj.profile_image_url:
			return '<a href="%s"><img src="%s"></a>' % (obj.profile_image_url, obj.profile_image_url)
		else:
			return obj.profile_image_url
	profile_image.allow_tags = True
	profile_image.short_description = 'Profile image'
	profile_image.admin_order_field = 'profile_image_url'

	def profile_image_link(self, obj):
		if obj.profile_image_url:
			return '<a href="%s">%s</a>' % (obj.profile_image_url, obj.profile_image_url)
		else:
			return obj.profile_image_url
	profile_image_link.allow_tags = True
	profile_image_link.short_description = 'Profile image url'
	profile_image_link.admin_order_field = 'profile_image_url'

	def facebook_link(self, obj):
		if obj.facebook_url:
			return '<a href="%s">%s</a>' % (obj.facebook_url, obj.facebook_url)
		else:
			return obj.facebook_url
	facebook_link.allow_tags = True
	facebook_link.short_description = 'Facebook url'
	facebook_link.admin_order_field = 'facebook_url'

admin.site.register(Vendor, VendorAdmin)