from django.db import models
from QMS.models.common import  EmployeDepartment
from QMS.models.employee_details import EmployeeDetails



class Project_Details(models.Model):
    project_code = models.CharField(max_length=15,null=True)
    project_name = models.CharField(max_length=300,null=True)
    project_type = models.IntegerField(default=0)
    project_start_date = models.DateField(null=True)
    project_end_date = models.DateField(null=True)
    project_status = models.IntegerField(default=0)

    class Meta:
        db_table = 'project_details'


class Teamwise(models.Model):
    tw_project_code = models.ForeignKey(Project_Details,related_name='tw_project_code',null=True, on_delete=models.CASCADE)
    sub_code = models.CharField(max_length=20,null=True)
    manager = models.ForeignKey(EmployeeDetails,related_name='manager',null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(EmployeDepartment,related_name='department_teamwise',null=True, on_delete=models.CASCADE)
    team_manhours = models.IntegerField()
    list_of_auditee = models.ForeignKey(EmployeeDetails,related_name='list_of_auditor',null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'teamwise'
