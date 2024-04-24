from django.urls import path 
from .import views
from django.contrib.auth import views as auth_views

app_name = 'marchant'

urlpatterns = [
    path('index',views.index, name = 'index'),
    path('details/<str:pk>/',views.details,name ='details'), 
    path('signup',views.signup, name = 'signup'),
    path('login',views.login, name = 'login'),
    path('notification_list',views.notification_list,name ='notification_list'),
    path('password_reset',views.password_reset, name = 'password_reset'),
    path('password-reset-confirm/<str:email>/<str:code>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('search',views.search, name = 'search'),
]