from django.conf.urls import patterns, url

from students import views as students_views


urlpatterns = patterns('',
    url(r'^students/$', view=students_views.api_students, name='students'),
    url(r'^checkins/$', view=students_views.api_checkins, name='checkins'),
)
