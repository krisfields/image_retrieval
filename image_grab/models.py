from django.db import models

class Vendor(models.Model):
	name = models.CharField(max_length=200)
	domain_name = models.URLField(max_length=200)
	profile_image_url = models.URLField(max_length=200)
	facebook_id = models.PositiveIntegerField()
	facebook_url = models.URLField(max_length=200)
	def __unicode__(self):
		return self.name
