#_*_coding:utf-8_*_
from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
import models,task,json,utils
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@login_required
def hosts_index(request):
    selected_gid = request.GET.get('selected_gid')
    if selected_gid:
        host_list = models.BindHostToGroup.objects.get(host_group=selected_gid).bind_hosts.all()
    else:
        host_list = request.user.bind_hosts.select_related()
    return render(request, "hosts/hosts.html",{'host_list':host_list})

@login_required
def hosts_files(request):
    return render(request, 'hosts/mutil_files_transfer.html')

@login_required
def hosts_commands(request):
    return render(request, 'hosts/mutil_cmd.html')

@login_required
def submit_task(request):
    # print request.POST
    tas_obj = task.Task(request)
    res = tas_obj.handle()
    return HttpResponse(json.dumps(res))

@login_required
def get_task_result(request):
    task_obj = task.Task(request)
    res = task_obj.get_task_result()
    return HttpResponse(json.dumps(res,default=utils.json_date_handler))

@csrf_exempt
@login_required
def file_upload(request):
    filename = request.FILES['file']
    file_path =utils.handle_upload_file(request,filename)
    # return HttpResponse(json.dumps({'uploaded_file_path':file_path}))
    return HttpResponse(file_path)

@csrf_exempt
@utils.token_required
def report_no_id(request):
    print request.POST
    response = {
         'error':['fail'],
        'info':[],
        'warning':[]
    }
    return HttpResponse(json.dumps(response))

@csrf_exempt
@utils.token_required
def report(request):
    print request.POST
    response = {
         'error':['fail'],
        'info':[],
        'warning':[]
    }
    return HttpResponse(json.dumps(response))