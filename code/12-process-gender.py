"""
In this script, I process the data generated from last step, which includes the gender data of each applicant.
Classification of each project is added, and the universities are included in the dataset.

Projects are classified depending on the keywords of the abstract, which was retrieved from Flavia's script.

The classification includes:
Aeronautics, Energy systems, Industrial Engineering, User experience design, 
Environmental monitering, Crop breeding, Food production, Recycling, Steel manufacturing, Pharmocology.
"""

__author__ = "Xuan Wang"
__contact__ = "xuan.wang22@imperial.ac.uk"
__date__ = "1 July 2023"
__name__ = "14-process-gender.py"

# loads the required packages
import pandas as pd
import re

# read the data
df = pd.read_csv("./clean-data/fine-scale/UK/gender-data.csv") # clean data with gender
df_abstract = pd.read_csv("./clean-data/fine-scale/STEM/titles-abstracts-tokenized-filtered.csv", sep = ' ', header = None, names = ['ProjectId', 'Institution', 'Abstract']) # raw data which includes the title abstracts

# drop the student names columns
df_PI = df.drop(['StudentFirstName', 'StudentOtherNames'], axis = 1)

# delete the front "UKRI-" in case the project ID doesn't match    
df_PI['ProjectId'] = df_PI['ProjectId'].str.replace('UKRI-', '')

# change the column name "LeadInstitution" to "Universities"
df_PI = df_PI.rename(columns={'LeadInstitution': 'Universities'})

# define a classification of the keywords
keyword_dict = {
    'Veterinary science': ['veterinary medicine', 'livestock', 'veterinary surgery', 'animal welfare'],
    'Agriculture, forestry & food science': ['crop production', 'food safety', 'forestry management', 'soil science', 'agribusiness', 'food technology', 'agricultural economics', 'agroecology'],
    'General engineering': ['mechanics', 'engineering principles', 'design', 'system analysis', 'industrial engineering', 'engineering ethics'],
    'Chemical engineering': ['chemical processes', 'reaction kinetics', 'process design', 'polymer engineering'],
    'Mineral, metallurgy & materials engineering': ['mining engineering', 'material properties', 'metallurgical processes', 'material characterization'],
    'Civil engineering': ['structural analysis', 'transportation engineering', 'geotechnical engineering', 'urban planning'],
    'Electrical, electronic & computer engineering': ['power systems', 'electronics', 'communications', 'computer networks'],
    'Mechanical, aero & production engineering': ['mechanical systems', 'aerospace engineering', 'manufacturing processes', 'robotics'],
    'IT, systems sciences & computer software engineering': ['software development', 'data science', 'information systems', 'artificial intelligence'],
    'Earth, marine & environmental sciences': ['geology', 'oceanography', 'climate change', 'environmental conservation'],
    'Biosciences': ['genetics', 'molecular biology', 'biochemistry', 'biotechnology'],
    'Chemistry': ['organic chemistry', 'inorganic chemistry', 'analytical chemistry', 'physical chemistry'],
    'Physics': ['quantum mechanics', 'particle physics', 'optics', 'condensed matter physics', 'particle accelerations'],
    'Mathematics': ['algebra', 'calculus', 'statistics', 'mathematical modeling', 'number theory', 'probability theory'],
}

# classify the projects using the title abstracts
def classify(abstract):
    
    # convert the abstract to lower letter
    abstract = str(abstract).lower()
    
    # count the number of keywords in the abstract
    num_key = {}
    
    for subject, keyword_list in keyword_dict.items():
        
        count = 0
        
        for key in keyword_list:
            if re.search(r'\b' + re.escape(key) + r'\b', abstract):
                count += 1
        
        num_key[subject] = count
    
    # classify the project depending on the number of keywords in each category
    return max(num_key, key = num_key.get, default = "unknown")

# apply the function to the title abstracts data
df_abstract['classification'] = df_abstract['Abstract'].apply(classify)

# add the classification to the clean data
df_PI = pd.merge(df_PI, df_abstract[['ProjectId', 'classification']], on='ProjectId')

# save the data
df_PI.to_csv('./clean-data/fine-scale/UK/classified_gender_data.csv', index=False)