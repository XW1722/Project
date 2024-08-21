"""
This script performs the Wilcoxon hypothesis test, and checks whether there is a gender bias across time.
"""

__author__ = "Xuan Wang"
__contact__ = "xuan.wang22@imperial.ac.uk"
__date__ = "21 Jul 2023"

# import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import mannwhitneyu 
from scipy.stats import chi2_contingency
import seaborn as sns  
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

# Test for Normality
print("Normality test for Female:", stats.shapiro(ratio_total['Female']))
print("Normality test for Male:", stats.shapiro(ratio_total['Male']))
# If p-value < 0.05 for the Shapiro-Wilk test, then the data is not normally distributed.
# p-value: Female 0.068 Male 0.294


# Test for Equality of Variances
print("Test for Equality of Variances:", stats.levene(ratio_total['Female'], ratio_total['Male']))
# If p-value < 0.05 for the Levene's test, then the variances are not equal.
# p-value: 0.13

# Are normally distributed, and have equal variances



###############updated###################################
# Mann Whitney test for the funding to males and females
results = {}
years = {2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022}
df = pd.read_csv('./results/total_funding/mean_funding_years.csv')
for x in years:
    year_data = df[df['year'] == x]  
    male_funding = year_data[year_data['gender'] == 'male']['FundingAmount']  
    female_funding = year_data[year_data['gender'] == 'female']['FundingAmount']  

    test_result = mannwhitneyu(male_funding, female_funding, alternative='two-sided')
    results[x] = test_result
    
female_funding = df[df['gender'] == 'female']['AverageFundingAmount']  
male_funding = df[df['gender'] == 'male']['AverageFundingAmount']  
u_statistic, p_value = mannwhitneyu(female_funding, male_funding, alternative='two-sided')  

print(f"U statistic: {u_statistic}")  #U statistic: 4105.0
print(f"P value: {p_value}")  #P value: 1.1809093512235603e-05

#record:{2016: MannwhitneyuResult(statistic=175.0, pvalue=0.00043975808677961485), 2017: MannwhitneyuResult(statistic=176.0, pvalue=0.00036952219864219997), 2018: MannwhitneyuResult(statistic=175.0, pvalue=0.00043975808677961485), 2019: MannwhitneyuResult(statistic=164.0, pvalue=0.0026161516350141035), 2020: MannwhitneyuResult(statistic=150.0, pvalue=0.01796661080755547), 2021: MannwhitneyuResult(statistic=152.0, pvalue=0.013963504288693081), 2022: MannwhitneyuResult(statistic=147.0, pvalue=0.007076941978404361), 2015: MannwhitneyuResult(statistic=175.0, pvalue=0.00043975808677961485)}

female_df = df[df['gender'] == 'female']  
male_df = df[df['gender'] == 'male']
plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(10, 6))   
sns.histplot(female_df['AverageFundingAmount'], bins=20, color='skyblue', kde = True, edgecolor='black')
plt.title('Distribution of Funding Amount for Females')   
plt.xlabel('Average Funding Amount (GBP)')  
plt.ylabel('Frequency') 
plt.grid(True)
plt.savefig('./results/female_funding_distribution.png')

plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(10, 6))  
sns.histplot(male_df['AverageFundingAmount'], bins=20, color='skyblue', kde = True, edgecolor='black')
plt.title('Distribution of Funding Amount for Males')  
plt.xlabel('Average Funding Amount (GBP)')    
plt.ylabel('Frequency')   
plt.grid(True)    
plt.savefig('./results/male_funding_distribution.png')

plt.figure(figsize=(10, 6))  
   
sns.histplot(female_df['AverageFundingAmount'], bins=20, color='skyblue', kde=True, edgecolor='black', alpha=0.5, label='Female')  
    
sns.histplot(male_df['AverageFundingAmount'], bins=20, color='lightgreen', kde=True, edgecolor='black', alpha=0.5, label='Male')  
  
