# !/bin/bash


# process text
echo "tokenising text"
# first argument is the language to use; second arg is the path to the python script; third arg is the path to where get the data from; 
# fourth arg is where to save the processed data
python ./code/helper-scripts/data-processing/tokenize_texts4mallet.py ./code/supporting-files/directories-path/titles-abstracts-dir-STEM.txt ./clean-data/fine-scale/STEM/
