from django import forms
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.db import models



class User(AbstractUser):
    ADMIN = 'ADM'
    CLOSER = 'CLS'
    SALES = 'SLS'

    EMPLOYEE_TYPES = (
        (SALES, 'sales'),
        (CLOSER, 'closer'),
        (ADMIN, 'admin'),

    )
    role = models.CharField(max_length=25, choices=EMPLOYEE_TYPES,default='SLS')
    telegram = models.CharField(max_length=30, blank=True)
    closer = models.ForeignKey('self',on_delete=models.SET_NULL, null=True,blank=True)

class Leads(models.Model):
    # ADMIN = 'ADM'
    # CLOSER = 'CLS'
    # SALES = 'SLS'

    STATUSES_TYPES = (

        ('new', 'New'),
        ('account fixing', 'Account fixing'),
        ('not interested', 'Not interested'),
        ('deposit', 'Deposit'),
        ('registered', 'Registered'),
        ('waiting', 'Waiting'),
        ('sales work', 'Sales work'),
    )
    date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    full_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    about_client=models.TextField(max_length=1000,blank=True)
    source=models.TextField(max_length=1000,blank=True)
    manager= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='lead_manager')
    status = models.CharField(max_length=25, choices=STATUSES_TYPES, default='new')

    class Meta:
        get_latest_by = ['id']

    def __str__(self):
        return self.full_name
class Planning(models.Model):
    TYPES = (

        ('First call', 'First call'),
        ('Callback', 'Callback'),
        ('Platform show', 'Platform show'),
        ('Account fixing', 'Account fixing'),
        ('Trial deal', 'Trial deal'),
        ('Deposit', 'Deposit'),
    )
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update = models.DateTimeField( blank=True, null=True)
    finished = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=False)
    notification = models.BooleanField(default=True)
    creator = models.CharField(max_length=25,blank=True, null=True)

    manager= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='planning_manager')
    lead= models.ForeignKey(Leads,on_delete=models.CASCADE,null=True,related_name='planning_manager')
    comment=models.TextField(max_length=500,blank=True)
    type=models.CharField(choices=TYPES,max_length=50,default='First call')
    def __str__(self):
        return self.type