
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('employee-add/', views.employee_add, name="employee_add"),
    path('employee-view/', views.employee_view, name="employee_view"),
    path('employee-delete/<str:employee_id>/', views.employee_delete, name="employee_delete")
]
