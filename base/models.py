from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
import uuid
import random
import string
from django.utils.text import slugify
from datetime import datetime
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
       phone_number =models.CharField(max_length =15,
   blank=True, null =True, validators = [
       RegexValidator(
           regex= '^[0-9]*$',
           message= 'phone Number must contain only digits',
           code = 'invalid_phone_number',
       )
   ]

                                   )
       bank_name =models.CharField(max_length =200,null= True)
       account_name =models.CharField(max_length=200, null =True)
       account_number =models.CharField(max_length=15,
              blank=True, null =True, validators = [
       RegexValidator(
           regex= '^[0-9]*$',
           message= 'phone Number must contain only digits',
           code = 'invalid_phone_number',
       )                         
              ]
       )
       reset_password_code = models.CharField( max_length=6,blank =True,null=True)
MALE = 'M'
FEMALE = 'F'
OTHER = 'O'
Gender = [
       (MALE , 'Male'),
       (FEMALE, 'Female'),
       (OTHER, 'Other'),
]
      



class Available_Balance(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      balance = models.DecimalField( max_digits=10, decimal_places=2,default=0.00)
   
      def __str__ (self):
            return f"{self.user.username} Available Balance {self.balance}"
def save_user_model(sender ,instance,created,**kwargs):
    if created:
          Available_Balance.objects.create(user=instance)
  

post_save.connect(save_user_model, sender=User )
def generate_unique_profile_id():
      random_string =''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
      return random_string

class UserProfile(models.Model):
       user = models.ForeignKey(User,on_delete=models.CASCADE)
       available_balance = models.ForeignKey("Available_Balance" ,on_delete=models.SET_NULL,null =True,blank=True)
       gender = models.CharField( choices= Gender, max_length=1,blank=True)
       profile_pic =models.ImageField( upload_to='images/',blank=True)
       date_of_birth =models.DateField(blank= True ,null =True)
       profile_id = models.CharField( default =generate_unique_profile_id, max_length=10)
    
       def save(self ,*args, **kwargs):
            if not self.available_balance:
                 available_balance =Available_Balance.objects.get(user=self.user)
                 self.available_balance=available_balance
                 super().save(*args ,**kwargs)
 
      
       class Meta:
              verbose_name_plural = "UserProfile"
       def __str__(self):
              return self.user.username
def save_user_model(sender ,instance,created,**kwargs):
    if created:
          UserProfile.objects.create(user=instance)     
  
post_save.connect(save_user_model, sender=User )


class Kyc(models.Model):
   user = models.ForeignKey(User,  on_delete=models.CASCADE,null=True)
   GENDER = [
        ('male', 'Male'),
        ('female', 'Female')
   ]
   Gender = models.CharField( max_length=20,choices=GENDER,blank=True)
   DOB =models.DateField( auto_now_add=False,blank=True, null=True)
   email =models.EmailField( null=True, max_length=254,blank=True)
   adress =models.CharField(null=True, max_length=250,blank=True)
   state = models.CharField(max_length=50,null=True,blank=True)
   photo = models.FileField( upload_to='images/', max_length=100,blank=True)
   nin = models.CharField( max_length=12 ,blank=True ,validators = [
       RegexValidator(
           regex= '^[0-9]*$',
           message= 'NIN must contain only digits',
           code = 'invalid NIN',
       )                         
              ])
   nin_photo = models.FileField( upload_to='nin/',blank=True)
   information = models.BooleanField(default=False,blank=True) 
def save_user_model(sender ,instance,created,**kwargs): 
    if created:
          Kyc.objects.create(user=instance)
  

post_save.connect(save_user_model, sender=User )
      

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
          return f"{self.message} ---- {self.is_read}"


 

class Ledger_Balance(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      balance = models.DecimalField( max_digits=10, decimal_places=2, default=0.00)

      def __str__ (self):
            return f"{self.user.username} Ledger Balance {self.balance}"
      
def save_user_model(sender ,instance,created,**kwargs):
    if created:
          Ledger_Balance.objects.create(user=instance)
  

post_save.connect(save_user_model, sender=User )



class NairaWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Naira Wallet"
def save_user_model(sender ,instance,created,**kwargs):
    if created:
          NairaWallet.objects.create(user=instance)
  

post_save.connect(save_user_model, sender=User )

class Transactions(models.Model):
    TRANSACTION_TYPES = (
        ('Exchange', 'Exchange'),
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_currency = models.CharField(max_length=3,default='USD')
    to_currency = models.CharField(max_length=3,default='NGN')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    conversion_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.timestamp}"


class UserTimestamp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timestamp = models.CharField(null=True, max_length=300)
    inputValue =models.CharField(null=True,max_length=50)
    time_bool =models.BooleanField( default=False)

    def __str__(self):
        return f"{self.user.username}'s Timestamp"
    
class Transaction(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class EURWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Naira Wallet"
def save_user_model(sender ,instance,created,**kwargs):
    if created:
          EURWallet.objects.create(user=instance)
  

post_save.connect(save_user_model, sender=User )

class GPBWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Naira Wallet"
def save_user_model(sender ,instance,created,**kwargs):
    if created:
        GPBWallet.objects.create(user=instance)
  
post_save.connect(save_user_model, sender=User )


