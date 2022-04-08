from msilib import datasizemask
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.db.models import Sum
from datetime import datetime
# Create your views here.


def login(request):
    authenticated = True
    if 'autherisation_id' in request.session:
        return render(request, 'dashboard.html')
    if request.method == 'POST':
        name = request.POST['user_name']
        passwd = request.POST['user_passwd']
        is_authenticated = Admin.objects.filter(
            user_name=name, user_passwd=passwd).exists()
        if is_authenticated:
            request.session['autherisation_id']='049172'
            return redirect('dashboard')
        else:
            
            authenticated = False
    return render(request, 'login.html', {'authenticated': authenticated})


def dashboard(request):
    return render(request, 'dashboard.html')


def add_expense(request):
    if request.method == 'POST':
        name = request.POST['n'].lower()
        dt = request.POST['dt']
        amount = request.POST['amt']

        print(name, amount, dt)
        obj = datetime.strptime(dt, '%Y-%m-%d')
        new_date = str(obj.day)+'/'+str(obj.month)+'/'+str(obj.year)
        data = Expense(name=name, dt=new_date, amount=amount)
        data.save()
        status = 'Expense Added'
        return JsonResponse({'status': status})
    return render(request, 'add_expense.html')

def add_sales(request):
    if request.method=='POST':
        sname = request.POST['sname'].lower()
        dt = request.POST['dt']
        cp = request.POST['cp'] 
        sp = request.POST['sp'] 
        obj = datetime.strptime(dt, '%Y-%m-%d')
        new_date = str(obj.day)+'/'+str(obj.month)+'/'+str(obj.year)
        data=Sales(name=sname,dt=new_date,cost_price=cp,selling_price=sp)
        data.save()
        status = 'Sales Added'
        
        return JsonResponse({'status': status})
    return render(request,'add_sales.html')


def view_expense(request):
    data_set = Expense.objects.all()
    total = 0
    show_total = False
    if request.method == 'POST':

        dt = request.POST['search_date']
        if dt != '':

            obj = datetime.strptime(dt, '%Y-%m-%d')
            search_date = str(obj.day)+'/'+str(obj.month)+'/'+str(obj.year)
            data_set = Expense.objects.filter(dt=search_date)

            for i in data_set:
                total += i.amount
            show_total = True
    return render(request, 'view_expenses.html', {'expenses': data_set, 'total': total,
                                                  'show_total': show_total})

def view_sales(request):
    data_set = Sales.objects.all()
    profit = 0
    total_sales=0
    actual_price=0
    show_total = False
    if request.method == 'POST':

        dt = request.POST['search_date']
        if dt != '':

            obj = datetime.strptime(dt, '%Y-%m-%d')
            search_date = str(obj.day)+'/'+str(obj.month)+'/'+str(obj.year)
            data_set = Sales.objects.filter(dt=search_date)

            for i in data_set:
                total_sales+=i.selling_price
                actual_price+=i.cost_price
            profit=total_sales-actual_price
            show_total = True
            print(total_sales,' ',actual_price)
    return render(request, 'view_sales.html', {'expenses': data_set,  
                                                  'profit': profit,'show_total':show_total})
                                                
                                            
def Profit(request):
    data_set=Sales.objects .values( 'dt').annotate(sp=Sum('selling_price'),cp=Sum('cost_price')).order_by()
    print(data_set)
    return render(request,'profit.html',{'data_set':data_set})