#_*_coding:utf-8_*_
import models,os,json
import  subprocess
from django.db import transaction
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
    def multi_cmd(self):
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
                event_log = '<img src="/static/css/plugins/jsTree/throbber.gif" alt="loadimage">',
            )
            obj.save()
         #invoke backens mylti_task script
        p = subprocess.Popen([
            'python',
            settings.MultiTaskScript,
            '-task_id',str(task_obj.id),
            '-run_type',settings.MultiTaskRunType,
        ])
        # 获取该进程pid 在linux有效 上行代码用后面代码替换  ],preexec_fn=os.setsid)
        # print '---->pid:',p.pid    #通过此方法获取pid 可用于强制结束该任务

        return {'task_id':task_obj.id}

    def multi_file_transfer(self):
        # print '----going to upload/download files'
        selected_hosts = set(self.request.POST.getlist("selected_hosts[]"))
        transfer_type = self.request.POST.get("file_transfer_type")
        remote_path = self.request.POST.get("remote_path")
        upload_files = self.request.POST.getlist("upload_files[]")
        #create task info
        data_dic = {
            'remote_path':remote_path,
            'upload_files':upload_files,
        }
        task_obj = models.TaskLog(
            task_type = transfer_type,
            user_id = self.request.user.id,
            #many to many 关系要创建记录后添加
            cmd = json.dumps(data_dic),
        )
        task_obj.save()
        task_obj.hosts.add(*selected_hosts) #添加many to many 关系 必须传入id 传入列表的时候前面加*号

        #create task detail for all hosts will be executed
        for bind_host_id in selected_hosts:
            obj = models.TaskLogDetail(
                child_of_task_id = task_obj.id,
                bind_host_id = bind_host_id,
                event_log = '<img src="/static/css/plugins/jsTree/throbber.gif" alt="loadimage">',
            )
            obj.save()
         #invoke backens mylti_task script
        p = subprocess.Popen([
            'python',
            settings.MultiTaskScript,
            '-task_id',str(task_obj.id),
            '-run_type',settings.MultiTaskRunType,
        ])
        # 获取该进程pid 在linux有效 上行代码用后面代码替换  ],preexec_fn=os.setsid)
        # print '---->pid:',p.pid    #通过此方法获取pid 可用于强制结束该任务

        return {'task_id':task_obj.id}

    def get_task_result(self):
        task_id = self.request.GET.get('task_id')
        if task_id:
            res_list = models.TaskLogDetail.objects.filter(child_of_task_id=task_id)
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
