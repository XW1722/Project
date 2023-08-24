import pandas as pd
import re
import numpy as np
import random
from scipy.spatial.distance import cdist

# get metadata
df_meta = pd.read_csv("./clean-data/fine-scale/STEM/project-metadata.csv", index_col = False)    
df_labels = pd.read_csv("./results/fine-scale/mallet-models/STEM/200-topic-files/1-200-keywords-labelled-new.csv")
tsne_200 = pd.read_csv("./results/fine-scale/tSNE/200-topics-TSNE_p300.csv")


#fix df_labels
tsne_200["Country"][tsne_200["Country"] == "New-Zealand"] = "New Zealand"
df_meta["Country"][df_meta["Country"] == "New-Zealand"] = "New Zealand"

#conver to lower
df_labels["Level_1_topic"] = df_labels["Level_1_topic"].str.lower()
df_labels["Level_2_topic"] = df_labels["Level_2_topic"].str.lower()
df_labels["Level_3_topic"] = df_labels["Level_3_topic"].str.lower()

#fix spelling
df_labels["Level_2_topic"][df_labels["Level_2_topic"] == "ocenography"] = "oceanography"
df_labels["Level_2_topic"][df_labels["Level_2_topic"] == "enviromental engineering"] = "environmental engineering"

#cpnvery computer science
df_labels["Level_1_topic"][df_labels["Level_2_topic"] == "computer science"] = "science"
df_labels["Level_1_topic"][df_labels["Level_1_topic"] == "science "] = "science"

# drop columns that are non-stem
to_drop = df_labels[df_labels["Level_1_topic"] == "non-stem"].index + 2
to_drop = [str(x) for x in to_drop]

to_keep = df_labels[df_labels["Level_1_topic"] != "non-stem"].index + 2
to_keep = [str(x) for x in to_keep]

tsne_200_labelled = tsne_200.drop(columns=to_drop)

# set probs bellow threshold to 0
for col in to_keep:
    tsne_200_labelled.loc[tsne_200_labelled[col] < 0.05, col] = 0.0

#divide probs by row sum - all docs have probs that sum to 1
tsne_200_labelled.loc[:,to_keep] = tsne_200_labelled.loc[:,to_keep].div(tsne_200_labelled.loc[:,to_keep].sum(axis=1), axis = 0)
#multiply by funding amount to get proportion of funding
tsne_200_labelled = tsne_200_labelled[tsne_200_labelled["3"].notnull()]

df_probs = {"ProjectId":[],"Country":[], "FundingBody":[], "LeadInstitution":[], "Topic":[], "prob":[]}

for row in tsne_200_labelled.itertuples():
    
    Amounts = list(row[3:139])
    topics = [[to_keep[i], Amounts[i]] for i,x in enumerate(Amounts) if x > 0]

    for t in topics:
       df_probs["ProjectId"].append(row[2]) 
       df_probs["Country"].append(row[140])
       df_probs["FundingBody"].append(row[142])
       df_probs["LeadInstitution"].append(row[143])
       df_probs["Topic"].append(t[0]) 
       df_probs["prob"].append(t[1]) 

df_probs = pd.DataFrame(df_probs)

# countries
# get the number of documents assign to each topic, we get half number because there are topics split in other topics
df_probs1 = df_probs.groupby(["Country","Topic"]).agg({"prob":"sum"}).reset_index()
df_probs1["Topic"] = df_probs1["Topic"].astype(int) - 2
df_probs1 = df_probs1.pivot(index = "Topic", columns = "Country", values = "prob").reset_index()
df_probs1 = df_probs1.merge(df_labels.iloc[:,0:4], on = "Topic")

df_probs1.to_csv("./results/fine-scale/distances/country-topic-sums.csv", index = False)

# institutes
df_probs1 = df_probs.query("Country == 'UK'").groupby(["LeadInstitution","Topic"]).agg({"prob":"sum"}).reset_index()
df_probs1["Topic"] = df_probs1["Topic"].astype(int) - 2
df_probs1 = df_probs1.pivot_table(index = "Topic", columns = "LeadInstitution", values = "prob").reset_index()
df_probs1 = df_probs1.merge(df_labels.iloc[:,0:4], on = "Topic")
df_probs1 = df_probs1.fillna(0)

df_probs1.to_csv("./results/fine-scale/distances/institute-topic-sums.csv", index = False)

# councils
df_probs1 = df_probs.query("Country == 'UK'").groupby(["FundingBody","Topic"]).agg({"prob":"sum"}).reset_index()
df_probs1["Topic"] = df_probs1["Topic"].astype(int) - 2
df_probs1 = df_probs1.pivot_table(index = "Topic", columns = "FundingBody", values = "prob").reset_index()
df_probs1 = df_probs1.merge(df_labels.iloc[:,0:4], on = "Topic")
df_probs1 = df_probs1.fillna(0)


df_probs1.to_csv("./results/fine-scale/distances/councils-topic-sums.csv", index = False)
