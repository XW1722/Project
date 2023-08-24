# load modules/packages
import requests
import json
import pandas as pd
import time
import os

## load csv file downloaded from URKI website
project_metadata = pd.read_csv("./raw-data/fine-scale/UK/UKRI/UKRI_raw_metadata.csv")
print("data loaded")
data = project_metadata
# filter projects by research grant and fellowships
# data = project_metadata[project_metadata.ProjectCategory.isin(["Research Grant", "Fellowship"])]
#filter STEM funding bodies
stem = ["BBSRC","EPSRC", "NERC", "STFC", "MRC", "Innovate UK"]
data = data[data.FundingOrgName.isin(stem)]

print('data filtered')
os.getcwd()

data.shape # 63963, 25
project_metadata.shape # 130258, 25

headers = {'Accept':'application/vnd.rcuk.gtr.json-v7'}

for ind in data.index:
    #check if file exists to prevent extra work
    if (data["ProjectId"][ind]+'.txt') not in os.listdir('/Users/flavia/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Funding-Landscape/raw-data/fine-scale/UK/UKRI/titles-abstracts/'):
        print(ind)
        #request data
        r = requests.get("https://gtr.ukri.org/gtr/api/projects/" + data["ProjectId"][ind], headers = headers)
         #if request is successful
        if r.status_code == 200:
            json_r = r.json()
            with open('/Users/flavia/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Funding-Landscape/raw-data/fine-scale/UK/UKRI/titles-abstracts/'+ data["ProjectId"][ind]+'.txt', 'w') as f:
                f.write(json_r["title"] + " " + json_r["abstractText"])
            
            time.sleep(0.5)    



    
    


    
