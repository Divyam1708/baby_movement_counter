from django.urls import path,include
from . import views

app_name='movement'

urlpatterns = [
    path('',views.home,name='home'),
    path('create-movement-unsynchronised',views.CreateMovementUnsynchronised,name='create-movement-unsynchronised'),
    path('go-to-date/<int:arg_1_dd>-<int:arg_2_mm>-<int:arg_3_yyyy>',views.GoToDate,name='go-to-date'),
    path('delete-movement/<int:arg_1_movement_id>', views.DeleteMovement,name='delete-movement'),
    path('delete-dated-movement/<int:arg_1_movement_id>', views.DeleteDatedMovement,name='delete-dated-movement'),
    path('month-wise-per-day-counter/<int:arg_1_month>-<int:arg_2_year>',views.MonthWiseDayCounter,name='month-wise-per-day-counter'),
]

