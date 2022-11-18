from django.shortcuts import render


def landing(request):

    c = {}

    if request.user.is_authenticated:

        c['logged_in'] = True
    
    else: 

        c['logged_in'] = False

    return render(request, 'landing.html', c)

def plans(request):
    
    if request.user.is_authenticated:
        
        c = {"user": request.user}
        
    
    return render(request, 'plans.html', c)

def contact(request):
    
    if request.user.is_authenticated():
        
        c = {"user": request.user}
        
    
    return render(request, 'contact.html', c)


# Terms

def terms(request):
    
    return render(request, 'terms/terms.html')

def privacy(request):
    
    return render(request, 'terms/privacy.html')

def juridical_info(request):
    
    return render(request, 'terms/juridical-info.html')

def online_payment_protection(request):
    
    return render(request, 'terms/online-payment-protection.html')

def information_security(request):
    
    return render(request, 'terms/information-security.html')