from django.conf.urls.defaults import *

urlpatterns = patterns('image_grab.views',
    url(r'^$', 'grab_images', name='grab_images'),
)