library(tidyverse)
library(modelr)
library(httpgd)
df1 <- read_csv("/home/dantegrassi/introduction-to-data-science-final-project/datasets/final_clean_jobs_dataset/exploration/final_clean_jobs_dataset.csv")

options(scipen = 999)

hgd()

view(df1)

glimpse(df1)

length(na.omit(df1$salary_avg))

df1salary <- df1 %>%
  filter(has_salary == TRUE)

df1notsalary <- df1 %>%
  filter(has_salary != TRUE)

# Forma correcta
ggplot(df1salary, aes(x = skills, y = salary_avg, color = country)) +
  geom_point(na.rm = TRUE)

library(dplyr)
df1_corregido <- df1 %>%
  mutate(salary_avg = ifelse(country == "India", salary_avg / 83.5, salary_avg))

df1_corregido %>%
  group_by(country) %>%
  summarise(avg_salary = mean(salary_avg, na.rm = TRUE))


ggplot(df1_corregido, aes(x = num_skills, y = salary_avg, color = country)) +
  geom_point(na.rm = TRUE)