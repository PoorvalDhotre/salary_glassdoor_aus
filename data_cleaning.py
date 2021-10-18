# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 14:04:03 2021

@author: poorv
"""

import pandas as pd

df = pd.read_csv('glassdoor_jobs.csv')



#job description - Tools, buzzwords, big data tools, cloud, PhD
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

#Drop the instrumental objects
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

#NOTE: 353 Rows are duplicates. Not an ideal dataset for Data Science but we will use for this project.


'''
Group Locations
'''
#df['Location'].value_counts()

#define tuples (since you cannot use a list as a key in dictionaries) to group together related suburbs 
syd_sub = tuple(['sydney', 'bella vista', 'parramatta', 'liverpool', 'alexandria', 'mascot', 'auburn'])
mel_sub = tuple(['melbourne', 'frankston','docklands', 'melton'])
other = tuple(['bunbury', 'darwin', 'bathurst', 'wollongong', 'gold coast'])

#Define dictionary
group_locations = {syd_sub:'Sydney',mel_sub:'Melbourne', other:'Other'}

#Define a function to check dictionary and assign value
#Note: we unpack the dictionary using .items() if we want to acces both key and val. otherwise a for loop will iterate over the keys by default
def loc_simplify(location):
    for key,val in group_locations.items():
        if location.lower().strip() in key:
            location = val    
    return location

#Map the fucntion over every value in the series using the apply method
df['Location'] = df['Location'].apply(loc_simplify)

#delete instrumental objects
del group_locations, mel_sub, other, syd_sub



'''
New feature: Seniority
'''

senior = ['senior', 'lead', 'principal', 'head']
junior = ['junior', 'entry level', 'graduate']

df['Seniority']=df['Job Title'].apply(lambda title: 'Senior' if any([x for x in senior if x in title.lower()]) else ('Junior' if any([x for x in junior if x in title.lower()]) else 'Mid'))


del senior, junior

#df['Seniority'].value_counts()



'''
New Feature: Job Function - Analyst vs Scientist
'''
#df['Job Title'].value_counts()

#New Feature: Job Function - Analyst vs Scientist
scientist = ['scientist', 'science', 'machine learning']

df['Job Function'] = df['Job Title'].apply(lambda title: 'Scientist' if any([x for x in scientist if x in title.lower()]) else 'Analyst')

del scientist



'''
Group Company Names
'''
#Group the company names that occur less than four times into Other group
val_counts=df['Company Name'].value_counts()

#creating a list of companies where count<4
other=list(val_counts.apply(lambda count: count if count<4 else None).dropna().index)

#Grouping companies in the other list into a category
df['Company Name']=df['Company Name'].apply(lambda name: 'Other' if name in other else name)    

#deleting instrumental columns
del other, val_counts


'''
Combine -1 and Unknown in Size
'''
#df['Size'].value_counts()

df['Size'].replace('-1','Unknown', inplace=True) 
#Using Pandas replace since replacing the whole value of the cell. If want to replace only part of it, need to use the standard library replace with a lambda fucntion (as we did to remove 'K' and '$')

'''
Clean up the mismatched data between Founded, Ownership, Industry, Sector, Revenue
'''
#Moving from Sector to Revenue
#df['Sector'].value_counts()

#defining a list of values to be moved from sector to revenue
sec_to_rev = ['$1 to $2 billion (USD)', '$500 million to $1 billion (USD)','$2 to $5 billion (USD)', '$5 to $10 million (USD)', '$10+ billion (USD)']

#creating a dataframe to check if the wrong values are just stray or are to be transferred to revenue column
wrong_sector=df[df['Sector'].isin(sec_to_rev)]

#Updating Revenue and deleting from Sector
df['Revenue'] = df.apply(lambda row: row['Sector'] if row['Sector'] in sec_to_rev else row['Revenue'], axis=1)
df['Sector'].replace(sec_to_rev, 'Unknown', inplace = True)

del wrong_sector, sec_to_rev


#Moving from Ownership to Revenue
#df['Type of ownership'].value_counts()

df['Revenue'] = df.apply(lambda row: row['Type of ownership'] if row['Type of ownership'] =='$50 to $100 million (USD)' else row['Revenue'], axis=1)
df['Type of ownership'].replace('$50 to $100 million (USD)', 'Unknown', inplace = True)


#Moving from Ownership to Industry
#df['Type of ownership'].value_counts()

own_to_ind = ['Government', 'College / University', 'Express Delivery Service', 'Hospital', 'Food & Drink Manufacturing', 'Consulting', 'Regional Agencies', 'Utilities', 'Telecommunications Service']

df['Industry'] = df.apply(lambda row: row['Type of ownership'] if row['Type of ownership'] in own_to_ind else row['Industry'], axis=1)
df['Type of ownership'].replace(own_to_ind, 'Unknown', inplace = True)

del own_to_ind


#Moving from Founded to 'Type of ownership'
#df['Founded'].value_counts()

found_to_own = ['College / University', 'Company - Private', 'Non-profit Organisation', 'Company - Public']

wrong_found=df[df['Founded'].isin(found_to_own)]

df['Type of ownership'] = df.apply(lambda row: row['Founded'] if row['Founded'] in found_to_own else row['Type of ownership'], axis=1)
df['Founded'].replace(found_to_own, 'Unknown', inplace = True)

del found_to_own,wrong_found


#Moving from Founded to Industry and Sector

df['Sector'] = df.apply(lambda row: row['Founded'] if row['Founded'] == 'Government' else row['Sector'], axis=1)
df['Industry'] = df.apply(lambda row: row['Founded'] if row['Founded'] == 'Government' else row['Industry'], axis=1)
df['Founded'].replace('Government', 'Unknown', inplace = True)




'''
Grouping together categories
'''
#Creating Others Categories in Industry and Sector



#df['Industry'].value_counts()

#Combine -1 and Unknown in Type of Owndership, Revenue, Founded, Industry, Sector




'''
Get company age from Founded
'''
# from datetime import datetime

# df['Company Age'] = datetime.now().year - df['Founded'].astype('int32')



'''
Extract information from Job Description

'''

