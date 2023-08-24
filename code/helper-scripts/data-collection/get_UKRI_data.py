# load modules/packages
import requests
import json
import pandas as pd
import time
import os

## load csv file downloaded from URKI website
project_metadata = pd.read_csv("./flavia/raw-data/fine-scale/UK/UKRI/UKRI_raw_metadata.csv")
print("data loaded")

#filter STEM funding bodies
stem = ["BBSRC","EPSRC", "NERC", "STFC", "MRC", "Innovate UK"]
project_metadata = project_metadata[project_metadata.FundingOrgName.isin(stem)]

#load existing data
existing_data = pd.read_csv("./flavia/raw-data/fine-scale/UK/UKRI/titles-abstracts.csv")
data = {"ProjectId": list(existing_data["ProjectId"]),
         "TitleAbstract":list(existing_data["TitleAbstract"])}

print('data filtered')
os.getcwd()

project_metadata.shape # 130258, 25

headers = {'Accept':'application/vnd.rcuk.gtr.json-v7'}

i = 0
for ind in project_metadata.index:
    #check if file exists to prevent extra work
    if project_metadata["ProjectId"][ind] not in data["ProjectId"]:
        print(ind)
        #request data
        r = requests.get("https://gtr.ukri.org/gtr/api/projects/" + project_metadata["ProjectId"][ind], headers = headers)
         #if request is successful
        if r.status_code == 200:
            json_r = r.json()

            data["ProjectId"].append(project_metadata["ProjectId"][ind])
            data["TitleAbstract"].append(json_r["title"] + " " + json_r["abstractText"])
           
            time.sleep(0.1)   
        
        i += 1

        if i % 100 == 0:
            print(i,"  saving")
            df = pd.DataFrame.from_dict(data)
            df.to_csv('./flavia/raw-data/fine-scale/UK/UKRI/titles-abstracts.csv')


# print("Fitting")
df = pd.DataFrame.from_dict(data)
df.to_csv('./flavia/raw-data/fine-scale/UK/UKRI/titles-abstracts.csv')
