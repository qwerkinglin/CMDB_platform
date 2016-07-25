from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    return render(request,'index.html')

@login_required
def acc_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def acc_login(request):
    login_err = ''
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')
        else:
            login_err = 'Username or password is invalid.'
    return  render(request, 'login.html',{'login_err':login_err})