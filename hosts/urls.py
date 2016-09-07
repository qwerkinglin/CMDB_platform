from django.conf.urls import include, url
import views
from django.contrib import admin

urlpatterns = [
    url("^$", views.hosts_index, name="hosts_index"),
    url("^files/$", views.hosts_files, name="hosts_files"),
    url("^commands/$", views.hosts_commands, name="hosts_commands"),
    url("^submit_task/$", views.submit_task, name="submit_task"),
    url("^get_task_result/$", views.get_task_result, name="get_task_result"),
    url("^file_upload/$", views.file_upload, name="file_upload"),
    url("^report/asset_with_no_asset_id/$", views.report_no_id, name="asset_report_no_id"),
    url(r'^new_assets/approval/$',views.new_assets_approval,name="new_assets_approval" ),
    url("^report/$", views.report, name="asset_report"),
]