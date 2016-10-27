#_*_coding:utf-8_*_
import paramiko,json
from hosts import models
from django.utils import timezone
from CMDB_platform import settings

def paramiko_sftp(task_id,host_obj,task_content,task_type,user_id):
    bind_host = host_obj
    try:
        t = paramiko.Transport((bind_host.host.lan_ip,int(bind_host.host.port) ))
        if bind_host.host_user.auth_type == 'ssh-password':
            t.connect(username=bind_host.host_user.username,password=bind_host.host_user.password)
        else:
            pass
            #key = paramiko.RSAKey.from_private_key_file(settings.RSA_PRIVATE_KEY_FILE)
            #t.connect(username=bind_host.host_user.username,pkey=key)
        sftp = paramiko.SFTPClient.from_transport(t)
        task_dic = json.loads(task_content)

        if task_type == 'file_send':
            upload_files = task_dic['upload_files']
            for file_path in upload_files:
                file_abs_path = "%s/%s/%s" %(settings.FileUploadDir,user_id,file_path)
                remote_filename = file_path.split("/")[-1]
                # print 'sending [%s] to [%s]'% (remote_filename,task_dic['remote_path'])
                sftp.put(file_abs_path,"%s/%s" %(task_dic['remote_path'],remote_filename))
                output_upload_list = ', '.join(map(lambda x:x.split('/')[1],upload_files))
            cmd_result = "send files [ %s ] to remote path [ %s ] successful" %(output_upload_list,task_dic['remote_path'])
            result = 'success'
        else:
            pass
    except Exception,e:
        print e
        cmd_result = e
        result = 'failed'
    log_obj= models.TaskLogDetail.objects.get(child_of_task_id=task_id,bind_host_id=bind_host.id)
    log_obj.event_log = cmd_result
    log_obj.date = timezone.now()
    log_obj.result = result
    log_obj.save()

def paramiko_ssh(task_id,host_obj,task_content):
    # print "going to run:",host_obj,task_content
    bind_host = host_obj
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if bind_host.host_user.auth_type == 'ssh-password':
            s.connect(bind_host.host.lan_ip,
                      int(bind_host.host.port),
                      bind_host.host_user.username,
                      bind_host.host_user.password,
                      timeout=3
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
        out_status = stdout.channel.recv_exit_status() #执行命令的返回值
        if result[0] or result[1]:
            cmd_result = filter(lambda  x:len(x)>0,result)[0]
        else:
            cmd_result = "[ %s ] [ return %s ]" %(task_content,out_status)
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


