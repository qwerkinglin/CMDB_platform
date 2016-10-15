from django.conf.urls import include, url
import views
from django.contrib import admin

urlpatterns = [
    url("^$", views.projects_index, name="projects_index"),
    url("^submit_task/$", views.submit_task, name="project_submit_task"),
]