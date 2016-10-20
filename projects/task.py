#^v^! coding: utf-8 ^v^!
__author__ = 'Alex hao'

import models as projects_models
import hosts.models as hosts_models
from django.db import transaction
from django.utils import timezone
from backends import ansible_project_task
from CMDB_platform import settings

class Task(object):
    def __init__(self,request):
        self.request = request
        self.task_type = self.request.POST.get("task_type")

    def handle(self):
        if self.task_type:
            if hasattr(self,self.task_type):
                func = getattr(self,self.task_type)
                return func()
            else:
                raise TypeError

    @transaction.atomic #函数执行完成后统一commit到数据库
    def update(self):
        ansible_module = "script"       #ansible调用的模块
        aaa = "/data/webapp/"
        bbb = "jetty-ronghe3/setup.properties"
        ccc = "2ffd 4g"
        ansible_script_args = ' '+ '"%s"'%aaa +' '+ '"%s"'%bbb +' '+ '"%s"'%ccc     #ansible script模块脚本参数
        ansible_args = settings.ProjectUpdateScript + ansible_script_args               #ansible模块参数
        project_id = self.request.POST.get("projectID")
        bind_hosts_user_id_list = []
        host_ip_list = []
        for bind_host in hosts_models.BindHostToGroup.objects.get(host_group=project_id).bind_hosts.all():
            bind_hosts_user_id_list.append(bind_host.id)
            host_ip_list.append(bind_host.host.lan_ip)
        bind_hosts_user_id_list = set(bind_hosts_user_id_list)
        task_obj = projects_models.ProjectTaskLog(
            task_type = self.task_type,
            user_id = self.request.user.id,
            belong_to_project_id = project_id
            #many to many 关系要创建记录后添加.
        )
        task_obj.save()
        task_obj.hosts.add(*bind_hosts_user_id_list)    #多对多关系添加需要传入 *加id列表
        for bind_host_id in bind_hosts_user_id_list:        #添加相关主机的操作记录
            obj = projects_models.ProjectTaskLogDetail(
                child_of_task_id = task_obj.id,
                bind_host_id = bind_host_id,
                event_log = '<img src="/static/css/plugins/jsTree/throbber.gif" alt="loadimage">',
            )
            obj.save()
        try:
            result = ansible_project_task.main(host_ip_list,ansible_module,ansible_args)    #执行项目任务事件

            for bind_host_id in bind_hosts_user_id_list:                #执行时间结果存入数据库
                obj = projects_models.ProjectTaskLogDetail.objects.get(child_of_task_id = task_obj.id,bind_host_id = bind_host_id,)
                host_ip = hosts_models.BindHostToUser.objects.get(id=bind_host_id).host.lan_ip      #host_ip的type为unicode
                rc = result[host_ip]['rc']
                if rc == 0:
                    script_result = 'success'
                else:
                    script_result = 'failed'
                obj.event_log = result[host_ip]['stdout']
                obj.result = script_result
                obj.date = timezone.now()
                obj.save()
            #添加project_task_log任务结束时间
            task_obj.end_time = timezone.now()
            task_obj.save()
            #print result, type(result)
        except Exception,e:
            print e
        return {'task_id':task_obj.id}

    def get_task_result(self):
        task_id = self.request.GET.get('task_id')
        if task_id:
            res_list = projects_models.ProjectTaskLogDetail.objects.filter(child_of_task_id=task_id)
            return list(res_list.values(
                                        'id',
                                        'bind_host__host__hostname',
                                        'bind_host__host__wan_ip',
                                        'bind_host__host__lan_ip',
                                        'bind_host__host_user__username',
                                        'date',
                                        'event_log',
                                        'result',
                                        ))