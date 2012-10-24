from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from image_grab.models import *
from image_grab.forms import *
from django.utils import simplejson
import urllib2
from urllib2 import urlopen
from django.shortcuts import render_to_response
from django.template import RequestContext
from time import sleep

def _create_or_update_vendor(domain_name):
	#check and get vendor with domain name if it exists.  create one otherwise.
	vendor, created = Vendor.objects.get_or_create(domain_name=domain_name)
	if vendor.profile_image_url:
			return vendor.profile_image_url
	if not vendor.facebook_id:
		#if vendor object doesn't have a facebook_id, then call method that uses facebook search api to search for an item by domain_name and returns the facebook id number.  store number
		vendor.facebook_id = _get_facebook_id(vendor.domain_name)	
	if vendor.facebook_id:
		#call method to retrieve facebook page and return facebook profile pic url, facebook url and company name when given a facebook id. 
		fb_variables = _grab_image(vendor.facebook_id)
		#store both urls and name
		vendor.name = fb_variables['name']
		vendor.profile_image_url = fb_variables['profile_image_url']
		vendor.facebook_url = fb_variables['facebook_url']
		print "Successfully grabbed profile url for %s" % domain_name
	else:
		vendor.name = None
		vendor.profile_image_url = None
		vendor.facebook_url = None
		print "Failed to grab profile url for %s" % domain_name
	vendor.save()
	sleep(2)
	return vendor.profile_image_url

def _get_facebook_id(domain_name, attempt_number=1):
	try:
		#use faceook search api to retrieve json data
		print "Attempting to grab facebook info for %s" % domain_name
		path = 'http://graph.facebook.com/search?q=%(domain_name)s&type=page' % {"domain_name": domain_name}
		content = simplejson.loads(urlopen(path).read())	
		#content is a dictionary of results.  grab facebook id from first search result.  if there aren't any results, then set id to None
		first_result = content['data'][0]
		facebook_id = first_result['id']
	except urllib2.HTTPError, err:  #error is usually because of facebook rate limiting.  pause and try twice more before moving on.
		print "HTTP ERROR: %s" % err  
		attempt_number += 1
		if attempt_number <= 3:
			sleep(2)
			facebook_id = _get_facebook_id(domain_name, attempt_number)
		else:
			facebook_id = None
	except:
		facebook_id = None
	return facebook_id

def _grab_image(facebook_id, attempt_number=1):
	try:
		#use facebook page api to grab name, profile_image_url and facebook_url
		path = 'http://graph.facebook.com/%(facebook_id)s?fields=picture,name,link' % {"facebook_id": facebook_id}
		content = simplejson.loads(urlopen(path).read())	
		name = content['name']
		profile_image_url = content['picture']['data']['url']
		facebook_url = content['link']
	except urllib2.HTTPError, err: #error is usually because of facebook rate limiting.  pause and try twice more before moving on.
		print "HTTP ERROR: %s" % err
		attempt_number += 1
		if attempt_number <= 3:
			sleep(2)
			fb_variables = _grab_image(facebook_id, attempt_number)
			#store both urls and name
			name = fb_variables['name']
			profile_image_url = fb_variables['profile_image_url']
			facebook_url = fb_variables['facebook_url']
		else:
			name = None
			profile_image_url = None
			facebook_url = None
	except:
		name = None
		profile_image_url = None
		facebook_url = None
	return {'name': name, 'profile_image_url': profile_image_url, 'facebook_url': facebook_url}

@staff_member_required
def grab_images(request):
	import csv
	if request.method == "POST":
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			file = form.cleaned_data['file']
			reader = csv.reader(file)
			for row in reader:
				domain_name = row[4].strip()
				_create_or_update_vendor(domain_name)
			return HttpResponseRedirect('/admin/image_grab/vendor/')
	else:
		form = UploadFileForm()
	return render_to_response('upload.html', RequestContext(request, {'form': form}))

def display_image(vendor_pk):
	try:
		vendor = Vendor.objects.get(pk=vendor_pk)
		return HttpResponseRedirect(vendor.profile_image_url)
	except Vendor.DoesNotExist:
		return
