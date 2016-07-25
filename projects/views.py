from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def projects_index(request):
    return render(request, "projects/projects.html")