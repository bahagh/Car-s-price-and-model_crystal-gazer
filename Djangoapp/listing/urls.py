from django.urls import path
from . import views 


urlpatterns = [
    path('',views.Cars , name="Cars"),
    path('<int:pk>/', views.car_details, name="car-details"),
    path('search/', views.search, name="search"),
    path('create/', views.create, name="create"),
    path('update/<int:pk>/', views.update, name="update"),
    path('<int:pk>/delete/', views.review_delete, name="delete"),
    path('submit_review/<int:car_id>/', views.submit_review, name='submit_review'),
    path('analyser/<int:pk>/', views.analyser_cars, name="analyser"),

]