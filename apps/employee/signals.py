from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Employee, Department


@receiver(post_save, sender=Employee)
@receiver(post_delete, sender=Employee)
def invalidate_employee_cache(sender, instance, **kwargs):
    cache.delete('employees')


@receiver(post_save, sender=Department)
@receiver(post_delete, sender=Department)
def invalidate_department_cache(sender, instance, **kwargs):
    cache.delete('departments')
