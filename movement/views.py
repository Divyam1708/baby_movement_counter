from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Movement
from .forms import CreateMovement, GoToDateForm, CreateMovementUnsynchronisedForm
from django.utils import timezone
from datetime import date

def home(request):
    
    today=timezone.localdate()
    movements=Movement.objects.filter(
        movement_time__date=today
    ).order_by('movement_time')
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
    
    
def DeleteDatedMovement(request,arg_1_movement_id):
    movement=Movement.objects.get(id=arg_1_movement_id)
    dd=movement.movement_time.day
    mm=movement.movement_time.month
    yyyy=movement.movement_time.year
    hour=movement.movement_time.hour
    minute=movement.movement_time.minute
    
    if (17<hour<24 and -1<minute<60):
        if(hour==18 and 29<minute<60):
            dd=dd+1 
        elif(hour>18):
            dd=dd+1
            
    movement.delete()
    
    url=reverse(
                'movement:go-to-date', 
                kwargs={
                    'arg_1_dd':dd,
                    'arg_2_mm':mm,
                    'arg_3_yyyy':yyyy
                }
            )
    return redirect(url)
    
    
    
    
def GoToDate(request, arg_1_dd,arg_2_mm,arg_3_yyyy):
    
    movements=Movement.objects.filter(movement_time__date=date(arg_3_yyyy,arg_2_mm,arg_1_dd)).order_by('movement_time')
    
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
            'year':arg_3_yyyy,
            'movement_count':movement_count_today,
        }
    )
    
    
def MonthWiseDayCounter(request, arg_1_month, arg_2_year):
    movements=Movement.objects.filter(
        movement_time__month=arg_1_month,
        movement_time__year=arg_2_year
    )
    movement_count=[]
    for day in range(1,32):
        movement_count.append(movements.filter(movement_time__day=day).count())
        
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


def CreateMovementUnsynchronised(request):
    
    if request.method=='POST':
        form=CreateMovementUnsynchronisedForm(request.POST)
        if (form.is_valid()):
            data=form.cleaned_data['movement_time']
            dd=data.day
            mm=data.month
            yyyy=data.year
            form.save()
            url =reverse(
                'movement:go-to-date',
                kwargs={
                    'arg_1_dd':dd,
                    'arg_2_mm':mm,
                    'arg_3_yyyy':yyyy,
                }
            )
            return redirect(url)
    else:
        form=CreateMovementUnsynchronisedForm()
            
    return render(
        request,
        'movement/CreateMovementUnsynchronised.html',
        context={
            'form':form,
        }
    )