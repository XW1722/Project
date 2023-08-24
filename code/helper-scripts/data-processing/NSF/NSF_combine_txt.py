# NSF (USA)

import os
import glob
import pandas as pd

# concat projects metadata

os.chdir("/Users/flavia/Projects/Ongoing/Funding-Landscape/flavia/raw-data/fine-scale/USA/NSF/")

csv_files = glob.glob('*.{}'.format('csv'))
csv_files 

# concatenate all files together
df_concat = pd.concat([pd.read_csv(f) for f in csv_files ], ignore_index=True)
len(df_concat)

df_concat.to_csv('/Users/flavia/Projects/Ongoing/Funding-Landscape/flavia/raw-data/fine-scale/USA/NSF/NSF-raw-metadata.csv', index = False)


# ---------------------------------------------
# concat raw texts

os.chdir("/Users/flavia/Projects/Ongoing/Funding-Landscape/flavia/raw-data/fine-scale/USA/NSF/NSF_raw_text/")

data = {"ProjectId":[], "TitleAbstract":[]}

files = os.listdir()
len(files)

for x in files:
    if not x.startswith('.'):
        #open file
        with open(x, 'r') as text:
            id = str('NSF-') + os.path.splitext(x)[0]
            content = "".join(text.readlines())

            data["ProjectId"].append(id)
            data["TitleAbstract"].append(content)

df = pd.DataFrame.from_dict(data)
len(df)
df.to_csv('/Users/flavia/Projects/Ongoing/Funding-Landscape/flavia/raw-data/fine-scale/USA/NSF/NSF-raw-text.csv', index = False)
