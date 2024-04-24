from django.urls import path
from . import views

app_name = 'admins'

urlpatterns = [
    path('index',views.index, name = 'index'),  
    path('signin',views.signin, name = 'signin'),
    path('signup',views.signup, name = 'signup'),
    path('message',views.message, name = 'message'),
    path('details/<str:pk>/',views.details, name = 'details'),
    path('userprofile/<str:pk>/',views.userprofile, name = 'userprofile'),
    path('delete/<str:pk>/',views.Rejected_Delete.as_view(),name='delete') ,
    path('Transcation',views.Transcation, name = 'Transcation'),
    path('Transcation1',views.Transcation1, name = 'Transcation1'),
    path('NewsUpdates',views.NewsUpdates, name = 'NewsUpdates'),
    path('DashboardtransferFunds',views.DashboardtransferFunds, name = 'DashboardtransferFunds'),
    path('DashboardtransferFunds1',views.DashboardtransferFunds1, name = 'DashboardtransferFunds1'),
    path('approve',views.approve, name = 'approve'),
    path('ChangePassword',views.ChangePassword, name='ChangePassword'),
    path('ChangePassword1',views.ChangePassword1, name='ChangePassword1'),
]
 