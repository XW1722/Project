# -*- coding: utf-8 -*-
"""
Functions and code to scrape Independent Research Fund Denmark website

"""

# import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import asyncio
import aiohttp
import nest_asyncio
import time
import codecs
import re

# define fetch and scrape functions to asynchronously request project htmls
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text(), response.status
    
async def scrape(urls):
    
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))
        htmls = await asyncio.gather(*tasks)
        return htmls
    
#############################################################################

# retrieve project urls from project pages
def get_pUrls(urls):
    
    pUrls = []
    
    for url in urls:
    
        r = requests.get(url)
        if r.status_code == 200:
            
            html = r.content
            soup = BeautifulSoup(html, 'html.parser')
            
            pages_tag = soup.find('nav', attrs={'class':'pagination'}).find('li', attrs={'class':'last'})
            
            pages = 0
            if pages_tag != None:
                pages = int(pages_tag.get_text())
            
            for i in range(0, pages):
                pUrls.append(url + '&b_start:int=' + str(i*10))
                
    return pUrls

#############################################################################

# get_rawtext extracts and saves project titles and abstracts in csv file
def get_rawtext(records):
    
    # initialize data frame columns and rows
    cols = ['ProjectId', 'AbstractTitle']
    
    rows = []
    
    # iterator is used to assign unique project identifier (none provided in website)
    i = 0
    
    # loop through project htmls, extract titles and abstracts, and save to csv file
    for record in records:
        if record[1] == 200:
            
            html = record[0]
            soup = BeautifulSoup(html, 'html.parser')
            
            project_tags = soup.findAll('div', attrs={'class':'result-item'})
            
            for tag in project_tags:
         
                title = tag.find('h2', attrs={'class':'result-title'}).get_text().strip()      
                
                abstract = ''
                if tag.find('div', attrs={'class':'row result-body'}) != None:
                    abstract = tag.find('div', attrs={'class':'row result-body'}).find('p').get_text().strip()
                 
                PID = i
         
                i += 1
             
                AbsTitle = title + '' + abstract
         
                rows.append({'ProjectId':PID, 'AbstractTitle':AbsTitle})
         
    df = pd.DataFrame(rows, columns=cols)
    
    df.to_csv('DFF_rawtext.csv', encoding='utf-8', mode='a', index=False)
            
#############################################################################

# get_general extracts project metadata from project htmls and saves it to csv file
def get_general(records):
    
    # initialize data frame columns and rows
    cols = ['ProjectId', 'Country', 'CountryFundingBody', 'FundingBody', 'LeadInstitution',
            'StartDate', 'EndDate', 'FundingAmount', 'FundingCurrency']
    rows = []
    
    # iterator to create project IDs
    i = 0
    
    # loop through project htmls, extract project metadata and save to csv file
    for record in records:
        if record[1] == 200:
             html = record[0]
             soup = BeautifulSoup(html, 'html.parser')
             
             project_tags = soup.findAll('div', attrs={'class':'result-item'})
             
             for tag in project_tags:
                 
                 country = 'Denmark'
                 CFB = 'DFF'
                 FB = 'DFF'
                 
                 LI = tag.find('div', attrs={'class':'col-xs-6 col-sm-12'}).get_text().split('\n')[5].strip()
                 
                 SD = tag.find('ul', attrs={'class':'listing-horizontal'}).findAll('li')[2].get_text()
                 ED = 'NA'
                 
                 FA = re.sub('[^0-9]', '', tag.find('div', attrs={'class':'col-sm-2 text-right result-amount'}).find('div', attrs={'class':'col-xs-6 col-sm-12'}).get_text())
                 FC = 'DKK'
                 
                 PID = i
                 i += 1
                 
                 rows.append({'ProjectId':PID, 'Country':country, 'CountryFundingBody':CFB, 'FundingBody':FB,
                              'LeadInstitution':LI, 'StartDate':SD, 'EndDate':ED, 'FundingAmount':FA, 'FundingCurrency':FC})
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv('DFF_general.csv', encoding='utf-8', mode='a', index=False)      
    
#############################################################################

wd = "WORKING_DIRECTORY"

os.chdir(wd)
# allow nested asyncio loops
nest_asyncio.apply()

# main urls containing projects
url_NU = 'https://dff.dk/forskningsprojekter/database?instrument:list=all&filed_method:list=methods2&period:list=all&SearchableText=' 

url_HD = 'https://dff.dk/forskningsprojekter/database?instrument:list=all&filed_method:list=sin5yd2slu&period:list=all&SearchableText='

url_Dig = 'https://dff.dk/forskningsprojekter/database?instrument:list=all&filed_method:list=en4yaaq2ke&period:list=all&SearchableText='

url_Eco = 'https://dff.dk/forskningsprojekter/database?instrument:list=all&filed_method:list=rtd5vfhdxg&period:list=all&SearchableText='

url_Clin = 'https://dff.dk/forskningsprojekter/database?instrument:list=all&filed_method:list=kmj5owptn1&period:list=all&SearchableText='

url_tech = 'https://dff.dk/forskningsprojekter/database?instrument:list=all&filed_method:list=py7wqcphvu&period:list=all&SearchableText='

mainUrls = [url_NU, url_HD, url_Dig, url_Eco, url_Clin, url_tech]

# get project urls from main urls
pUrls = get_pUrls(mainUrls)

# initialize asyncio event loop
loop = asyncio.get_event_loop()

# retrieve htmls from project urls
records = loop.run_until_complete(scrape(urls=pUrls))

# extract and save project titles and abstracts
get_rawtext(records)

# extract and save project metadata
get_general(records)

#############################################################################
