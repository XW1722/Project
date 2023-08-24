# This script includes the generation of the first plot in the report, which displays the funding pattern across time.

library(ggplot2)
library(tidyr)
library(reshape2)
library(gridExtra)
library(ggpubr)
library(stringr)
library(dplyr)
library(cowplot)
library(grid)

df_2015 = read.csv('./results/final_data/final_data_2015.csv')
df_2016 = read.csv('./results/final_data/final_data_2016.csv')
df_2017 = read.csv('./results/final_data/final_data_2017.csv')
df_2018 = read.csv('./results/final_data/final_data_2018.csv')
df_2019 = read.csv('./results/final_data/final_data_2019.csv')
df_2020 = read.csv('./results/final_data/final_data_2020.csv')
df_2021 = read.csv('./results/final_data/final_data_2021.csv')
df_2022 = read.csv('./results/final_data/final_data_2022.csv')

funding_2015 <- df_2015 %>% group_by(gender, Classification) %>% summarise(FundingAmount = sum(FundingAmount))
funding_2016 <- df_2016 %>% group_by(gender, Classification) %>% summarise(FundingAmount = sum(FundingAmount))
funding_2017 <- df_2017 %>% group_by(gender, Classification) %>% summarise(FundingAmount = sum(FundingAmount))
funding_2018 <- df_2018 %>% group_by(gender, Classification) %>% summarise(FundingAmount = sum(FundingAmount))
funding_2019 <- df_2019 %>% group_by(gender, Classification) %>% summarise(FundingAmount = sum(FundingAmount))
funding_2020 <- df_2020 %>% group_by(gender, Classification) %>% summarise(FundingAmount = sum(FundingAmount))
funding_2021 <- df_2021 %>% group_by(gender, Classification) %>% summarise(FundingAmount = sum(FundingAmount))
funding_2022 <- df_2022 %>% group_by(gender, Classification) %>% summarise(FundingAmount = sum(FundingAmount))

funding_2015$Year = '2015'
funding_2016$Year = '2016'
funding_2017$Year = '2017'
funding_2018$Year = '2018'
funding_2019$Year = '2019'
funding_2020$Year = '2020'
funding_2021$Year = '2021'
funding_2022$Year = '2022'

funding_all <- rbind(funding_2015, funding_2016, funding_2017, funding_2018, funding_2019, funding_2020, funding_2021, funding_2022)

funding_all <- filter(funding_all, gender != 'unknown')
funding_all$Classification <- tools::toTitleCase(funding_all$Classification)
funding_all$Classification <- gsub("It,", "IT,", funding_all$Classification)


plot_all <- ggplot(funding_all, aes(x = Classification, y = FundingAmount, fill = gender)) +
            geom_bar(stat = "identity", position = "dodge") +
            facet_wrap(~Year, ncol = 2) +
            theme_bw() +
            theme(axis.text.x = element_text(angle = 55, hjust = 1, size = 5), 
                strip.text.x = element_text(size = 10))


pdf('./results/funding_all.pdf')
print(plot_all)
graphics.off()

# hypothesis testing
funding_male <- filter(funding_all, gender == 'male')
funding_male <- funding_male %>% pull(FundingAmount)
funding_female <- filter(funding_all, gender == 'female')
funding_female <- funding_female %>% pull(FundingAmount)

result <- t.test(funding_male, funding_female)
