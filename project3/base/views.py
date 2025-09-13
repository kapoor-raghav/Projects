from django.shortcuts import render
from .utilities import save_employee
from django.contrib import messages

# Create your views here.
def employee_add(request):
    print("Employee Added")
    if request.method == "POST":
        try:
            post_data = request.POST.copy()
            post_data.pop('csrfmiddlewaretoken', None)
            print(post_data)
            save_employee(post_data)
            messages.success(request, 'The form is saved')
        except Exception as e:
            print(e)
            messages.error(request, f'The form has errors {e}')
    return render(request, 'index.html')