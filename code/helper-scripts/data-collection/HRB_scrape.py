# -*- coding: utf-8 -*-
"""

Functions and code to scrape projects from the Health Research Board, Ireland

"""
# import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import asyncio
import aiohttp
import nest_asyncio
import re

#############################################################################
# define fetch and scrape functions to asynchronously scrape project urls
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

##############################################################################
# get_awardUrls retrieves available project urls from HRB awards pages
def get_awardUrls(url):
    
    r = requests.get(url=url)
    
    if r.status_code == 200:
        
        html = r.content
        soup = BeautifulSoup(html, 'html.parser')
        field_tags = soup.findAll(['li'])
        
        p_range = range(127, 839)

        p_urls = []

        for p in p_range:
            if field_tags[p].find('a', {'href':True}) != None:
                p_urls.append(field_tags[p].find('a').get('href'))
                
        urls = ['https://www.hrb.ie/' + p for p in p_urls]
        
        return urls
##############################################################################        
# get_abstitles extracts and saves abstracts and titles from project htmls 
def get_abstitles(records):
    
    # initialize wd and data frame fields
    os.chdir(wd)
    cols = ['ProjectId', 'AbstractTitle']
    
    rows = []
    
    # initialize iterator to assing unique projects identifiers (not provieded by website)
    i = 0
    
    # loop through scraped project urls
    for record in records:
        # check ifrecord contains html
        if record[1] == 200:
            
            # find and append titles and abstracts 
            html=record[0]
            soup = BeautifulSoup(html, 'html.parser')

            text_tags = soup.find('div', attrs={'class':'col-md-8'})

            title = text_tags.find('h1').get_text().strip()

            abstract_tags = text_tags.findAll('p')

            abstract = ''

            for tag in abstract_tags:
                print(tag)
                abstract = abstract + tag.get_text() + '\n'
                
            AbsTitle = title + ' ' + abstract
            
            rows.append({'ProjectId':i, 'AbstractTitle':AbsTitle})
            
            i += 1
            
    df = pd.DataFrame(rows, columns=cols)
        
    df.to_csv('HRB_rawtext.csv', encoding='utf-8', mode='a', index=False)
    
############################################################################## 
# get_general extracts and saves project metadata to csv file
def get_general(records):
    
    # initialize wd and data frame fields
    os.chdir(wd)
    cols = ['ProjectId', 'Country', 'CountryFundingBody', 'FundingBody', 'LeadInstitution',
            'StartDate', 'EndDate', 'FundingAmount', 'FundingCurrency']
    
    rows = []
    
    # initialize PID iterator
    i = 0
    
    # loop through records
    for record in records:
        # check if record has html
        if record[1] == 200:
            # find and append metadata fields to data frame
            html=record[0]
            soup = BeautifulSoup(html, 'html.parser')
            
            general_tags = soup.find('div', attrs={'class':'col-md-4'}).findAll('dd')
            
            SDate = general_tags[0].get_text().strip()
            FAmount = re.sub('[^0-9]', '', general_tags[1].get_text())
            LIn = general_tags[3].get_text()
            Country = 'Ireland'
            CFB = 'NA'
            EDate = 'NA'
            FCurrency = 'EUR'
            FB = 'HRB'
            
            rows.append({'ProjectId':i, 'Country':Country, 'CountryFundingBody':CFB, 'FundingBody':FB, 
                         'LeadInstitution':LIn, 'StartDate':SDate, 'EndDate':EDate, 'FundingAmount':FAmount,
                         'FundingCurrency':FCurrency})
        i += 1
        
    df = pd.DataFrame(rows, columns=cols)
    
    df.to_csv('HRB_general.csv', encoding='utf-8', mode='a', index=False)
            
            
        
        
##############################################################################          
        
    

url = "https://www.hrb.ie/funding/approved-awards/awards-approved/"

wd = "WORKING_DIRECTORY"

######################################################################################################################

# allow nested asyncio event loops
nest_asyncio.apply()

# retrieve project urls
urls = get_awardUrls(url)

# initialize asyncio event loop
loop = asyncio.get_event_loop()

# retrieve htmls from project urls
records = loop.run_until_complete(scrape(urls=urls))

# extract and save abstracts and titles 
get_abstitles(records)
# extract and save metadata
get_general(records)
