#_*_coding:utf-8_*_
import paramiko
from hosts import models
from django.utils import timezone

def paramiko_ssh(task_id,host_obj,task_content):
    # print "going to run:",host_obj,task_content
    bind_host = host_obj
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if bind_host.host_user.auth_type == 'ssh-password':
            s.connect(bind_host.host.wan_ip,
                      int(bind_host.host.port),
                      bind_host.host_user.username,
                      bind_host.host_user.password,
                      timeout=5
                      )
        else:
            pass
            # key = paramiko.RSAKey.from_private_key_file(settings.RSA_PRIVATE_KEY_FILE)
            # s.connect(bind_host.host.wan_ip,
            #           int(bind_host.host.port),
            #           bind_host.host_user.username,
            #           pkey=key,
            #           timeout=5)
        stdin,stdout,stderr = s.exec_command(task_content)
        result = stdout.read(),stderr.read()
        cmd_result = filter(lambda  x:len(x)>0,result)[0]
        result = 'success'
    except Exception,e:
        print(e)
        cmd_result = e
        result = 'failed'

    # for line in cmd_result:
    #     print line

    #save output into db
    log_obj = models.TaskLogDetail.objects.get(child_of_task_id=task_id,bind_host_id=bind_host.id)
    log_obj.event_log = cmd_result
    log_obj.date = timezone.now()
    log_obj.result = result

    log_obj.save()


