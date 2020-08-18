from django.db import models
from QMS.models import Audittype
from QMS.models import ManualCheckList
from QMS.models import EmployeDepartment
from QMS.models import WorkManual
from QMS.models import Auditschedule

class Audit_comments(models.Model):

    workmanual = models.ForeignKey(WorkManual,related_name='workmanualid',null=True, on_delete=models.CASCADE)
    auditschedule = models.ForeignKey(Auditschedule,related_name='auditscheduleid',null=True, on_delete=models.CASCADE)
    cls_refno = models.CharField(max_length=8,null=True,blank=True)
    description = models.CharField(max_length=100,null=True,blank=True)
    auditor_comments = models.TextField(null=True,blank=True)
    comment_status = models.IntegerField(null=True,blank=True)
    department = models.ForeignKey(EmployeDepartment,related_name='department',blank=True,null=True, on_delete=models.CASCADE)
    auditee_correction = models.TextField(null=True,blank=True)
    auditee_status = models.IntegerField(null=True,blank=True)
    verified_comments = models.TextField(null=True,blank=True)
    verified_status = models.IntegerField(null=True,blank=True)
    mr_comments = models.TextField(null=True,blank=True)
    mr_status = models.IntegerField(null=True,blank=True)
    audit_comment_status = models.IntegerField(null=True)
    create_by = models.CharField(max_length=50,null=True)
    create_on = models.DateTimeField(null=True)
    create_ip = models.GenericIPAddressField(null=True)
    modified_by = models.CharField(max_length=50,null=True)
    modified_on = models.DateTimeField(auto_now=True)
    modified_ip = models.GenericIPAddressField(null=True)

    class Meta:
        db_table = 'audit_comments'


class NCR_Comment(models.Model):
    ncr_code = models.CharField(max_length=15,null=True)
    job_code = models.CharField(max_length=15,null=True)
    root_cause_analysis = models.TextField(null=True)
    correction = models.TextField(null=True)
    corrective_action = models.TextField(null=True)
    audit_id = models.IntegerField(null=True)
    command_id = models.IntegerField(null=True)
    ncr_status = models.IntegerField(default=0 )
    ncr_closed_on = models.DateTimeField(null=True)
    create_by = models.CharField(max_length=50,null=True)
    create_on = models.DateTimeField()
    create_ip = models.GenericIPAddressField(null=True)
    modified_by = models.CharField(max_length=50,null=True)
    modified_on = models.DateTimeField(auto_now=True)
    modified_ip = models.GenericIPAddressField(null=True)

    class Meta:
        db_table = 'ncr_comment'
