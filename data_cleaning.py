# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 14:04:03 2021

@author: poorv
"""

import pandas as pd

df = pd.read_csv('glassdoor_jobs.csv')



#Job titles Junior/Graduate/Entry Level vs nothing vs Senior/Principal/Head/Lead
#Salary estimate - New column for Gumtree vs Employer Provided
#Salary separate columns for min and max
#Salary check out if any hourly rates
#job description - Tools, buzzwords, big data tools, cloud, PhD
#Location collapse suburbs into city names. 
#Location think about what to do with country and state names
#Remove the word employees from Size
#Get Age from Founded.
#Consider creating Age group categories
#Get rid of stray values in Type of Ownership, Sector, Industry and Founded


df2=df[df['Salary Estimate']!='-1']
