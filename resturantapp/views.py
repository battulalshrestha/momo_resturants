from django.shortcuts import render,redirect
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .models import Address
from django.http import HttpResponse
# for test pass
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
@login_required
def index(request):
     if request.method == "POST":
        # name email phone message
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        print(name,email,phone,message)
        data = Address(name= name,email= email,phone =phone,message = message)
        data.save()
        messages.success(request,"you send the message successfully")
        return redirect('index')
     return render(request, 'base.html')

def menu(request):
    return render(request, 'menu.html')

def services(request):
    return render(request, 'services.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email =request.POST['email']
        password= request.POST['password']
        password1= request.POST['password1']
# for the password validation for the user
        try:
            validate_password(password)
            # checking if password is or is not equal to confirm password
            if password == password1:
                if User.objects.filter(username= username).exists():
                  messages.info(request,"This username is already exist. please try the another username again!!")
                  return redirect("register")
                elif User.objects.filter(email = email).exists():
                    messages.info(request,"Same type of email is already exist. please try the next one")
                    return redirect('register')
                else:
                    User.objects.create_user(first_name = first_name,last_name = last_name,username= username,email = email,password=password)
                    messages.success(request,'sucessfully registered')
                    return redirect('register')
            else: 
                messages.error(request,"password doesnot match!!")
                return redirect("register")
         #for test pass       
        except ValidationError as e:
            for error in e.messages:
                messages.error(request,error)
                return redirect('register')
    return render(request,'auth/register.html')

def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password= request.POST['password']
        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            messages.info(request,"login successfully!!")
            return redirect('index')
        messages.error(request,"Username or password does not match")
    return render(request,"auth/login.html")