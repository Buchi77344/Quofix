from django.urls import path
from . import views
from django.conf.urls import handler404
from base.views import custom_404_view
from django.contrib.auth import views as auth_views

handler404 = custom_404_view


urlpatterns = [
    path('',views.index,name ='index'), 
    path('signup',views.signup,name ='signup'),  
    path('bank',views.bank,name ='bank'), 
    path('login',views.login,name ='login'),
    path('logout',views.logout,name ='logout'),
    path('notification_list',views.notification_list,name ='notification_list'),
    path('mark_all_notifications_as_read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
    path('exchange',views.exchange,name ='exchange'), 
    path('dashboard',views.dashboard,name ='dashboard'), 
    path('withdraw',views.withdraw,name ='withdraw'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name = 'reset_password.html'),
    name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = 'reset_password_sent.html'),
    name= 'password_reset_done') ,
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='reset.html'),
    name= 'password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name= 'reset_password_complete.html'),
    name= 'password_reset_complete'),
    path('fetchapi',views.fetchapi, name="fetchapi"),
    path('fetch',views.fetch, name="fetch"),
    path('getapi',views.getapi, name="getapi"),
    path('transfer_money',views.transfer_money, name="transfer_money"),
    path('check',views.check, name='check'),
    path('kyc-verification',views.kycverification, name='kyc-verification-1'),
    path('account',views.account, name='account'),
    path('pin',views.pin, name='pin'),
    path('rate',views.rate, name='rate'),
    path('phonenumber1',views.phonenumber1, name='phonenumber1'),
     path('buywithdrawexchange',views. buywithdrawexchange, name=' buywithdrawexchange'),
     path('kyc',views.kyc, name='kyc'),
      path('kyc1',views.kyc1, name='kyc1'),
    

] 