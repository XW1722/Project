# !/bin/bash

echo filtering data
# call helper script to filter minimum number of tokens
# first argument below is the language of the script being called; second argument is the path to where the script is located; thrid argument is where to get the
# input data from; fourth argument is where to save the filtered data to. 
python ./code/helper-scripts/data-processing/filter-tokens.py ./clean-data/fine-scale/STEM/titles-abstracts-tokenized.csv ./clean-data/fine-scale/STEM/

# importing data with Mallet
# this command uses the filtered data as input
# first argument below is Mallet; second arg is the Mallet function to use; the third to the sixth arguments are options from the mallet argument itself. You can look at all the 
# options and what they mean by typing "mallet bulk-load --help" on the terminal.
echo importing data
mallet bulk-load --input ./clean-data/fine-scale/STEM/titles-abstracts-tokenized-filtered.csv --keep-sequence TRUE --prune-count 20 --prune-doc-frequency 0.8 --output ./clean-data/fine-scale/STEM/mallet-tokens.mallet --line-regex "^(\S*)[\s,]*(\S*)[\s,]*(.*)$"

