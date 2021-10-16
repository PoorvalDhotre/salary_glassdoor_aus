# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 19:22:25 2021

@author: poorv
"""

import glassdoor_scraper as gs 
import pandas as pd 

path = r"C:\Users\poorv\Poorval\Analytics\git\salary_glassdoor_aus\chromedriver.exe"


#Enter Keyword with Hyphens
df = gs.get_jobs(800, False, path, 10)

df.to_csv('glassdoor_jobs.csv', index = False)