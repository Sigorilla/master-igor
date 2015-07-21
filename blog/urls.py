from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.BlogList.as_view(), name='index'),
    # url(r'^(?P<page>\d+)/$', views.index, name='page'),
    url(r'^post/$', views.PostCreateView.as_view(), name='create'),
    url(r'^post/(?P<pk>\d+)/$', views.PostView.as_view(), name='detail'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.PostEditView.as_view(), name='edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.PostDeleteView.as_view(), name='delete'),
    # url(r'^post/tag_add/(?P<post_id>\d+)/$', views.tag_add, name='tag_add'),
    # url(r'^post/tag_del/(?P<post_id>\d+)/$', views.tag_del, name='tag_del'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^tag/$', views.TagList.as_view(), name='tags'),
    url(r'^tag/(?P<slug>[-\w]+)/$', views.tag, name='tag'),
)