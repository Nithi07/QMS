from django.db import models
from QMS.models import ListAuditors
from QMS.models import  Audittype
from QMS.models.common import  EmployeDepartment
from QMS.models.employee_details import EmployeeDetails
from QMS.models.project_teamwise import Project_Details
from django.contrib.postgres.fields import ArrayField


class Auditschedule(models.Model):
    schedule_auditype = models.ForeignKey(Audittype,related_name='audit_type', on_delete=models.CASCADE)
    schedule_job_code = models.CharField(max_length=15,null=True)
    schedule_project = models.ForeignKey(Project_Details,null=True,related_name='schedule_project', on_delete=models.CASCADE)
    schedule_sub_job_code = models.CharField(max_length=15,blank=True,null=True)
    schedule_job_audit_no = models.CharField(max_length=15,blank=True,null=True)
    schedule_audit_no = models.CharField(max_length=5,blank=True,null=True)
    schedule_audit_code = models.CharField(max_length=50,blank=True,null=True)
    schedule_audit_date = models.DateField(null=True)
    schedule_audit_time = models.TimeField(null=True)
    schedule_auditee_list = models.ManyToManyField(EmployeeDetails, blank=True, related_name='auditee_list')
    schedule_auditor_list = models.ManyToManyField(ListAuditors, related_name='auditor_list')
    schedule_department_status = models.IntegerField(default=0)
    schedule_department_username = ArrayField(models.CharField(max_length=50,blank=True),null=True,blank=True,default=list)
    schedule_department_date = ArrayField(models.CharField(max_length=30,blank=True),null=True,default=list)
    schedule_final_auditor_list = models.ManyToManyField(EmployeeDetails, related_name='schedule_final_auditor_list')
    schedule_team_member_list = models.ManyToManyField(EmployeeDetails, blank=True, related_name='team_member_list')
    schedule_audit_mr_status = models.IntegerField(default=0)
    schedule_description = models.CharField(max_length=15,blank=True,null=True)
    audit_comment_status = models.IntegerField(default=0)
    schedule_status = models.IntegerField(default=0)
    schedule_file_path = models.URLField(max_length = 500,blank=True,null=True)
    schedule_iso_year = models.CharField(max_length = 50,null=True)
    create_by = models.CharField(max_length=50,null=True)
    create_on = models.DateTimeField(null=True)
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
