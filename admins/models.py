from django.db import models
from marchant.models import MarchantUser
from base.models import UserProfile ,User


class AdminUser(models.Model):
    username = models.CharField(max_length=30,null=True)
    email = models.EmailField(null=True)
    password = models.CharField( max_length=20,null=True)

    def __str__(self):
        return f"{self.email}" 
    
class MarchantPendingTransaction(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE,)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    action = models.CharField(max_length=10) 
    message = models.TextField(null =True)
    time = models.DateTimeField(null=True,  auto_now_add=True)
    is_approved = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.action} - {self.amount}--{self.time}"
    
class MarchantApproveTransaction(models.Model):
    message = models.TextField(null=True)
    is_approve  =models.BooleanField(default=True)
    timestamp = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return f"you successfully  approved the transaction made by Marchant  -----{self.timestamp} "


class RejectedTransaction(models.Model):
    message = models.TextField(null=True)
    is_rejected= models.BooleanField(default=True)
    timestamp = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return f"{self.message} ---{self.timestamp}"