"""
This script reads the keyword labels and gender dataset. 
We analyse the distribution of gender under each label.
The proportion of different gender under each label will be calculated.

The classification includes: 
Veterinary Science; Agriculture, Forestry & Food Science; General Engineering; Chemical Engineering; Mineral, Metallurgy & Materials Engineering; Civil Engineering; Electrical, Electronic & Computer Engineering; Mechanical, Aero & Production Engineering; IT, Systems Sciences & Computer Software Engineering; Earth, Marine & Environmental Sciences; Biosciences; Physics; Chemistry; Mathematics.
"""

__author__ = "Xuan Wang"
__contact__ = "xuan.wang22@imperial.ac.uk"
__date__ = "9 Jun 2023"
__name__ = "gender.py"

# import the required pacakges
import pandas as pd
import numpy as np
import csv

# load the dataset
df = pd.read_csv('./results/fine-scale/mallet-models/STEM/200-topic-files/3-200-topics-doc.txt', delimiter = '\t', engine = 'python', skiprows = 1, header = None)
df.columns = ['Number', 'ProjectId'] + [str(i) for i in range(200)]
df_gender = pd.read_csv('./clean-data/fine-scale/UK/gender-data.csv')
df_gender['ProjectId'] = df_gender['ProjectId'].str.replace('UKRI-', '')
df_keywords = pd.read_csv('./results/fine-scale/mallet-models/STEM/200-topic-files/3-200-keywords.csv')


