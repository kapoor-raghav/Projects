
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('employee-add/', views.employee_add, name="employee_add")
]
