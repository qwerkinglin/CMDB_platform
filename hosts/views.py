from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
import models,task
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
    return render(request, 'hosts/mutilfiles.html')

@login_required
def hosts_commands(request):
    return render(request, 'hosts/mutilcmd.html')

@login_required
def submit_task(request):
    print request.POST
    tas_obj = task.Task(request)
    res = tas_obj.handle()
    return HttpResponse('dddd')