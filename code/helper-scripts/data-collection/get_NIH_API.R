rm(list = ls())

# Define a working directory
WORKING_DIR <- "path to directory where NIH_general*.csv is located"

setwd(WORKING_DIR)

# Load in modules
library(dplyr)
library(ggplot2)
library(tidyr)
library(repoRter.nih)

wd = getwd()

# Create a save directory for .txt files
saveDir = paste(wd, "/NIH_rawtxt/", sep = "")

# Read NIH_general*.csv into a data frame
df <- read.csv("NIH_general*.csv")

# Create list of project IDs
Appl_IDs <- df$ProjectId

# Initialize iterator for loop and set maximum number of batch iterations (retrieves 1000 records
# per loop iteration), get residual iterations for individual record retrieval
itr = 1

itr_max <- floor(length(Appl_IDs)/1000)*1000

itr_res <- length(Appl_IDs)%%1000


# While loop for batch request, stops when itr > itr_max
while(itr < itr_max){
  
  # Request 1000 records (from itr to itr+1000 of the ID list) and get project titles
  # and abstracts
  req <- make_req(criteria = 
                    list(appl_ids = c(Appl_IDs[itr:(1000+itr)])),
                  include_fields = c("ProjectTitle", "AbstractText"))
  res <- get_nih_data(req, max_pages = 10)
  
  
  # For each record retrieved write title and abstract into text file
  for(i in 1:nrow(res)){
    
    # retrieve project ID
    id <- Appl_IDs[itr + i]
    
    # retrieve title and abstract
    title = res$project_title[i]
    abstract = res$abstract_text[i]
    text = paste(title, abstract, sep ="\n")
    
    # open new file named by project ID and write text
    fileConn<-file(paste(saveDir, as.character(id),".txt"))
    writeLines(text, fileConn)
    close(fileConn)
  }
  
  
  # print progress out of all projects
  progress = (itr*100)/length(Appl_IDs)
  
  print(cat(progress, "%"))
  
  # Increase iterator for next batch of requests
  itr <- itr + 1000
  
  
}


# for loop makes individual requests for remaining projects
for(i in 1:itr_res){
  
  
  req <- make_req(criteria = 
                    list(appl_ids = c(Appl_IDs[itr_max+i])),
                  include_fields = c("ProjectTitle", "AbstractText"))
  res <- get_nih_data(req, max_pages = 1)
  
  id <- Appl_IDs[itr_max + i]
  
  if(is.atomic(res) == FALSE){
    title = res$project_title
    abstract = res$abstract_text
    text = paste(title, abstract, sep ="\n")
  } else{
    text = paste(as.character(res), sep ="\n")
  }
  
  
  fileConn<-file(paste(saveDir, as.character(id),".txt"))
  writeLines(text, fileConn)
  close(fileConn)
  
}


