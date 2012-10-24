from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required #do i need?
from image_grab.models import *
from image_grab.forms import *
from django.conf import settings #do i need?
from django.utils import simplejson #do i need?
# from simplejson import loads
from urllib2 import urlopen
from django.shortcuts import render_to_response, get_object_or_404 #do i need get_object_or_404?
from django.template import RequestContext

def _get_facebook_id(domain_name):	
	try:
		#use faceook search api to retrieve json data
		#parse result
		print "DOMAIN NAME TO SEARCH FOR"
		print domain_name
		path = 'http://graph.facebook.com/search?q=%(domain_name)s&type=page' % {"domain_name": domain_name}
		content = simplejson.loads(urlopen(path).read())	
		#grab facebook id from data.  if none, set facebook_id to None
		print "CONTENT INSIDE GET FACEBOOK ID"
		print content
		first_result= content['data'][0]
		print "FIRST RESULT RETURNED FROM GET FACEBOOK ID ATTEMPT"
		print first_result
		facebook_id = first_result['id']
		print "Facebook ID"
		print facebook_id
	except:
		facebook_id = None
	#return facebook id
	return facebook_id

def _grab_image(facebook_id):
	try:
		#use fql to query for name, profile_image_url and facebook_url
		print "FACEBOOK ID in GRAB IMAGE FUNCTION"
		print facebook_id
		path = 'http://graph.facebook.com/%(facebook_id)s?fields=picture,name,link' % {"facebook_id": facebook_id}
		# path = 'http://graph.facebook.com/fql?q=SELECT name, page_url, pic_small FROM page WHERE page_id=%(facebook_id)s' % {"facebook_id": facebook_id}
		print "PATH to GRAB IMAGE AND OTHER DATA"
		print path
		content = simplejson.loads(urlopen(path).read())	
		#parse result
		print "CONTENT FOUND WHEN GRABBING IMAGE AND OTHER DATA"
		print content
		# first_result= content['data'][0]
		name = content['name']
		profile_image_url = content['picture']['data']['url']
		facebook_url = content['link']
	except:
		name = None
		profile_image_url = None
		facebook_url = None
	#grab and store those 3 items from data.  if not present, set them to nil
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
				domain_name = row[4]
				#check if Vendor with domain_name exists.  
				try:
					vendor = Vendor.objects.get(domain_name=domain_name)
				except Vendor.DoesNotExist: 
					#if not, then call method that uses facebook search api to search for an item by domain_name and returns the facebook id number
					#store facebook id number
					facebook_id = _get_facebook_id(domain_name)
					if facebook_id:
						#call method that uses facebook fql to return facebook profile pic url, facebook url and company name when given a facebook id. 
						variables = _grab_image(facebook_id)
						#store both urls and name
						name = variables['name']
						profile_image_url = variables['profile_image_url']
						facebook_url = variables['facebook_url']
						#get or create Vendor object with name, domain_name, facebook url, facebook pic url, and id
						vendor = Vendor(name=name, domain_name=domain_name, facebook_id=facebook_id, profile_image_url=profile_image_url, facebook_url=facebook_url)
						vendor.save()		
			return HttpResponseRedirect('/admin/image_grab/vendor/')
	else:
		form = UploadFileForm()
	return render_to_response('upload.html', RequestContext(request, {'form': form}))


