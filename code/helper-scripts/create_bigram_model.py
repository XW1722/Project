#!/usr/bin/env python3

""" 
This script creates bigram models from titles and abstracts. The titles and abstracts were previously tokenised and are used here as 
the input for the bigram model. Due to the large size of the tokenised files, this script reads and process the file line-by -line. 

The first argument should be the path to the processed tokens (tokenised titles and abstracts), and the second argument should the 
path to save the frozen bigram model.
Example:

argv[1]= "./clean-data/fine-scale/UK/UKRI/"
argv[2]= "./code/supporting-files/bigram_models/"
"""

__appname__ = 'create_bigram_models.py'
__author__ = 'Flavia C. Bellotto-Trigo (flaviacbtrigo@gmail.com)'
__version__ = '0.0.1'

#  imports

from gensim.models.phrases import Phrases, ENGLISH_CONNECTOR_WORDS
import pandas as pd
import sys
import csv
import ast
import os


# create iterator to read line by line of processed tokes. Files are too large, so this uses less memory.  
class TokenIterator:
    def __init__(self, fpath) -> None:
        self.fpath = fpath

    def __iter__(self):
        with open(self.fpath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            next(reader, None) # ignores the header
            for row in reader:
                yield(ast.literal_eval(row[1])) # reads lines as lists




def main(argv):
    tokens = TokenIterator(os.path.join(argv[1], "titles-abstracts-tokenized.csv"))

#create bigram model #10 - 5
    bigram_model = Phrases(tokens, min_count = 5, threshold=10, connector_words=ENGLISH_CONNECTOR_WORDS)
    frozen_model = bigram_model.freeze()

    frozen_model.save(os.path.join(argv[2], "bigram_model_uk_usa.pkl"))

    return 0

if __name__ == "__main__": 
    """Makes sure the "main" function is called from command line"""  
    status = main(sys.argv)
    sys.exit(status)
