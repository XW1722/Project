import pandas as pd
import re
import numpy as np
import random
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

# get metadata
df_meta = pd.read_csv("./clean-data/fine-scale/STEM/project-metadata.csv", index_col = False)    
# delete the front "UKRI-" in case the project ID doesn't match    
df_meta['ProjectId'] = df_meta['ProjectId'].str.replace('UKRI-', '')

k = 200
#read topic probs (100 topics)
df_topics = pd.read_csv("./results/fine-scale/mallet-models/STEM/"+str(k)+"-topic-files/1-"+str(k)+"-topics-doc.txt", delimiter = "\t", header = None, skiprows = [0], index_col = 0)
df_cleaned = df_topics.rename(columns={1: "ProjectId"})

#merge files
df_joined = df_cleaned.merge(df_meta, on= ["ProjectId"], validate= "one_to_one")

#filter to russel group
russell_group = ["University of Birmingham", "University of Bristol", "University of Cambridge", "Cardiff University", "Durham University", "University of Edinburgh", "University of Exeter", 
"University of Glasgow", "Imperial College London", "King's College London", "University of Leeds", "University of Liverpool", 
"University of Manchester", "Newcastle University", "University of Nottingham", "University of Oxford", "Queen Mary University of London", "Queen’s University Belfast", "University of Sheffield", 
"University of Southampton", "University College London", "University of Warwick", "University of York"]

df_joined = df_joined[df_joined["LeadInstitution"].isin(russell_group)]

#remove topics
to_remove = [16,25,53,55, 185]
df_joined.loc[:, to_remove] = 0.0

#find topic max
df_joined["Topic"] = df_joined.iloc[:, range(1,201)].idxmax(axis = "columns")

#get country-topic matrix
df_summary = df_joined.groupby(['LeadInstitution', 'Topic']).size().unstack().fillna(0)

df_summary[to_remove] = 0.0
df_summary = df_summary[[i for i in range(2,202)]]

#calculate cosine dist
df_dist = pd.DataFrame(
    squareform(pdist(df_summary, metric='cosine')),
    columns = df_summary.index,
    index = df_summary.index
)

df_dist.to_csv("./results/fine-scale/distances/uni-topic-dist.csv")
df_summary.to_csv("./results/fine-scale/distances/uni-topic-summary.csv")

