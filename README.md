image_retrieval
===============

Given a list of vendors, grab profile images for each from social networks (currently facebook only)

Image Retrieval is a blank project to make sure image_grab app is working.
To add image_grab app to a project:
+ move image_grab folder to your project folder

+ to your project's urls.py patterns, add: 
    
        url(r'^image_grab/', include('image_grab.urls')),

+ to INSTALLED_APPS in your project's settings.py, add: 

        'image_grab',

+ to TEMPLATE_DIRS in your project's settings.py, add: 

        os.path.join(PROJECT_ROOT, 'image_grab', 'templates'),

+ run 

        python manage.py syncdb

+ optionally, to create a link to the upload merchant file page directly from primary admin page, in the admin template index.html, right before the last \</div>, add: 
       
        <a href="/image_grab">Grab Images for Vendors</a>