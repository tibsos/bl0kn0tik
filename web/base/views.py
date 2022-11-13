from django.shortcuts import render

def landing(request):

    c = {}

    if request.user.is_authenticated:

        c['logged_in'] = True
    
    else: 

        c['logged_in'] = False

    return render(request, 'landing.html', c)