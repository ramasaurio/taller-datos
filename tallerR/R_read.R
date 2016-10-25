# # Data de copas del mundo
# 
# ## el problema hasta ahora es que no logro ordenarlos en una tabla, el separador es confuso!
# folders<-list.files(path = "world-cup")
# for (i in 1:20)
# {
#         x<-read.table(paste0(getwd(),"/world-cup/",folders[i],"/cup.txt"), sep="\t", 
#                               encoding = "UTF-8", comment.char = "#")
#         assign(paste0('data', folders[i]),x)
# }


# Data de jugadores (y partidos de ligas europeas) from: https://www.kaggle.com/hugomathien/soccer/
# son datos desde 2007 para stats de jugadores
library(RSQLite)
library(dplyr)

con <- dbConnect(SQLite(), dbname=paste0(getwd(),"/../Dataset/database.sqlite"))
dbListTables(con)

player       <- tbl_df(dbGetQuery(con,"SELECT * FROM player"))
player_stats <- tbl_df(dbGetQuery(con,"SELECT * FROM player_stats"))
Match        <- tbl_df(dbGetQuery(con,"SELECT * FROM Match"))
Team         <- tbl_df(dbGetQuery(con,"SELECT * FROM Team"))
Country      <- tbl_df(dbGetQuery(con,"SELECT * FROM Country"))
League       <- tbl_df(dbGetQuery(con,"SELECT * FROM League"))
SQLite       <- tbl_df(dbGetQuery(con,"SELECT * FROM sqlite_sequence"))

consulta = 
"SELECT player_name, height, weight, overall_rating, potential, finishing
FROM player
JOIN player_stats
ON player.player_api_id = player_stats.player_api_id
WHERE player_name like '%ingham%'
GROUP BY player_name"

a<-tbl_df(dbGetQuery(con,consulta))
tail(player)
tail(player_stats)
player_stat_final <- tbl_df(dbGetQuery(con, "SELECT DISTINCT player_fifa_api_id FROM player_stats"))
player_stat_final
# Este c?digo lo saqu? del sitio Kaggle. Hay un ejemplo de como calcular el promedio de FIFA rating para cada equipo en cada partido
write.table(player, file="players.csv", sep=",", row.names=FALSE)
write.table(match, file="matches.csv", sep=",", row.names=FALSE)

