
library(RSQLite)
library(dplyr)

con <- dbConnect(SQLite(), dbname=paste0(getwd(),"/../Dataset/database.sqlite"))
dbListTables(con)
player <- tbl_df(dbGetQuery(con,"SELECT * FROM player"))
head(player)
nacimiento <- tbl_df(dbGetQuery(con,"SELECT player_name, birthday FROM player"))
head(nacimiento)
nac = nacimiento[order(nacimiento$birthday),]

match <- tbl_df(dbGetQuery(con,"SELECT * FROM Match"))
league = tbl_df(dbGetQuery(con,"SELECT * FROM League"))

leaguematches = match[(match$league_id == 1729 | match$league_id == 7775 | match$league_id == 10223 | match$league_id == 21484),]

premiermatches = match[match$league_id == 1729,]
bundesmatches = match[match$league_id == 7775,]
serieamatches = match[match$league_id == 10223,]
spainmatches = match[match$league_id == 21484,]

columnas = c(4,56:77)
premierplayers = premiermatches[,columnas]
bundesplayers = bundesmatches[,columnas]
serieaplayers = serieamatches[,columnas]
spainplayers = spainmatches[,columnas]

write.table(premierplayers, file="premierplayers2.csv", sep=",", row.names=FALSE)
write.table(bundesplayers, file="bundesplayers2.csv", sep=",", row.names=FALSE)
write.table(serieaplayers, file="serieaplayers2.csv", sep=",", row.names=FALSE)
write.table(spainplayers, file="spainplayers2.csv", sep=",", row.names=FALSE)


head(premierplayers)

names(leaguematches)
leaguematches[1:2,]
head(leaguematches)

aleix = tbl_df(dbGetQuery(con, "SELECT * FROM player WHERE player_name like '%neil%'"))
aleix

leagueplayers = leaguematches[,columnas]
write.table(leagueplayers, file="league-players.csv", sep=",", row.names=FALSE)
write.table(leagueplayers, file="total-players.csv", sep=",", row.names=FALSE)


playerids = read.csv("player_ids_in_leagues.csv", header=FALSE)
playerids
matched = player$player_api_id %in% playerids[,1]

# Chequeo para ver is encontró los 4952
counter = 0
for (i in 1:length(matched)){
  if (matched[i]){
    counter = counter+1
  }
}
counter

playerinleagues = player[matched,]
write.table(playerinleagues, file="players_in_leagues_table.csv", sep=",", row.names=FALSE)

player[player$player_api_id == 26223,]
head(match$season)
match$season
names(match)
