# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 00:16:52 2021

@author: poorv
"""


import pandas as pd
import numpy as np


clean = pd.read_csv('data_cleaned.csv')



#Create field for description length
clean['Description Length'] = clean['Job Description'].str.len()


#Group job titles appearing only once into  'Other'
clean['Job Title'].loc[clean['Job Title'].isin(clean['Job Title'].value_counts()[clean['Job Title'].value_counts()==1].index)] = 'Other'


#Drop unnecessary columns
clean.drop(columns=['Job Description', 'Founded'], inplace = True)

#Replace company age 2022 with -1
clean['Company Age'].replace(2022,-1,inplace=True)

#Histograms
clean['Rating'].hist()
clean['Company Age'].hist()
clean['Average Salay'].hist()
clean['Description Length'].hist()
