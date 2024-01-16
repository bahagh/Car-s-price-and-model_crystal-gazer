from email import message
from django.shortcuts import render
import pandas as pd
import numpy as np
import joblib
from joblib import load
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# Create your views here.
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
from tensorflow import Graph
import numpy as np
from PIL import Image

import PIL

model = load('./savedModels/model.joblib')
@login_required
def priceestimation(request):
    try : 
        data = pd.read_csv('./savedModels/df.csv')
        gouvernorats=data['Gouvernorat'].unique()
        price=0
        if request.method == 'POST':
            marqu=request.POST['marque']
            mod=request.POST['modele']
            puiss=request.POST['puissance']
            kilo=request.POST['kilo']
            carburant=request.POST['carburant']
            boite=request.POST['boite']
            gouvernorat=request.POST['gouvernorat']
            age=request.POST['age']
            pred=model.predict(pd.DataFrame(columns=['Marque','Model','Puissance_fiscale','Kilometrage','Carburant','Boite_Vitesse','Gouvernorat','age_of_car'],data=np.array([marqu,mod,puiss,kilo,carburant,boite,gouvernorat,age]).reshape(1,8)))
            price=pred[0]
            messages.success(request,'You can see your predicted price on clicking the botton on the left corrner')
        return render (request,'priceprediction/price.html',{'price': int(price),'gouvernorats':gouvernorats})

    except : 
        return render (request,'priceprediction/price.html')

