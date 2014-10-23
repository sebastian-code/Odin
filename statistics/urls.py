from django.conf.urls import patterns, url



urlpatterns = patterns('statistics.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),

    url(r'^partners/all/$', 'show_partners_stats', name='show_partners_stats'),
    url(r'^partners/(?P<partner_id>[0-9]+)/$', 'show_partner_stats', name='show_partner_stats'),
    url(r'^companies/all/$', 'show_companies_stats', name='show_companies_stats'),
    # url(r'^companies/(?P<company_id>[0-9]+)/$', 'show_company_stats', name='show_company_stats'),
    # url(r'^assignments/$', 'show_assignments_stats', name='show_assignments_stats'),
    url(r'^assignments/$', 'show_all_assignments_stats', name='show_all_assignments_stats'),
    url(r'^assignments/all$', 'show_all_assignments_stats', name='show_all_assignments_stats'),
    url(r'^assignments/active$', 'show_active_assignments_stats', name='show_active_assignments_stats'),
    url(r'^assignments/expired$', 'show_expired_assignments_stats', name='show_expired_assignments_stats'),

    url(r'^courses/all/$', 'show_courses_stats', name='show_courses_stats'),
    url(r'^courses/(?P<course_id>[0-9]+)/$', 'show_course_stats', name='show_course_stats'),
)
