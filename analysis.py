
# import sqlalchemy
# import csv
# import requests
# from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import mapper
# import re
# import unidecode
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
# import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import math

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
print(DF.shape)
DF["population"] = DF["population"].apply(pd.to_numeric)
#DF["first_mandate_date"] = DF["first_mandate_date"].apply(pd.to_numeric)
# DF['latitude'] = DF['latitude'].astype(numeric)


# def import_data():
# 	'''
# 	TODO : 
# 	Code that will eventually import our scrapped data
# 	'''
# 	query = session.query(Mairies).all()

# 	df = pd.read_sql(query,engine)

# 	# df = pd.concat([df1,df2],axis=1)
# 	return df

DF_filtered = DF[DF.population>5000]

#####################################
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from time import time


n_clusters=5
DF2 = DF_filtered[['latitude','longitude']]#,'birthdate','first_mandate_date']]
DF2 = DF2[DF2.latitude != 'None']
DF2 = DF2[DF2.longitude != 'None']
data = DF2.as_matrix()


kmeans = KMeans(init='k-means++', n_clusters=n_clusters, n_init=10)
kmeans.fit(data)

Z = kmeans.predict(data)
print(Z)
