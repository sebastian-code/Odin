from django.conf.urls import patterns, url


urlpatterns = patterns('forum.views',
    url(r'^forum/$', 'show_categories', name='forum'),
    url(r'^forum/category/(?P<category_id>[0-9]+)/$', 'show_category', name='show_category'),
    url(r'^forum/topic/(?P<topic_id>[0-9]+)/$', 'show_topic', name='show_topic'),
    url(r'^forum/add-topic/(?P<category_id>[0-9]+)/$', 'add_topic', name='add_topic'),
    url(r'^forum/edit-topic/(?P<topic_id>[0-9]+)/$', 'edit_topic', name='edit_topic'),
    url(r'^forum/edit-comment/(?P<comment_id>[0-9]+)/$', 'edit_comment', name='edit_comment'),
    url(r'^forum/unsubscribe/(?P<topic_id>[0-9]+)/$', 'unsubscribe', name='unsubscribe'),
    url(r'^forum/subscribe/(?P<topic_id>[0-9]+)/$', 'subscribe', name='subscribe'),
)
