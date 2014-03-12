from django.conf.urls import patterns, url


urlpatterns = patterns('faq.views',
    url(r'^FAQ/$', 'show_faqs', name='show-faqs'),
)
