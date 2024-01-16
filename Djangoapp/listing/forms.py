from django.forms import ModelForm
from .models import Listing
from django import forms
from .models import ReviewRating
 
INTEGER_CHOICES= [tuple([x,x]) for x in range(1990,2022)]
Fuel_CHOICES = (
('',''),   
('Diesel', 'Diesel'),
('Petrol', 'Petrol'),
('Others', 'Others'),)
Transmission_CHOICES = (
('',''),   
('Automatic', 'Automatic'),
('Manuel', 'Manuel'),)
'''class ListingForm(ModelForm):
    
    Year =  forms.IntegerField( widget=forms.Select(choices=INTEGER_CHOICES))

    Fuel= forms.CharField(widget=forms.Select(choices=Fuel_CHOICES))
    Transmission= forms.CharField(widget=forms.Select(choices=Transmission_CHOICES))

    class Meta:
       model = Listing
       fields = ['title','Make','Model','Mileage','price','Year','Fuel','Engine_Horsepower' ,'Transmission','Number_of_seats','Doors','Color','address', 'Governorate' ,'Phone_number','Vehicle_description','Vehicle_extras','photo_main', 'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6']
    '''
class ListingForm(forms.Form):

    title= forms.CharField()
    Make= forms.CharField()
    Model= forms.CharField()
    Year =  forms.IntegerField()
    Mileage =  forms.IntegerField()
    price =  forms.IntegerField()
    address= forms.CharField()
    Governorate= forms.CharField()
    Phone_number =  forms.IntegerField()
    Fuel= forms.CharField()
    Engine_Horsepower= forms.CharField()
    Transmission= forms.CharField()
    Color= forms.CharField()
    Number_of_seats= forms.CharField()
    Doors= forms.CharField()
    
    Vehicle_extras= forms.CharField()
    Vehicle_extras_Interior= forms.CharField()
    Vehicle_extras_Safety= forms.CharField()

    Vehicle_description= forms.CharField()
    photo_main=forms.ImageField()
    photo_1=forms.ImageField()
    photo_2=forms.ImageField()
    photo_3=forms.ImageField()
    photo_4=forms.ImageField()
    photo_5=forms.ImageField()
    photo_6=forms.ImageField()


class UpdateForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','Vehicle_description','price','photo_main']



class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review']