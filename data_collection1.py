# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 17:56:29 2021

@author: poorv
"""

import glassdoor_scraper as gs 
import pandas as pd 

path = r"C:\Users\poorv\Poorval\Analytics\git\salary_glassdoor_aus\chromedriver.exe"


#Enter Keyword with Hyphens
df = gs.get_jobs('data-scientist',15, False, path, 15)

df.to_csv('glassdoor_jobs.csv', index = False)