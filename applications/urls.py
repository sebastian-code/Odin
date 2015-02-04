from django.conf.urls import patterns, url


urlpatterns = patterns('applications.views',
    url(r'^apply/$', 'apply', name='apply'),
    url(r'^thanks/$', 'thanks', name='thanks'),
    url(r'^thanks-user/$', 'thanks_user', name='thanks_user'),
    url(r'^applications/add-solution/$', 'add_solution', name='add_solution'),
    url(r'^applications/(?P<course_url>\S+)/$', 'show_submitted_applications', name='show_submitted_applications'),
    url(r'^applications/(?P<course_url>\S+)/solutions$', 'solutions', name='solutions'),
)
