library(tidyverse)
library(modelr)
library(httpgd)
hgd()

df <- read_csv('/home/dantegrassi/introduction-to-data-science-final-project/datasets/amazon/data/amazon_cleaned.csv')

view(df)

sum(is.na(df))
colSums((is.na(df)))

plot(df)

ggplot(df, aes(x=discount_percentage,y=actual_price)) +
  geom_point()
