#_*_coding:utf-8_*_
import os,sys
BaseDir = "\\".join(os.path.dirname(os.path.abspath(__file__)).split('\\')[:-2])
sys.path.append(BaseDir)    #加入系统环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CMDB_platform.settings")       #加入django的环境变量
from hosts import models
import django
import multiprocessing,paramiko_handle
from django.core.exceptions import ObjectDoesNotExist
django.setup() #allow outsider scripts invoke django db models

def by_paramiko(task_id):
    try:
        task_obj = models.TaskLog.objects.get(id=task_id)
        pool = multiprocessing.Pool(processes=5)
        res = []
        for h in task_obj.hosts.select_related():
            p = pool.apply_async(paramiko_handle.paramiko_ssh,args=(task_id,h,task_obj.cmd))
            res.append(p)
        pool.close()
        pool.join()

    except ObjectDoesNotExist,e:
        sys.exit(e)

def by_ansible(task_id):
    pass

if __name__ == '__main__':
    required_args = ['-task_id','-run_type']

    for arg in required_args:
        if not arg in sys.argv:
            sys.exit("arg [%s] is required!" % arg)

    if len(sys.argv) <5:
        sys.exit("5 arguments expected bu %s given" % len(sys.argv))

    task_id = sys.argv[sys.argv.index("-task_id") + 1]
    run_type = sys.argv[sys.argv.index("-run_type") +1]

    if hasattr(__import__(__name__),run_type):
        func = getattr(__import__(__name__),run_type)
        func(task_id)
    else:
        sys.exit("Invalid run_type, only support [by_paramiko,by_ansible]")

