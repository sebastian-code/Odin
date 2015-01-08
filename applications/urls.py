from django.conf.urls import patterns, url


urlpatterns = patterns('applications.views',
    url(r'^$', 'apply', name='apply'),
    url(r'^/thanks/$', 'thanks', name='thanks')
)
