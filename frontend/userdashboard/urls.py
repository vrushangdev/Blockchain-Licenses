from django.contrib import admin
from django.urls import path,include
from userdashboard import views

urlpatterns = [
    path('userdashboard/',views.userdashboard,name='userdashboard'),
]
