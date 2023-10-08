from django.urls import path
from .views import department_tree_view, default_view, department_employees_view, employees_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', default_view, name="default"),
    path('departments-tree/', department_tree_view, name="departments-tree"),
    path('departments-tree/<int:department_id>/', department_employees_view, name='department_employees'),
    path('employees/', employees_view, name="employees"),
]

urlpatterns += staticfiles_urlpatterns()
