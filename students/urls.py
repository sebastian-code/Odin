from django.conf.urls import patterns, url

urlpatterns = patterns('students.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^api/students/$', 'api_students', name='api-students'),
    url(r'^assignment/(?P<id>[0-9]+)/$', 'assignment', name='assignment'),
    url(r'^accounts/profile/$', 'user_profile', name='user-profile'),
    url(r'^set-check-in/$', 'set_check_in', name='set-check-in'),
    url(r'^accounts/edit/$', 'edit_profile', name='edit-profile'),
    url(r'^logout/$', 'logout', name='logout'),
)