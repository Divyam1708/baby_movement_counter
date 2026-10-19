from django.urls import path,include
from . import views

app_name='movement'

urlpatterns = [
    path('',views.home,name='home'),
    path('go-to-date/<int:arg_1_dd>-<int:arg_2_mm>-<int:arg_3_yyyy>',views.GoToDate,name='go-to-date'),
    path('delete-movement/<int:arg_1_movement_id>', views.DeleteMovement,name='delete-movement')
]
