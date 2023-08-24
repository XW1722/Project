#!/usr/bin/env python3

"""  
This script reads the raw text files and save them in a format to be used by 
MALLET (i.e., [TAG] [LABEL] [TEXT]). MALLET is a Java-based program for statistical natural 
language processing, document classification, clustering, topic modeling, information extraction, 
and other machine learning applications to text. It has an extremely fast and highly scalable 
implementation of Gibbs sampling, efficient methods for document-topic hyperparameter optimization, 
and tools for inferring topics for new documents given trained models.

The TokenizeTexts class reads raw text files in chunks from different directories if given a file listing paths
to all directories (i.e., [argv1]), and applies the 'TextProcessor' class. The TexProcessor class was defined 
in the ./code/TextProcessor.py script, this pre-process words for text analysis (i.e. lowercases, 
tokenizes, remove accents and punctuations, lemmatizes and tags words). The chunking of the data makes 
it quicker and memory efficient. 

This script also loads a file with stop_words to be removed from the data. Stop_words are a set of commonly used 
words in a language with no value in topic allocation (i.e., 'I', 'how', 'and'). This stop_word file also include
words that we deemed to have no value for the purpose of our analysis (i.e. 'grant', 'professor', 'research')

Here we also lemmatize words, that is, we reduce words to their lemmas (i.e running, runners -> run).

Then we save the tokenized text to a file called "titles-abstracts-tokenized.csv" in a path given 
by [argv2].

How to run this script from the command line - example:
python ./code/helper-scripts/data-processing/tokenize_texts4mallet.py ./code/supporting-files/directories-path/titles-abstracts-dir-STEM.txt ./clean-data/fine-scale/STEM/

"""

__appname__ = 'TokenizeTexts'
__author__ = 'Flavia C. Bellotto-Trigo (flaviacbtrigo@gmail.com)'
__version__ = '0.0.1'

# imports
from operator import index
import pandas as pd
from nltk.stem import WordNetLemmatizer
import TextProcessor
import sys
import os
import nltk
import csv
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

class TokenizeTexts:
    def __init__(self, text_processor, dirnames, savefile) -> None:
        self.text_processor = text_processor
        self.dirnames = dirnames
        self.savefile = savefile

    def tokenize_csv(self):
        
        i = 0

        for fname in self.dirnames:
            print(fname.split()[0]+"\n")

            with pd.read_csv(fname.split()[0], chunksize=10000) as f:
                # print(len(f))
                
                # using chunks so to not load all data into memory at once
                for chunk in f:
                    print("chunk "+ str(i) + "\n")

                    chunk['TitleAbstract'] = chunk['TitleAbstract'].map(lambda x: " ".join(self.text_processor.pre_process(x)))

                    # count number of tokens
                    chunk['n_tokens'] = chunk['TitleAbstract'].map(lambda x: len(x.split()))
                    chunk['Label'] = fname.split()[1]

                    # keep only columns for Mallet input "ID", "tag", "text"    
                    chunk = chunk[["ProjectId", "Label", "TitleAbstract"]]

                    #sanatise outputs - replacing all spaces with underscores
                    chunk.ProjectId = chunk.ProjectId.apply(lambda x: str(x).strip()).replace(" ", "-", regex=True)
                    

                    if i == 0:
                        chunk.to_csv(self.savefile,mode = 'w', index=False, header = False, sep = " ")
                    else:
                        chunk.to_csv(self.savefile,mode = 'a', index=False, header = False, sep = " ")

                    i += 1

                

def main(argv):
    #read in stop words
    with open("./code/supporting-files/stop-words.txt","r") as f:
        stop_words = f.read().splitlines()

    # define lemmatizer
    lemmatizer = WordNetLemmatizer()

    # read file with path to directories
    with open(argv[1],'r') as f:
        dirnames = f.read().splitlines()

    print(dirnames)

    text_processor = TextProcessor.TextProcessor(stop_words=stop_words, lemmatizer=lemmatizer)

    tokenize_text = TokenizeTexts(text_processor=text_processor, dirnames=dirnames, savefile=os.path.join(argv[2], "titles-abstracts-tokenized.csv"))

    tokenize_text.tokenize_csv()

    return 0

if __name__ == "__main__": 
    """Makes sure the "main" function is called from command line"""
    status = main(sys.argv)
    sys.exit(status)
