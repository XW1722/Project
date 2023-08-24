"""
This script performs the Wilcoxon hypothesis test, and checks whether there is a gender bias across time.
"""

__author__ = "Xuan Wang"
__contact__ = "xuan.wang22@imperial.ac.uk"
__date__ = "21 Jul 2023"

# import packages
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import wilcoxon
# load packages
ratio_2015 = pd.read_csv('./results/total_ratio/2015_ratio.csv', index_col= 0)
ratio_2016 = pd.read_csv('./results/total_ratio/2016_ratio.csv', index_col= 0)
ratio_2017 = pd.read_csv('./results/total_ratio/2017_ratio.csv', index_col= 0)
ratio_2018 = pd.read_csv('./results/total_ratio/2018_ratio.csv', index_col= 0)
ratio_2019 = pd.read_csv('./results/total_ratio/2019_ratio.csv', index_col= 0)
ratio_2020 = pd.read_csv('./results/total_ratio/2020_ratio.csv', index_col= 0)
ratio_2021 = pd.read_csv('./results/total_ratio/2021_ratio.csv', index_col= 0)
ratio_2022 = pd.read_csv('./results/total_ratio/2022_ratio.csv', index_col= 0)

# combine the data to one dataframe
ratio_total = pd.concat([ratio_2015, ratio_2016, ratio_2017, ratio_2018, ratio_2019, ratio_2020, ratio_2021, ratio_2022])

# two sample t-test
print(stats.ttest_ind(ratio_total['Female'], ratio_total['Male']))
