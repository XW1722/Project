# author: Xuan Wang
# date: 07 Jul 2024
library(ggplot2)
library(dplyr)
data <- read.csv('./results/subject-result/dist-class.csv')

df <- data[, c("Classification", "ratio_Female", "ratio_Male", "Year")]  

df$Classification <- tools::toTitleCase(df$Classification)
df$Classification <- gsub("It,", "IT,", df$Classification)
# 将数据框重塑为长格式，以便于ggplot2绘图  
df_plot_long <- reshape2::melt(df, id.vars = c("Classification", "Year"), variable.name = "Gender", value.name = "Ratio")  
  
# 绘制分组条形图  
df_dist <- ggplot(df_plot_long, aes(x = Year, y = Ratio, color = Gender, group = interaction(Classification, Gender))) +  
  geom_line() +  
  facet_wrap(~ Classification, scales = "free_x") +
  labs(x = "Year", y = "Ratio", color = "Gender", title = "Male and Female Ratios Across Classifications and Years") +  
  theme_minimal() +  
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 5.5),
        strip.text = element_text(size = 4),
        legend.title = element_text(size = 12),   
        legend.text = element_text(size = 10),
        plot.margin = unit(c(1, 1, 1, 5), "lines")) 

pdf('./results/distribution_year.pdf')
print(df_dist)
graphics.off()

df2 <- data[, c("Classification", "Funded_Female", "Funded_Male", "Year")]  

df2$Classification <- tools::toTitleCase(df2$Classification)
df2$Classification <- gsub("It,", "IT,", df2$Classification)
# 将数据框重塑为长格式，以便于ggplot2绘图  
df_plot_long_2 <- reshape2::melt(df2, id.vars = c("Classification", "Year"), variable.name = "Gender", value.name = "Funded")  
  
# 绘制分组条形图  
df_dist_2 <- ggplot(df_plot_long_2, aes(x = Year, y = Funded, color = Gender, group = interaction(Classification, Gender))) +  
  geom_line() +  
  facet_wrap(~ Classification, scales = "free_x") +
  labs(x = "Year", y = "Number of Each Gender Getting Funded", color = "Gender", title = "Funded Male and Female Across Classifications and Years") +  
  theme_minimal() +  
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 4),
        strip.text = element_text(size = 3),
        legend.title = element_text(size = 12),   
        legend.text = element_text(size = 10),
        plot.margin = unit(c(1, 1, 1, 5), "lines")) 
  
pdf('./results/distribution_year_number.pdf')
print(df_dist_2)
graphics.off()
