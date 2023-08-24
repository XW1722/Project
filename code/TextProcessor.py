#!/usr/bin/env python3

""" blah blah """

__appname__ = 'TextProcessor'
__author__ = 'Flavia C. Bellotto-Trigo (flaviacbtrigo@gmail.com)'
__version__ = '0.0.1'

#imports
import gensim
import nltk
import sys

#define class
class TextProcessor:
    def __init__(self, stop_words, lemmatizer) -> None:
        #load bigram from frozen pkl file
        # self.bigram = Phrases.load(bigram_dir)
        self.stop_words = stop_words
        self.lemmatizer = lemmatizer

    def pre_process(self, text):
        tokens = text
        # tokenise and split
        # lowercases, tokenizes and remove accents and punctuations
        tokens = gensim.utils.simple_preprocess(str(tokens), deacc=True)
        
        # remove stop-words
        tokens = [word for word in tokens if word not in (self.stop_words)]
        
        # filter word tags (we are keeping only Nouns (NN) and verbs (VB))
        tags = nltk.pos_tag(tokens)
        tokens = [word[0] for word in tags if word[1].startswith(tuple(["NN", "VB"]))]
        
        # lemmatize
        # reduce words to their lemmas/basic form
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        
        # remove short words (keep words bigger than 3 characteres)
        tokens = [word for word in tokens if len(word) > 3]
        
        # remove stop words one more time, in case they were created after other processing (e.g lemmatization)
        tokens = [word for word in tokens if word not in (self.stop_words)]
        
        return(tokens)

def main(argv):
    return 0

if __name__ == "__main__": 
    """Makes sure the "main" function is called from command line"""  
    status = main(sys.argv)
    sys.exit(status)
