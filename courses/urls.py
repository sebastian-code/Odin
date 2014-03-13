from django.conf.urls import patterns, url


urlpatterns = patterns('courses.views',
    url(r'^course/(?P<course_id>\d+)/$', 'show_course', name='show-course'),
url(r'^course', 'show_all_courses', name='show-all-courses'),
)
