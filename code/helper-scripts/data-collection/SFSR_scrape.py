# -*- coding: utf-8 -*-
"""

Code and functions for scraping projects from the Swedish Foundation for Strategic Research (SFSR)

"""

# Import all necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import asyncio
import aiohttp
import nest_asyncio
import time

# define fetch and scrape functions which asynchronously request project site htmls
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
# define get_pUrls function which acquires the urls of all listed projects
def get_pUrls(url):
    
    prop_page = requests.get(url=url)
    
    prop_page.status_code

    html = prop_page.content
    soup = BeautifulSoup(html, 'html.parser')

    prop_tags = soup.find('div', attrs={'class':'tekla--table-wrap tekla--table-wrap--sm'}).findAll('a')


    prop_urls = []
    for tag in prop_tags:
        prop_urls.append(tag.get('href'))
        
    prop_proj_urls = [p + 'project/' for p in prop_urls]
    
    loop = asyncio.get_event_loop()

    records = loop.run_until_complete(scrape(urls=prop_proj_urls))
    p_urls = []
    for record in records:
        if record[1] == 200:
            html2 = record[0]
            soup2 = BeautifulSoup(html2, 'html.parser')
            
            if soup2.find('div', attrs={'class':'tekla--table-wrap tekla--table-wrap--sm'}) != None:
                p_tags = soup2.find('div', attrs={'class':'tekla--table-wrap tekla--table-wrap--sm'}).findAll('a')
            
            for tag in p_tags:
                p_urls.append(tag.get('href'))
                
    return list(set(p_urls))

##############################################################################
# get_rawtext extracts abstracts and titles from html records scraped from project urls
def get_rawtext(records):
    
    os.chdir(wd)
        
    cols = ['ProjectId', 'AbstractTitle']
    rows = []
    
    for record in records:
        if record[1] == 200:
            html = record[0]
            soup = BeautifulSoup(html, 'html.parser')
            
            content_tag = soup.find('article', attrs={'class':'article--content'})
            
            PID = content_tag.find('dl', attrs={'class':'tekla--dl'}).findAll('dd')[0].get_text()
            
            title = content_tag.find('h1').get_text()
            
            abstract_tags = content_tag.findAll('p')
            
            abstract = ''
            
            for tag in abstract_tags:
                abstract += tag.get_text()
                
            AbsTitle = title + ' ' + abstract
            
            rows.append({'ProjectId':PID, 'AbstractTitle':AbsTitle})
            
    df = pd.DataFrame(rows, columns=cols)
    
    df.to_csv('SFSR_rawtext.csv', encoding='utf-8', mode='a', index=False)
            
            

##############################################################################
# get general extracts metadata from html records scraped from project urls
def get_general(records):
    
    os.chdir(wd)
    
    cols = ['ProjectId', 'Country', 'CountryFundingBody', 'FundingBody', 'LeadInstitution',
            'StartDate', 'EndDate', 'FundingAmount', 'FundingCurrency']
    
    rows = []
    
    for record in records:
        if record[1] == 200:
            
            html = record[0]
            soup = BeautifulSoup(html, 'html.parser')
            
            gen_tags = soup.find('dl', attrs={'class':'tekla--dl'}).findAll('dd')

            PID = gen_tags[0].get_text()

            LeadIn = gen_tags[3].get_text()

            SD = gen_tags[1].get_text().split('-')[0]
            ED = gen_tags[1].get_text().split('-')[1]

            FA = gen_tags[2].get_text().strip('SEK')
            
            rows.append({'ProjectId':PID, 'Country':'Sweden', 'CountryFundingBody':'SFSR', 'FundingBody':'SFSR', 
                         'LeadInstitution':LeadIn, 'StartDate':SD, 'EndDate':ED, 'FundingAmount':FA,
                         'FundingCurrency':'SEK'})
            
    df = pd.DataFrame(rows, columns=cols)
    
    df.to_csv('SFSR_general.csv', encoding='latin1', mode='a', index=False)
            
            

##############################################################################

wd = "WORKING_DIRECTORY"

os.chdir(wd)

# Enable nested asyncio event loops
nest_asyncio.apply()

# SFSR url containing projects
url = 'https://strategiska.se/en/research/completed-research/'

# retrieve project urls
p_urls = get_pUrls(url=url)

# initialize event loop
loop = asyncio.get_event_loop()

# fetch records from p_urls
r_range = range(0, 15)
records = []



for i in r_range:
    floor = i*100
    batch = []
    batch = p_urls[(floor):(floor+100)]
    records[(floor):(floor+100)] = loop.run_until_complete(scrape(urls = batch))
    time.sleep(1)
    
    
records[1500:1577] = loop.run_until_complete(scrape(urls=p_urls[1500:1577]))

# save project metadata to csv file
get_rawtext(records=records)

# save project text to csv file
get_general(records=records)




