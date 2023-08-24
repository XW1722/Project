#!/usr/bin/env python3

""" This code process the UKRI data from file 'UKRI_raw_metadata.csv'. It selects and rename columns to match the processed metadata
of all other countries, saving this as a new file called 'UKRI_project_metadata.csv'.

If run from the command line, it takes 3 arguments: 
1) the file path to the raw xml files
2) the file path to save text data, which will be the input to the script 01_process_multiple_text.py
3) the file path to save the projects metadata which will be used for analysis after running the LDA model

argv[1] = "./raw-data/fine-scale/UK/UKRI/"
argv[2] = "./clean-data/fine-scale/UK/UKRI/"


Example:  python code/helper-scripts/data-processing/UKRI_process_raw_data.py ./raw-data/fine-scale/UK/UKRI/ ./clean-data/fine-scale/UK/UKRI 
"""


__appname__ = 'UKRI_process_raw_data.py'
__author__ = 'Flavia C. Bellotto-Trigo (flaviacbtrigo@gmail.com)'
__version__ = '0.0.1'


## Imports ## 
from re import X
import sys # module to interface our program with the operating system
import xml.etree.ElementTree as Xet
import pandas as pd
import os
from datetime import datetime
from datetime import date


def main(argv):
         
    ukri_metadata = pd.read_csv(os.path.join(argv[1], 'UKRI-raw-metadata.csv')) 

    # filter projects by research grant and fellowships
    # data_filtered = ukri_metadata[ukri_metadata.ProjectCategory.isin(["Research Grant", "Fellowship"])]
    
    #filter STEM funding bodies
    data_filtered = ukri_metadata[ukri_metadata.FundingOrgName.isin(["BBSRC","EPSRC", "NERC", "STFC", "Innovate UK"])]

    # select columns
    ukri_cleaned = data_filtered[["ProjectId","FundingOrgName","LeadROName","StartDate","EndDate","AwardPounds","PIFirstName", "PIOtherNames", "StudentFirstName", "StudentOtherNames"]]
    # rename columns to match other countries' project metadata
    ukri_cleaned = ukri_cleaned.rename(columns = {"FundingOrgName":"FundingBody", "LeadROName":"LeadInstitution","AwardPounds":"FundingAmount"})
            
    # add columns to match other countries' project metadata 
    ukri_cleaned["Country"] = "UK"
    ukri_cleaned["CountryFundingBody"]= "UKRI"
    ukri_cleaned["FundingCurrency"] = "GBP"
    ukri_cleaned["ProjectId"] = "UKRI-" + ukri_cleaned["ProjectId"]

    # reorder columns
    ukri_cleaned = ukri_cleaned[['ProjectId', 'Country', 'CountryFundingBody', 'FundingBody','LeadInstitution', 'StartDate', 'EndDate', 'FundingAmount','FundingCurrency', "PIFirstName", "PIOtherNames", "StudentFirstName", "StudentOtherNames"]]

    # save project_metadata file 
    ukri_cleaned.to_csv(os.path.join(argv[2], "UKRI-project-metadata.csv"), index=False)

              
if __name__ == "__main__": 
    """Makes sure the "main" function is called from command line"""  
    status = main(sys.argv)
    sys.exit(status) 
