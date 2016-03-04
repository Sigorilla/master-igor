from django.conf.urls import url

from fitness import views

urlpatterns = [
    url(r'^$', views.FitnessView.as_view(), name='index'),
    url(r'^save_results/$', views.save_results, name='save_results'),
]
