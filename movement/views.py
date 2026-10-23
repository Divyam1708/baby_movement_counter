from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from .models import Movement
from .forms import CreateMovement, GoToDateForm
from django.utils import timezone
from datetime import date

def home(request):
    
    today=timezone.localdate()
    movements=Movement.objects.filter(
        time__date=today
    )
    movement_count_today=movements.count()
    
    if request.method=='POST' and 'movement-recorder' in request.POST:
        form=CreateMovement(request.POST)
        if (form.is_valid):
            form.save()
            return redirect(
                'movement:home'
            )
            
    if request.method=='POST' and 'go-to-date' in request.POST:
        go_to_date_form=GoToDateForm(request.POST)
        if (go_to_date_form.is_valid()):
            dd=go_to_date_form.cleaned_data['day']
            mm=go_to_date_form.cleaned_data['month']
            yyyy=go_to_date_form.cleaned_data['year']
            url=reverse(
                'movement:go-to-date', 
                kwargs={
                    'arg_1_dd':dd,
                    'arg_2_mm':mm,
                    'arg_3_yyyy':yyyy
                }
            )
            return redirect(url)
            
    else:
        form=CreateMovement()   
        go_to_date_form=GoToDateForm()
            
    return render(
        request,
        'movement/Home.html',
        context={
            'movements':movements,
            'form':form,
            'go_to_date_form':go_to_date_form,
            'today':today,
            'movement_count':movement_count_today
        }
    )
    
    

def DeleteMovement(request,arg_1_movement_id):
    Movement.objects.get(id=arg_1_movement_id).delete()
    
    return redirect(
        'movement:home'
    )
    
    
def GoToDate(request, arg_1_dd,arg_2_mm,arg_3_yyyy):
    
    movements=Movement.objects.filter(time__date=date(arg_3_yyyy,arg_2_mm,arg_1_dd))
    movement_count_today=movements.count()
    if request.method=='POST':
        form=GoToDateForm(request.POST)
        if(form.is_valid()):
            dd=form.cleaned_data['day']
            mm=form.cleaned_data['month']
            yyyy=form.cleaned_data['year']
            url=reverse(
                'movement:go-to-date', 
                kwargs={
                    'arg_1_dd':dd,
                    'arg_2_mm':mm,
                    'arg_3_yyyy':yyyy
                }
            )
            return redirect(url)
            
    else:
        form=GoToDateForm()
        
    return render(
        request,
        'movement/DateMovement.html',
        context={
            'movements':movements,
            'form':form,
            'date':f'{arg_1_dd}/{arg_2_mm}/{arg_3_yyyy}',
            'month':arg_2_mm,
            'movement_count':movement_count_today,
        }
    )
    
    
def MonthWiseDayCounter(request, arg_1_month, arg_2_year):
    today_year=timezone.localdate().year
    movements=Movement.objects.filter(
        time__month=arg_1_month,
        time__year=arg_2_year
    )
    movement_count=[]
    for day in range(1,32):
        movement_count.append(movements.filter(time__day=day).count())
        
    per_day_count_this_month=[count for count in movement_count]
    
    return render(
        request,
        'movement/MonthWisePerDayMovement.html',
        context={
            'per_day_movement':per_day_count_this_month,
            'today_year':arg_2_year,
            'today_month':arg_1_month,
        }
    )
