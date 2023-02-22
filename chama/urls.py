from django.conf.urls import include, patterns, url
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^digicert', views.digicert, name='digicert'),
]
