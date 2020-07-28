from django.db import models


class JobType(models.Model):
    j_type = models.CharField(max_length=25)

    class Meta:
        db_table = 'job_type'


class ClientName(models.Model):
    c_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'clients_name'


class EndUser(models.Model):
    e_user = models.CharField(max_length=25)

    class Meta:
        db_table = 'end_users'


class JobDetails(models.Model):
    job_type = models.ForeignKey(JobType,related_name='job_type', on_delete=models.CASCADE)
    job_name = models.CharField(max_length=25)
    client_name = models.ForeignKey(ClientName,related_name='client_name', on_delete=models.CASCADE)
    end_user = models.ForeignKey(EndUser,related_name='end_user', on_delete=models.CASCADE)
    job_startdate = models.DateField()
    job_enddate = models.DateField()
    job_Description = models.TextField()

    class Meta:
        db_table = 'job_details'
