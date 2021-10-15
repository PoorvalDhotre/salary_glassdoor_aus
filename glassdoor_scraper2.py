# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 19:21:47 2021

@author: poorv
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

def get_jobs(keyword, location, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    #driver.set_window_size(1120, 1000)


    url='https://www.glassdoor.com.au/Job/australia-data-scientist-jobs-SRCH_IL.0,9_IN16_KO10,24.htm'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.
        print('Started Main While Loop')
                   
        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.  
       
        try:
            driver.find_element_by_css_selector('[alt="Close"]').click()  #clicking to the X.
            print('Popup closed')
        except NoSuchElementException:
            #print('No Popup')
            pass
        
        
        print('Starting to go through the jobs')
        #Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("eigr9kq0")  #the class for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            print('Job Button clicked')
            time.sleep(2)            
            
            #Test for the "Sign Up" prompt and get rid of it.  
            try:
                driver.find_element_by_css_selector('[alt="Close"]').click()  #clicking to the X.
                print('Popup closed')
            except NoSuchElementException:
                print('No Popup')
                pass

            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_class_name("e1tk4kwz5").text.splitlines()[0] #the element contains both company name and rating, so converting to list and grabbing 0 index
                    location = driver.find_element_by_class_name('e1tk4kwz1').text
                    #print(location)
                    job_title = driver.find_element_by_class_name("e1tk4kwz2").text
                    #print(job_title)
                    job_description = driver.find_element_by_class_name('desc').text
                    #print(job_description)
                    collected_successfully = True
                    #print('Collected Successfully')
                except:
                    #print('Not collected Successfully. Trying again.')
                    time.sleep(5)
                    

            try:
                salary_estimate = driver.find_element_by_xpath("//div[@id='JDCol']//div//article//div//div//div//div//div//div//div//div//span[@data-test='detailSalary']").text
                print(salary_estimate)

            except NoSuchElementException:
                print('did not find salary')
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element_by_class_name("e1tk4kwz4").text
                print(rating)
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))


            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element_by_xpath('//*[@id="SerpFixedHeader"]/div/div/div[2]').click()

                try:
                    size = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[1]/span[2]').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[3]/span[2]').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[5]/span[2]').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[6]/span[2]').text
                except NoSuchElementException:
                    revenue = -1


            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
               

                
            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,})
            #add job to jobs

        #Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('//*[@id="FooterPageNav"]/div/ul/li[7]/a/span').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.