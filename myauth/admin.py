#_*_coding:utf8_*_
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
import auth_admin
# Register your models here.
import models
from hosts import models as host_models

class HostAdmin(admin.ModelAdmin):
    list_editable = ('hostname',)
    list_display = ('sn','hostname','wan_ip','lan_ip','port','os_version','idc','out_bandwidth','enabled')
    search_fields = ('hostname','wan_ip','lan_ip','sn')
    list_filter = ('enabled','idc')

class HostUserAdmin(admin.ModelAdmin):
    list_display = ('username','memo','auth_type')
    list_editable = ('memo',)

class HostBindAdmin(admin.ModelAdmin):
    list_display = ('host','host_user',)
    list_editable = ('host_user',)

class GroupBindAdmin(admin.ModelAdmin):
    list_display = ("host_group","get_hosts")
    filter_horizontal = ('bind_hosts',)

class AssetApprovalZoneAdmin(admin.ModelAdmin):
    list_display = ('approved','sn','asset_type','wan_ip','lan_ip','cpu_num','memory_size','disk_size','os_version','ssh_port','date','approved_by','approved_date')
    list_filter = ('approved',)
    actions = ['approve_selected_objects']
    def approve_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/hosts/new_assets/approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
    approve_selected_objects.short_description = "批准资产入库"

admin.site.register(models.UserProfile,auth_admin.UserProfileAdmin)
admin.site.register(host_models.Host,HostAdmin)
admin.site.register(host_models.HostGroup)
admin.site.register(host_models.HostUser,HostUserAdmin)
admin.site.register(host_models.BindHostToUser,HostBindAdmin)
admin.site.register(host_models.IDC)
admin.site.register(host_models.BindHostToGroup,GroupBindAdmin)
admin.site.register(host_models.TaskLog)
admin.site.register(host_models.TaskLogDetail)
admin.site.register(host_models.NewAssetApprovalZone,AssetApprovalZoneAdmin)