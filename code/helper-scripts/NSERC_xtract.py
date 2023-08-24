

import requests
import json
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
import xml.etree.ElementTree as Xet
import pandas as pd
import os
import codecs
import io

wd = "C:\\Users\\micho\\OneDrive\\Documentos\\Global_Funding_Landscape\\Funding-Landscape\\Python\\NSERC"

os.chdir(wd)

rawtext_dir = "C:\\Users\\micho\\OneDrive\\Documentos\\Global_Funding_Landscape\\Funding-Landscape\\Python\\NSERC\\NSERC_rawtext"

url = "https://www.nserc-crsng.gc.ca/ase-oro/Details-Detailles_eng.asp?id="

idmax = 718955

headers = CaseInsensitiveDict()
headers["Accept"] = "text/html"
headers["Content-Type"] = "application/x-www-form-urlencoded, charset=utf-8, text/html"
headers["Accept-Encoding"] = "gzip, deflate, br"

## headers["user-key"] = "fad9adeb1b0ab60755a6eeee5720bf63"
## data = "fiscalyearfrom=2020&fiscalyearto=2020&competitionyearfrom=0&competitionyearto=0&PersonName=&KeyWords=&KeyWordsIn=&OrgType=0&AreaApplicationOther=&ResearchSubjectOther=&Department=&AwardAmountMin=&AwardAmountMax=&ResultsBy=1&button="

Country = "Canada"
FundingBody = "NSERC"
FundingCurrency = "CAD"

cols = ["WebID", "ProjectId", "Country", "FundingBody", "LeadUniversity", "StartDate", "EndDate", "FundingAmount", "FundingCurrency"]


def tag_val(tag_list):
    val = []
    for tag in tag_list:
        if tag.find('strong'):
            val.append(tag.findNext('td').get_text())
    return val

rows = []
for i in range(125000, 150000):
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
        
        txtname = ProjectID + '.txt'
        
        
        os.chdir(rawtext_dir)
        with io.open(txtname, 'w', encoding='utf-8') as f:
            f.write(title)
            f.write('\n')
            f.write(Abstract)
        
        
        rows.append({"WebID": idstr, "ProjectId": ProjectID, "Country": Country, "FundingBody": FundingBody,
                     "LeadUniversity": LeadUni, "StartDate": StartDate, "EndDate": "NA", 
                     "FundingAmount": FundingAmount, "FundingCurrency": FundingCurrency})
        os.chdir(wd)


df = pd.DataFrame(rows, columns=cols)
df.head()
    
df.to_csv("./NIH_125000-149999.csv", encoding="latin1", mode='a', index=False)




