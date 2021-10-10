# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 19:22:25 2021

@author: poorv
"""

import scraper2 as gs2 
import pandas as pd 

path = r"C:\Users\poorv\Poorval\Analytics\git\salary_glassdoor_aus\chromedriver.exe"


#Enter Keyword with Hyphens
df = gs2.get_jobs2('data scientist','Australia', 15, False, path, 15)

df.to_csv('glassdoor_jobs.csv', index = False)