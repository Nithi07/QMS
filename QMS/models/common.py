from django.db import models



class Audittype(models.Model):
   audittype = models.CharField(max_length = 25)
   auditcode = models.CharField(max_length = 25)

   class Meta:
       db_table = 'audittype'




class EmployePosition(models.Model):

    emp_posn = models.CharField(max_length=50)

    class Meta:
       db_table = 'master_position'



class EmployeDepartment(models.Model):

    department_name = models.CharField(max_length=50)
    dept_code = models.CharField(max_length=50)


    class Meta:
       db_table = 'master_department'
