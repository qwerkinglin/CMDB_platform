"""CMDB_platform URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
import hosts.urls as hosts_urls
import projects.urls as project_urls
import myauth.views as myauth_view
from hosts import rest_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^api/', include(rest_urls)),
    url(r'^$', myauth_view.index, name='index'),
    url(r'^login/$', myauth_view.acc_login, name='login'),
    url(r'^logout/$', myauth_view.acc_logout, name='logout'),
    url(r'^hosts/', include(hosts_urls)),
    url(r'^projects/', include(project_urls)),
]
