# This script produces the plot for the ranking of the degree of bias.

library(ggplot2)
library(tidyr)
library(reshape2)
library(gridExtra)
library(ggpubr)
library(stringr)
library(dplyr)
library(cowplot)
library(grid)

subject_2015 <- read.csv('./results/subject-result/2015-class.csv')
subject_2016 <- read.csv('./results/subject-result/2016-class.csv')
subject_2017 <- read.csv('./results/subject-result/2017-class.csv')
subject_2018 <- read.csv('./results/subject-result/2018-class.csv')
subject_2019 <- read.csv('./results/subject-result/2019-class.csv')
subject_2020 <- read.csv('./results/subject-result/2020-class.csv')
subject_2021 <- read.csv('./results/subject-result/2021-class.csv')
subject_2022 <- read.csv('./results/subject-result/2022-class.csv')

uni_2015 <- read.csv('./results/uni-result/2015-uni.csv')
uni_2016 <- read.csv('./results/uni-result/2016-uni.csv')
uni_2017 <- read.csv('./results/uni-result/2017-uni.csv')
uni_2018 <- read.csv('./results/uni-result/2018-uni.csv')
uni_2019 <- read.csv('./results/uni-result/2019-uni.csv')
uni_2020 <- read.csv('./results/uni-result/2020-uni.csv')
uni_2021 <- read.csv('./results/uni-result/2021-uni.csv')
uni_2022 <- read.csv('./results/uni-result/2022-uni.csv')

# add a column of the year
subject_2015$Year <- 2015
subject_2016$Year <- 2016
subject_2017$Year <- 2017
subject_2018$Year <- 2018
subject_2019$Year <- 2019
subject_2020$Year <- 2020
subject_2021$Year <- 2021
subject_2022$Year <- 2022

uni_2015$Year <- 2015
uni_2016$Year <- 2016
uni_2017$Year <- 2017
uni_2018$Year <- 2018
uni_2019$Year <- 2019
uni_2020$Year <- 2020
uni_2021$Year <- 2021
uni_2022$Year <- 2022

# combine the dataset
subject <- rbind(subject_2015, subject_2016, subject_2017, subject_2018, subject_2019, subject_2020, subject_2021, subject_2022)
uni <- rbind(uni_2015, uni_2016, uni_2017, uni_2018, uni_2019, uni_2020, uni_2021, uni_2022)

# set the university name to upper case
uni$LeadInstitution <- tools::toTitleCase(uni$LeadInstitution)
uni$Classification <- tools::toTitleCase(uni$Classification)
uni$Classification <- gsub("It,", "IT,", uni$Classification)

subject$Classification <- tools::toTitleCase(subject$Classification)
subject$Classification <- gsub("It,", "IT,", subject$Classification)


# ranking for classification
# calculate the degree of bias
all <- subject %>% group_by(Classification) %>% summarise(Funded_Male = sum(Funded_Male), Funded_Female = sum(Funded_Female), class_Male = sum(class_Male), class_Female = sum(class_Female))
all$difference <- (all$Funded_Male / all$class_Male) - (all$Funded_Female / all$class_Female)
rank_class <- ggplot(all, aes(x = difference, y = reorder(Classification, difference))) +
            geom_bar(stat = "identity", position = "dodge")+
            theme_bw() +
            labs(x = "Bias", y = "Classifications")

# ranking for universities
unis <- uni %>% group_by(LeadInstitution) %>% summarise(Funded_Male = sum(Funded_Male), Funded_Female = sum(Funded_Female), uni_Male = sum(uni_Male), uni_Female = sum(uni_Female))
unis$difference <- (unis$Funded_Male / unis$uni_Male) - (unis$Funded_Female / unis$uni_Female)
unis <- unis %>% filter(LeadInstitution %in% c("University of Liverpool", "University of Manchester", "University of Leeds",
                "University of Glasgow", "Imperial College London", "University College London",
                "University of Sheffield", "University of Cambridge", "University of Oxford",
                "University of Edinburgh", "University of Warwick", "King's College London"))
rank_uni <- ggplot(unis, aes(x = difference, y = reorder(LeadInstitution, difference))) +
            geom_bar(stat = "identity", position = "dodge")+
            theme_bw() +
            labs(x = "Bias", y = "Universities")