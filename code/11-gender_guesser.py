"""
This script distinguishes the genders of the applicants.
The following package is required to run this script: gender-guesser.
It can be downloaded by running: pip install gender-guesser
"""

__author__ = "Xuan Wang"
__contact__ = "xuan.wang22@imperial.ac.uk"
__date__ = "9 Jun 2023"
__name__ = "gender.py"

# import the required packages
import pandas as pd
import gender_guesser.detector as gender

# load the clean dataset
df = pd.read_csv("./clean-data/fine-scale/UK/UKRI/UKRI-project-metadata.csv")

# get the detector
d = gender.Detector()

# define a function to distinguish the gender of the applicants by their names
def gender_app(name):
    gender = d.get_gender(name)
    if gender in ['male', 'female']:
        return gender
    elif gender == 'mostly_male':
        return 'male'
    elif gender == 'mostly_female':
        return 'female'
    else:
        return 'unknown'

# determine the gender of each applicant by using the PI first name
df['gender'] = df['PIFirstName'].apply(gender_app)
# if the gender of PI is unknwon, apply the PI other name column
df['gender'] = df.apply(lambda row: gender_app(row['PIOtherNames']) if row['gender'] == 'unknown' else row['gender'], axis=1)
# if the gender of PI is unknown, apply the student name
# df['gender'] = df.apply(lambda row: gender_app(row['StudentFirstName']) if row['gender'] == 'unknown' else row['gender'], axis=1)

# count the number of unknown
df['gender'].value_counts()['unknown'] # 43121 
df['StudentFirstName'].isna().sum() # 74516 unknown student names
df['PIFirstName'].isna().sum() # 35693 unknown PI names

# save the file
df.to_csv("./clean-data/fine-scale/UK/gender-data.csv")