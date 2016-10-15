from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
import models,task,json
# Create your views here.

@login_required
def projects_index(request):
    selected_project_id = request.GET.get('selected_project_id')
    if selected_project_id:
        project_detail = models.ProjectList.objects.get(id=selected_project_id)
        return render(request, "projects/projects_detail.html",{'project_detail':project_detail})
    return render(request, "projects/projects_index.html")

@login_required
def submit_task(request):
    tas_obj = task.Task(request)
    res = tas_obj.handle()
    return HttpResponse(json.dumps(res))

