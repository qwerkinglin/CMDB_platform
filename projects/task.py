#^v^! coding: utf-8 ^v^!
__author__ = 'Alex hao'

import models as projects_models
import hosts.models as hosts_models
from django.db import transaction
from django.utils import timezone
from backends import ansible_project_task
from CMDB_platform import settings
import threading

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

    def _ansible_task(self):
        try:
            result = ansible_project_task.main(self.host_ip_list,self.ansible_module,self.ansible_args)    #执行项目任务事件
            #print result
            for bind_host_id in self.bind_hosts_user_id_list:                #执行事件结果存入数据库
                obj = projects_models.ProjectTaskLogDetail.objects.get(child_of_task_id = self.task_obj.id,bind_host_id = bind_host_id,)
                host_ip = hosts_models.BindHostToUser.objects.get(id=bind_host_id).host.lan_ip      #host_ip的type为unicode
                if 'rc' in result[host_ip]:
                    rc = result[host_ip]['rc']
                    if rc == 0:
                        script_result = 'success'
                    else:
                        script_result = 'failed'
                else:
                    script_result = 'failed'

                if 'msg' in result[host_ip]:
                    obj.event_log = result[host_ip]['msg']
                else:
                    obj.event_log = result[host_ip]['stdout']
                obj.result = script_result
                obj.date = timezone.now()
                obj.save()
            self.task_obj.end_time = timezone.now()      #添加project_task_log任务结束时间
            self.task_obj.save()
        except Exception,e:
            print e

    @transaction.atomic #函数执行完成后统一commit到数据库
    def update(self):
        self.ansible_module = "script"       #ansible调用的模块
        aaa = "/data/webapp/"
        bbb = "jetty-ronghe3/setup.properties"
        ccc = "2ffd 4g"
        ansible_script_args = ' '+ '"%s"'%aaa +' '+ '"%s"'%bbb +' '+ '"%s"'%ccc     #ansible script模块脚本参数
        self.ansible_args = settings.ProjectUpdateScript + ansible_script_args               #ansible模块参数
        project_id = self.request.POST.get("projectID")
        self.bind_hosts_user_id_list = []
        self.host_ip_list = []
        for bind_host in hosts_models.BindHostToGroup.objects.get(host_group=project_id).bind_hosts.all():
            self.bind_hosts_user_id_list.append(bind_host.id)
            self.host_ip_list.append(bind_host.host.lan_ip)
        bind_hosts_user_id_list = set(self.bind_hosts_user_id_list)
        self.task_obj = projects_models.ProjectTaskLog(
            task_type = self.task_type,
            user_id = self.request.user.id,
            belong_to_project_id = project_id
            #many to many 关系要创建记录后添加.
        )

        self.task_obj.save()
        self.task_obj.hosts.add(*bind_hosts_user_id_list)    #多对多关系添加需要传入 *加id列表
        for bind_host_id in bind_hosts_user_id_list:        #添加相关主机的操作记录
            obj = projects_models.ProjectTaskLogDetail(
                child_of_task_id = self.task_obj.id,
                bind_host_id = bind_host_id,
                event_log = '<img src="/static/css/plugins/jsTree/throbber.gif" alt="loadimage">',
            )
            obj.save()

        t = threading.Thread(target=self._ansible_task,args=())     #多线程执行ansible事件任务，解决函数阻塞问题
        t.start()
        return {'task_id':self.task_obj.id}

    def get_project_result(self):
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