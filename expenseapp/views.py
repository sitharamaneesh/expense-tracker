from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core import exceptions
from django.db.models import query
from django.db.models.fields import NullBooleanField
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.db import models
from django.utils.functional import empty
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .models import balance, expense 
from Expensetracker.settings import EMAIL_HOST_USER 
from django.core.mail import send_mail
from decimal import Decimal


@login_required
def home(request):
    return render(request,'home.html')

def loginview(request):
    username=request.POST['username']
    password=request.POST['password']
    userauth=authenticate(request,username=username,password=password)
    if userauth is not None:
        login(request,userauth)
        return redirect('home')
    else:
        return render(request,"login.html")

def logoutview(request):
      print("logout")
      logout(request)
      return redirect('login')

def signupview(request):
    if request.method=="POST":
        formobj=UserCreationForm(request.POST)
        if formobj.is_valid():
            formobj.save()
            username=formobj.cleaned_data["username"]
            password=formobj.cleaned_data["password1"]
            user=authenticate(request,username=username,password=password)
            login(request,user)
            return redirect('login')
        else:
            return render (request,'registration/sign_up.html', {'error':'Password does not match!','formobj':formobj})
    else:
        formobj=UserCreationForm()
        return render(request,'registration/sign_up.html',{'formobj':formobj})

def addbalpage(request):
    msg1={}
    print(request.user)
    balobj=balance.objects.filter(user=request.user).values()
    print(balobj)
    if balobj.count!=0:
        baldict=balobj.values()
        print(baldict.values())
        bal=0
        for i in baldict:
            print("for")
            keylist=list(i.keys())
            vallist=list(i.values())
            bal=vallist[2]
        msg1["b"]="Balance Available:"+str(bal)
        return render(request,'addBalance.html',msg1)
    else:
        msg1["b"]="Balance Available:0"
        return render(request,'addBalance.html',msg1)

def addexpage(request):
    msg1={}
    balobj=balance.objects.filter(user=request.user)
    if balobj.count!=0:
        baldict=balobj.values()
        print(baldict.values())
        bal=0
        for i in baldict:
            print("for")
            keylist=list(i.keys())
            vallist=list(i.values())
            bal=vallist[2]
        msg1["b"]="Balance Available:"+str(bal)
        return render(request,'addExpense.html',msg1)
        
    else:
        msg1["b"]="Balance Available:0"
        return render(request,'addExpense.html',msg1)

def viewpage(request):
    return render(request,'view.html')

def totalexppage(request):
    return render(request,'totalexp.html')
def addExpense(request):
    errormsg={}
    
    print("addExpense")
    try:
        if request.method=="POST":
            exp=request.POST["expense"]
            amnt=Decimal(request.POST["cost"])
            balobj=balance.objects.filter(user=request.user).values()
            baldict=balobj.values()
            print(baldict.values())
            bal=0
            for i in baldict:
                print("for")
                keylist=list(i.keys())
                vallist=list(i.values())
                bal=vallist[2]
            if(amnt>bal):
                print("insufficient balance")
                errormsg["msg"]="Insufficient Balance"
                return render(request,'addExpense.html',errormsg)
            else:
                print(exp,amnt)
                expobj=expense.objects.filter(user=request.user,expense=exp)
                print(type(expobj.count()))
                if  expobj.count()!=0:
                    expobj=expense.objects.filter(user=request.user)
                    expdict=expobj.values()
                    for i in expdict:
                        expvallist=list(i.values())
                        c=expvallist[3]
                    sm=c+amnt
                    expobj=expense.objects.filter(user=request.user,expense=exp).update(amount=sm)
                    errormsg["msg"]="Expense Updated"
                    bal-=amnt
                    balance.objects.filter(user=request.user).update(deposit=bal)
                else:
                    print("else")
                    expobj=expense(expense=exp,amount=amnt,user=request.user)
                    expobj.save()
                    print(expense.objects.all())
                    errormsg["msg"]="Expense added"
                    bal-=amnt
                    print(bal)
                    balance.objects.filter(user=request.user).update(deposit=bal)
           
            return render(request,"addExpense.html",errormsg)
    except Exception as e:
         print(e)
         errormsg["msg"]="Expense Not Added"
         return render(request,"addExpense.html",errormsg)

def Resethome(request):
    return render(request,'registration/ResetPassword.html')

def resetpassword(request):
        responsedic={ }
        try:
            username=request.POST['username']
            receipent=request.POST['email']
            pwd=request.POST['newpassword']
            user=User.objects.get(username=username)
            subject="Password Reset"
            try:
                if user is not None:
                    user.set_password(pwd)
                    user.save()
                    message="Your Password Changed"
                    send_mail(subject,message,EMAIL_HOST_USER,[receipent])
                    responsedic["errmsg"]="Password Reset Successful"
                    return render(request,'registration/ResetPassword.html',responsedic)
            except Exception as e:
                print(e)
                responsedic["errmsg"]="Email doesnot exist"
                return render(request,'registration/ResetPassword.html',responsedic)
        except Exception as e:
            print(e)
            responsedic["errmsg"]="Failed"
            return render(request,'registration/ResetPassword.html',responsedic)



def addBalance(request):
        errormsg={}
        try:
            if request.method=="POST":
                amount=Decimal(request.POST["balance"])
                bal=balance.objects.filter(user=request.user)
                print(bal.count())
                if bal.count()==1:
                    balobj=balance.objects.filter(user=request.user).values()
                    baldict=balobj.values()
                    print(baldict.values())
                    bal=0.0
                    for i in baldict:
                        print("for")
                        keylist=list(i.keys())
                        vallist=list(i.values())
                        bal=vallist[2]
                    c=bal+amount
                    balobj=balance.objects.filter(user=request.user).update(deposit=c)
                    errormsg["msg"]="Balance updated"
                    return render(request,'addBalance.html',errormsg)  
                else:
                    balobj=balance(user=request.user,deposit=amount)
                    balobj.save()
                    errormsg["msg"]="Balance Added"
                    return render(request,'addBalance.html',errormsg) 
        except Exception as e:
            print (e)
            errormsg["msg"]="Balance  not Added"
            return render(request,'addBalance.html',errormsg)



def viewExpense(request):
    try:
        msg={}
        expobj=expense.objects.filter(user=request.user)
        if expobj:
            return render(request,'view.html',{"exp":expobj})
        else:
            msg["msg1"]="No Expenses To Show"
            return render(request,'view.html',msg)
    except Exception as e:
        print(e)
        msg["msg1"]="Error"
        return render(request,'view.html',msg)

def checkbalpage(request):
    return render(request,'balance.html')

def checkBal(request):
    try:
        msg={}
        if request.method=="POST":
            balobj=balance.objects.filter(user=request.user)
            if balobj:
                return render(request,'balance.html',{"bal":balobj})
            else:
                msg["msg1"]="No Balance To Show"
                return render(request,'balance.html',msg)
    except Exception as e:
        print(e)
        msg["msg1"]="Error"
        return render(request,'balance.html',msg)
    

def totalExp(request):
    try:
        expdict={}
        print(request.user)
        if request.method=="POST":
            allData=expense.objects.filter(user=request.user)
            c=0
            for i in allData:
                c+=i.amount
        print(c)
        expdict[request.user]=c
        return render(request,'totalexp.html',{"expTot":expdict})
    except Exception as e:
        print(e)
        return render(request,'totalexp.html')

