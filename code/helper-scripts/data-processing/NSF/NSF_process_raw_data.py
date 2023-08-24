#!/usr/bin/env python3

""" This code creates the project metadata file with columns to match other countries' metadata. 

If run from the command line, it takes 2 arguments: 
1) the file path to the raw xml files
2) the file path to save the projects metadata which will be used for analysis after running the LDA model

argv[1] = "./raw-data/fine-scale/USA/NSF/NSF-raw-xml"
argv[2] = "./clean-data/fine-scale/USA/NSF/"

Example:  python3 ./code/helper-scripts/data-processing/NSF_process_raw_data.py ./raw-data/fine-scale/USA/NSF/NSF_raw_xml ./clean-data/fine-scale/USA/NSF/

"""


__appname__ = 'NSF_process_raw_data.py'
__author__ = 'Michael Mustri (email), Flavia C. Bellotto-Trigo (flaviacbtrigo@gmail.com)'
__version__ = '0.0.3'


## Imports ## 
from re import X
import sys # module to interface our program with the operating system
import xml.etree.ElementTree as Xet
import pandas as pd
import os
import io
import numpy

# one = "./raw-data/fine-scale/USA/NSF/NSF-raw-xml"
# two = "./clean-data/fine-scale/USA/NSF/"
# old_two = "./raw-data/fine-scale/USA/NSF/titles-abstracts/"

## Constants ##
metadata = {"ProjectId": [], "Country": [], "CountryFundingBody": [], "FundingBody":[], "LeadInstitution":[], 
"StartDate": [], "EndDate": [], "FundingAmount": [], "FundingCurrency": []}

## funcions ##
def check_text(x):
    # print(x)
    if x != None:
        if x.text == None:
            return("None")
        else:
            return(x.text)
    return("None")


def main(argv):
    ## Loop through years folders in the NSF_xml_raw folder
    for folder in os.listdir(os.path.join(argv[1])):
        current_year_path = os.path.join(argv[1], folder)
        print(folder)
        ## Loop through files in each year folder 
        for filename in os.listdir(current_year_path):
            
            
            ## Check if a file has xml format, if so, parse xml file, store its name without ".xml" suffix and create a name for .txt file
            if filename.endswith(".xml"):
                rawname = filename.removesuffix('.xml')
                xmlparse = Xet.parse(os.path.join(current_year_path,filename))
                root = xmlparse.getroot()
                
                # first check if Funding body is part of STEM
                FundingBody = check_text(root.find(".//Directorate/Abbreviation"))
                stem_fundingBodies = ['BIO', 'CISE', 'ENG', 'ERE', 'GEO', 'OIA', 'OISE', 'MPS', 'TIP']

                if FundingBody in stem_fundingBodies:

                    # get projects metadata and store
                    ProjectId = check_text(root.find(".//AwardID"))
                    metadata["ProjectId"].append("NSF-" + ProjectId)

                    metadata["FundingBody"].append(FundingBody)

                    StartDate = check_text(root.find(".//AwardEffectiveDate"))
                    metadata["StartDate"].append(StartDate)

                    EndDate = check_text(root.find(".//AwardExpirationDate"))
                    metadata["EndDate"].append(EndDate)
                    
                    FundingAmount = check_text(root.find(".//AwardAmount"))
                    metadata["FundingAmount"].append(FundingAmount) 

                    LeadInst = check_text(root.find(".//Performance_Institution/Name"))
                    metadata["LeadInstitution"].append(LeadInst)

                    # values that are the same for all documents
                    metadata["Country"].append("USA")
                    metadata["CountryFundingBody"].append("NSF")
                    metadata["FundingCurrency"].append("USD")

    # turn dict into dataframe and save it
    df = pd.DataFrame.from_dict(metadata)
    df.to_csv(os.path.join(argv[2], "NSF-project-metadata.csv"), index=False)

              
if __name__ == "__main__": 
    """Makes sure the "main" function is called from command line"""  
    status = main(sys.argv)
    sys.exit(status)
