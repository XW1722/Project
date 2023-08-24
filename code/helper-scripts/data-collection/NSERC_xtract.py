
"""
Code to scrape and parse htmls from NSERC project database. Asynchronous requests were not used on this occasion 
however the code can be easily streamlined with the inclusion of asyncio and aiohttp libraries

"""

# Import all necessary libraries
import requests
import json
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
import xml.etree.ElementTree as Xet
import pandas as pd
import os
import codecs
import io

wd = "WORKING_DIRECTORY"

os.chdir(wd)

rawtext_dir = "RAWTEXT_DIRECTORY"

# NSERC database url
url = "https://www.nserc-crsng.gc.ca/ase-oro/Details-Detailles_eng.asp?id="

# idmax is the largest Web ID for which a project record exists
idmax = 718955

# Initialize request headers
headers = CaseInsensitiveDict()
headers["Accept"] = "text/html"
headers["Content-Type"] = "application/x-www-form-urlencoded, charset=utf-8, text/html"
headers["Accept-Encoding"] = "gzip, deflate, br"

# Set some static values
Country = "Canada"
FundingBody = "NSERC"
FundingCurrency = "CAD"

# Define metadata column names
cols = ["WebID", "ProjectId", "Country", "FundingBody", "LeadUniversity", "StartDate", "EndDate", "FundingAmount", "FundingCurrency"]

# Define tag_val() function which retrieves certain fields from html
def tag_val(tag_list):
    val = []
    for tag in tag_list:
        if tag.find('strong') and tag.findNext('td'):
            val.append(tag.findNext('td').get_text())
    return val

maxId = "upper bound of Web ID range"
minId = "lower bound of Web ID range"

# Initialize rows list
rows = []

# loop through Web IDs (projects) and store metadata in data frame
for i in range(minID, maxID):
    idstr = str(i)
    
    new_url = url + idstr
    
    print(new_url)
    
    r = requests.get(url=new_url, headers=headers)
    
    print(r.status_code) 
    
    if r.status_code == 200:
        html = codecs.decode(r.content, 'utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        field_tags = soup.findAll(['td', 'strong'])
        
        va = tag_val(field_tags)
        
        ProjectID = va[0]
        LeadUni = va[4]
        StartDate = va[1]
        FundingAmount = va[7]
        
        rows.append({"WebID": idstr, "ProjectId": ProjectID, "Country": Country, "FundingBody": FundingBody,
                     "LeadUniversity": LeadUni, "StartDate": StartDate, "EndDate": "NA", 
                     "FundingAmount": FundingAmount, "FundingCurrency": FundingCurrency})
        os.chdir(wd)

df = pd.DataFrame(rows, columns=cols)
df
    

df.to_csv("./NIH_maxID-minID.csv", encoding="latin1", mode='a', index=False)


# loop through Web IDs (projects) and write abstracts and titles into text files named using WebID
for i in range(713534, 720000):
    idstr = str(i)
    
    new_url = url + idstr
    
    print(new_url)
    
    r = requests.get(url=new_url, headers=headers)
    
    
    if r.status_code == 200:
        html = codecs.decode(r.content, 'utf-8')
        soup = BeautifulSoup(html, 'html.parser')     

        h2_tags = soup.findAll(['h2'])
        
        award_tag = soup.findAll('p')
        
        h2_vals = []
        for tag in h2_tags:
            h2_vals.append(tag.get_text())
        
        title = h2_vals[3]
        
        p_vals = []
        for tag in award_tag:
            p_vals.append(tag.get_text())
        
        Abstract = p_vals[1]
        
        if title != "No title - Aucun titre":
        
            txtname = idstr + '.txt'
            
            os.chdir(rawtext_dir)
            with io.open(txtname, 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n')
                f.write(Abstract)
                


