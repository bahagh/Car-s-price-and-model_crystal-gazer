from django.shortcuts import render
from listing.models import Listing
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


# Create your views here.
def index(request) : 
    Cars = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(Cars, 3)
    page = request.GET.get('page')
    page_listings  = paginator.get_page(page)
    context = {
        'listings': page_listings
       }
    return render(request,'pages/index.html',context)

def about(request) :
    return render(request,'pages/about.html')

def contact(request) :
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        data ={
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }
        message ='''
        New message : {}
        
        From : {}
        '''.format(data['message'], data['email'])
        send_mail(data['subject'], message, '', ['ala.garbey@esprit.tn'])
        messages.success(request, 'Message sended with succes')

        return render(request, 'pages/index.html')

    return render(request,'pages/contact.html',{})

    


