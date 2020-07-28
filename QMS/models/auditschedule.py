from django.db import models
from QMS.models import ListAuditors
from QMS.models import  Audittype
from QMS.models.common import  EmployeDepartment
from QMS.models.employee_details import EmployeeDetails
from django.contrib.postgres.fields import ArrayField



class Project_Details(models.Model):
    project_code = models.CharField(max_length=15,null=True)
    project_name = models.CharField(max_length=300,null=True)
    project_type = models.CharField(max_length=10)
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


class Auditschedule(models.Model):
    schedule_auditype = models.ForeignKey(Audittype,related_name='audit_type', on_delete=models.CASCADE)
    schedule_job_code = models.CharField(max_length=15,null=True)
    schedule_project = models.ForeignKey(Project_Details,null=True,related_name='schedule_project', on_delete=models.CASCADE)
    schedule_sub_job_code = models.CharField(max_length=15,blank=True,null=True)
    schedule_job_audit_no = models.CharField(max_length=15,blank=True,null=True)
    schedule_audit_no = models.CharField(max_length=50 ,blank=True,null=True)
    schedule_audit_code = models.CharField(max_length=50,blank=True,null=True)
    schedule_audit_date = models.DateField(null=True)
    schedule_audit_time = models.TimeField(null=True)
    schedule_auditee_list = models.ManyToManyField(EmployeeDetails, blank=True, related_name='auditee_list' )
    schedule_auditor_list = models.ManyToManyField(ListAuditors, blank=True, related_name='auditor_list' )
    schedule_department_status = models.IntegerField(default=0)
    schedule_department_username = ArrayField(models.CharField(max_length=50,blank=True),null=True,blank=True,default=list)
    schedule_department_date = models.DateField(blank=True,null=True)
    schedule_final_auditor_list = models.ManyToManyField(ListAuditors, blank=True, related_name='final_auditor_list')
    schedule_team_member_list = models.ManyToManyField(EmployeeDetails, blank=True, related_name='team_member_list')
    schedule_audit_mr_status = models.IntegerField(default=0)
    schedule_description = models.CharField(max_length=15,blank=True,null=True)
    schedule_audit_status = models.IntegerField(default=0)
    comment_status = models.CharField(max_length=200,null=True)
    schedule_file_path = models.URLField(max_length = 500,blank=True,null=True)
    schedule_iso_year = models.CharField(max_length = 50,null=True)
    create_by = models.CharField(max_length=50,null=True)
    create_on = models.DateTimeField(auto_now=True,null=True)
    create_ip = models. GenericIPAddressField(blank=True,null=True)
    modified_by = models.CharField(max_length=50,null=True)
    modified_on = models.DateTimeField(auto_now=True)
    modified_ip = models. GenericIPAddressField(blank=True,null=True)

    class Meta:
       db_table = 'audit_schedule'



class Postpond(models.Model):
    auditschedule = models.ForeignKey(Auditschedule,related_name='schedule_id',null=True, on_delete=models.CASCADE)
    post_date = models.DateField(null=True)
    post_time = models.TimeField(null=True)
    reason = models.TextField(null=True)

    class Meta:
        db_table = 'postpond'



class Cancel(models.Model):
    auditschedule = models.ForeignKey(Auditschedule,related_name='sch_id', on_delete=models.CASCADE)
    cancelled_reason = models.TextField()
    modified_by = models.CharField(max_length=50,null=True)
    modified_on = models.DateTimeField(auto_now=True)
    modified_ip = models. GenericIPAddressField(blank=True,null=True)


    class Meta:
        db_table = 'cancel'








#
#
# class AuditscheduleConfirm(models.Model):
#     auditschedule_id = models.CharField(max_length=4,null=True)
#     auditee_name = models.CharField(max_length=50,null=True)
#     auditee_department = models.CharField(max_length=50,null=True)
#     approved_by = models.CharField(max_length=50,null=True)
#     approved_status = models.CharField(max_length=50,null=True)
#
#     class Meta:
#        db_table = 'auditschedule_confirm'
