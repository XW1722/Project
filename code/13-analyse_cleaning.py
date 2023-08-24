"""
This script processes the previous result and merge them to a dataset that can be directly used for analysing.
"""


__author__ = 'Xuan Wang'
__contact__ = 'xuan.wang22@imperial.ac.uk'
__date__ = '05 July 2023'

# import packages
import pandas as pd

# load the dataset
classif = pd.read_csv('./results/fine-scale/3-200-result.csv', index_col=0)
gender_agriculture = pd.read_csv('./raw-data/HESA/2022/agriculture.csv', skiprows=12, header = 0)
gender_engine = pd.read_csv('./raw-data/HESA/2022/engine_tech.csv', skiprows=12, header = 0)
gender_maths = pd.read_csv('./raw-data/HESA/2022/maths.csv', skiprows = 12, header = 0)
gender_uni = pd.read_csv('./raw-data/HESA/2022/uni-gender.csv', skiprows = 18, header = 0, usecols=['HE provider', 'Female', 'Male', 'Other', 'Total'])
start_time = pd.read_csv('./clean-data/UKRI-project-metadata.csv', usecols = ['ProjectId', 'StartDate'])
start_time['ProjectId'] = start_time['ProjectId'].str.replace('UKRI-', '')

# concat the HESA gender data
gender_hesa = pd.concat([gender_agriculture, gender_engine, gender_maths], ignore_index=True)

# checks the number of projects in each classification
(classif['Classification'] == 'Veterinary Science').sum() # 970
(classif['Classification'] == 'Agriculture, Forestry & Food Science').sum() # 4387
(classif['Classification'] == 'General Engineering').sum() # 10874
(classif['Classification'] == 'Chemical Engineering').sum() # 2226
(classif['Classification'] == 'Mineral, Metallurgy & Materials Engineering').sum() # 3645
(classif['Classification'] == 'Civil Engineering').sum() # 1514
(classif['Classification'] == 'Electrical, Electronic & Computer Engineering').sum() # 4886
(classif['Classification'] == 'Mechanical, Aero & Production Engineering').sum() # 3470
(classif['Classification'] == 'IT, Systems Sciences & Computer Software Engineering').sum() # 9109
(classif['Classification'] == 'Earth, Marine & Environmental Sciences').sum() # 11758
(classif['Classification'] == 'Biosciences').sum() # 17507
(classif['Classification'] == 'Chemistry').sum() # 1419
(classif['Classification'] == 'Physics').sum() # 8139
(classif['Classification'] == 'Mathematics').sum() # 3806
(classif['Classification'] == 'Other').sum() # 442

# process the data
gender_hesa['Cost centre'] = gender_hesa['Cost centre'].str.replace(r'^\d+\s', '', regex=True)
gender_hesa = gender_hesa.rename(columns={'Cost centre': 'Classification', 'Female':'class_Female', 'Male': 'class_Male'})
gender_uni = gender_uni.rename(columns = {'HE provider': 'LeadInstitution', 'Female':'uni_Female', 'Male':'uni_Male', 'Other':'uni_Other', 'Total':'uni_Total'})

# delete the columns where the university does not have value
gender_uni = gender_uni.dropna(how='any')

# set the classification into lower case and merge data
gender_hesa['Classification'] = gender_hesa['Classification'].str.lower()
classif['Classification'] = classif['Classification'].str.lower()


df = pd.merge(classif, gender_hesa, on = 'Classification')

gender_uni['LeadInstitution'] = gender_uni['LeadInstitution'].str.lower()
df['LeadInstitution'] = df['LeadInstitution'].str.lower()

# checks whether there is "the" at the front
gender_uni['LeadInstitution'] = gender_uni['LeadInstitution'].apply(lambda x: x[4:] if x.lower().startswith('the ') else x)
df['LeadInstitution'] = df['LeadInstitution'].apply(lambda x: x[4:] if x.lower().startswith('the ') else x)

df = pd.merge(gender_uni, df, on = 'LeadInstitution')

# delete the commas

df['uni_Female'] = df['uni_Female'].str.replace(',', '').astype(int)
df['uni_Male'] = df['uni_Male'].str.replace(',', '').astype(int)
df['uni_Other'] = df['uni_Other'].astype(int)
df['uni_Total'] = df['uni_Total'].str.replace(',', '').astype(int)

df['class_Male'] = df['class_Male'].astype(str)
df['class_Male'] = df['class_Male'].str.replace(',', '')
df['class_Male'] = df['class_Male'].astype(int)

df['class_Female'] = df['class_Female'].astype(str)
df['class_Female'] = df['class_Female'].str.replace(',', '')
df['class_Female'] = df['class_Female'].astype(int)

# merge with the corresponding time
start_time['StartDate'] = pd.to_datetime(start_time['StartDate'], format = '%d/%m/%Y')
year_2022 = start_time[start_time['StartDate'].dt.year == 2022]
df = pd.merge(df, year_2022, on = 'ProjectId')

# save the final data for analyse
df.to_csv('./results/final_data/final_data_2022.csv', index = False)