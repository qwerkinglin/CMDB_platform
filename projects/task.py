#^v^! coding: utf-8 ^v^!
__author__ = 'Alex hao'

import models as projects_models
import hosts.models as hosts_models
from backends import ansible_project_task

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

    def update(self):
        project_id = self.request.POST.get("projectID")
        bind_hosts_user_id_list = []
        for bind_host in hosts_models.BindHostToGroup.objects.get(host_group=project_id).bind_hosts.all():
            bind_hosts_user_id_list.append(bind_host.id)
        bind_hosts_user_id_list = set(bind_hosts_user_id_list)
        task_obj = projects_models.ProjectTaskLog(
            task_type = self.task_type,
            user_id = self.request.user.id,
            belong_to_project_id = project_id
            #many to many 关系要创建记录后添加
        )
        task_obj.save()
        task_obj.hosts.add(*bind_hosts_user_id_list)    #多对多关系添加需要传入 *加id列表
        for bind_host_id in bind_hosts_user_id_list:
            obj = projects_models.ProjectTaskLogDetail(
                child_of_task_id = task_obj.id,
                bind_host_id = bind_host_id,
                event_log = '<img src="/static/css/plugins/jsTree/throbber.gif" alt="loadimage">',
            )
            obj.save()

        ansible_result = ansible_project_task.ansible_runner()
        print ansible_result
        return {'task_id':task_obj.id}