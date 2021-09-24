from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.home,name='home'),
    path('accounts/login/',views.loginview,name="login"),
    path('logout',views.logoutview,name='logout'),
    path('accounts/sign_up/',views.signupview,name='signup'),
    path('passwordreset',views.resetpassword,name='resetpassword'),
    path('reset',views.Resethome,name='reset'), 
    path('addExpense',views.addExpense,name="addExpense"),
    path('viewExpense',views.viewExpense,name="viewExpense"),
    path('addBalance',views.addBalance,name="addBalance"),
    path('checkBal',views.checkBal,name="checkBal"),
    path('totalExp',views.totalExp,name='totalExp'),
    path('addexpensepage',views.addexpage,name="addexpensepage"),
    path('addbalancepage',views.addbalpage,name="addbalancepage"),
    path('viewpage',views.viewpage,name="viewpage"),
    path('checkbalancepage',views.checkbalpage,name='checkbalancepage'),
    path('totalexppage',views.totalexppage,name='totalexppage')
]+static(settings.STATIC_URL)