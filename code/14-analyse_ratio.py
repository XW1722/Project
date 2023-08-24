"""

In this script, I conducted three calculations:
Each classification, what is the percentage of each gender getting funded;
Each university, what is the percentage of each gender getting funded, in different classifications;
The last one is the proportion of each gender getting funded, in all classification and all universities.

For the first one, I used the result of (gender funded in each classification / total number of male/female hesa staff in that classification).
The dataset is splitted into different subsets depending on the classification, and then the results are calculated.

For the second one, I used the result of (gender funded each classification of this uni / total number of male/female hesa staff in this university), for each uni.
Isplitted the dataset into different subsets depending on the leading institution.

For the third one, I used the result of (gender funded in all STEM subjects / total number of STEM staff).

This script is used to generate the classified data for each year.
"""

__author__ = "Xuan Wang"
__date__ = "18 Jul 2023"
__contact__ = "xuan.wang22@imperial.ac.uk"

# load packages
import pandas as pd

# import the dataset
df = pd.read_csv('./results/final_data/final_data_2022.csv')

# split the data
# regarding universities
df_uni = df.groupby(['LeadInstitution', 'Classification'])
df_class = df.groupby('Classification')


#############################################
############### First Ratio #################
#############################################

# sum up the number of funded males and females in each classification

male_funded_class = df[df['gender'] == 'male'].groupby('Classification').size().to_frame()
male_funded_class = male_funded_class.rename(columns={0: 'Funded_Male'})
female_funded_class = df[df['gender'] == 'female'].groupby('Classification').size().to_frame()
female_funded_class = female_funded_class.rename(columns={0: 'Funded_Female'})

total_Female = df_class['class_Female'].unique().to_frame()
total_Female['class_Female'] = total_Female['class_Female'].apply(lambda x: int(str(x[0]).strip('[]')))
total_Male = df_class['class_Male'].unique().to_frame()
total_Male['class_Male'] = total_Male['class_Male'].apply(lambda x: int(str(x[0]).strip('[]')))

funded_class = pd.merge(male_funded_class, female_funded_class, on = 'Classification')
funded_class = pd.merge(funded_class, total_Male, on = 'Classification')
funded_class = pd.merge(funded_class, total_Female, on = 'Classification')


# calculate the proportion
funded_class['ratio_Male'] = funded_class['Funded_Male'] / funded_class['class_Male']
funded_class['ratio_Female'] = funded_class['Funded_Female'] / funded_class['class_Female']


###############################################
############### Second Ratio ##################
###############################################

# count the number of funded gender

male_funded_uni = df[df['gender'] == 'male'].groupby(['LeadInstitution', 'Classification']).size().to_frame()
male_funded_uni = male_funded_uni.rename(columns={0: 'Funded_Male'})
female_funded_uni = df[df['gender'] == 'female'].groupby(['LeadInstitution', 'Classification']).size().to_frame()
female_funded_uni = female_funded_uni.rename(columns={0: 'Funded_Female'})

# total number of each gender in each university 
total_Female_uni = df_uni['uni_Female'].unique().to_frame()
total_Female_uni['uni_Female'] = total_Female_uni['uni_Female'].apply(lambda x: int(str(x[0]).strip('[]')))

total_Male_uni = df_uni['uni_Male'].unique().to_frame()
total_Male_uni['uni_Male'] = total_Male_uni['uni_Male'].apply(lambda x: int(str(x[0]).strip('[]')))

# merge the dataset
funded_uni = pd.merge(male_funded_uni, female_funded_uni, on = ['LeadInstitution', 'Classification'])
funded_uni = pd.merge(funded_uni, total_Female_uni, on = ['LeadInstitution', 'Classification'])
funded_uni = pd.merge(funded_uni, total_Male_uni, on = ['LeadInstitution', 'Classification'])

# calculate the ratio
funded_uni['ratio_Male'] = funded_uni['Funded_Male'] / funded_uni['uni_Male']
funded_uni['ratio_Female'] = funded_uni['Funded_Female'] / funded_uni['uni_Female']

##########################################
############# Third Ratio ################
##########################################

# sum the number of each gender getting funded
num_funded_female = df['gender'].value_counts()['female']
num_funded_male = df['gender'].value_counts()['male']
num_total_female = df['class_Female'].unique().sum()
num_total_male = df['class_Male'].unique().sum()

# calculate the ratio
ratio_female_2022 = num_funded_female / num_total_female
ratio_male_2022 = num_funded_male / num_total_male

ratio_total = {'Female': ratio_female_2022, 'Male': ratio_male_2022}
ratio_total = pd.DataFrame(data = ratio_total, index = ['2022'])

# save the data
funded_uni.to_csv('./results/uni-result/2022-uni.csv')
funded_class.to_csv('./results/subject-result/2022-class.csv')
ratio_total.to_csv('./results/total_ratio/2022_ratio.csv')
