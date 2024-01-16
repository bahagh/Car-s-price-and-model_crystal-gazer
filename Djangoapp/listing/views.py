from audioop import reverse
from multiprocessing import context
import string
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from sklearn.tree import export_text
from .choices import price_choices,engine_Horsepower_choices,mileage_choices
from .models import Listing,ReviewRating
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from .forms import ListingForm, UpdateForm
from .forms import ReviewForm
from Core.models import User
import pandas as pd
import numpy as np
from tqdm.auto import tqdm
import tensorflow as tf
from transformers import BertTokenizer
from transformers import TFBertModel
from django.db.models import Avg, Count
from .models import Listing, ReviewRating
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
sns.set()




with open('./savedModels/model.joblib','rb') as file:
    model = pickle.load(file)
used_check = pd.read_excel('./savedModels/Used_car2.xlsx')
used_check = used_check.dropna()
data = pd.read_excel('Used_car2.xlsx')
data = data.dropna()
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

#car_models = pd.read_excel('./savedModels/marquemodel.xlsx')


#model = load('./savedModels/model.joblib')

def Cars(request):
        Cars = Listing.objects.order_by('-list_date').filter(is_published=True)
        paginator = Paginator(Cars, 6)
        page = request.GET.get('page')
        page_listings  = paginator.get_page(page)
        context = {
        'listings': page_listings
        }

        return render  (request,'listings/Cars.html',context)
   

def car_details(request,pk):
        listing = get_object_or_404(Listing, pk=pk)
        reviews = ReviewRating.objects.order_by()
        context = {
            'listing': listing,
            'reviews': reviews,
        }

        return render (request,'listings/car-details.html',context)



def search(request):

    companies = sorted(used_check['Marque'].unique().astype(str))
    models = sorted(used_check['Marque Model'].unique().astype(str))


    query_set = Listing.objects.order_by('-list_date')
    if 'Make' in request.GET:
        Make = request.GET['Make']
        if Make:
                query_set = query_set.filter(Make__iexact=Make)
    if 'Model' in request.GET:
        Model = request.GET['Model']
        if Model:
                query_set = query_set.filter(Model__iexact=Model)
    if 'Color' in request.GET:
        Color = request.GET['Color']
        if Color:
                query_set = query_set.filter(Color__iexact=Color)
    if 'Fuel' in request.GET:
        Fuel = request.GET['Fuel']
        if Fuel:
                query_set = query_set.filter(Fuel__iexact=Fuel)
    if 'Transmission' in request.GET:
        Transmission = request.GET['Transmission']
        if Transmission:
                query_set = query_set.filter(Transmission__iexact=Transmission)
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            query_set = query_set.filter(price__lte=price)
    if 'Engine_Horsepower' in request.GET:
        Engine_Horsepower = request.GET['Engine_Horsepower']
        if Engine_Horsepower:
            query_set = query_set.filter(Engine_Horsepower__lte=Engine_Horsepower)
    if 'Mileage' in request.GET:
        Mileage = request.GET['Mileage']
        if Mileage:
            query_set = query_set.filter(Mileage__lte=Mileage)
    context = {
                'query_set': query_set, 
                'companies': companies,
                'price_choices': price_choices,
                'mileage_choices': mileage_choices,
                'engine_Horsepower_choices': engine_Horsepower_choices,
                'models': models,  
                'values': request.GET,  
        }
    return render(request, 'listings/search.html', context)



@login_required
def create(request):
    #companies_check = sorted(used_check['make'].unique())

    #models_check = sorted(used_check['make_model'].unique())

    companies = sorted(used_check['Marque'].unique().astype(str))
    

    models = sorted(used_check['Marque Model'].unique().astype(str))

    context = {
            'companies': companies,
            'models': models,

        }
    Predictedprice=0
    if request.method == 'POST':
        owner = request.user

        title = request.POST.get('title')
        Make = request.POST.get('Make')
        Model = request.POST.get('Model')
        Year = request.POST.get('Year')
        Mileage = request.POST.get('Mileage')
        price = request.POST.get('price')
        address = request.POST.get('address')
        Governorate = request.POST.get('Governorate')
        Phone_number = request.POST.get('Phone')
        Fuel = request.POST.get('Fuel')
        Engine_Horsepower = request.POST.get('Engine')
        Transmission = request.POST.get('Transmission')
        Color = request.POST.get('Color')
        Number_of_seats = request.POST.get('Number_of_seats')
        Doors = request.POST.get('Doors')
      
        Vehicle_extras = request.POST.getlist('Vehicle_extras[]')
        
        Vehicle_extras_Interior = request.POST.getlist('Vehicle_extras_Interior[]')
        Vehicle_extras_Safety = request.POST.getlist('Vehicle_extras_Safety[]')

        Fuel_pred = ""
        if Fuel == 'Petrol' : 
            Fuel_pred = "Essence"
        else : 
            Fuel_pred = "Diesel"
        Transmission_pred = ""
        if Transmission == 'Automatic' : 
            Transmission_pred = "Automatique"
        else : 
            Transmission_pred = "Manuelle"
        
        Model_pred =tuple (Model.split())
        Governorate_pred = Governorate.lower()

        Model_pred = Model_pred[1]
        
        age_of_the_car = 2022 - int(Year) 

        
        Vehicle_description = request.POST.get('Vehicle_description')
        photo_main = request.FILES['photo_main']
        photo_1 = request.FILES.get('photo_1', None)
        photo_2 = request.FILES.get('photo_2', None)
        photo_3 = request.FILES.get('photo_3', None)
        photo_4 = request.FILES.get('photo_4', None)
        photo_5 = request.FILES.get('photo_5', None)
        photo_6 = request.FILES.get('photo_6', None)
        try : 
            pred=model.predict(pd.DataFrame(columns=['Marque','Model','Puissance_fiscale','Kilometrage','Carburant','Boite_Vitesse','Gouvernorat','age_of_car'],data=np.array([Make,Model_pred,Engine_Horsepower,Mileage,Fuel_pred,Transmission_pred,Governorate_pred,age_of_the_car]).reshape(1,8)))
            Predictedprice=pred[0]
        except :
            Predictedprice = 0
        list=Listing(owner=owner,title=title,Make=Make,Model=Model,Year=Year,Mileage=Mileage,
        price=price,address=address,Governorate=Governorate,
        Phone_number=Phone_number,Fuel=Fuel,Engine_Horsepower=Engine_Horsepower,Transmission=Transmission,
        Color=Color,Number_of_seats=Number_of_seats,Doors=Doors,
        Vehicle_extras=Vehicle_extras,
        Predictedprice=Predictedprice,
        Vehicle_extras_Interior=Vehicle_extras_Interior,
        Vehicle_extras_Safety=Vehicle_extras_Safety,
        Vehicle_description=Vehicle_description,
        photo_main=photo_main,photo_1=photo_1,photo_2=photo_2,
        photo_3=photo_3,photo_4=photo_4,photo_5=photo_5,photo_6=photo_6)

        list.save()
        return redirect('dashboard')
       
     
    return  render(request,'listings/create2.html',context)
   
