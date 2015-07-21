from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
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
  url(r'^joinme/', include('joinme.urls', namespace="joinme")),
  url(r'^test/', RedirectView.as_view(url=reverse_lazy("joinme:index")), name="redirect-joinme"),
)

handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'
