library(tidyverse)
library(modelr)
library(httpgd)
hgd()

df <- read_csv('/home/dantegrassi/introduction-to-data-science-final-project/datasets/S&P+500+Stock+Prices+2014-2017.csv/S&P 500 Stock Prices 2014-2017_formatted.csv')

view(df)

sum(is.na(df))
colSums((is.na(df)))

# ggplot(df, aes(x=high, y=close, color=day)) +
#   geom_point(alpha=0.5)
