from django.db import models
from datetime import datetime
from Core.models import User
from django.db.models import Avg, Count
from django.utils import timezone

# Create your models here.
class Listing(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    Make = models.CharField(max_length=100)
    Model = models.CharField(max_length=100)
    Year  = models.IntegerField()

    Mileage = models.IntegerField()
    price = models.IntegerField()
    address = models.CharField(max_length=100)
    Governorate = models.CharField(max_length=100)
    Phone_number = models.IntegerField()
    Fuel = models.CharField(max_length=100)
    Engine_Horsepower = models.IntegerField()
    Transmission = models.CharField(max_length=100)
    Color = models.CharField(max_length=100)
    Number_of_seats = models.IntegerField()
    Doors = models.IntegerField()

    Vehicle_description = models.TextField(blank=True)
    Vehicle_extras = models.TextField(blank=True)
    Vehicle_extras_Interior = models.TextField(blank=True)
    Vehicle_extras_Safety = models.TextField(blank=True)

   

    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateField(default=timezone.now)
    Predictedprice = models.IntegerField(blank=True,default=0)

    

    def __str__(self):
        return self.title
    
    def avaregereview(self):
        reviews = ReviewRating.objects.filter(car_id=self).aggregate(avarage=Avg('rating'))
        avg = 0
        if reviews["avarage"] is not None :
            avg = float(reviews["avarage"])
        return avg


    def countreview(self):
        reviews = ReviewRating.objects.filter(car_id=self).aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None :
            cnt = reviews["count"]
        return cnt


class ReviewRating(models.Model):
    car = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    review = models.TextField(max_length=500)
    rating = models.FloatField(default=0)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    
    
