import pandas as pd

text = pd.read_csv("/home/flavia/Projects/Funding-Landscape/raw-data/fine-scale/UK/UKRI/titles-abstracts.csv", index_col=False)
metadata = pd.read_csv("/home/flavia/Projects/Funding-Landscape/raw-data/fine-scale/UK/UKRI/UKRI-raw-metadata.csv", index_col=False)

text.head()
text = text.drop(['Unnamed: 0'],axis=1)
text.columns

metadata.head()
metadata.columns

df = pd.merge(text, metadata, on = "ProjectId")
df.columns

len(df) - len(df.query("FundingOrgName == 'MRC'"))
len(df.query("FundingOrgName == 'MRC'"))

df_cleaned = df.loc[df["FundingOrgName"]!='MRC']
len(df_cleaned)

df_cleaned.to_csv("/home/flavia/Projects/Funding-Landscape/raw-data/fine-scale/UK/UKRI/titles-abstracts.csv")