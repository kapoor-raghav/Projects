from django.shortcuts import render, redirect
from .utilities import save_employee, view_employees, delete_employee
from django.contrib import messages

# Create your views here.
def employee_add(request):
    if request.method == "POST":
        try:
            save_employee(request.POST)
            messages.success(request, 'The form is saved')
        except Exception as e:
            messages.error(request, f'The form has errors {e}')
    return render(request, 'index.html')

def employee_view(request):
    employees = view_employees()
    return render(request, 'employee_view.html', {'emps': employees})

def employee_delete(request, employee_id):
    try:
        delete_employee(employee_id)
        messages.success(request, 'Employee Details successfully deleted')
    except Exception as e:
        messages.error(request, f'{e}')
    return redirect('employee_view')

def home(request):
    return render(request, 'layout.html')