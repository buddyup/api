from django.conf.urls import patterns, include, url
from django.contrib import admin
from events import views

urlpatterns = patterns(
    '',
    url(r'^event$', views.event, name='event'),
    url(r'^speed$', views.speed, name='speed'),
)
