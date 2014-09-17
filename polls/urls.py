from django.conf.urls import patterns, url


urlpatterns = patterns('polls.views',
    url(r'^(?P<poll_id>\d+)/$', 'poll', name='vote'),
    url(r'^(?P<poll_id>\d+)/results/$', 'results', name='results'),
)