'''  form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.owner = request.user
            new.save()
            return  render(request,'accounts/dashboard.html')
        else:
            pass
    else:
        return render (request,'listings/create.html',{'form': ListingForm()})

'''
@login_required
def update(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    context = {
        'form': UpdateForm(instance=listing),
        'update': True,
        'pk': pk
    }
    if request.method=="POST":
        form = UpdateForm(request.POST,request.FILES,instance=listing)
        print(form)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        return render(request, 'listings/create.html', context)

@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    if request.method=="POST":
        listing.delete()
        return redirect('dashboard')

def prepare_data(input_text, tokenizer):
    token = tokenizer.encode_plus(
        input_text,
        max_length=256, 
        truncation=True, 
        padding='max_length', 
        add_special_tokens=True,
        return_tensors='tf'
    )
    return {
        'input_ids': tf.cast(token.input_ids, tf.float64),
        'attention_mask': tf.cast(token.attention_mask, tf.float64)
    }

def make_prediction(model, processed_data, classes=[1,2,3,4,5]):
    probs = model.predict(processed_data)[0]
    return classes[np.argmax(probs)]


def submit_review(request, car_id):

    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, car__id=car_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
           
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            sentiment_model = tf.keras.models.load_model('sentiment_model.h5')
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                #data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                input_text = request.POST.get('review')
                processed_data = prepare_data(input_text, tokenizer)
                data.rating = make_prediction(sentiment_model, processed_data=processed_data)
                data.ip = request.META.get('REMOTE_ADDR')
                data.car_id = car_id
                data.user_id = request.user.id
               
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)


def review_delete(request, pk) : 
    url = request.META.get('HTTP_REFERER')

    reviewRating = ReviewRating.objects.filter(user = pk)
    reviewRating.delete()
    return redirect(url)


def analyser_cars(request,pk) : 

        url = request.META.get('HTTP_REFERER')
        listing = get_object_or_404(Listing, pk=pk)
        model = listing.Model
        model = model.split()
        model = model[1]
        try :
                nb=data[data.model_upper==model].shape[0]
                prix_moy=int(data['Prix'][data.model_upper==model].dropna().mean())
                kil_moy=int(data['Kilometrage'][data.model_upper==model].dropna().mean())
                age_moy=2022-int(data['Mise_en_circulation'][data.model_upper==model].dropna().mean())
                prix=data.sort_values(['Mise_en_circulation'])['Prix'][data.model_upper==model].tolist()
                prix2=data.sort_values(['Kilometrage'])['Prix'][data.model_upper==model].tolist()
                age=data.sort_values(['Mise_en_circulation'])['Mise_en_circulation'][data.model_upper==model].tolist()
                kil=data.sort_values(['Kilometrage'])['Kilometrage'][data.model_upper==model].tolist()
                #carb=data['Carburant'][data.Model=='Golf7'].tolist()
                ess=data['Carburant'][data.model_upper==model].dropna().value_counts()[0]
                try : 
                    dies=data['Carburant'][data.model_upper==model].dropna().value_counts()[1]
                except :
                    dies=0
                manu=data['Boite_Vitesse'][data.model_upper==model].dropna().value_counts()[0]
                try :
                    auto=data['Boite_Vitesse'][data.model_upper==model].dropna().value_counts()[1]
                except : 
                    auto=0
                sns.set_theme(style="ticks")

                f, ax = plt.subplots(figsize=(10, 10))
                sns.despine(f)

                ch=sns.histplot(
                    data,
                    x=data['Prix'],
                    multiple="stack",
                    palette="light:m_r",
                    edgecolor=".3",
                    linewidth=.5,
                    log_scale=True,
                )
                ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
                context = {
                    'listing':listing,
                    'nb_an':nb,
                    'prix_moy':prix_moy,
                    'kil_moy':kil_moy,
                    'age_moy':age_moy,
                    'prix':prix,
                    'prix2':prix2,    
                    'age':age,
                    'kil':kil,
                    'ess':ess,
                    'dies':dies,
                    'manu':manu,
                    'auto':auto,
                    'ch':ch,
                }
                return render (request, 'listings/analyser.html',context)
        except :
            messages.error(request, 'We don''t have enough data to do Statistics on this model ')
            return redirect(url)



