#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 19:34:25 2020

@author: nehaprakash
"""

import os, random, sys, time
from selenium import webdriver
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium.webdriver.common.keys import Keys
import csv

def Extract(Job_title,Job_location):
    
    try:
        os.mkdir(Job_title.replace(' ','_') + '_' + Job_location.split(',')[0].replace(' ','_'))
    except:
        print('ignore')
    
    os.chdir(Job_title.replace(' ','_') + '_' + Job_location.split(',')[0].replace(' ','_'))
    
    file_name=Job_title.replace(' ','_') + '_' + Job_location.split(',')[0].replace(' ','_').strip()+'.csv'
    fw=open(file_name,'w',encoding='utf8') # output file
    writer=csv.writer(fw,lineterminator='\n')

    driver=webdriver.Chrome('/Users/nehaprakash/Documents/BIA 660-B/chromedriver')
    url = 'https://www.indeed.com/'
    driver.get(url)

    search_job = driver.find_element_by_xpath('//*[@id="text-input-what"]')
    #search_job = driver.find_element_by_xpath('//*[@id="what"]')
    search_job.send_keys(Keys.COMMAND, 'a')
    search_job.send_keys(Keys.BACKSPACE)
    search_job.send_keys([Job_title])
    search_location = driver.find_element_by_xpath('//*[@id="text-input-where"]')
    #search_location = driver.find_element_by_xpath('//*[@id="where"]')
    search_location.send_keys(Keys.COMMAND, 'a')
    search_location.send_keys(Keys.BACKSPACE)
    search_location.send_keys([Job_location])
    
    try:
        initial_search_button = driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button')
        initial_search_button.click()
    except:
        print('handling exception')
        
    try:
        close_popup = driver.find_element_by_id("popover-close-link")
        close_popup.click()
    except:
        print("No Popup")
    
    links=[]
    for i in range(0,15):  #change range as per ur convenience
        job_card = driver.find_elements_by_xpath('//div[contains(@class,"clickcard")]') # every page(40 pages)
        
        counter=0
        for job in job_card: #(every link/job ad in that specific page(15 links per page))
            link = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name='href')
#            print (link)
            links.append(link+'\n')
            counter=counter+1
#        print(counter)
    print("Page: {}".format(str(i+1)))
    x=len(links)
    print ('Number of links:',x)
    
    titles=[]
    descriptions=[]
    title,description='NA','NA'
   
    counter=0
    for link in links:
        try:
            driver.get(link)
            description = driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text
 #           print(description)
            descriptions.append(description)
            title = driver.find_element_by_xpath('//div[contains(@class, "jobsearch")]//h1').text
 #           print(title)
            titles.append(title)
        except:
            print('Description missing')
            
        writer.writerow([description,title])
        Job_Ad_html = Job_title.replace(' ','_') + '_' + Job_location.split(',')[0].replace(' ','_').strip() + '_' + str(counter) + '.html'        
        with open(Job_Ad_html,"w",encoding='utf8') as f:
            f.write(driver.page_source)    
            counter = counter + 1
            time.sleep(2)
            
    fw.close()
    
    os.chdir('../')

    return    

Input_File = open('cities.txt', 'r')
Lines = Input_File.readlines()
for line in Lines:
    Extract(line.split(';')[0],line.split(';')[1])
#    print(line.split(';')[0],line.split(';')[1])
