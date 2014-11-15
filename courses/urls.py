from django.conf.urls import patterns, url


urlpatterns = patterns('courses.views',
    url(r'^course/(?P<course_url>\S+)/$', 'show_course', name='show_course'),
    url(r'^courses/$', 'show_all_courses', name='show_all_courses'),
    url(r'^course/(?P<course_id>[0-9]+)/solutions$', 'show_submitted_solutions', name='show_submitted_solutions'),
    url(r'^course_students/(?P<course_id>[0-9]+)/$', 'show_course_students', name='show_course_students'),

    url(r'^partners/$', 'show_all_partners', name='show_all_partners'),
    url(r'^certificate/(?P<assignment_id>[0-9]+)/$', 'show_certificate', name='show_certificate'),
)
