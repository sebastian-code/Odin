from django.conf.urls import patterns, url


urlpatterns = patterns('statistics.views',
    url(r'^all/$', 'show_all_stats', name='show_all_stats'),
    url(r'^partners/$', 'show_partners_stats', name='show_partner_stats'),
    url(r'^partners/(?P<partner_id>[0-9]+)/$', 'show_partner_stats', name='show_partner_stats'),
    url(r'^companies/$', 'show_companies_stats', name='show_companies_stats'),
    url(r'^companies/(?P<company_id>[0-9]+)/$', 'show_company_stats', name='show_company_stats'),
    url(r'^assignments/$', 'show_assignments_stats', name='show_assignments_stats'),
    url(r'^courses/$', 'show_courses_stats', name='show_courses_stats'),
    url(r'^courses/(?P<course_id>[0-9]+)/$', 'show_course_stats', name='show_course_stats'),
)
