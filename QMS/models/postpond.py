from django.db import models
from QMS.models import Auditschedule
from QMS.models import Audit_comments

class Postpond(models.Model):
    auditschedule_id = models.CharField(max_length=5,null=True)
    post_date = models.DateField(null=True)
    post_time = models.TimeField(null=True)
    reason = models.TextField(null=True)
    status = models.CharField(max_length=10,null=True)

    class Meta:
        db_table = 'postpond'
