
## This script takes the NIH RePORTER csv files for each fiscal year and extracts the necessary fields of interest
# ["APPLICATION_ID", "ORG_COUNTRY", "FundingBody", "ORG_NAME", "PROJECT_START", "PROJECT_END", "FundingAmount","FundingCurrency"]
# it then concatenates a data frame with all projects from every csv present and writes another csv with the specified data.

#import modules
import pandas as pd
import os
import io
import numpy
import shutil

# Define the path to working directory, should contain all NIH RePORTER csv files you intend to extract information from and nothing else

# Note: there are over 1,000,000 projects present in the NIH database, which exceeds the row limit for excel. Run this
# script in batches to avoid creating unreasonably large csv files.

wd = "PATH_TO_WORKING_DIR"
os.chdir(wd)

# Defines a list of present csv files
csv_files = os.listdir()

# We initialize an empty DataFrame
NSF_general = pd.DataFrame

# Initialize an iterator for control loop
itr = 0

# Iterate over each csv file
for file in csv_files:
    # Print filename and read csv file into a DataFrame
    print(file)
    df1 = pd.read_csv(file, low_memory=False, encoding = "utf-8")
    
    # Subset dataframe with fields of interest
    df_sub = df1.loc[:, ["APPLICATION_ID", "ORG_COUNTRY", "ORG_NAME", "PROJECT_START",
                         "PROJECT_END", "TOTAL_COST", "TOTAL_COST_SUB_PROJECT"]]
    
    # Promote funding figures to integer type for arithmetic operations
    df_sub["TOTAL_COST"] = df_sub["TOTAL_COST"].astype("Int64") 
    df_sub["TOTAL_COST_SUB_PROJECT"] = df_sub["TOTAL_COST_SUB_PROJECT"].astype("Int64") 
    
    # Create funding amount field which sums subproject and project costs
    df_sub["FundingAmount"] = df_sub.fillna(0)["TOTAL_COST_SUB_PROJECT"] + df_sub.fillna(0)["TOTAL_COST"]
    
    # Define funding body and funding currencies
    df_sub["FundingBody"] = "NIH"
    df_sub["FundingCurrency"] = "US Dollars"
    
    # Subset dataframe further and rename columns to match format
    df_final = df_sub.loc[:, ["APPLICATION_ID", "ORG_COUNTRY", "FundingBody", "ORG_NAME", "PROJECT_START", "PROJECT_END", "FundingAmount",
                          "FundingCurrency"]]
    df_final = df_final.rename(columns={"APPLICATION_ID":"ProjectId", "ORG_COUNTRY":"Country", "ORG_NAME":"LeadUniversity", 
                         "PROJECT_START":"StartDate", "PROJECT_END":"EndDate"})
    
    # if this is the first iteration, define NIH_general as df_final, if not, concatenate df_final to NIH_general
    if itr == 0:
        NIH_general = df_final
    else:
        NIH_general = pd.concat([NIH_general, df_final], ignore_index=True)
    itr += 1
    
# Save NIH_general to a csv file with an identifier (I used the range of fiscal years
NIH_general.to_csv("NIH_general_IDENTIFIER", encoding="utf-8", index=False)