from django.conf.urls import patterns, url


urlpatterns = patterns('students.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^assignment/(?P<id>[0-9]+)/$', 'assignment', name='assignment'),
    url(r'^assignment/(?P<id>[0-9]+)/solutions/$', 'assignment_solutions', name='assignment_solutions'),
    url(r'^solutions/(?P<course_url>\S+)/$', 'solutions', name='solutions'),
    url(r'^add-solution/$', 'add_solution', name='add_solution'),
    url(r'^accounts/profile/$', 'user_profile', name='user_profile'),
    url(r'^set-check-in/$', 'set_check_in', name='set_check_in'),
    url(r'^accounts/edit/$', 'edit_profile', name='edit_profile'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^github-login/$', 'github_login'),
)
