import umap
from umap.umap_ import nearest_neighbors

import numpy as np
import pandas as pd
import seaborn as sns
import os
import numba

numba.set_num_threads(10)
print("cores:" + str(numba.get_num_threads()))

#read meta-data
df_meta = pd.read_csv("./clean-data/fine-scale/STEM/project-metadata.csv", index_col = False)
# delete the front "UKRI-" in case the project ID doesn't match    
df_meta['ProjectId'] = df_meta['ProjectId'].str.replace('UKRI-', '')


for k in [50]:
    print(str(k) + "  loading and merging")
    #read topic probs (100 topics)
    df_topics = pd.read_csv("./results/fine-scale/mallet-models/STEM/"+str(k)+"-topic-files/1-"+str(k)+"-topics-doc.txt", delimiter = "\t", header = None, skiprows = [0], index_col = False)
    df_cleaned = df_topics.rename(columns={1: "ProjectId"})

    #merge files
    df_joined = df_cleaned.merge(df_meta, on= ["ProjectId"], validate= "one_to_one")

    # model = set(df_cleaned["ProjectId"])
    # meta = set(df_meta["ProjectId"])
    joined = set(df_joined["ProjectId"])

    #get np array of probs
    probs = np.array(df_cleaned[df_cleaned["ProjectId"].isin(joined)].drop(columns=["ProjectId",0]))
    
    print("Precomputing nearest neighbour \n")
    #precompute nearest_neighbors
    mnist_knn = nearest_neighbors(probs,
                              n_neighbors=200,
                              metric="euclidean",
                              metric_kwds=None,
                              angular=False,
                              random_state=None,
                              verbose = True
                             )


    for p in [50, 75, 100, 150, 200]:
        
        print("UMAP: " + str(p), " N Topics: " + str(k))
        umap_model = umap.UMAP(n_neighbors= p, min_dist = 0.2, n_components = 2, metric = 'euclidean', verbose=True, precomputed_knn=mnist_knn)
        umap_fit = umap_model.fit_transform(probs)

        df_joined["UMAP_1_" + str(p)] = umap_fit[:, 0]
        df_joined["UMAP_2_" + str(p)] = umap_fit[:, 1]

    # print("umap: " + str(50), " N Topics: " + str(k))
    # umap = umap(n_jobs=40, n_components=2, verbose=1, random_state=0,perplexity=50)
    # umap_fit = umap.fit_transform(probs)

    # df_joined["umap_1_" + str(50)] = umap_fit[:, 0]
    # df_joined["umap_2_" + str(50)] = umap_fit[:, 1]

    df_joined.to_csv("./results/fine-scale/umap/"+str(k)+"-topics-umap.csv", index = False)

