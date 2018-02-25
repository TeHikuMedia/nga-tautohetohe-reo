# Load in the required libraries
library(data.table)
library(stringr)
library(ggplot2)
library(scales)

# Plot Māori words as a proportion of the total words
days <- fread('../hansardrāindex.csv')
days[ , year := as.integer(str_match(date2, '[12][0-9]{3}')[, 1])]

# Note: The following commented out code is for the csv output files from a previous version of the scraping scripts.

# Some years are incorrect. Remove any years that are outside of the range,
# This could be improved.
# days[year < 1854, year := NA]
# days[year > 2018, year := NA]

# Some years are missing, due to OCR issues. Simply fill in from the rows above.
# This could be improved, but is good enough for a plot.
# while(sum(is.na(days$year))){
#     x <- which(is.na(days$year))
#     days$year[x] <- days$year[x-1]
# }

years <- days[, .(.N, reo=sum(reo),ambiguous=sum(ambiguous), other=sum(other)), by=year][year < 2018]

#g <- ggplot(years, aes(x=year, y = reo/(reo+other+ambiguous))) + 
#     geom_bar(fill='#DB2850', stat='identity', width=1) + 
#     scale_x_continuous(breaks=seq(1860, 2010, by=10), expand=c(0, 0), limits=c(1850, 2020)) +
#     scale_y_continuous(labels=percent,expand=c(0,0), limits=c(0, 0.03)) +
#     theme_bw() +
#     ylab('Te Reo words (percentage of total)') +
#     xlab('Year') +
#     theme(panel.grid.major.x = element_blank(), panel.grid.minor = element_blank())
#ggsave(g, width=30, height=10, unit='cm', filename='reo-by-year.png')
#

# Repeat, but restricting to reo that was in speeches with at least 10 non-ambiguous Māori words.
reo <- fread('../hansardreomāori.csv')
reo[ , year := as.integer(str_match(date2, '[12][0-9]{3}')[, 1])]
# reo[ , year := as.integer(str_match(date, '(18|19|20)[0-9]{2}')[, 1])]

# Some years are incorrect. Remove any years that are outside of the range,
# This could be improved.
# reo[year < 1854, year := NA]
# reo[year > 2018, year := NA]

# Some years are missing, due to OCR issues. Simply fill in from the rows above.
# This could be improved, but is good enough for a plot.
# while(sum(is.na(reo$year))){
#     x <- which(is.na(reo$year))
#     reo$year[x] <- days$year[x-1]
# }

# reo_by_year <- reo[reo>10, .(reo_speeches=sum(reo)), by=year]
koreromaori_by_year <- reo[percent>=70, .(reo_speeches=sum(reo)+sum(ambiguous)), by=year]
years <- merge(years, koreromaori_by_year, by='year', all.x=T)

g <- ggplot(years, aes(x=year, y = reo_speeches/(reo+other+ambiguous))) + 
     geom_bar(fill='#DB2850', stat='identity', width=1) + 
     scale_x_continuous(breaks=seq(1860, 2010, by=10), expand=c(0, 0), limits=c(1850, 2020)) +
     scale_y_continuous(labels=percent,expand=c(0,0), limits=c(-0.0002, 0.025)) +
     theme_bw() +
     ylab('Te Reo Māori spoken in parliament') +
     xlab('Year') +
     theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.border = element_blank())
ggsave(g, width=20, height=12, unit='cm', filename='reo-speeches-by-year.png')

g <- ggplot(years, aes(x=year, y = reo/(reo+other))) + 
  geom_bar(fill='#DB2850', stat='identity', width=1) + 
  scale_x_continuous(breaks=seq(1860, 2010, by=10), expand=c(0, 0), limits=c(1850, 2020)) +
  scale_y_continuous(labels=percent,expand=c(0,0), limits=c(-0.0002, 0.03)) +
  theme_bw() +
  ylab('Māori words spoken in parliament') +
  xlab('Year') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.border = element_blank())
ggsave(g, width=20, height=12, unit='cm', filename='kupu-maori-by-year.png')