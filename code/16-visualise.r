# This script performs the visualisation of the results.
# The following packages are needed: ggplot2; tidyverse; tidyr; reshape2; gridExtra; cowplot.
# install the package
# install.packages("ggplot2")
# install.packages("tidyverse")
# install.packages("tidyr")
# install.packages("reshape2")
# install.packages("gridExtra")
# install.packages("ggpubr")
# install.packages("stringr")
# install.packages("dplyr")
# author: Xuan Wang


# load the package
library(ggplot2)
library(tidyr)
library(reshape2)
library(gridExtra)
library(ggpubr)
library(stringr)
library(dplyr)
library(cowplot)
library(grid)
# read the dataset
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

# plot the graph
# depending on classification
classifications <- unique(subject$Classification)
combined <- ggplot(subject) + geom_smooth(aes(x = Year, y = ratio_Male, color = 'Male')) +
            geom_smooth(aes(x = Year, y = ratio_Female, color = 'Female')) +
            theme_bw() +
            theme(aspect.ratio = 0.6,
                strip.text = element_text(size = 5),
                axis.text = element_text(size = 6)) +
            facet_wrap(.~Classification, scales = "free") +
            labs(x = "Year", y = "Proportion of each gender getting funded", title = "The proportion funded in each classification")

# depending on university
university <- unique(uni$LeadInstitution)
plot_uni <- list()
uni_long <- gather(uni, Gender, Ratio, ratio_Male, ratio_Female)
uni_long$Gender <- factor(uni_long$Gender, levels = c("ratio_Male", "ratio_Female"), labels = c("Male", "Female"))

for (each in university){
    data_uni <- subset(uni_long, LeadInstitution == each)

    m <- ggplot(data_uni, aes(x = Year, y = Ratio, color = Classification)) +
        geom_line() +
        facet_wrap(~Gender, nrow = 1, scales = "fixed") +
        ylim(0, 0.0075)+
        labs(x = "", y = "", color = NULL, title = paste(each)) +
        theme_bw() +
        theme(legend.position = "none", 
            plot.title = element_text(hjust = 0.5, size = 7),
            axis.text.x = element_text(angle = 55, hjust = 1, size = 6),
            axis.text.y = element_text(size = 6),
            strip.text = element_text(size = 7, margin = margin(2, 0, 2, 0)),
            legend.text = element_text(size = 8),
            legend.spacing.x = unit(0.02, "cm")) +
        guides(color = guide_legend(ncol = 3))
    
    plot_uni[[each]] <- m
}

selected_uni <- plot_uni[c(7, 14, 55, 19, 21, 24, 26, 28, 29, 31, 34, 39)]

legend_plot <- ggplot(uni_long, aes(x = Year, y = Ratio, color = Classification)) +
  geom_line() +
  guides(color = guide_legend(ncol = 3, keywidth = unit(0.8, "cm"), keyheight = unit(0.5, "cm")))

legend <- get_legend(legend_plot)
grid.draw(legend)
# funded male and female in 2015 ~ 2022
all <- subject %>% group_by(Classification) %>% summarise(Funded_Male = sum(Funded_Male), Funded_Female = sum(Funded_Female))
all <- melt(all, variable.name = "Gender", value.name = "Number")
all_plot <- ggplot(all, aes(x = Classification, y = Number, fill = Gender)) +
            geom_bar(stat = "identity", position = "dodge") +
            theme_bw() +
            theme(axis.text.x = element_text(angle = 55, hjust = 1, size = 6)) +
            labs(y = "Number of research getting funded", title = "The total number getting funded in each gender from 2015 to 2022")


# save the plots
pdf('./results/plots_classification.pdf')
print(combined)
graphics.off()


pdf('./results/plots_uni.pdf', width = 8)
print(plot_uni)
plot.new()
graphics.off()

pdf('./results/uni_selected.pdf')
grid.arrange(grobs = selected_uni, ncol = 4)
graphics.off()

pdf('./results/legend.pdf', width = 10, height=3)
grid.draw(legend)
graphics.off()

pdf('./results/plots_all.pdf')
print(all_plot)
graphics.off()

