from django.db import models

class Vendor(models.Model):
	name = models.CharField(max_length=200, blank=True, null=True)
	domain_name = models.CharField(max_length=200)
	profile_image_url = models.URLField(max_length=200, blank=True, null=True)
	facebook_id = models.PositiveIntegerField(blank=True, null=True)
	facebook_url = models.URLField(max_length=200, blank=True, null=True)
	def __unicode__(self):
		return self.domain_name
