# This script includes the generation of the first plot in the report, which displays the funding pattern across time.
# author = "Xuan Wang"
# date = "18 Jul 2023"
# contact = "xuan.wang22@imperial.ac.uk"

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
# add a column of year
df_2015$year <- 2015
df_2016$year <- 2016
df_2017$year <- 2017
df_2018$year <- 2018
df_2019$year <- 2019
df_2020$year <- 2020
df_2021$year <- 2021
df_2022$year <- 2022

data_combined <- rbind(df_2015, df_2016, df_2017, df_2018, df_2019, df_2020, df_2021, df_2022)
df <- data_combined[, c("Classification", "FundingAmount", "gender", "year", "class_Female", "class_Male")]  

print("Checking for NA values in FundingAmount column before summarization:")
print(sum(is.na(data_combined$FundingAmount)))
print("Rows with NA values in FundingAmount:")
print(data_combined[is.na(data_combined$FundingAmount), ])
funding_all <- data_combined %>% filter(gender != 'unknown') %>% group_by(gender, Classification) %>% summarise(MeanFundingAmount = mean(FundingAmount)) %>% ungroup()
df <- df %>% filter(gender != 'unknown') %>% group_by(gender, Classification, year) %>% summarise(AverageFundingAmount = mean(FundingAmount)) %>% ungroup()
df_plot_comparison <- reshape2::melt(funding_years, id.vars = c("Classification", "Year"), variable.name = "Gender", value.name = "Funding")  

write.csv(df, file = "./results/total_funding/mean_funding_years.csv")

# formatting
funding_all$Classification <- tools::toTitleCase(funding_all$Classification)
funding_all$Classification <- gsub("It,", "IT,", funding_all$Classification)
df$Classification<- tools::toTitleCase(df$Classification)
df$Classification <- gsub("It,", "IT,", df$Classification)

plot_all <- ggplot(funding_all, aes(x = Classification, y = MeanFundingAmount, fill = gender)) +
            geom_bar(stat = "identity", position = "dodge") +
            theme_bw() +
            theme(axis.text.x = element_text(angle = 60, hjust = 1, size = 8), 
                strip.text.x = element_text(size = 25)) +
            labs(y = "Mean of Funding Amount (GBP)")


pdf('./results/funding_all.pdf')
print(plot_all)
graphics.off()

df_plot <- reshape2::melt(df, id.vars = c("Classification", "year", "gender"), value.name = "AverageFundingAmount")  
df_plot <- df_plot[, c("Classification", "year", "gender", "AverageFundingAmount")]
  
# 绘制分组条形图  
df_comparison <- ggplot(df_plot, aes(x = year, y = AverageFundingAmount, fill = gender, group = interaction(Classification, gender))) +  
  geom_bar(stat = "identity", position = "dodge") +  
  facet_wrap(~ Classification, scales="free") +
  labs(x = "Year", y = "Mean of the Funding amount (GBP)", fill = "Gender", title = "Mean Funding Amount to Male and Female Across Classifications and Years") +  
  theme_minimal() +  
  theme(axis.text.x = element_text(angle = 50, hjust = 1, size = 6),
        strip.text = element_text(size = 4.5))

distribution_plot <- ggplot(df_plot, aes(x = AverageFundingAmount, fill = gender, color = gender)) +  
  geom_density(alpha = 0.5) +  
  facet_grid(Classification ~ ., scales = "free_y") + 
  labs(x = "Average Funding Amount (GBP)", fill = "Gender", color = "Gender",  
       title = "Distribution of Mean Funding Amount by Gender and Classification") +  
  theme_minimal() +  
  theme(legend.position = "bottom", 
        strip.text.x = element_text(angle = 0, size = 2),  
        panel.spacing = unit(0.5, "lines"),
        plot.margin = unit(c(1, 1, 1, 1), "cm")) 

pdf('./results/funding_comparison.pdf')
print(df_comparison)
graphics.off()

pdf('./results/distribution_plot_classified.pdf')
print(distribution_plot)
graphics.off()

# hypothesis testing
funding_male <- filter(funding_all, gender == 'male')
funding_male <- funding_male %>% pull(FundingAmount)
funding_female <- filter(funding_all, gender == 'female')
funding_female <- funding_female %>% pull(FundingAmount)

result <- t.test(funding_male, funding_female)

# Mann-Whitney
results <- list()

years <- 2015:2022

for (x in years) {
  funding_male <- filter(df, year == x, gender == male) %>% pull(FundingAmount)
  funding_female <- filter(data, year == x, gender == female) %>% pull(FundingAmount)
  
  test_result <- wilcox.test(male_ratios, female_ratios, alternative = "two.sided")
  
  results[[as.character(year)]] <- test_result
}

