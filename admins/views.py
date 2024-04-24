from django.shortcuts import render ,redirect ,get_object_or_404 
from .models import AdminUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import MarchantApproveTransaction ,AdminUser, MarchantPendingTransaction ,RejectedTransaction
from django.contrib import messages
from base.models import Available_Balance ,Ledger_Balance ,User ,UserProfile
from marchant.models import MarchantUser, MarchantNotification
from django.views import generic
from django.urls import reverse




def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email  =  request.POST.get('email')
        password =request.POST.get('password')
        password1 = request.POST.get('password1')
        if password != password1:
            messages(request,'password do not match')
            return redirect ('admins:signup')
        elif AdminUser.objects.filter(email=email).exists():
               messages(request, 'email already exist')
               return redirect('admins:signup')
        elif AdminUser.objects.filter(username=username).exists():
            messages(request, 'username already exist')
            return redirect('admins:signup')
        hashed_password = make_password(password)
        user= AdminUser(username=username, email=email, password=hashed_password)
        user.save()
        return redirect ('admins:signin')
    else:
        return render (request, 'admins/signup.html')
def signin(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = AdminUser.objects.filter(email=email).first()

        if user:
            if check_password(password, user.password):
                # Password is correct, set user's session and redirect to dashboard
                request.session['user_id'] = user.id
                return redirect('admins:index')
            else:
                # Password is incorrect
                messages.error (request,'Invalid username or password')
        else:
            # User does not exist
          messages.error (request,'Invalid username or password')

    return render(request, 'admins/signin.html', {'error': error})


def index(request):
    tran = MarchantPendingTransaction.objects.all()
    
    context ={
        'tran':tran,
       
    }
    return render (request, 'admins/index.html',context)

def approve(request):
    tran = MarchantPendingTransaction.objects.all()
    
    context ={
        'tran':tran,
       
    }
    return render (request, 'admins/approve.html',context)


def userprofile(request,pk):
    profile= get_object_or_404(UserProfile, pk=pk) 
    context = {
        'profile':profile
    }
    return render (request, 'admins/userprofile.html', context)



def details(request, pk):
    transaction = get_object_or_404(MarchantPendingTransaction, pk=pk)
    available_balance = get_object_or_404(Available_Balance,user=transaction.user)
    ledger_balance = get_object_or_404(Ledger_Balance,user=transaction.user)
    user =get_object_or_404(MarchantUser)
   
    
    
    if request.method == 'POST':
        action =request.POST.get('action')  
        # Update available balance if transaction is approved
     
        if transaction.action == 'add':
            available_balance.balance += transaction.amount
            available_balance.save()
            ledger_balance.balance -=transaction.amount
            ledger_balance.save()
            MarchantApproveTransaction.objects.create(message =f"you successfully  approved the transaction made by Marchant {user.username} " )
            MarchantNotification.objects.create(user=user, message =f"Admin  succesfully approve your transaction")
              

        
        # Delete the pending transaction after approval
        transaction.delete()
        messages.success(request, message) 
      
        return redirect('admins:message')
    return render (request, 'admins/details.html')

def message(request):
    return render (request, 'admins/message.html')


class Rejected_Delete(generic.DeleteView):
    model =MarchantPendingTransaction
    template_name = 'admins/delete.html' 


    def get_success_url(self):
        RejectedTransaction.objects.create(message =f"you successfully rejected this transaction")
        return reverse ('admins:index')   

def Transcation(request):
    return render (request, 'admins/Transcation.html')


def Transcation1(request):
    return render (request, 'admins/Transcation1.html')

def NewsUpdates(request):
    return render (request, 'admins/NewsUpdates.html')
def DashboardtransferFunds(request):
    return render (request, 'admins/DashboardtransferFunds.html')
def DashboardtransferFunds1(request):
    return render (request, 'admins/DashboardtransferFunds1.html')

def ChangePassword(request):
    if request.method == 'POST':
       email = request.POST.get('email')
       if AdminUser.objects.filter(email=email).exists():
           return redirect('admins:ChangePassword1')
       else:
           messages.error(request, 'email does not exist')
           return redirect('admins:ChangePassword')
    return render (request, 'admins/ChangePassword.html')

def ChangePassword1(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if password != password1 :
            messages.error(request,'password do not match')
            return redirect('admins:ChangePassword1')
        else:  
            hash_password = make_password(password)
            AdminUser.objects.update(password =hash_password)
            
            return redirect('admins:signin')
    return render (request, 'admins/ChangePassword1.html')