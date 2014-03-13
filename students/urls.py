from django.conf.urls import patterns, url

urlpatterns = patterns('students.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^profile/$', 'user_profile', name='user-profile'),
    # url(r'^logout/$', 'logout', name='logout'),
)