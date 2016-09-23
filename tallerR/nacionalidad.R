
library(RSQLite)
library(dplyr)

con <- dbConnect(SQLite(), dbname=paste0(getwd(),"/../Dataset/database.sqlite"))
dbListTables(con)
player       <- tbl_df(dbGetQuery(con,"SELECT * FROM player"))
head(player)
nacimiento <- tbl_df(dbGetQuery(con,"SELECT player_name, birthday FROM player"))
head(nacimiento)
nac = nacimiento[order(nacimiento$birthday),]
nrow(nac)
head(nac)
tail(nac)
