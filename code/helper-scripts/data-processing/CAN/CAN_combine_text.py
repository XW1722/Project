# Canada

import os
import pandas as pd

# concat CIHR raw text

os.chdir("/Users/flavia/Projects/Ongoing/Funding-Landscape/flavia/raw-data/fine-scale/CAN/CIHR/CIHR_rawtext")

data = {"ProjectId":[], "TitleAbstract":[]}

files = os.listdir()
len(files)

for x in files:
    # ignore hidden files
    if not x.startswith('.'):
        #open file
        with open(x, 'r', encoding='mac_roman') as text:
            id = str('CIHR-') + os.path.splitext(x)[0] 
            content = "".join(text.readlines())

            data["ProjectId"].append(id)
            data["TitleAbstract"].append(content)

df = pd.DataFrame.from_dict(data)
len(df)
os.chdir("/Users/flavia/Projects/Ongoing/Funding-Landscape/flavia/raw-data/fine-scale/CAN/CIHR")
df.to_csv('/Users/flavia/Projects/Ongoing/Funding-Landscape/flavia/raw-data/fine-scale/CAN/CIHR/CIHR-raw-text.csv', index = False)



# concat NSERC raw text

os.chdir("/Users/flavia/Projects/Ongoing/Funding-Landscape/flavia/raw-data/fine-scale/CAN/NSERC/NSERC_rawtext")

data = {"ProjectId":[], "TitleAbstract":[]}

files = os.listdir()
len(files)

for x in files:
    # ignore hidden files
    if not x.startswith('.'):
        #open file
        with open(x, 'r', encoding='mac_roman') as text:
            id = str('NSERC-') + os.path.splitext(x)[0] 
            content = "".join(text.readlines())

            data["ProjectId"].append(id)
            data["TitleAbstract"].append(content)

df = pd.DataFrame.from_dict(data)
len(df)
os.chdir("/Users/flavia/Projects/Ongoing/Funding-Landscape/flavia/raw-data/fine-scale/CAN/NSERC")
df.to_csv('/Users/flavia/Projects/Ongoing/Funding-Landscape/flavia/raw-data/fine-scale/CAN/NSERC/NSERC-raw-text.csv', index = False)
