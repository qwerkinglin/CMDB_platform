from django.contrib import admin
import auth_admin
# Register your models here.
import models
from hosts import models as host_models

class HostAdmin(admin.ModelAdmin):
    list_editable = ('enabled','idc')
    list_display = ('hostname','wan_ip','lan_ip','port','out_bandwidth','os_version','idc','enabled')
    search_fields = ('hostname','wan_ip','lan_ip')
    list_filter = ('enabled','idc')

class HostUserAdmin(admin.ModelAdmin):
    list_display = ('username','memo','auth_type')
    list_editable = ('memo',)

class HostBindAdmin(admin.ModelAdmin):
    list_display = ('host','host_user','get_groups')
    list_editable = ('host_user',)
    filter_horizontal = ('host_groups',)

admin.site.register(models.UserProfile,auth_admin.UserProfileAdmin)
admin.site.register(host_models.Host,HostAdmin)
admin.site.register(host_models.HostGroup)
admin.site.register(host_models.HostUser,HostUserAdmin)
admin.site.register(host_models.BindHostToUser,HostBindAdmin)
admin.site.register(host_models.IDC)