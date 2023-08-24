# UKRI

import os
import re
import pandas as pd

os.chdir("/Users/flavia/OneDrive - Imperial College London/Funding-Landscape/raw-data/fine-scale/UK/UKRI")

data = {"ProjectId":[], "TitleAbstract":[]}

files = os.listdir()
for x in files:
    if not x.startswith('.'):
        #open file
        with open(x, 'r') as text:
            id = str('UKRI-') + os.path.splitext(x)[0]
            content = "".join(text.readlines())

            data["ProjectId"].append(id)
            data["TitleAbstract"].append(content)

df = pd.DataFrame.from_dict(data)
df.to_csv('/Users/flavia/Projects/Ongoing/Funding-Landscape/flavia/raw-data/fine-scale/UK/UKRI/UKRI-raw-text.csv', index = False)

