import pandas as pd
import os
import numpy as np


with open('../../supporting-files/directories-path/raw-metadata-directories.txt','r') as f:
        dirnames = f.read().splitlines()

for path in dirnames:
    print(path)
    try:
        df = pd.read_csv(path, usecols=["ProjectId", "Country", "FundingBody", "LeadInstitution", "StartDate", "EndDate", "FundingAmount", "FundingCurrency"])
    except:
        df = pd.read_csv(path, encoding='mac_roman', usecols=["ProjectId", "Country", "CountryFundingBody", "FundingBody", "LeadInstitution", "StartDate", "EndDate", "FundingAmount", "FundingCurrency"])
    else:
        country = path.split("/")[5]
        if len(path.split("/")) == 8:
            funding_body = path.split("/")[6]  
            df.to_csv(os.path.join("../../../clean-data/fine-scale/", country, funding_body, funding_body + "-project-metadata.csv"), index=False)
        else:
            df.to_csv(os.path.join("../../../clean-data/fine-scale/", country, country + "-project-metadata.csv"), index=False)


        