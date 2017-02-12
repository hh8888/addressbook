from django.db import models

# Create your models here.


class address(models.Model):
    email = models.CharField('Email',  primary_key=True, max_length=50)
    name = models.CharField('Name', max_length=50)
    class Meta:
        db_table = 'address'