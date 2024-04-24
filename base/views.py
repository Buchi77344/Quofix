from django.shortcuts import render ,redirect ,get_object_or_404 ,HttpResponseRedirect
import requests
from django.contrib import messages
from  .models import User ,UserProfile ,Notification,Available_Balance ,Ledger_Balance,NairaWallet,Transactions ,UserTimestamp ,EURWallet, GPBWallet ,Kyc
from django.contrib.auth import authenticate, login 
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random
from .exchange import get_exchange_rate
from marchant.time import time_get
import json
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_POST
import string
from django.core.mail import send_mail
from base.decorator import check_session
from base.kyc import kyc_authentication



def index(request): 
    return render(request, 'index.html')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

@login_required(login_url='login')
def dashboard(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    balance =get_object_or_404(Available_Balance, user =request.user)
    # ledger_balance = get_object_or_404(Ledger_Balance, user=request.user)
    greet =time_get()
    context ={
         'profile':profile,
         'balance':balance,
         'greet':greet,
        #  'ledger_balance':ledger_balance
    }
    return render (request, 'dashboard.html',context)

 
def signup(request):
    if request.method == "POST":
        first_name =request.POST['first_name']
        last_name =request.POST['last_name']
        email =request.POST['email']
        phone_number =request.POST['phone_number']
        username =request.POST['username']
        password = request.POST['password']
        password1 =request.POST['password1']
        if password == password1:

           if User.objects.filter(username=username).exists():
                        messages.error(request, 'username already exist')
                        return redirect('signup')
           
                
           elif first_name and last_name and email and phone_number and username and password:
                request.session['first_name']= first_name
                request.session['last_name']= last_name
                request.session['email']= email
                request.session['phone_number']= phone_number
                request.session['username']= username
                request.session['password']= password
                request.session['password1']= password1
           
                return redirect('bank')
        else: 
            messages.error(request, 'password do not match')
            return redirect('signup')
    else:
        return render (request, 'signup.html')
    

def bank(request):
    if request.method == 'POST':
        bank_name =request.POST['bank_name']
        account_name =request.POST['account_name']
        account_number =request.POST['account_number']
        first_name = request.session.pop('first_name',None)
        last_name = request.session.pop('last_name',None)
        email = request.session.pop('email',None)
        phone_number = request.session.pop('phone_number',None)
        username = request.session.pop('username',None)
        password = request.session.pop('password',None)
        if first_name and last_name and email and username and password and bank_name and account_name and account_number and phone_number:
                user = User.objects.create_user(
                username=username,
                first_name =first_name,
                last_name =last_name,
                email =email,
                password =password
                )
                user.bank_name =bank_name
                user.account_name =account_name
                user.account_number =account_number
                user.phone_number =phone_number
                user.save()
            
                return redirect('login')
        else:
            return redirect('signup')
    else:
        return render (request, 'signup3.html')




def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate( username=username, password=password)

        if user is not None:
            auth.login(request, user)
            Notification.objects.create(user=user, message ="you have just logged in")
            return redirect('exchange')
        else:         
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')

def generate_reset_code():
     return ''.join(random.choices(string.digits,k=6))

def  forget_password(request):
     if request.method  == "POST":
          email =request.POST.get('email')
          user =None

          if '@' in email:
               user= User.objects.filter(email =email).first()
          if user:
               code = generate_reset_code()
               user.reset_password_code = code
               user.save()

               send_mail(
                    'Password Reset Code',
                    f'Your reset code is :{code}',
                    ['vacan4002gmail.com'],
                    [user.email],
                    fail_silently=False
               )
               return redirect('verify_code')
          else:
               pass
     return render(request, 'forget_password.html')

def notification_list(request):
    notifications = Notification.objects.filter(user=request.user, is_read=True)
   
    return render(request, 'notification_list.html', {'notifications': notifications})

def mark_all_notifications_as_read(request):
    if request.method == 'POST':
        try:
            notifications = Notification.objects.filter(user=request.user, is_read=False)
            notifications.update(is_read=True)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': str(e)})
    else:
        return JsonResponse({'success': False, 'error_message': 'Invalid request method'})


api_key = 'b7ff85d0b03d4e070f723655'
url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'

from datetime import datetime, timedelta
from django.utils import timezone
import time

@require_POST
def fetchapi(request):
    if request.method =="POST": 
        data = json.loads(request.body)
        timestamp = data.get('countDownDate')
        time_bool = data.get('timeBool')
        inputValue =data.get('inputValue')
       
        user_timestamp, created = UserTimestamp.objects.update_or_create(
            user=request.user,
          
            defaults={'timestamp': timestamp,'time_bool': time_bool,'inputValue':inputValue},
           
        )
        
        stamp =UserTimestamp.objects.get(user= request.user, timestamp=timestamp, time_bool=time_bool)
  
        return JsonResponse({ 
            "success":timestamp,"time":time_bool, 
            "success":stamp.time_bool, 
            "timestamp":stamp.timestamp,
            "inputValue":inputValue
            })

def getapi(request):
  
    stamp =UserTimestamp.objects.get(user= request.user,)
    return JsonResponse({"success":True, "stamp":stamp.timestamp,"time":stamp.time_bool,"inputvalue":stamp.inputValue })

@require_POST
def fetch(request):
    if request.method =="POST":
        data = json.loads(request.body)
        time_bool =data.get('timeFetch')
         
        fex_time ,created = UserTimestamp.objects.update_or_create(user =request.user, defaults={"time_bool":time_bool})
        return JsonResponse({"fex":time_bool})
    return JsonResponse({"success":True})

@kyc_authentication
@login_required(login_url='login')
def exchange(request,instance):
  
    wallet  = NairaWallet.objects.get(user=request.user) 
    usd = Available_Balance.objects.get(user=request.user)
   
    
    context = {
            'wallet':wallet,
            'usd':usd,
           
        }
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', 0.00))
        available_balance = Available_Balance.objects.get(user=request.user)
        if amount > available_balance.balance:
            messages.error (request, 'Insufficient available balance')
            return redirect('exchange')
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            conversion_rate = data['conversion_rates']['NGN']  
            converted_amount = amount * Decimal(conversion_rate)
            available_balance.balance -= amount
            available_balance.save()
            naira_wallet ,created = NairaWallet.objects.get_or_create(user=request.user)
            naira_wallet.balance += converted_amount 
            naira_wallet.save()
            return redirect('exchange')
           
        else:
            context ={
                  'converted_amount': converted_amount,
                  
            }
            return render(request, 'exchange.html', {'error': 'Failed to fetch exchange rate data','instance':instance})
    else:
       
        return render(request, 'exchange.html',context) 

from decimal import Decimal 
from datetime import datetime
@kyc_authentication
@login_required(login_url='login')
def withdraw(request,instance):
    now = datetime.now()
    
    
    allowed_days = {
        2: Decimal('0.05'),  # Wednesday
        6: Decimal('0.03')   # Friday
    }

    if now.weekday() in allowed_days:
        if request.method == 'POST':
            amount = Decimal(request.POST.get('amount'))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
            naira_wallet = get_object_or_404(NairaWallet, user=request.user)
            user = request.user

            if amount <= naira_wallet.balance:
                # Calculate the charge percentage
                charge_percentage = allowed_days[now.weekday()]
                # Calculate the withdrawal amount including the charge
                withdrawal_charge = amount * charge_percentage
                total_withdrawal_amount = amount + withdrawal_charge
                # Deduct the total withdrawal amount from the user's balance
                naira_wallet.balance -= total_withdrawal_amount
                naira_wallet.save()
                Notification.objects.create(user=user, message = f'you have successfully withdraw {total_withdrawal_amount} from your account')
                return redirect('withdraw')
            else:
                return render(request, 'withdraw.html', {'error': 'Insufficient funds.'})
        else:
            naira_wallet = get_object_or_404(NairaWallet,  user =request.user)
            withdrawal_charge = allowed_days[now.weekday()]  
            total_withdrawal_amount = Decimal('0.00') 
            context = {
                 'withdrawal_charge': withdrawal_charge,
                'total_withdrawal_amount': total_withdrawal_amount,
                'naira_wallet': naira_wallet
            }
            return render(request, 'withdraw.html', context)
    else:
        return render(request, 'withdraw.html', {'error': 'Withdrawals are only allowed on Wednesdays (5% charge) and sunday (3% charge).','instance':instance})

from django.shortcuts import render
from django.http import HttpResponse
from .models import UserProfile, Transaction

# def transfer_money_view(request):
#     if request.method == 'POST':
#         sender_profile_id = request.POST.get('sender_profile_id')
#         receiver_profile_id = request.POST.get('receiver_profile_id')
#         amount = float(request.POST.get('amount', 0))  # Assuming amount is sent as a string
        
#         # Get sender and receiver profiles
#         sender_profile = UserProfile.objects.filter(profile_id=sender_profile_id).first()
#         receiver_profile = UserProfile.objects.filter(profile_id=receiver_profile_id).first()
        
#         # Check if sender or receiver profile is not found
#         if not sender_profile or not receiver_profile:
#             return HttpResponse('Sender or receiver profile not found', status=400)
        
#         # Transfer money
#         success, message = transfer_money(sender_profile, receiver_profile, amount)
        
#         # Return HTTP response
#         if success:
#             return HttpResponse('Transfer successful')
#         else:
#             return HttpResponse(message, status=400)
    
#     return HttpResponse('Invalid request', status=400)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserProfile, Transaction

@kyc_authentication
@check_session
@login_required(login_url="login")
def transfer_money(request):
    if request.method == 'POST':
        receiver_profile_id = request.POST.get('receiver_profile_id')
        amount = Decimal(request.POST.get('amount', 0))

        sender_profile = get_object_or_404(UserProfile, user=request.user)
        receiver_profile = UserProfile.objects.filter(profile_id=receiver_profile_id).first()
        
        if receiver_profile is None:
            messages.error(request, 'Receiver profile does not exist')
            return redirect('transfer_money')
        
        sender_available_balance = sender_profile.available_balance
        receiver_balance = receiver_profile.available_balance
        if Kyc.objects.filter(user=request.user).exists():   
                if sender_available_balance.balance >= amount:
                    # Deduct amount from sender's available balance
                    sender_available_balance.balance -= amount
                    sender_available_balance.save()
                    
                    # Add amount to receiver's balance
                    receiver_balance.balance += amount
                    receiver_balance.save()
                    
                    # Record transaction
                    Transaction.objects.create(sender=sender_profile, receiver=receiver_profile, amount=amount) 
                    
                    messages.success(request, 'Transfer successful')
                    return redirect('transfer_money')  # Redirect after successful transfer
                else:
                    messages.error(request, 'Insufficient available balance')
                    return redirect('transfer_money')  # Redirect after failed transfer
        else: 
           return redirect('kyc1') 
    else:
        available_balance = get_object_or_404(Available_Balance, user=request.user)
        context = {'available_balance': available_balance}
        return render(request, 'transfer_money.html', context)

   
   

def check(request):
    ngn = EURWallet.objects.first()
    if ngn is None:
        return HttpResponse("user dose not exis")
    else:
        return JsonResponse({ "success":f"user exist {ngn.user.username}"})

def kycverification(request): 
    return render(request, 'kyc-verification-1.html')

def account(request): 
    return render(request, 'account.html')
def pin(request): 
    return render(request, 'pin.html')
def rate(request): 
    return render(request, 'rate.html')
def phonenumber1(request): 
    return render(request, 'phone-number1.html')
def buywithdrawexchange(request): 
    return render(request, 'buy-withdraw-exchange.html')

def kyc(request): 
    if request.method == 'POST':
        nin =request.POST.get('nin')
        nin_photo =request.POST.get('nin_photo')
        information =request.POST.get('information')
        Gender = request.session.pop('Gender',None)
        DOB = request.session.pop('DOB',None)
        email = request.session.pop('email',None)
        adress = request.session.pop('adress',None)
        state = request.session.pop('state',None)
        photo = request.session.pop('photo',None)
       
        if nin and nin_photo and information and Gender and DOB and email and adress and state and photo:
            kycs = Kyc.objects.update(
            
                nin=nin,
                nin_photo =nin_photo,
                information =True,
                Gender =Gender,
                DOB =DOB,
                email=email,
                adress =adress,
                state=state,
                photo =photo
            ) 
            
            return redirect('exchange')

    return render(request, 'kyc-verification-2.html')

@login_required(login_url="login")
def kyc1(request): 
    if request.method == 'POST':
        Gender =request.POST.get('Gender')
        DOB =request.POST.get('DOB') 
        email =request.POST.get('email')
        adress =request.POST.get('adress')
        state =request.POST.get('state')
        photo =request.POST.get('photo')
        if Gender and DOB and email and adress and state and photo:
            request.session['Gender']=Gender
            request.session['DOB']=DOB
            request.session['email']=email
            request.session['adress']=adress
            request.session['state']=state
            request.session['photo']=photo
            return redirect('kyc')
         
    
    return render(request, 'kyc1.html') 

  