from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def hosts_index(request):
    return render(request, "hosts/hosts.html")

@login_required
def hosts_files(request):
    return render(request, 'hosts/mutilfiles.html')

@login_required
def hosts_commands(request):
    return render(request, 'hosts/mutilcmd.html')