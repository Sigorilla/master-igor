from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.contrib import admin
admin.autodiscover()

import views

urlpatterns = [
    # Examples:
    # url(r'^$', views.home, name='home'),
    url(r'^gsoc/$', views.gsoc, name='gsoc'),
    url(r'^scrobbler/$', views.scrobbler, name='scrobbler'),
    url(r'^schedule/$', views.schedule, name='schedule'),
    url(r'^about/$', views.home, name='about'),
    url(r'^about/travel/$', views.travel, name='travel'),
    url(r'^base/$', views.base, name='base'),
    url(r'^projects/$', views.projects, name='projects'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^fitness/', include('fitness.urls')),
    url(r'^', include('blog.urls', namespace='blog')),
    # url(r'^test/', RedirectView.as_view(url=reverse_lazy('joinme:index')), name='redirect-joinme'),
]

handler404 = views.handler404
handler403 = views.handler403
handler500 = views.handler500
