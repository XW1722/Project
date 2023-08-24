# -*- coding: utf-8 -*-
"""
Functions and code to scrape projects from the Netherlands Organization for Scientific Research website

"""
# import necessary libraries
from bs4 import BeautifulSoup
import pandas as pd
import os
import asyncio
import aiohttp
import nest_asyncio
import time
import codecs
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
import random
import re

# define fetch and scrape functions to asynchronously scrape urls
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text(), response.status

##### NOTE: NWO website has antiscraping measures (blacklisting large request IPs) so it was necessary to use
##### proxies to avoid the rather small request quota. In this case socks5 proxies were used. 
async def scrape(urls):
    
    connectors = ["LIST_OF_PROXY_CONNECTORS"]
    
    connector = random.choice(connectors)
    print('connector No.', connectors.index(connector))
    
    tasks = []
    async with aiohttp.ClientSession(connector=connector) as session:
        for url in urls:
            tasks.append(fetch(session, url))
        htmls = await asyncio.gather(*tasks)
        return htmls
    
##############################################################################

# get_pUrls retrieves project urls from NWO project pages
def get_pUrls(url):
    
    # range of pages containing projects
    page_range = range(0, 248)
    
    # create list of page urls
    page_urls = []
    for i in page_range:
        page_urls.append(url + str(i))
        
    # initialize asyncio event loop
    loop = asyncio.get_event_loop()
    
    # slowly scarpe htmls from page urls (to avoid blacklisting)
    l_range = range(0, 24)
        
    records = []
    for i in l_range:
        floor = i*10
        records[floor:(floor+10)] = loop.run_until_complete(scrape(urls=page_urls[floor:(floor+10)]))
        print(i)
        time.sleep(3)
        
        
    records[240:248] = loop.run_until_complete(scrape(urls=page_urls[240:248]))
    
    # scrape project pages for project urls and append to list
    proj_urls = []
    for record in records:
        if record[1] == 200:
            html = record[0]
            soup = BeautifulSoup(html, 'html.parser')
            
            proj_tags = soup.find('ul', attrs={'class':'listing listing-cards'}).findAll('li', attrs={'class':'list-item reveal reveal-slideup'})

            for tag in proj_tags:
                proj_urls.append(tag.find('a').get('href'))
                
    proj_urls = ['https://www.nwo.nl' + p for p in proj_urls]
    
    return proj_urls
        
##############################################################################
# get_rawtext extracts abstracts and titles from projects htmls and saves to csv file
def get_rawtext(records):
    
    # initialize wd and data frame
    os.chdir(wd)
    
    cols = ['ProjectId', 'AbstractTitle']
     
    rows = []
    
    # go through project records a extract titles and abstracts
    for record in records:
        # check if record has html
        if record[1] == 200:
            
            html = record[0]
            soup = BeautifulSoup(html, 'html.parser')

            title = soup.find('h1', attrs={'class':'articleHead__title'}).get_text()

            abstract_el = [ tag.get_text() for tag in soup.find('div', attrs={'class':'nwo-project-summary'})]

            abstract = ''

            for element in abstract_el:
                abstract += ' ' + element
                
            AbsTitle = title + ' ' + abstract
            
            PID = ''
            
            PID_tags = soup.find('div', attrs={'class':'sidebar--content'}).findAll('p')

            for tag in PID_tags:
                if 'File number' in tag.get_text():
                    PID = tag.get_text().replace('File number', '').strip()
            
            rows.append({'ProjectId':PID, 'AbstractTitle':AbsTitle})
            
    df = pd.DataFrame(rows, columns=cols)
    
    df.to_csv('NWO_rawtext.csv', encoding='utf-8', mode='a', index=False)
            
            

##############################################################################
# get_general extracts project metadata from htmls and saves to csv file
def get_general(records):
    
    # initialize wd and dataframe
    os.chdir(wd)
    
    cols = ['ProjectId', 'Country', 'CountryFundingBody', 'FundingBody', 'LeadInstitution',
            'StartDate', 'EndDate', 'FundingAmount', 'FundingCurrency']
    rows = []
    
    # loop through records and extract project metadata from htmls
    for record in records:
        # check if record contains html
        if record[1] == 200:
            
            html = record[0]
            soup = BeautifulSoup(html, 'html.parser')
            
            side_tags = soup.find('div', attrs={'class':'sidebar--content'}).findAll('p')
            
            PID = ''
            
            for tag in side_tags:
                if 'File number' in tag.get_text():
                    PID = tag.get_text().replace('File number', '').strip()
                    
            LeadIn = ''
            for tag in side_tags:
                if 'Institution' in tag.get_text():
                    LeadIn = tag.get_text().replace('Institution', '').strip()
                    
            SD = ''
            ED = ''
            for tag in side_tags:
                if 'Duration' in tag.get_text():
                    Duration = tag.get_text().replace('Duration', '').strip()
                    Dates = Duration.split(' to')
                    SD = Dates[0].strip()
                    ED = Dates[1].strip()
                    
                    
                    
            FB = 'NWO'
            FA = 'NA'
            FC = 'NA'
            
            Country = 'Netherlands'
            CFB = 'NWO'
            
            rows.append({'ProjectId':PID, 'Country':Country, 'CountryFundingBody':CFB, 'FundingBody':FB, 
                         'LeadInstitution':LeadIn, 'StartDate':SD, 'EndDate':ED,'FundingAmount':FA,
                         'FundingCurrency':FC})
            
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv('NWO_general.csv', encoding='utf-8', mode='a', index=False)
            
            

##############################################################################

# set working direcory and NWO url
wd = "WORKING_DIRECTORY"

os.chdir(wd)

url = 'https://www.nwo.nl/en/projects?f%5B0%5D=nwo_projects_discipline%3A51477&f%5B1%5D=nwo_projects_discipline%3A51478&f%5B2%5D=nwo_projects_discipline%3A51479&f%5B3%5D=nwo_projects_discipline%3A51480&f%5B4%5D=nwo_projects_discipline%3A51504&f%5B5%5D=nwo_projects_discipline%3A51507&f%5B6%5D=nwo_projects_discipline%3A51509&f%5B7%5D=nwo_projects_discipline%3A51510&f%5B8%5D=nwo_projects_discipline%3A51511&f%5B9%5D=nwo_projects_discipline%3A51512&f%5B10%5D=nwo_projects_discipline%3A51513&f%5B11%5D=nwo_projects_discipline%3A51514&f%5B12%5D=nwo_projects_discipline%3A51515&page='

# allow nested asyncio event loops
nest_asyncio.apply()

# get project urls from project pages
p_urls = get_pUrls(url)

# initialize asyncio event loop
loop = asyncio.get_event_loop()

# scrape 50 records at a time from lower range to upper range (maximum is 118 for records 5850-5900)
r_range = range(lower, upper)

for i in r_range:
    floor = i*50
    batch = []
    batch = p_urls[(floor):(floor+50)]
    records[(floor):(floor+50)] = loop.run_until_complete(scrape(urls = batch))
    print(i)
    time.sleep(30)
    
# scrape last 40 records
records[5900:5940] = loop.run_until_complete(scrape(urls=p_urls[5900:5940]))

# extract titles and abstracts and save to csv file
get_rawtext(records)
# extract project metadata and save to csv file
get_general(records)


