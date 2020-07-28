from django.db import models
from .employee_details import EmployeeDetails



class Auditorlist_two(models.Model):
    auditorlisttwo = models.ForeignKey(EmployeeDetails,null=True,related_name='auditorlisttwo',on_delete=models.CASCADE)


    class Meta:
       db_table = 'auditorlist_two'





class ListAuditors(models.Model):
    auditors = models.ForeignKey(EmployeeDetails,null=True,related_name='auditors',on_delete=models.CASCADE)


    class Meta:
       db_table = 'list_auditors'
