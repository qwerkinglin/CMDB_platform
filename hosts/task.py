#_*_coding:utf-8_*_
import models
from django.db import transaction

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
    def multi_cmd(self):
        print '------going to run cmds-----'
        selected_hosts = set(self.request.POST.getlist("selected_hosts[]"))
        cmd = self.request.POST.get("cmd")
        #create task info
        task_obj = models.TaskLog(
            task_type = self.task_type,
            user_id = self.request.user.id,
            #many to many 关系要创建记录后添加
            cmd = cmd,
        )
        task_obj.save()
        task_obj.hosts.add(*selected_hosts) #添加many to many 关系 必须传入id 传入列表的时候前面加*号

        #create task detail for all hosts will be executed
        for bind_host_id in selected_hosts:
            obj = models.TaskLogDetail(
                child_of_task_id = task_obj.id,
                bind_host_id = bind_host_id,
                event_log = "N/A",
            )
            obj.save()

        return {'task_id':task_obj.id}

    def multi_file_transfer(self):
        pass

    def get_task_result(self):
        task_id = self.request.GET.get('task_id')
        if task_id:
            res_list = models.TaskLogDetail.objects.filter(child_of_task_id=task_id)
            return list(res_list.values(
                                        'id',
                                        'bind_host__host__hostname',
                                        'bind_host__host__wan_ip',
                                        'bind_host__host_user__username',
                                        'date',
                                        'event_log',
                                        'result',
                                        ))
