from pyexpat.errors import messages
from django.shortcuts import render,redirect
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

model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model = load_model('./savedModels/resnet50-saved-model-20-val_acc-0.95.hdf5')

img_height, img_width = 256, 256

def index(request):
    context = {'a': 1}
    return render(request, 'priceprediction/test.html', context)


def predictImage(request):
    try : 
            print(request)
            print(request.POST.dict())
            fileObj = request.FILES['filePath_']
            fs = FileSystemStorage()
            filePathName = fs.save(fileObj.name, fileObj)
            filePathName = fs.url(filePathName)
            testimage = '.' + filePathName
            img = tf.keras.utils.load_img(testimage, target_size=(img_height, img_width))

            # resize ml matrice
            # x = image.img_to_array(img)
            # x = x / 255
            # x = x.reshape(1, img_height, img_width, 3)
            # ///////////////////////////////////////////////////////////////////////
            fixed_height = 256

            height_percent = (fixed_height / float(img.size[1]))
            width_size = int((float(img.size[0]) * float(height_percent)))
            new_image = img.resize((width_size, fixed_height), PIL.Image.NEAREST)

            # ///////////////////////////////////////////////////////////////////////////////////////////////
            x = tf.keras.utils.img_to_array(new_image)
            img_batch = np.expand_dims(x, 0)
            with model_graph.as_default():
                with tf_session.as_default():
                    predi = model.predict(img_batch)
            CLASS_NAMES = ['Citroen DS 6WR',
                        'Citroën  C-Elysée',
                        'Citroën DS4',
                        'GMC truck 2014',
                        'Golf 7',
                        'ISUZU DMAX 4P',
                        'Land Rover Charleroi R. Leone',
                        'MITSUBISHI ASX',
                        'Mazda 3 hatchback',
                        'Mazda 6',
                        'Mini Cooper SD 5-door (2015)',
                        'Renault Captur',
                        'Renault Duster 2011',
                        'Renault Duster 2014',
                        'Renault symbol',
                        'Toyota Land Cruiser 79 4.2 l Diesel 4x4',
                        'Toyota RAV 4 2013',
                        'Toyota yaris',
                        'amarok',
                        'clio 4',
                        'fiesta ford',
                        'jeep liberty 2014',
                        'jeep wrangler 2014',
                        'mazda cx 9 2013',
                        'mini cooper s cabrio r57',
                        'passat',
                        'peugeot 2008',
                        'peugeot 207',
                        'peugeot 301',
                        'polo 7',
                        'toyota corolla 2014',
                        'volw ibeetel']
            # /////////////////////////////////////////////////////////////////////////////////////////////////

            predictedLabel = CLASS_NAMES[np.argmax(predi)]
            confidence = np.max(predi[0]) * 100
            confidence = round(confidence, 2)

            # /////////////////////////////////
            # /////////////////////////////////
            context = {'filePathName': filePathName, 'predictedLabel': predictedLabel, 'confidence': confidence}
            messages.success(request,'You can see your predicted model on clicking the botton on the top page')
            return render(request, 'priceprediction/test.html', context)
    except : 
            messages.error(request, 'You need to upload a image first')
            return render(request, 'priceprediction/test.html')