# classify the topics
topics = [
    (0, "Mechanical, Aero & Production Engineering"),
    (1, "Biosciences"),
    (2, "IT, Systems Sciences & Computer Software Engineering"),
    (3, "Mineral, Metallurgy & Materials Engineering"),
    (4, "Physics"),
    (5, "Agriculture, Forestry & Food Science"),
    (6, "General Engineering"),
    (7, "Earth, Marine & Environmental Sciences"),
    (8, "Earth, Marine & Environmental Sciences"),
    (9, "Veterinary Science"),
    (10, "IT, Systems Sciences & Computer Software Engineering"),
    (11, "Earth, Marine & Environmental Sciences"),
    (12, "Mineral, Metallurgy & Materials Engineering"),
    (13, "Physics"),
    (14, "General Engineering"),
    (15, "Biosciences"),
    (16, "Biosciences"),
    (17, "Biosciences"),
    (18, "Biosciences"),
    (19, "Biosciences"),
    (20, "Electrical, Electronic & Computer Engineering"),
    (21, "Biosciences"),
    (22, "Biosciences"),
    (23, "Mathematics"),
    (24, "General Engineering"),
    (25, "IT, Systems Sciences & Computer Software Engineering"),
    (26, "Earth, Marine & Environmental Sciences"),
    (27, "Biosciences"),
    (28, "Mathematics"),
    (29, "Agriculture, Forestry & Food Science"),
    (30, "Biosciences"),
    (31, "Biosciences"),
    (32, "Agriculture, Forestry & Food Science"),
    (33, "Agriculture, Forestry & Food Science"),
    (34, "Chemistry"),
    (35, "Physics"),
    (36, "Biosciences"),
    (37, "Civil Engineering"),
    (38, "Mathematics"),
    (39, "Biosciences"),
    (40, "Mathematics"),
    (41, "Earth, Marine & Environmental Sciences"),
    (42, "Chemistry"),
    (43, "Biosciences"),
    (44, "Biosciences"),
    (45, "Electrical, Electronic & Computer Engineering"),
    (46, "Mineral, Metallurgy & Materials Engineering"),
    (47, "Agriculture, Forestry & Food Science"),
    (48, "Chemistry"),
    (49, "IT, Systems Sciences & Computer Software Engineering"),
    (50, "IT, Systems Sciences & Computer Software Engineering"),
    (51, "Physics"),
    (52, "Biosciences"),
    (53, "Agriculture, Forestry & Food Science"),
    (54, "Biosciences"),
    (55, "Mechanical, Aero & Production Engineering"),
    #有问题了，什么答辩啊
    (56, "Electrical, Electronic & Computer Engineering"),
    (57, "Earth, Marine & Environmental Sciences"),
    (58, "IT, Systems Sciences & Computer Software Engineering"),
    (59, "IT, Systems Sciences & Computer Software Engineering"),
    (60, "Mechanical, Aero & Production Engineering"),
    (61, "Veterinary Science"),
    (62, "General Engineering"),
    (63, "Earth, Marine & Environmental Sciences"),
    (64, "Mineral, Metallurgy & Materials Engineering"),
    (65, "Physics"),
    (66, "General Engineering"),
    (67, "Biosciences"),
    (68, "Biosciences"),
    (69, "Biosciences"),
    (70, "Biosciences"),
    (71, "Civil Engineering"),
    (72, "Chemical Engineering"),
    (73, "General Engineering"),
    (74, "Earth, Marine & Environmental Sciences"),
    (75, "Agriculture, Forestry & Food Science"),
    (76, "General Engineering"),
    (77, "Biosciences"),
    (78, "IT, Systems Sciences & Computer Software Engineering"),
    (79, "Mineral, Metallurgy & Materials Engineering"),
    (80, "Biosciences"),
    (81, "Earth, Marine & Environmental Sciences"),
    (82, "Earth, Marine & Environmental Sciences"),
    (83, "Agriculture, Forestry & Food Science"),
    (84, "Physics"),
    (85, "Biosciences"),
    (86, "Biosciences"),
    (87, "Electrical, Electronic & Computer Engineering"),
    (88, "Earth, Marine & Environmental Sciences"),
    (89, "Electrical, Electronic & Computer Engineering"),
    (90, "Electrical, Electronic & Computer Engineering"),
    (91, "Physics"),
    (92, "Biosciences"),
    (93, "Biosciences"),
    (94, "IT, Systems Sciences & Computer Software Engineering"),
    (95, "Other"),
    (96, "IT, Systems Sciences & Computer Software Engineering"),
    (97, "Mechanical, Aero & Production Engineering"),
    (98, "General Engineering"),
    (99, "Mechanical, Aero & Production Engineering"),
    (100, "Biosciences"),
    (101, "Chemical Engineering"),
    (102, "Physics"),
    (103, "Biosciences"),
    (104, "Biosciences"),
    (105, "Mechanical, Aero & Production Engineering"),
    (106, "Biosciences"),
    (107, "Biosciences"),
    (108, "Agriculture, Forestry & Food Science"),
    (109, "Earth, Marine & Environmental Sciences"),
    (110, "Biosciences"),
    (111, "Biosciences"),
    (112, "Biosciences"),
    (113, "Earth, Marine & Environmental Sciences"),
    (114, "Earth, Marine & Environmental Sciences"),
    (115, "Biosciences"),
    (116, "Agriculture, Forestry & Food Science"),
    (117, "IT, Systems Sciences & Computer Software Engineering"),
    (118, "Biosciences"),
    (119, "IT, Systems Sciences & Computer Software Engineering"),
    (120, "Other"),
    (121, "Electrical, Electronic & Computer Engineering"),
    (122, "IT, Systems Sciences & Computer Software Engineering"),
    (123, "Physics"),
    (124, "Physics"),
    (125, "Chemical Engineering"),
    (126, "Biosciences"),
    (127, "Earth, Marine & Environmental Sciences"),
    (128, "Earth, Marine & Environmental Sciences"),
    (129, "Biosciences"),
    (130, "Electrical, Electronic & Computer Engineering"),
    (131, "Earth, Marine & Environmental Sciences"),
    (132, "Mineral, Metallurgy & Materials Engineering"),
    (133, "General Engineering"),
    (134, "Biosciences"),
    (135, "Biosciences"),
    (136, "General Engineering"),
    (137, "Earth, Marine & Environmental Sciences"),
    (138, "General Engineering"),
    (139, "Mineral, Metallurgy & Materials Engineering"),
    (140, "Physics"),
    (141, "Mineral, Metallurgy & Materials Engineering"),
    (142, "Earth, Marine & Environmental Sciences"),
    (143, "Biosciences"),
    (144, "Electrical, Electronic & Computer Engineering"),
    (145, "IT, Systems Sciences & Computer Software Engineering"),
    (146, "Chemical Engineering"),
    (147, "Biosciences"),
    (148, "Earth, Marine & Environmental Sciences"),
    (149, "Civil Engineering"),
    (150, "IT, Systems Sciences & Computer Software Engineering"),
    (151, "Earth, Marine & Environmental Sciences"),
    (152, "Veterinary Science"),
    (153, "Biosciences"),
    (154, "Agriculture, Forestry & Food Science"),
    (155, "Physics"),
    (156, "Biosciences"),
    (157, "Mineral, Metallurgy & Materials Engineering"),
    (158, "General Engineering"),
    (159, "Biosciences"),
    (160, "Biosciences"),
    (161, "Earth, Marine & Environmental Sciences"),
    (162, "Agriculture, Forestry & Food Science"),
    (163, "General Engineering"),
    (164, "Biosciences"),
    (165, "Biosciences"),
    (166, "Earth, Marine & Environmental Sciences"),
    (167, "IT, Systems Sciences & Computer Software Engineering"),
    (168, "Earth, Marine & Environmental Sciences"),
    (169, "Physics"),
    (170, "General Engineering"),
    (171, "IT, Systems Sciences & Computer Software Engineering"),
    (172, "Earth, Marine & Environmental Sciences"),
    (173, "Physics"),
    (174, "General Engineering"),
    (175, "Biosciences"),
    (176, "Earth, Marine & Environmental Sciences"),
    (177, "IT, Systems Sciences & Computer Software Engineering"),
    (178, "General Engineering"),
    (179, "IT, Systems Sciences & Computer Software Engineering"),
    (180, "Electrical, Electronic & Computer Engineering"),
    (181, "Earth, Marine & Environmental Sciences"),
    (182, "Physics"),
    (183, "Chemistry"),
    (184, "General Engineering"),
    (185, "Earth, Marine & Environmental Sciences"),
    (186, "Biosciences"),
    (187, "General Engineering"),
    (188, "General Engineering"),
    (189, "Earth, Marine & Environmental Sciences"),
    (190, "Earth, Marine & Environmental Sciences"),
    (191, "Biosciences"),
    (192, "General Engineering"),
    (193, "Biosciences"),
    (194, "Biosciences"),
    (195, "Biosciences"),
    (196, "Earth, Marine & Environmental Sciences"),
    (197, "Biosciences"),
    (198, "Biosciences"),
    (199, "General Engineering")
]




output_file = './results/fine-scale/mallet-models/STEM/200-topic-files/3-200-discipline.csv'

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Topic number', 'Classification'])
    writer.writerows(topics)

# merge the classification with the gender data
# find the most likely topic for each project
df['Topic number'] = df.iloc[:, 3:202].idxmax(axis=1)
df_discipline = pd.read_csv('./results/fine-scale/mallet-models/STEM/200-topic-files/3-200-discipline.csv')
df['Topic number'] = df['Topic number'].astype(int)
df_discipline['Topic number'] = df_discipline['Topic number'].astype(int)

df_merge = pd.merge(df, df_discipline, on='Topic number')[['ProjectId', 'Classification']]

final_data = pd.merge(df_gender, df_merge, on='ProjectId')

# clean the data
final_data_clean = final_data[['ProjectId', 'LeadInstitution', 'FundingAmount', 'FundingCurrency', 'gender', 'Classification']]
final_data_clean.to_csv('./results/fine-scale/3-200-result.csv')



