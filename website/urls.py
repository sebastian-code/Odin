from django.conf.urls import patterns

urlpatterns = patterns('website.views',
    (r'^$', 'index'),
)
