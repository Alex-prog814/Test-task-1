from apps.employee.models import Department
from django.core.cache import cache


def build_department_tree():
    departments = cache.get('departments')

    if departments is None:
        departments = Department.objects.all()
        cache.set('departments', departments, 60 * 60 * 24)

    if(departments.count() == 0):
        return

    root_department = departments.get(name='Root')

    def build_tree(department):
        children = departments.filter(parent_department=department)
        if not children:
            return {'id': department.id, 'name': department.name, 'children': []}
        return {'id': department.id, 'name': department.name, 'children': [build_tree(child) for child in children]}

    department_tree = build_tree(root_department)

    return department_tree
