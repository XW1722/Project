# -*- coding: utf-8 -*-
"""
Functions and code to scrape projects from the Australian Centre for International Agricultural Research (ACIAR)

"""
# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import asyncio
import aiohttp
import nest_asyncio
import re

# Define fetch and scrape functions to asynchronously scrape html from a given set of urls
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
# get_pUrls retreives available project page urls for scraping
def get_pUrls(p_range, url):
    
    # initialize project url list
    proj_urls = []
    
    # loop through project pages
    for i in page_range:
        
        # make request to project page url
        page_url = url + str(i)
        
        r = requests.get(page_url)
        
        # check if request was successful
        if r.status_code == 200:
          
            html = r.content
            soup = BeautifulSoup(html, 'html.parser')

            # find all projects on page
            proj_tags = soup.findAll('div', attrs={'class':'views-row field__item'})
            
            # loop through project tags and append url to list
            for tag in proj_tags:
                if tag.find('a', {'href':True}) != None:
                   proj_urls.append(tag.find('a').get('href'))
       
    # create list with full urls
    urls = ['https://www.aciar.gov.au' + p for p in proj_urls]
                   
    return urls

##############################################################################
# get_AbsTitles extracts projects titles and abstracts from scraped htmls and saves them in csv file 
def get_AbsTitles(records):
    
    # initialize data frame columns and rows
    cols = ['ProjectId', 'AbstractTitle']
    
    rows = []
    
    os.chdir(wd)
    
    # loop through scraped project htmls
    for record in records:
        # check if html is available for a given record
        if record[1] == 200:
            
            # find, extract and append titles and abstracts to data frame
            html = record[0]
            soup = BeautifulSoup(html, 'html.parser')

            t_tags = soup.findAll('div', attrs={'class':'view-content field__items'})

            for tag in t_tags:
                if tag.find('h1') != None:
                    title = tag.get_text().strip()
                    
            a_tags = soup.findAll('div', attrs={'class':'project-page-content'})

            abstract = a_tags[0].find('div', attrs={'class':'col-right'}).get_text()
            
            AbsTitle = title + ' ' + abstract
            
            id_tags = soup.findAll('div', attrs={'class':'project-page-below-banner'})[0].find('div', attrs={'class':'field field--name-field-project-code field--type-string field--label-inline'})

            PID = id_tags.find('div', attrs={'class':'field__item'}).get_text().strip()
            
            rows.append({'ProjectId':PID, 'AbstractTitle':AbsTitle})
            
    df = pd.DataFrame(rows, columns=cols)
    
    df.to_csv('ACIAR_rawtext.csv', encoding='utf-8', mode='a', index=False)
    
    
##############################################################################
# get_general retrieves project metadata from project htmls and saves them to a csv file
def get_general(records):
     
    # initialize wd, data frame columns and rows
    os.chdir(wd)
    cols = ['ProjectId', 'Program', 'Country', 'CountryFundingBody', 'FundingBody', 'LeadInstitution',
            'StartDate', 'EndDate', 'FundingAmount', 'FundingCurrency']
    
    rows = []
    
    # loop through scraped project htmls
    for record in records:
        # check if html is available for record
        if record[1] == 200:
            
            # find, extract and append metadata fields to data frame
            html = record[0]
            soup = BeautifulSoup(html, 'html.parser')
            
            banner_tags = soup.findAll('div', attrs={'class':'project-page-below-banner'})[0] 
            
            id_tags = banner_tags.find('div', attrs={'class':'field field--name-field-project-code field--type-string field--label-inline'})

            PID = id_tags.find('div', attrs={'class':'field__item'}).get_text().strip()

            proj_tag = banner_tags.find('div', attrs={'class':'field field--name-field-program field--type-entity-reference field--label-inline'})

            Proj = proj_tag.find('div', attrs={'class':'field__item'}).get_text().strip()

            Bud_tag = banner_tags.find('div', attrs={'class':'field field--name-field-budget field--type-decimal field--label-inline'})

            FundingAmount = re.sub('[^0-9]', '', Bud_tag.find('div', attrs={'class':'field__item'}).get_text())

            CO_tag = banner_tags.find('div', attrs={'class':'field field--name-field-commissioned-organisation field--type-entity-reference field--label-inline'})
            
            LeadUni = 'NA'
            
            if CO_tag != None:
                LeadUni = CO_tag.find('div', attrs={'class':'field__item'}).get_text().strip()

            date_tags = banner_tags.find('div', attrs={'class':'date'})

            StartDate = date_tags.find('div', attrs={'class':'start'}).get_text()

            EndDate = date_tags.find('div', attrs={'class':'end'}).get_text()
            
            rows.append({'ProjectId':PID, 'Program':Proj, 'Country':'Australia', 'CountryFundingBody':'NA', 'FundingBody':'ACIAR',
                         'LeadInstitution':LeadUni, 'StartDate':StartDate, 'EndDate':EndDate,
                         'FundingAmount':FundingAmount, 'FundingCurrency':'AUD'}) 
            
    df = pd.DataFrame(rows, columns=cols)
    
    df.to_csv('ACIAR_general.csv', encoding='utf-8', mode='a', index=False)
    
   

##############################################################################


##############################################################################

url = 'https://www.aciar.gov.au/project?search_api_fulltext=&page='

wd = "WORKING_DIRECTORY"

# range of pages with scrapable projects
page_range = range(0, 64)
    
# retrieve project urls from pages   
p_urls = get_pUrls(page_range, url=url)

# allow nested asyncio loops
nest_asyncio.apply()

# initialize event loop
loop = asyncio.get_event_loop()

# retrieve htmls from project urls
records = loop.run_until_complete(scrape(urls=p_urls))

# extract and write abstracts and titles
get_AbsTitles(records)

# extract and write project metadata
get_general(records)
