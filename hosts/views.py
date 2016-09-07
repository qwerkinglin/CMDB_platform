#_*_coding:utf-8_*_
from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
import models,task,json,utils,core
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
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

def new_assets_approval(request):
    if request.method == 'POST':
        request.POST = request.POST.copy()
        approved_asset_list = request.POST.getlist('approved_asset_list')
        approved_asset_list = models.NewAssetApprovalZone.objects.filter(id__in=approved_asset_list)
        response_dic = {}
        for obj in approved_asset_list:
            request.POST['asset_data'] = obj.data       #把待审批的资产数据提取出来放入POST的asset_data中，用data_is_valid_without_id()函数检测POST中asset_data数据的合法性
            ass_handler = core.Asset(request)
            if ass_handler.data_is_valid_without_id():
                # ass_handler.data_inject()
                obj.approved = True
                obj.approved_date = timezone.now()
                obj.approved_by_id = request.user.id
                obj.save()
            response_dic[obj.id]= ass_handler.response
        return render(request,'hosts/new_assets_approval.html',{'new_assets':approved_asset_list,'response_dic':response_dic})
    else:
        ids = request.GET.get('ids')
        id_list = ids.split(',')
        new_assets = models.NewAssetApprovalZone.objects.filter(id__in=id_list)
        return render(request,'hosts/new_assets_approval.html',{'new_assets':new_assets})

@csrf_exempt
@utils.token_required
def report_no_id(request):
    if request.method == 'POST':
        ass_handler = core.Asset(request)
        res = ass_handler.get_asset_id_by_sn()
        return HttpResponse(json.dumps(res))

@csrf_exempt
@utils.token_required
def report(request):
    if request.method == 'POST':
        ass_handler = core.Asset(request)
        if ass_handler.data_is_valid():
            ass_handler.data_inject()
        return HttpResponse(json.dumps(ass_handler.response))
    return HttpResponse('--test--')