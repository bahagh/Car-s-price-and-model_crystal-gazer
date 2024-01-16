from django.urls import path
from . import views 

urlpatterns = [
    path('price/', views.priceestimation, name="price"),
]