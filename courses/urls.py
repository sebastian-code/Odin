from django.conf.urls import patterns, url


urlpatterns = patterns('courses.views',
    url(r'^course/(?P<course_url>\S+)/$', 'show_course', name='show-course'),
    url(r'^course', 'show_all_courses', name='show-all-courses'),
    url(r'^course-materials/(?P<course_id>\S+)/$', 'course_materials', name='course-materials'),
)
