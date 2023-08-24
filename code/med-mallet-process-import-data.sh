# !/bin/bash


# process text
echo "tokenising text"
python ./code/tokenize_texts4mallet.py ./code/supporting-files/directories-path/titles-abstracts-directories.txt ./clean-data/fine-scale/ENG-speaking-countries/

# importing data with Mallet
echo importing data
mallet bulk-load --input ./clean-data/fine-scale/ENG-speaking-countries/titles-abstracts-tokenized.csv --keep-sequence TRUE --prune-count 20 --prune-doc-frequency 0.8 --output ./clean-data/fine-scale/ENG-speaking-countries/mallet-tokens.mallet --line-regex "^(\S*)[\s,]*(\S*)[\s,]*(.*)$"



