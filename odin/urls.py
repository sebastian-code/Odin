from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),
    url(r'^tinymce/', include('tinymce.urls')),
    
    url(r'', include('website.urls')),
    url(r'', include('courses.urls', namespace='courses')),
    url(r'', include('faq.urls')),
    url(r'', include('students.urls', namespace='students')),
    url(r'', include('forum.urls', namespace='forum')),

)
