from django.shortcuts import redirect, render
from .models import *
# Create your views here.


def login(request):
    authenticated=True
    if request.method=='POST':
        name=request.POST['user_name']
        passwd=request.POST['user_passwd']
        is_authenticated=Admin.objects.filter(user_name=name,user_passwd=passwd).exists()
        if is_authenticated:
            return redirect('dashboard')
        else:
            print('Not')
            authenticated=False
    return render(request,'login.html',{'authenticated':authenticated})

def dashboard(request):
    return render(request,'dashboard.html')