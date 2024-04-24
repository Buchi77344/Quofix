from django.shortcuts import render,get_object_or_404 ,redirect
from marchant.time import time_get
from base.models import UserProfile ,Available_Balance ,Ledger_Balance 
from .forms import AvailableBalanceForm ,Searchform
from decimal import Decimal
from django.contrib.auth.decorators import login_required
# from .forms import MarchantUserForm
from .models import MarchantUser ,MarchantNotification
from django.contrib import messages
from base.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from admins.models import MarchantPendingTransaction,MarchantApproveTransaction
# Create your views here.
def index(request):
    base =  UserProfile.objects.all()
   
    context = {
        'base':base,
    
    }
       
    return render (request, 'Marchant/index.html', context)


@login_required(login_url='marchant:login')
def details(request, pk):
    # base = get_object_or_404(UserProfile , pk=pk)
    gree = time_get
   
 
    # users = MarchantUser.objects.get(user=request.user)
    boss = UserProfile.objects.get(pk=pk)
    if boss.user.username == 'buchi':
        messages.error(request, 'why are u tryin to accesss the backend developer account')
        return redirect('marchant:index')
    else:
        ledger_balance =get_object_or_404(Ledger_Balance ,pk=pk)

    
        # user = Ledger_Balance.objects.get(user=request.user)
        userx= get_object_or_404(MarchantUser)
    
        if request.method == 'POST':
            user = get_object_or_404(User,pk=pk)
            amount = Decimal(request.POST.get('amount', 0))
            action = request.POST.get('action')
        
            if action == 'add':
                ledger_balance.balance += amount
                MarchantPendingTransaction.objects.create( user=user, amount= amount, action= action ,message = f"{ userx.username} Transfer {amount} to  {ledger_balance.user.username} please click on approve" )
                # MarchantNotification.objects.create(user=user, message= f"{user.username} successfully transfer ${amount} to {ledger_balance.user.username}")
            elif action == 'subtract':
                if amount <= ledger_balance.balance:
                    ledger_balance.balance -= amount 
                    # PendingTransaction.objects.create(user =user, amount= amount, action= action )
                    # MarchantNotification.objects.create(user=user, message= f"{user.username} debited ${amount} from {ledger_balance.user.username} account")
                else:
                    # Handle insufficient balance error
                    pass
            ledger_balance.save() 
            

            return redirect('marchant:details', pk=pk)
    

        else:
        
         context = {
            # 'base':base,
            'gree':gree,
            
            'ledger_balance':ledger_balance,
            
        }
        return render (request, 'Marchant/details.html', context)  

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email  =  request.POST.get('email')
        password =request.POST.get('password')
        password1 = request.POST.get('password1')
        if password != password1:
            messages(request,'password do not match')
            return redirect ('marchant:signup')
        elif MarchantUser.objects.filter(email=email).exists():
              messages(request, 'email already exist')
              return redirect('marchant:signup')
        hashed_password = make_password(password)
        user= MarchantUser(first_name=first_name, last_name=last_name,username=username, email=email, password=hashed_password)
        user.save()
        return redirect ('marchant:login')
    else:
        return render (request, 'Marchant/signup.html')


def login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = MarchantUser.objects.filter(username=username).first()

        if user:
            if check_password(password, user.password):
                # Password is correct, set user's session and redirect to dashboard
                request.session['user_id'] = user.id
                return redirect('marchant:index')
            else:
                # Password is incorrect
                error = 'Invalid username or password'
        else:
            # User does not exist
            error = 'Invalid username or password'

    return render(request, 'Marchant/login.html', {'error': error})


def notification_list(request):
    notifications = MarchantNotification.objects.filter(user=request.user, is_read=True)
   
    return render(request, 'notification_list.html', {'notifications': notifications})


from django.shortcuts import render
from django.core.mail import send_mail
import secrets
from django.template.loader import render_to_string
from django.conf import settings
from  django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import random
import string




from django.urls import reverse

def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        merchant = MarchantUser.objects.filter(email=email).first()
        if merchant:
            password_reset_code = generate_password_reset_code()
            send_password_reset_email(email, password_reset_code)
            # Redirect to the confirmation view with email and code as URL parameters
            return redirect(reverse('marchant:password_reset_confirm', kwargs={'email': email, 'code': password_reset_code}))
        else:
            messages.error(request, 'Email does not exist. Please enter a valid email.')
            return redirect('password_reset')  # Redirect back to the password reset page
    else:
        return render(request, 'Marchant/password_reset.html')


def generate_password_reset_code():
    # Generate a random password reset code using Python's secrets module
    return ''.join(random.choices(string.digits,k=6))


def send_password_reset_email(email, password_reset_code):
    # Send email containing password reset code
    subject = 'Password Reset Code'
    from_email =settings.EMAIL_HOST_USER  
    recipient_list= [email]
    html_message = render_to_string('Marchant/email_message.html', {'password_reset_code': password_reset_code})  
    msg = EmailMultiAlternatives(subject,'', from_email, recipient_list)

    # Attach HTML content
    msg.attach_alternative(html_message, "text/html")
    msg.send()  
 

def password_reset_confirm(request):
         if request.method == 'POST':
                code = request.POST.get('reset_code')
                email = request.session.pop('email',None)
                stored_code = request.session.pop('password_reset_code',None )
                
                if code  == stored_code:
                    emails= MarchantUser.objects.filter(email=email).exists()
                    email=emails
                    return redirect('comfirm_password')
    
                else:
                    # Invalid code, display an error message
                    messages.error = (request,'Invalid code. Please try again.')
                    return redirect('marchant:password_reset_confirm')
         else:
            # GET request, render the password reset confirmation form
            return render(request, 'Marchant/password_reset_confirm.html')
    



def search(request):
    if request.method == 'GET':
        form = Searchform(request.GET)
        result = None
        if form.is_valid(): 
            query =form.cleaned_data['query']
            
            result = UserProfile.objects.filter(user=query) | UserProfile.objects.filter(profile_id__icontains=query) 

            context = {
                'result':result,
                'form':form
            }
            return render (request, 'Marchant/index.html',context)






