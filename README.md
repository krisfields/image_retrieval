image_retrieval
===============

Given a list of vendors, grab profile images for each from social networks (currently facebook only)

Image Retrieval is a blank project to make sure image_grab app is working.
To add image_grab app to a project:
+ to urls.py patterns, add: url(r'^image_grab/', include('image_grab.urls')),
+ to settings.py, add: 'image_grab',
+ optionally, to create a link to the upload merchant file page, in the admin template base_site.html, right before the last \</div>, add: \<a href="/image_grab">Grab Images for Vendors\</a>