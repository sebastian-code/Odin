from django.conf.urls import patterns, url

from students import views as students_views
from courses import views as courses_views
from applications import views as applications_views

urlpatterns = patterns('',
    url(r'^students/$', view=students_views.api_students, name='students'),
    url(r'^checkins/$', view=students_views.api_checkins, name='checkins'),
    url(r'^courses/get_video/$', view=courses_views.get_course_video, name='get_video'),
    url(r'^applications/get_applications/$', view=applications_views.get_applications, name='get-applications'),
    url(r'^applications/get_finished_applications/$', view=applications_views.get_finished_applications, name='get-finished-applications'),
    url(r'^applications/get_accepted/$', view=applications_views.get_accepted, name='get-accepted'),

)
