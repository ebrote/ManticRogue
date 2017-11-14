
import sqlalchemy
import csv
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import mapper
import re
import unidecode
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from time import time

import math

####### Database extraction ######
class Mairies():
	pass

engine = create_engine('sqlite:///data/database.db', echo=False)
metadata = MetaData(engine)
mairies = Table('mairies', metadata, autoload=True)
mapper(Mairies, mairies)
Session = sessionmaker(bind=engine)
session = Session()

def data_frame(query, columns):
    """
    Takes a sqlalchemy query and a list of columns, returns a dataframe.
    """
    def make_row(x):
        return dict([(c, getattr(x, c)) for c in columns])       
    return pd.DataFrame([make_row(x) for x in query])

# dataframe with all fields in the table
query = session.query(Mairies).all()
DF = data_frame(query, ["insee_code","postal_code","city", "population" ,"latitude" ,"longitude","first_name","last_name","birthdate","first_mandate_date","party"])

DF2 = pd.DataFrame(session.query(mairies).all()).query("latitude != 'None' and longitude != 'None'")
DF["population"] = DF["population"].apply(pd.to_numeric)
#DF["first_mandate_date"] = DF["first_mandate_date"].apply(pd.to_numeric)
# DF['latitude'] = DF['latitude'].astype(numeric)


####### Data analysis ######


DF['birthyear'] = DF['birthdate'].apply(lambda x: (dt.datetime.today() - dt.datetime.strptime(x.strip(), '%Y-%m-%d')).days//365)

def data_clense(DF):
	data_scale = scale(DF)
	return data_scale

def clustering(DF_o,n_clusters=5):
	data = DF_o.as_matrix()


	kmeans = KMeans(init='k-means++', n_clusters=n_clusters, n_init=10)
	kmeans.fit(data)

	Z = kmeans.predict(data)

	DF_cluster = pd.DataFrame(Z,columns=['cluster'])
	df = pd.concat([DF2, DF_cluster], axis=1)
	print(df.head())

	return DF

DF_filtered = DF2[DF2.population>5000]

DF3 = DF_filtered[['latitude','longitude']]#,'birthyear']]
#DF2 = DF2[DF2.latitude != 'None']
# DF2 = DF2[DF2.longitude != 'None']
print(DF3.head())

DF3 = clustering(DF3)
print(DF3.head())
