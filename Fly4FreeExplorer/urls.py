"""Fly4FreeExplorer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from DataManager import views

urlpatterns = [
    # url( r'^api/', include( 'api.urls' ) ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^country/$', views.countries),
    url(r'^country/(?P<pk>[0-9]+)$', views.country),
    url(r'^airline/$', views.airlines),
    url(r'^airline/(?P<pk>[0-9]+)$', views.airline),
    url(r'^city/(?P<pk>[0-9]+)$', views.city),
    url(r'^city/.*$', views.cities),
    url(r'^analyze/$', views.analyze),
    # url(r'^airline/', include(airline_urls)),
]
