from django.conf.urls import patterns, url


urlpatterns = patterns('applications.views',
    url(r'^$', 'apply', name='apply'),
    url(r'^thanks/$', 'thanks', name='thanks'),
    url(r'^add-solution/$', 'add_solution', name='add_solution'),
    url(r'^solutions/(?P<course_url>\S+)/$', 'solutions', name='solutions'),
)
