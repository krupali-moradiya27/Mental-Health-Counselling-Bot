from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
        path('', views.registerFun, name="registerPage"),
        path('login/', views.loginFun, name='loginPage'),
        path('editprofile', views.editProfileFun, name='editprofilePage'),
        path('profile', views.profileFun, name='profilePage'),
        path('healthprofile/', views.healthprofileFun, name='healthprofilePage'),
        path('changepassword/', views.changepasswordFun, name='changepasswordPage'),
        path('logout/', views.logoutFun, name='logoutPage'),]
