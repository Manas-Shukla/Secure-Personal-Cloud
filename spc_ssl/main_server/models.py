from django.db import models

# Create your models here.

class registered_clients(models.Model):
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    is_syncing = models.BooleanField(default=False)
    class Meta:
        db_table = 'registered_clients'

class global_data(models.Model):
    user = models.ForeignKey('registered_clients',on_delete=models.CASCADE)
    file = models.BinaryField(max_length=1000)
    fname = models.CharField(max_length=100)
    md5sum = models.CharField(max_length=50)
    ftype = models.CharField(max_length=50)
    fdesc = models.CharField(max_length=1000)
    fpath = models.CharField(max_length=100)

    class Meta:
        db_table = 'global_data'
