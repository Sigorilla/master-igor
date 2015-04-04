from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Examples:
  url(r'^$', 'main.views.home', name='home'),
  url(r'^gsoc/$', 'main.views.gsoc', name='gsoc'),
  url(r'^scrobbler/$', 'main.views.scrobbler', name='scrobbler'),
  url(r'^schedule/$', 'main.views.schedule', name='schedule'),
  url(r'^about/$', 'main.views.about', name='about'),
  url(r'^base/$', 'main.views.base', name='base'),
  url(r'^projects/$', 'main.views.projects', name='projects'),

  url(r'^admin/', include(admin.site.urls)),

  url(r'^findme/', include('findme.urls')),
  url(r'^fitness/', include('fitness.urls')),
)

handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'
