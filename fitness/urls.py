from django.conf.urls import patterns, url

from fitness.views import FitnessView

urlpatterns = patterns('',
  url(r'^$', FitnessView.as_view(), name='index'),
  url(r'^save_results/$', 'fitness.views.save_results', name='save_results'),
)