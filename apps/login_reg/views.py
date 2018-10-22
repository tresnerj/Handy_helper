from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    return render(request, 'login_reg/index.html')

def register(request):
    if request.method == 'POST':
        email = Users.objects.filter(email=request.POST['email'])
        if len(email) > 0: 
            messages.error('email is already registered')
        errors = Users.objects.registration_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        newpass = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
        user = Users.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=newpass)
        request.session['id'] = user.id
        return redirect('/dashboard')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        try:
            errors = Users.objects.login_validator(request.POST)
            if len(errors):
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/')
        except:
            pass
        user = Users.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
        return redirect('/dashboard')
    return redirect('/')