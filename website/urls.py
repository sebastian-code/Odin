from django.conf.urls import patterns
from django.contrib.flatpages import views
from django.conf.urls import url


urlpatterns = patterns('website.views',
    url(r'^about-us/$', views.flatpage, {'url': '/about-us/'}, name='about-us'),
    (r'^$', 'index'),
)


handler400 = 'website.views.page_not_found'
handler500 = 'website.views.server_error'
