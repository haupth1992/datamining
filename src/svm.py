# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 17:10:13 2018

@author: Thomas Hauptvogel
"""
import pandas as pd
import numpy as np
from sklearn import svm

from sklearn import preprocessing

# for learning and the evaluation
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score

# create data frame containing your data, each column can be accessed # by data['column   name']
data = pd.read_csv('hashtagData.csv', header=0)
le = preprocessing.LabelEncoder()

#Encode our categorical features into numerical features
cleanup_places = {"place_type": {"city": 1, "admin": 2, "poi": 3, "neighborhood": 4,"country": 5}}
data.replace(cleanup_places, inplace=True)
data['hashtag']=le.fit_transform(data['hashtag'])
data.head()

#Create numpy array with our transformed data
all = np.array(data)

y = all[:,1]
X = np.column_stack((data.hashtag,data.hashtag))
X.shape 

#Split our data into training and test data
X_train, X_test, y_train, y_test = tts(X, y, test_size=0.33 ,random_state=42)
#Define our Classifier
clf = svm.SVC(kernel='linear',gamma=0.001, C=1.50)
#Fit our model to the classifier
model = clf.fit(X_train, y_train)

#Predict our Test Data Set
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
print (accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))