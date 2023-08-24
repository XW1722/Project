"""
This script creates labelling to the processed data for analysis of the potential causes of the bias.
The method is using the topic probability distribution to determine the label for each topic.

The labels are the classifications of the subjects, including: Aeronautics, Energy systems, Industrial Engineering, User experience design, 
Environmental monitering, Crop breeding, Food production, Recycling, Steel manufacturing, Pharmocology.
These are the labels used by Flavia in the paper - 'Placing UK Research within the International STEM Funding Landscape'.
Code generated with the help of ChatGPT!
"""

__author__ = "Xuan Wang"
__contact__ = "xuan.wang22@imperial.ac.uk"
__date__ = "7 Jun 2023"
__name__ = "06-label-prob.py"

# import the packages
import pandas as pd

# load the clean dataset file
df = pd.read_csv("./clean-data/fine-scale/STEM/project-metadata.csv")


# Define the topic labels
topic_labels = {
    0: 'Aeronautics',
    1: 'Energy Systems',
    2: 'Industrial Engineering',
    3: 'User Experience Design',
    4: 'Environmental Monitoring',
    5: 'Crop Breeding',
    6: 'Food Production',
    7: 'Recycling',
    8: 'Steel Manufacturing',
    9: 'Pharmocology'
}

# define the number of topics
k = 200

# Iterate over the generated topic distribution files
# r is the value of set.seed()
for r in range(1, 4):
    # read the generated distribution files
    topic_dist_file = f"./results/fine-scale/mallet-models/STEM/{k}-topic-files/{r}-{k}-topics-doc.txt"

    with open(topic_dist_file, "r") as file:
        # read all lines except the first line, which are the column names
        all_lines = file.readlines()[1:]
        
        for line in all_lines:
            # read the project ID
            projectID = line.split("\t")[1]
            # get the probability data by splitting the line by tab and exclude the first & second column
            topic_probs = line.split("\t")[2:]
            # convert probabilities to float
            topic_probs = [float(prob) for prob in topic_probs]
            # get the index of the topic with maximum probability
            dominant_topic = topic_probs.index(max(topic_probs))
            # Get the label based on the dominant topic
            label = topic_labels.get(dominant_topic, "Others")
            # match the label to each project by project ID, and create a new column
            df.loc[df["ProjectId"] == projectID, "Label"] = label

# Save the labeled dataframe
df.to_csv("./clean-data/fine-scale/STEM/project-metadata-labeled.csv", index=False)
