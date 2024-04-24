from django.db import models
from  django.contrib.auth.models import AbstractUser
from base.models import Available_Balance ,Ledger_Balance
from base.models import User
from django.db.models.signals import post_save

class MarchantUser(models.Model):
    username = models.CharField(max_length=30,null=True)
    first_name =models.CharField( max_length=30,null=True)
    last_name =models.CharField(max_length=30,null=True)
    email = models.EmailField(null=True)
    password = models.CharField( max_length=20,null=True)

    def __str__ (self):
       return self.username


class Transaction(models.Model):
    available_balance = models.ForeignKey(Available_Balance, on_delete=models.CASCADE)
    ledger_balance_balance = models.ForeignKey(Ledger_Balance, on_delete=models.CASCADE)
    timestap =  models.DateTimeField( auto_now_add=True)

class MarchantNotification(models.Model):
    user = models.ForeignKey(MarchantUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
          return f"{self.message} ---- {self.is_read}"  

class Marchantprofile(models.Model):
    user =models.ForeignKey(MarchantUser, on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    email =models.EmailField(blank=True)
    def __str__(self):
        return self.user.username

def save_profile(sender,instance,created,**kwargs):
    if created:
        Marchantprofile.objects.create(user=instance)
post_save.connect(save_profile, sender=MarchantUser) 