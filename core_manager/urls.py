from django.conf.urls import include, patterns, url
import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
