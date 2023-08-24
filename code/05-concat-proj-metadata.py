import pandas as pd
from collections import Counter
import re

# reads each project metadata
with open('./code/supporting-files/directories-path/project-metadata-directories.txt','r') as f:
        dirnames = f.read().splitlines()

for (i, path) in enumerate(dirnames):
    print(i, path)
    
    if i == 0:
        print(i)
        df = pd.read_csv(path, usecols=["ProjectId", "Country", "CountryFundingBody", "FundingBody", "LeadInstitution", "StartDate", "EndDate", "FundingAmount", "FundingCurrency"], dtype = {'ProjectId':str})
    
    else:
        df_2 = pd.read_csv(path, usecols=["ProjectId", "Country", "CountryFundingBody", "FundingBody", "LeadInstitution", "StartDate", "EndDate", "FundingAmount", "FundingCurrency"], dtype = {'ProjectId':str})
        df = pd.concat([df,df_2])

#cleaning funding amounts
df["FundingAmount"] = df["FundingAmount"].apply(lambda x: str(x).replace("$",""))

#remove trailing decimals / commas
r1 = re.compile("[\.\,]")

def process_number(x):
    if bool(r1.search(x)):
        sub_str = r1.split(x)
        lengths = [len(x) for x in sub_str]

        if lengths[-1] != 3:
            return("".join(sub_str[:-1]))

        return("".join(sub_str))

    return(x)

df["FundingAmount"] = df["FundingAmount"].apply(lambda x: process_number(x))

#convert to Int and remove invalid values
df["FundingAmount"] = pd.to_numeric(df["FundingAmount"], errors = 'coerce')

#sum all funding within each project ID
df = df.join(df.groupby('ProjectId')['FundingAmount'].sum(), on='ProjectId', rsuffix='_total')

#get only top funded institution in each Project ID
df = df.sort_values("FundingAmount", ascending= False).groupby('ProjectId').head(1)

#test if projectId repeats
rep_Id = df.groupby('ProjectId').size().to_frame("size").reset_index().query("size > 1")["ProjectId"]

# # put funding amount back in correct column
df["FundingAmount"] = df["FundingAmount_total"]
df = df.drop(columns = ["FundingAmount_total"])

# delete the front "UKRI-" in case the project ID doesn't match    
df['ProjectId'] = df['ProjectId'].str.replace('UKRI-', '')

#parse Time into common format

#save file
df.to_csv("./clean-data/fine-scale/STEM/project-metadata.csv", index = False)    
