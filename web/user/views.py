from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate 

from django.contrib.auth.forms import UserCreationForm

from uuid import uuid4 as u4

from .helpers import send_forgot_password_mail

from app.models import *
from .models import Profile

def register(request):

    c = {}

    if request.method == 'POST':

        rp = request.POST

        name = rp.get('name')

        username = rp.get('username')
        password = rp.get('password1')

        _mutable = rp._mutable
        rp._mutable = True
        rp['password2'] = password
        rp.pop('name', None)
        rp._mutable = _mutable

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            profile = user.profile

            profile.name = name
            
            profile.initials = ''.join([i[0].upper() for i in name.split(' ')])

            notepad = Notepad.objects.create(creator = user, title = 'Первый', color = 'blue')
            note = Note.objects.create(creator = user, title = '', content = '')
            notepad.notes.add(note)

            profile.active_notepad = notepad
            profile.active_note = note

            profile.save()
            user = authenticate(username = username, password = password)
            login(request, user)

            return redirect('app:home')

    return render(request, 'auth/register.html', c)


def forgot_password(request):
    
    try:
        
        if request.method == 'POST':
            
            user = User.objects.get(username = request.POST.get('username'))
    
            if not user:
                
                return render(request, 'auth/forgot-password.html', {'user_found': False})
            
            token = str(u4())
            
            profile = user.profile
            profile.forgot_password_token = token
            profile.save()
            
            send_forgot_password_mail(user, token)
            
            return redirect('/email-sent/')

    except Exception as e:
        
        pass
    
    return render(request, 'auth/forgot-password.html')

def change_password(request, token):
    
    try:
        
        profile = Profile.objects.get(forget_password_token = token)
        
        if request.method =='POST':
            
            new_password = request.POST.get('new_password')
            
            profile.user.set_password = new_password
            profile.user.save()
            
            return redirect('/login/')
            
        
        
        
    except Exception as e:
        
        pass
    
    return render(request, 'password-recovery/change_password.html', {'user': profile.user})