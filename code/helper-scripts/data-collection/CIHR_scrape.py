# -*- coding: utf-8 -*-
"""

Code to scrape CIHR and medical funding grants from their online dataabse 


"""
# Import ilbraries
import io
import asyncio
import aiohttp
from aiohttp import ClientSession, ClientConnectorError
import nest_asyncio
from bs4 import BeautifulSoup
import os
import time
import json
import pandas as pd
import numpy
import re
import codecs

##############################################################################  
# aiohttp fetch function for asynchronous scraping
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text(), response.status
    
##############################################################################  
# scrape function fetches a set of urls defined buy range(lower, upper)
async def scrape(lower, upper):
    
    # initialize urls list
    urls = []
    
    # spcify CIHR webapp and desired response format
    Search_url = "https://webapps.cihr-irsc.gc.ca/decisions/sq?q=id:"
    response_format = "&version=2.2&start=0&rows=50&indent=on&wt=json"
    
    
    # populate urls list 
    rng = range(lower, upper)
    
    for i in rng:
        idstr = str(i)
        
        new_url = Search_url + idstr + response_format
        urls.append(new_url)
    
    # create and gather tasks to fetch urls asynchronously
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))
        htmls = await asyncio.gather(*tasks)
        return htmls
##############################################################################    
# Takes list of fetched htmls and extracts project metadata into a csv file
def record_to_csv(min, max, data):
    
    records = range(0, max-min)
    
    cols = ["ProjectID", "Country", "FundingBody", "LeadUniversity",
            "StartDate", "Duration", "FundingAmount", "FundingCurrency"]

    rows = []
    
    for record in records:
        
        jdata = json.loads(data[record][0])

        field_dict = jdata['response']
        
        if field_dict['numFound'] != 0:

            true_dict = field_dict['docs'][0]

            ID = true_dict['id']

            Country = true_dict['country'][0]

            FundingBody = 'CIHR'

            LeadUni = true_dict['orgname'][0]

            StartDate = true_dict['competitiondate'][0:4]

            Duration = true_dict['approvedterm2'][0]

            FundingAmount = true_dict['cihramount'][0]

            FundingAmount = int(re.sub(r'[^0-9]', '', FundingAmount))

            rows.append({"ProjectID": ID, "Country": Country, "FundingBody": FundingBody,
                         "LeadUniversity": LeadUni, "StartDate": StartDate, "Duration": Duration, 
                         "FundingAmount": FundingAmount, "FundingCurrency": 'CAD'})

    df = pd.DataFrame(rows, columns=cols)
    
    os.chdir(wd)
    
    csv_name = str(min) + '-' + str(max) + '.csv'

    df.to_csv(csv_name, encoding='latin1', mode='a', index=False)

##############################################################################  
# takes list of fetched htmls and extracts abstracts and titles, saving them in text files    
def record_to_text(min, max, data):
    
    records = range(0, max-min)
   
    for record in records:
        
        jdata = json.loads(results[record][0])
        
        field_dict = jdata['response']
        
        if field_dict['numFound'] != 0:
            
            true_dict = field_dict['docs'][0]
            
            if 'abstract' in true_dict:
            
                ID = true_dict['id']
            
                title = true_dict['projecttitle'][0]
            
                abstract = true_dict['abstract'][0]
            
                if title != "No title - Aucun titre":
            
                    txtname = ID + '.txt'
                
                    os.chdir(rawtext_dir)
                    with io.open(txtname, 'w', encoding='utf-8') as f:
                        f.write(title)
                        f.write('\n')
                        f.write(abstract)
    
    
############################################################################################

wd = "WORKING_DIRECTOY"

rawtext_dir = "RAWTEXT_DIRECTORY"

os.chdir(wd)

# allow nested asyncio loops
nest_asyncio.apply()

# initialize event loop
loop = asyncio.get_event_loop()

# max project range is 600000

upper = 'upper_range'
lower = 'lower_range'

# scrape projects within range
results = loop.run_until_complete(scrape(lower, upper))

# save metadata to csv
record_to_csv(min=lower, max=upper, data=results)

# save rawtext to text files
record_to_text(min=lower, max=upper, data=results)






