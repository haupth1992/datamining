# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 17:02:27 2017

@author: Thomas Hauptvogel
"""

import numpy as np
from pymongo import MongoClient
import nltk
import io
#nltk.download('all')

client = MongoClient("-Insert-MongoDB-Connection-String-Here-")

#Get data from database
db = client.mfdata #database

#Lemmatizer for used hashtags
st = nltk.wordnet.WordNetLemmatizer()

#creates array with all hashtags stored in a specific mongodb collection, transforms data strings to lowercase, uses lemmatizer to erase plural form
cursorUS = db.tweetsUSA.find({}, {'place':1,'entities':1})
cursorUK = db.tweetsUK.find({}, {'place':1,'entities':1})

#Open/Create file and fill it with our data
with io.open('hashtagData.csv', "w", encoding="utf-8") as f:
    f.write('place_type,country,hashtag\n')
    for doc in cursorUS:
            for hashtag in doc['entities']['hashtags']:
                if(doc['place'] is not None):
                    f.write(doc['place']['place_type'])
                    if (doc['place']['country'] == "United States"):
                        f.write(',1,')
                    elif (doc['place']['country'] == "United Kingdom"):
                        f.write(',0,')
                    else:
                        f.write(',2,')
                    f.write(st.lemmatize(hashtag['text'].lower()))
                    f.write('\n')
    for doc in cursorUK:
            for hashtag in doc['entities']['hashtags']:
                if(doc['place'] is not None):
                    f.write(doc['place']['place_type'])
                    if (doc['place']['country'] == "United States"):
                        f.write(',1,')
                    elif (doc['place']['country'] == "United Kingdom"):
                        f.write(',0,')
                    else:
                        f.write(',2,')
                    f.write(st.lemmatize(hashtag['text'].lower()))
                    f.write('\n')
f.close()