from django.conf.urls import patterns, url


urlpatterns = patterns('forum.views',
    url(r'^forum/$', 'show_categories', name='forum'),
    url(r'^category/(?P<category_id>[0-9]+)/$', 'show_category', name='show-category'),
    url(r'^topic/(?P<topic_id>[0-9]+)/$', 'show_topic', name='show-topic'),
    url(r'^add-topic/(?P<category_id>[0-9]+)/$', 'add_topic', name='add-topic'),
    url(r'^edit-topic/(?P<topic_id>[0-9]+)/$', 'edit_topic', name='edit-topic'),
    url(r'^edit-comment/(?P<comment_id>[0-9]+)/$', 'edit_comment', name='edit-comment'),
    url(r'^unsubscribe/(?P<topic_id>[0-9]+)/$', 'unsubscribe', name="unsubscribe"),
    url(r'^subscribe/(?P<topic_id>[0-9]+)/$', 'subscribe', name="subscribe"),
)
