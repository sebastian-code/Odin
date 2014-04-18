from django.conf.urls import patterns
from django.contrib.flatpages import views
from django.conf.urls import url


urlpatterns = patterns('website.views',
    url(r'^about-us/$', views.flatpage, {'url': '/about-us/'}, name='about-us'),

    (r'^$', 'index'),
)
