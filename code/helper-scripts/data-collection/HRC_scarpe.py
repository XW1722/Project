# -*- coding: utf-8 -*-
"""
Functions and code for scraping projects from the New Zealand Health Research Council

"""
# import required libraries
import pandas as pd
import os
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import nest_asyncio
import re

#############################################################################
# define fetch and scrape functions for asynchronous url requests
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
# get_pUrls retrieves project urls from HRC website 
def get_pUrls(p_range, url):
    
    # initialize page and project url lists
    page_urls = []
    
    proj_urls = []
    
    # populate project page urls
    for i in p_range:
        
        page_urls.append(url + str(i))
        
    loop = asyncio.get_event_loop()
    
    # retrieve project page htmls
    records = loop.run_until_complete(scrape(urls=page_urls))
    
    # extract project urls from page htmls
    for record in records:
        if record[1] == 200:
            html = record[0]
            soup = BeautifulSoup(html, 'html.parser')
            
            proj_tags = soup.findAll('div', attrs={'class':'view-content'})

            for tag in proj_tags[0].findAll('a'):
                proj_urls.append(tag.get('href'))
            
            
        
                   
    urls = ['https://www.hrc.govt.nz' + p for p in proj_urls]
                   
    return urls
##############################################################################
# get_pHost exclusively retrieves lead research institution for each project, which had to be fetched separately
def get_pHost(p_range, url):
    
    # initialize project page and lead institution lists
    page_urls = []
    
    hosts = []
    
    # populate and retrieve project page urls
    for i in p_range:
        
        page_urls.append(url + str(i))
        
    loop = asyncio.get_event_loop()
    
    records = loop.run_until_complete(scrape(urls=page_urls))
    
    # retrieve lead institutions from project pages
    for record in records:
        if record[1] == 200:
            html = record[0]
            soup = BeautifulSoup(html, 'html.parser')
            
            proj_tags = soup.findAll('div', attrs={'class':'view-content'})[0].findAll('li')

            for tag in proj_tags:
                host = 'NA'
                host_tag = tag.find('div', attrs={'class':'slat__term field field--name-field-host field--type-entity-reference field--label-inline'})
                if host_tag != None:
                    host = host_tag.find('div', attrs={'class':'field--item'}).get_text()
                
                hosts.append(host)
            
                   
    return hosts

##############################################################################
# get_rawtext extracts and saves project titles and abstracts into a csv file
def get_rawtext(records):
    # initialize data frame
    rows = []
    
    cols = ['ProjectId', 'AbstractTitle']
    
    # initialize iterator for use as project identifier (none provided in website)
    i=0
    # loop through project records
    for record in records:
        # check if record contains html
        if record[1] == 200:
            
            # extract abstracts and titles from html and append to dataframe
            html = record[0]
            soup = BeautifulSoup(html, 'html.parser')
            
            title = soup.findAll('div', attrs={'class':'region region-pre-content'})[0].find('h1').get_text().strip()

            a_tag = soup.findAll('div', attrs={'class':'prose field field--name-body field--type-text-with-summary field--label-above'})

            abstract = ''

            if len(a_tag) > 0:            

                abstract = a_tag[0].find('div', attrs={'class':'field--item'}).get_text()
            
            AbsTitle = title + ' ' + abstract
            
            rows.append({'ProjectId':i, 'AbstractTitle':AbsTitle})
            
            i += 1
            
    df = pd.DataFrame(rows, columns=cols)
    
    df.to_csv('HRC_rawtext.csv', encoding='utf-8', mode='a', index=False)
    
##############################################################################
# get_general extracts project metadata from retrieved html records and saves them into a csv file
def get_general(records, hosts):
    
    # initialize data frame columns and rows
    rows = []
    cols = ['ProjectId', 'Country', 'CountryFundingBody', 'FundingBody', 'LeadInstitution', 
            'StartDate', 'Duration', 'FundingAmount', 'FundingCurrency']
    # initialize iterator 
    i = 0
    # loop through project records
    for record in records:
        # check if record contains html
        if record[1] == 200:
            # extract project metadata from html and append to dataframe
            html = record[0]
            soup = BeautifulSoup(html, 'html.parser')
            
            LeadIn = hosts[i]
            
            SD_tag = soup.findAll('div', attrs={'class':'field field--name-field-year field--type-integer field--label-inline'})

            SD = SD_tag[0].find('div', attrs={'class':'field--item'}).get_text()
            
            Dur_tag = soup.findAll('div', attrs={'class':'field field--name-field-duration field--type-integer field--label-inline'})
            
            Dur = 'NA'
            if len(Dur_tag) > 0:
                Dur = Dur_tag[0].find('div', attrs={'class':'field--item'}).get_text()
            
            PID = i
            
            FA_tag = soup.findAll('div', attrs={'class':'field field--name-field-approved-budget field--type-decimal field--label-inline'})
            
            FA = 'NA'
            if len(FA_tag) > 0:
                FA = re.sub('[^0-9]', '', FA_tag[0].find('div', attrs={'class':'field--item'}).get_text())
            
            rows.append({'ProjectId':PID, 'Country':'New Zealand', 'CountryFundingBody':'NA', 'FundingBody':'HRC', 
                         'LeadInstitution':LeadIn, 'StartDate':SD, 'Duration':Dur, 'FundingAmount':FA, 
                         'FundingCurrency':'NZD'})
            i += 1
            
    df = pd.DataFrame(rows, columns=cols)
    
    df.to_csv('HRC_general.csv', encoding='utf-8', mode='a', index=False)
            
        


##############################################################################
# initialize wd and url link
wd = "WORKING_DIRECTORY"

os.chdir(wd)

url = 'https://www.hrc.govt.nz/resources/research-repository?query=&page='

# define range of pages that are to be scraped
p_range = range(0, 66)

# allow nested asyncio loops
nest_asyncio.apply()

# retrieve project urls from project pages
proj_urls = get_pUrls(p_range, url)
# initialize asyncio event loop
loop = asyncio.get_event_loop()
# retrieve project html from urls
records = loop.run_until_complete(scrape(proj_urls))
# retrieve lead institution details from project pages
hosts = get_pHost(p_range, url)
# extract and save project abstracts and titles to csv file
get_rawtext(records=records)
# extract and save project metadata to csv fiel
get_general(records=records, hosts=hosts)


##############################################################################
