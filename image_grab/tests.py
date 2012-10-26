"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from image_grab.models import *
from image_grab.views import _get_facebook_id as getFBID
from image_grab.views import _grab_image as grabImage
from image_grab.views import _create_or_update_vendor as createOrUpdateVendor
from image_grab.views import display_image as displayImage

class ImageGrabTests(TestCase):
	def test_facebook_id_retrieval(self):
		self.assertEqual(getFBID('AMAZON.COM'), '9465008123')
		self.assertEqual(getFBID('1000BULBS.COM'), '170271204445')
		self.assertEqual(getFBID('BECOME.COM'), '25597601080')
	def test_grab_image_function(self):
		fb_variables = grabImage('25597601080')
		self.assertEqual(fb_variables['name'], 'Become.com')
		self.assertEqual(fb_variables['profile_image_url'], 'http://profile.ak.fbcdn.net/hprofile-ak-ash4/373147_25597601080_882238666_q.jpg')
		self.assertEqual(fb_variables['facebook_url'], 'http://www.facebook.com/becomecom')
	def test_create_or_update_vendor(self):
		self.assertEqual(createOrUpdateVendor('BECOME.COM', 2), 'http://profile.ak.fbcdn.net/hprofile-ak-ash4/373147_25597601080_882238666_q.jpg')
	def test_display_image_function(self):
		vendor_profile_url = createOrUpdateVendor('AMAZON.COM', 2)
		vendor = Vendor.objects.all()[0]
		self.assertNotEqual(displayImage(vendor.pk), None)
