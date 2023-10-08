from django.db import models
from django.core.exceptions import ValidationError


class Department(models.Model):
    name = models.CharField(max_length=100)
    parent_department = models.ForeignKey(
        'self', null=True, blank=True, related_name='child_departments', on_delete=models.CASCADE
    )
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def clean(self):
        if self.level > 5:
            raise ValidationError('The maximum hierarchy depth (5 levels) has been exceeded!')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Employee(models.Model):
    full_name = models.CharField(max_length=100, db_index=True)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name