plt.title('Distribution of Funding Amount for Females and Males')  
plt.xlabel('Average Funding Amount (GBP)')  
plt.ylabel('Frequency')  
plt.grid(True)  
plt.legend()  
  
# 保存并展示图表  
plt.savefig('./results/funding_distribution_overlap.png')  
plt.show()
# Chi-squared test for the funded ratio of males and females
df = {}
results = []
total_funded_female = 0
total_funded_male = 0
total_female = 0
total_male = 0
df[1] = pd.read_csv('./results/final_data/final_data_2015.csv')
df[2] = pd.read_csv('./results/final_data/final_data_2016.csv')
df[3] = pd.read_csv('./results/final_data/final_data_2017.csv')
df[4] = pd.read_csv('./results/final_data/final_data_2018.csv')
df[5] = pd.read_csv('./results/final_data/final_data_2019.csv')
df[6] = pd.read_csv('./results/final_data/final_data_2020.csv')
df[7] = pd.read_csv('./results/final_data/final_data_2021.csv')
df[8] = pd.read_csv('./results/final_data/final_data_2022.csv')
for key in df:
    # total funded number
    total_funded_female += df[key]['gender'].value_counts()['female'].sum()
    total_funded_male += df[key]['gender'].value_counts()['male'].sum()
    # total number
    total_female += df[key]['class_Female'].unique().sum()
    total_male += df[key]['class_Male'].unique().sum()
chi_test = np.array([[total_funded_female, total_female - total_funded_female], 
                     [total_funded_male, total_male - total_funded_male]])
chi2, p, dof, expected = chi2_contingency(chi_test)    
#p-value: 4.7959998887009086e-107
for x in range(1, 9):
    data = df[x]
    # the total number of each gender
    num_funded_female = data['gender'].value_counts()['female']
    num_funded_male = data['gender'].value_counts()['male']
    # the number of each gender getting funded
    num_total_female = data['class_Female'].unique().sum()
    num_total_male = data['class_Male'].unique().sum()
    # chi-squared test
    observe = np.array([[num_funded_female, num_total_female - num_funded_female],   
                         [num_funded_male, num_total_male - num_funded_male]]) 
    chi2, p, dof, expected = chi2_contingency(observe)  
    results.append({'year': x + 2014, 'chi2': chi2, 'p': p, 'dof': dof})  
    
significant_p = 0.05 
gender_bias_years = [result['year'] for result in results if result['p'] < significant_p]  
  
if gender_bias_years:  
    print(f"\nThere is evidence of gender bias in the following years: {', '.join(map(str, gender_bias_years))}")  
else:  
    print("\nNo evidence of gender bias found in any year.")
 
 
# record: >>> results   [{'year': 2015, 'chi2': 69.35564871317261, 'p': 8.221681680624271e-17, 'dof': 1}, {'year': 2015, 'chi2': 69.35564871317261, 'p': 8.221681680624271e-17, 'dof': 1}, {'year': 2015, 'chi2': 69.35564871317261, 'p': 8.221681680624271e-17, 'dof': 1}, {'year': 2016, 'chi2': 66.01376060321063, 'p': 4.477857825381542e-16, 'dof': 1}, {'year': 2017, 'chi2': 48.128445382292945, 'p': 3.9919314001099835e-12, 'dof': 1}, {'year': 2018, 'chi2': 49.333136515098225, 'p': 2.159831619262401e-12, 'dof': 1}, {'year': 2019, 'chi2': 46.862875280661875, 'p': 7.613129116833515e-12, 'dof': 1}, {'year': 2020, 'chi2': 24.813862071199438, 'p': 6.314175160209205e-07, 'dof': 1}, {'year': 2021, 'chi2': 49.1927143142357, 'p': 2.3201082997548396e-12, 'dof': 1}, {'year': 2022, 'chi2': 27.430201382251322, 'p': 1.628677399366993e-07, 'dof': 1}]
    
   
    

