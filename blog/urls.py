from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.PostListView.as_view(), name='index'),
    # url(r'^archive/$', views.archive, name='archive'),
    url(r'^search/$', views.SearchPostListView.as_view(), name='search'),
    url(r'^post/$', views.PostCreateView.as_view(), name='create'),
    url(r'^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.PostDeleteView.as_view(), name='delete'),
    url(r'^tag/$', views.TagListView.as_view(), name='tags'),
    url(r'^tag/search/$', views.SearchTagListView.as_view(), name='tag-search'),
    url(r'^tag/(?P<slug>[-\w]+)/$', views.PostByTagListView.as_view(), name='tag'),
)