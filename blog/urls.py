from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<page>\d+)/$', views.index, name='page'),
    url(r'^post/$', views.detail, name='first'),
    url(r'^post/(?P<post_id>\d+)/$', views.detail, name='detail'),
    # url(r'^post/tag_add/(?P<post_id>\d+)/$', views.tag_add, name='tag_add'),
    # url(r'^post/tag_del/(?P<post_id>\d+)/$', views.tag_del, name='tag_del'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^tag/$', views.tags, name='tags'),
    url(r'^tag/(?P<slug>[-\w]+)/$', views.tag, name='tag'),
)