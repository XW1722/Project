__author__ = "Xuan Wang"
__date__ = "07 Jul 2024"
__contact__ = "xuan.wang22@imperial.ac.uk"


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu

# load the csvs
df_2015 = pd.read_csv('./results/subject-result/2015-class.csv')
df_2016 = pd.read_csv('./results/subject-result/2016-class.csv')
df_2017 = pd.read_csv('./results/subject-result/2017-class.csv')
df_2018 = pd.read_csv('./results/subject-result/2018-class.csv')
df_2019 = pd.read_csv('./results/subject-result/2019-class.csv')
df_2020 = pd.read_csv('./results/subject-result/2020-class.csv')
df_2021 = pd.read_csv('./results/subject-result/2021-class.csv')
df_2022 = pd.read_csv('./results/subject-result/2022-class.csv')

# add a column of the year
df_2015["Year"] = 2015
df_2016["Year"] = 2016
df_2017["Year"] = 2017
df_2018["Year"] = 2018
df_2019["Year"] = 2019
df_2020["Year"] = 2020
df_2021["Year"] = 2021
df_2022["Year"] = 2022

# Combine all DataFrames into one
data = pd.concat([df_2015, df_2016, df_2017, df_2018, df_2019, df_2020, df_2021, df_2022])

data.to_csv('./results/subject-result/dist-class.csv')


plt.tight_layout()
plt.show()




results
