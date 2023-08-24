from MulticoreTSNE import MulticoreTSNE as TSNE
import numpy as np
import pandas as pd
import seaborn as sns
import os

#read meta-data
df_meta = pd.read_csv("./clean-data/fine-scale/STEM/project-metadata.csv", index_col = False)    
for r in range(1, 4):
    print(str(r))
    for k in range(50, 401, 25):
        print(str(k) + "  loading and merging")
        #read topic probs doc for each k
        df_topics = pd.read_csv("./results/fine-scale/mallet-models/STEM/"+str(k)+"-topic-files/"+str(r)+"-"+str(k)+"-topics-doc.txt", delimiter = "\t", header = None, skiprows = [0], index_col = False)
        df_cleaned = df_topics.rename(columns={1: "ProjectId"})

        #merge files
        df_joined = df_cleaned.merge(df_meta, on= ["ProjectId"], validate= "one_to_one")

        # model = set(df_cleaned["ProjectId"])
        # meta = set(df_meta["ProjectId"])
        joined = set(df_joined["ProjectId"])


        #get np array of probs
        probs = np.array(df_cleaned[df_cleaned["ProjectId"].isin(joined)].drop(columns=["ProjectId",0]))

        for p in [5]:

            print("TSNE: " + str(p), " N Topics: " + str(k))
            tsne = TSNE(n_jobs=40, n_components=2, verbose=1, random_state=0, perplexity=p, n_iter=5000)
            tsne_fit = tsne.fit_transform(probs)

            df_joined["TSNE_1_" + str(p)] = tsne_fit[:, 0]
            df_joined["TSNE_2_" + str(p)] = tsne_fit[:, 1]


        df_joined.to_csv("./results/fine-scale/tSNE/"+str(k)+"-topics-TSNE_p300.csv", index = False)

