from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.core.paginator import Paginator
from .models import Department, Employee
from .utils import build_department_tree
import json


def default_view(request):
    return HttpResponseRedirect('/departments-tree/')


def department_tree_view(request):
    departments = cache.get('departments')

    if departments is None:
        departments = Department.objects.all()
        cache.set('departments', departments, 60 * 60 * 24)

    department_tree = json.dumps(build_department_tree())

    return render(request, 'employee/department_tree.html', {
        'departments': departments,
        'department_tree': department_tree
    })


def department_employees_view(request, department_id):
    employees = cache.get('employees')
    departments = cache.get('departments')

    if employees is None:
        employees = Employee.objects.all()
        cache.set('employees', employees, 60 * 60 * 24)

    if departments is None:
        departments = Department.objects.all()
        cache.set('departments', departments, 60 * 60 * 24)

    department = departments.get(id=department_id)

    employees = employees.filter(department=department)

    paginator = Paginator(employees, 50)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'employee/department_employees.html', {
        'department': department,
        'employees': page,
    })


def employees_view(request):
    employees = cache.get('employees')

    if employees is None:
        employees = Employee.objects.select_related('department').all()
        cache.set('employees', employees, 60 * 60 * 24)

    paginator = Paginator(employees, 100)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'employee/employees.html', {
        'employees': page,
    })
