from django.db import models
from .common import EmployePosition, EmployeDepartment


class EmployeeDetails(models.Model):
    emp_code = models.CharField(max_length=3)
    emp_name = models.CharField(max_length=50)
    emp_department = models.ForeignKey(EmployeDepartment,null=True,related_name='emp_department',on_delete=models.CASCADE)
    emp_position = models.ForeignKey(EmployePosition,null=True, related_name='emp_position',on_delete=models.CASCADE)
    emp_reporting_to = models.ForeignKey('self', related_name='report_to',on_delete=models.CASCADE)
    emp_approved_by = models.ForeignKey('self', related_name='approved_by',on_delete=models.CASCADE)
    emp_status = models.CharField(max_length=20)


    class Meta:
       db_table = 'employee_details'
