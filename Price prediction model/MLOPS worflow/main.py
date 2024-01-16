# Importing necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
sns.set()
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression,chi2
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler ,MaxAbsScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import LinearSVR, SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder # For Feature Engineering Method - Label Encoding
from sklearn.preprocessing import MinMaxScaler # For Normalization
from sklearn.model_selection import train_test_split # For Splitting the data into train data and test data
from sklearn.ensemble import RandomForestRegressor # For Creation of Random Forest Regressor Model
from sklearn.linear_model import LinearRegression # For Creation of Linear Regression Model
from sklearn.model_selection import learning_curve
# Libraries for calculationg Metrics of the Model we create:
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import mlflow
import mlflow.sklearn

import warnings
warnings.filterwarnings('ignore')
if __name__ == '__main__':
    mlflow.set_experiment(experiment_name="mlflow debut")
    data = pd.read_excel('Used_car2.xlsx')
    print("loaded training data")
    data.Gouvernorat = data.Gouvernorat.str.lower()

    def replace_name(a,b):
        data.Gouvernorat.replace(a,b,inplace=True)

    replace_name('benarous','ben-arous')
    replace_name('mannouba','manouba')
    replace_name('lamanouba','manouba')
    replace_name('lekef','kef')
    replace_name('sidibouzid','sidi-bouzid')
    replace_name('kébili','kebili')
    replace_name('le-kef','kef')
    replace_name('béja','beja')
    replace_name('gabès','gabes')
    replace_name('médenine','medenine')


    data.Marque = data.Marque.str.lower()
    def replace_name(a,b):
        data.Marque.replace(a,b,inplace=True)
    replace_name('AC','Citroen')
    replace_name('ALFA','Alfaromeo')
    replace_name('GREAT','Greatwall')
    replace_name('Austin','aston martin')
    replace_name('Land','Land rover')
    replace_name('Land-rover','Land rover')
    replace_name('Landrover','Land rover')
    replace_name('Land_rover','Land rover')
    replace_name('Rover','Land rover')
    replace_name('Wallys','Wallyscar')

    data = data[data['Gouvernorat'].notna()]
    data = data.reset_index(drop=True)
    data.drop_duplicates()
    #removing repetitive lines

    def replace_name_marque(a,b):
        data.Marque.replace(a,b,inplace=True)

    replace_name_marque('MG','MGMOTORS')
    replace_name_marque('WALLYSCAR','WALLYS')
    replace_name_marque('LAND_ROVER','LAND-ROVER')
    replace_name_marque('ROVER','LAND-ROVER')
    replace_name_marque('DEAWOO','DAEWOO')
    replace_name_marque('GREAT','GREATWALL')

    data = data[data['Gouvernorat'].notna()]
    data = data[data['Marque'].notna()]
    data = data.reset_index(drop=True)

    max_thresold= data['Prix'].quantile(0.95)

    data=data[data.Prix < max_thresold]
    data["age_of_car"] = 2022 - data["Mise_en_circulation"]
    data = data.drop(columns = ["Mise_en_circulation"])
    counts_Model = data['Model'].value_counts()
    data = data.loc[data['Model'].isin(counts_Model.index[counts_Model > 5])]


    counts_Marque = data['Marque'].value_counts()
    data = data.loc[data['Marque'].isin(counts_Marque.index[counts_Marque > 5])]

    y = data['Prix']
    X = data.drop('Prix', axis=1)

    ohe=OneHotEncoder()
    ohe.fit(X[['Marque','Model','Carburant','Boite_Vitesse','Gouvernorat']])

    column_trans=make_column_transformer((OneHotEncoder(categories=ohe.categories_),['Marque','Model','Carburant','Boite_Vitesse','Gouvernorat']),
                                        remainder='passthrough')
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.15,random_state=41,shuffle=True)


    mlflow.log_param("shape_of_x_train", X_train.shape)

    mlflow.log_param("shape_of_x_test", X_test.shape)

    mlflow.log_param("shape_of_y_train", y_train.shape)

    mlflow.log_param("shape_of_the_y_test", y_test.shape)

    ## Importing Random Forest Regressor from the sklearn.ensemble

    rf = RandomForestRegressor()

    pipe=make_pipeline(column_trans,MaxAbsScaler(),RandomForestRegressor(n_estimators=50,min_samples_split=2,min_samples_leaf=1,max_features='sqrt',bootstrap=False,random_state=1))
    pipe.fit(X_train,y_train)
    y_pred=pipe.predict(X_test)
    print('the_R2_score: ')
    r2=r2_score(y_test, y_pred)
    mlflow.log_metric("R2_Score",r2)
    mlflow.sklearn.log_model(pipe,"model")

    accuracies = cross_val_score(estimator=pipe, X=X_train, y=y_train, cv=50)

    mlflow.log_metric("maximum_of_different_train_test_partitions",accuracies.max() )
    print('maximum of cv calculated')
    mlflow.log_metric("mean_of_different_train_test_partitions", accuracies.mean())
    print('mean of cv calculated')


