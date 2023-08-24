import pandas as pd
import os
import numpy as np
import re

can = pd.read_csv('/home/flavia/Projects/Funding-Landscape/raw-data/fine-scale/Canada/NSERC/NSERC-raw-metadata.csv', encoding = 'mac_roman')

can.head()

can["CountryFundingBody"] = "NSERC"

cols = df.columns.tolist()
cols = ['ProjectId', 'Country', 'CountryFundingBody', 'FundingBody', 'LeadInstitution', 'StartDate', 'EndDate', 'FundingAmount', 'FundingCurrency']

can = can[cols]

# def find_nth(haystack, needle, n):
#     start = haystack.find(needle)
#     while start >= 0 and n > 1:
#         start = haystack.find(needle, start+len(needle))
#         n -= 1
#     return start

# can["ProjectId"] = can["ProjectId"].apply(lambda x: x[:find_nth(x, "-", 2)]+"_"+x[find_nth(x, "-", 2)+1:])
# can["ProjectId"] = can["ProjectId"].apply(lambda x: x.replace("_","-"))
# can["ProjectId"] = "NSERC-" + can["ProjectId"].astype(str) + "-" + can["StartDate"].astype(str)

can.to_csv('/home/flavia/Projects/Funding-Landscape/raw-data/fine-scale/Canada/NSERC/NSERC-raw-metadata.csv', index=False)
