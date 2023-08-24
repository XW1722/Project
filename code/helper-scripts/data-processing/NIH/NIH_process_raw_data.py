#!/usr/bin/env python3

""" This code process the NIH data from file 'NIH_raw_metadata.csv'. It selects and rename columns to match the processed metadata
of all other countries, saving this as a new file called 'UKRI_project_metadata.csv'.

If run from the command line, it takes 2 arguments: 
1) the file path to the raw metadata
2) the file path to save the projects metadata which will be used for analysis after running the LDA model

argv[1] = "./flavia/raw-data/fine-scale/USA/NIH/"
argv[2] = "./flavia/clean-data/fine-scale/USA/NIH/"

Example:  python3 code/helper-scripts/data-processing/NIH_process_raw_data.py ./flavia/raw-data/fine-scale/USA/NIH/ ./flavia/clean-data/fine-scale/USA/NIH/

"""


__appname__ = 'NIH_process_raw_data.py'
__author__ = 'Flavia C. Bellotto-Trigo (flaviacbtrigo@gmail.com)'
__version__ = '0.0.1'



## Imports ## 
import sys # module to interface our program with the operating system
import pandas as pd
import os
import numpy as np

os.getcwd()

def main(argv):
    ## load NIH project metadata
    project_metadata = pd.read_csv(os.path.join(argv[1], 'NIH_raw_metadata.csv', dtype={'StartDate': str, 'EndDate':str}))
    print("data loaded")

    # change US name in the column 'country' from UNITED STATES to USA
    project_metadata["Country"] = project_metadata["Country"].replace(to_replace="UNITED STATES", value="USA")

    # change US Dollars to USD
    project_metadata["FundingCurrency"] = project_metadata["FundingCurrency"].replace(to_replace="US Dollars", value="USD")

    # rename columns to match other countries' project metadata
    NIH_updated = project_metadata.rename(columns = {"LeadUniversity":"LeadInstitution"})
    NIH_updated.head()

    df = pd.DataFrame.from_dict(NIH_updated)
    df.to_csv(os.path.join(argv[2], 'NIH-project-metadata.csv', index=False))

if __name__ == "__main__": 
    """Makes sure the "main" function is called from command line"""  
    status = main(sys.argv)
    sys.exit(status) 
