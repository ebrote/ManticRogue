import pandas as pd
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
import matplotlib.pyplot as plt
import numpy as np
import math
import datetime as dt


engine = create_engine('sqlite:///data/database.db', echo=False)
metadata = MetaData(engine)
mayor = Table('mayors', metadata, autoload=True)
Session = sessionmaker(bind=engine)
session = Session()

metadata.create_all(engine)


#Communes with fewer than 5000 inhabitants filtered

df = pd.DataFrame(session.query(mayor).all()).query('population > 5000')

#NNumber of mayors per party

nbre_mayor_per_party = df[['party', 'first_name']].groupby("party").count()

#Population per party

pop_per_party = df[['party', 'population']].groupby("party").sum().sort_values('population')

#mayor average age by party

table_average = df[['party', 'birthdate']]
table_average['birthdate'] = table_average['birthdate'].apply(lambda x: x.strip())
table_average['birthdate'] = table_average['birthdate'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
table_average['birthdate'] = table_average['birthdate'].apply(lambda x: (dt.datetime.today() - x).days//365)

average_age_per_party = table_average.groupby('party')['birthdate'].mean()

#number of mayors per party depending on size of commune

def size(population):
	if 5000 <= float(population) <= 10000 :
		return '5000<= x <= 10000'
	if 10000 <= float(population) <= 20000 :
		return '10000<= x <= 20000'
	if 20000 <= float(population) <= 50000 :
		return '20000<= x <= 50000'
	if 50000 <= float(population) <= 100000 :
		return '50000<= x <= 100000'
	if 100000 <= float(population) :
		return '100000<= x'


size_list = [size(row['population']) for index, row in df.iterrows()]

dataframe_size = df[['party', 'population']]
commune_size = pd.Series(size_list, dataframe_size.index)
dataframe_size['size'] = commune_size.values
 mayors
_by_size = dataframe_size[['size', 'party']].groupby('party').count()
print mayors_by_size)












