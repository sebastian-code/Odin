from django.conf.urls import patterns, url

urlpatterns = patterns('forum.views',
    url(r'^forum/$', 'show_categories', name='forum'),
)