# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 14:04:03 2021

@author: poorv
"""

import pandas as pd

df = pd.read_csv('glassdoor_jobs.csv')



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


'''
Remove the observations where the salary data is missing
'''
df=df[df['Salary Estimate']!='-1']


'''
Remove irrelevant Job Titles 
'''
relevant= ['scientist', 'data', 'analyst', 'science', 'analysis', 'insight', 'machine learning']

relevance_bool = df['Job Title'].apply(lambda title: True if any([x for x in relevant if x in title.lower()]) else False)
df = df[relevance_bool]

del relevance_bool, relevant


'''
Create new column Salary Source by extracting information from Salary field
'''

df['Salary Source']=df['Salary Estimate'].apply(lambda sal: sal.split('(')[1][0:-2] if 'Glassdoor' in sal else sal.split(':')[0])
df['Salary Estimate']=df['Salary Estimate'].apply(lambda sal: sal.split('(')[0] if 'Glassdoor' in sal else sal.split(':')[1])



'''
#Alternative method as an exercise (using pandas str.split, which usually is more convenient but not in this case)

#Splitting to create two new dataframes
sal_est_glass=df['Salary Estimate'].str.split('(', expand=True)
sal_est_emp=df['Salary Estimate'].str.split(':', expand=True)

#Ensure each dataframe shows values only for the relevant rows
sal_est_emp[0].where(sal_est_emp[1].notna(), inplace=True)
sal_est_glass[0].where(sal_est_glass[1].notna(), inplace=True)

#Modify dataframe
df['Salary Source'] = sal_est_glass[1].fillna(sal_est_emp[0])
df['Salary Estimate'] = sal_est_emp[1].fillna(sal_est_glass[0])

#Drop the temporary objects
del sal_est_emp, sal_est_glass
'''


'''
Handle Hourly Salaries
'''
#create new feature to indicate hourly
df['Hourly'] = df['Salary Estimate'].apply(lambda sal: 1 if 'per hour' in sal.lower() else 0)

#Remove Per Hour from Salary Estimate
df['Salary Estimate']=df['Salary Estimate'].apply(lambda sal: sal.split('Per')[0].strip() if 'Per Hour' in sal else sal)

#Remove 'K's and '$'s and convert to integers
df['Salary Estimate'] = df['Salary Estimate'].apply(lambda sal: sal.replace('K','',3).replace('$','',3))


#Split to get min and max salaries as Integers
df['Min Salary'] = df['Salary Estimate'].apply(lambda sal: sal.split(' - ')[0] if '-' in sal else sal).astype('int32')
df['Max Salary'] = df['Salary Estimate'].apply(lambda sal: sal.split(' - ')[1] if '-' in sal else sal).astype('int32')


#Multiply Hourly Salaries to get Annual Salary
#Note that here we are using apply on a dataframe instead of a series, so the lambda will work on each row (since axis=1) instead of each cell
df['Min Salary'] = df.apply(lambda row: row['Min Salary']*1.72 if row['Hourly']==1 else row['Min Salary'], axis=1)
df['Max Salary'] = df.apply(lambda row: row['Max Salary']*1.72 if row['Hourly']==1 else row['Max Salary'], axis=1)

#Get Average Salary column and drop the Salary Estimate column
df['Average Salary'] = (df['Min Salary']+df['Max Salary'])*0.5

df=df.drop(columns='Salary Estimate')


'''
Check for Missing Values
'''
#df.isnull().sum()



'''
Check for dupliated rows
'''

#df.duplicated().value_counts()

#NOTE: 353 Rows are duplicates. Not an ideal dataset for Data Science.


'''
Group Locations
'''
#df['Location'].value_counts()


'''
Group Company Names
'''

'''
Extract information from Job Description
'''