import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_task.settings')
django.setup()

import random
from faker import Faker
from datetime import datetime
from apps.employee.models import Department, Employee
from django.db import transaction

fake = Faker()

start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 1, 1)
min_salary = 30000
max_salary = 80000


def random_date(start_date, end_date):
    return fake.date_between_dates(date_start=start_date, date_end=end_date)


def generate_employee():
    full_name = fake.name()
    position = fake.job()
    hire_date = random_date(start_date=start_date, end_date=end_date)
    salary = random.randint(min_salary, max_salary)
    departments = Department.objects.exclude(name='Root')
    department = random.choice(departments)
    return Employee(
        full_name=full_name,
        position=position,
        hire_date=hire_date,
        salary=salary,
        department=department
    )


def generate_departments():
    Department.objects.create(name='Root', level=0)
    levels = 5
    departments_per_level = 25
    for level in range(1, levels + 1):
        for _ in range(departments_per_level):
            name = fake.company()
            parent_department = Department.objects.filter(level=level - 1).order_by('?').first()
            Department.objects.create(name=name, parent_department=parent_department, level=level)


generate_departments()

total_employees = 50000
with transaction.atomic():
    for _ in range(total_employees):
        employee = generate_employee()
        employee.save()

print("Data generation is complete!")
