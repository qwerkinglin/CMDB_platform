from django.conf.urls import include, url
import views
from django.contrib import admin

urlpatterns = [
    url("^$", views.hosts_index, name="hosts_index"),
    url("^files/$", views.hosts_files, name="hosts_files"),
    url("^commands/$", views.hosts_commands, name="hosts_commands"),
    url("^submit_task/$", views.submit_task, name="submit_task"),
]