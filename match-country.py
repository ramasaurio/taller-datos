from player import FifaPlayer
from nacionalidad import getPlayersFifa
from match import Match, Matches


def run():
    playerCountryPath = 'Dataset/jugadores_con_pais.csv'
    playerPath = 'tallerR/players.csv'
    matchPath = 'tallerR/matches_no_xml.csv'

    # Para leer y guardar los partidos
    homePlayers = []
    awayPlayers = []
    for i in range(11):
        homePlayers.append('home_player_' + str(i + 1))
        awayPlayers.append('away_player_' + str(i + 1))
    matches = Matches(matchPath, idM='id', league='league_id', date='date', home=homePlayers, away=awayPlayers)
    print('Cantidad de partidos:', len(matches))

    # Para leer y guardar los datos de los jugadores
    fifaPlayersById = {}
    fifaPlayers = getPlayersFifa(playerPath)
    for player in fifaPlayers:
        fifaPlayersById[player.idapi] = player
    print('Cantidad de jugadores:', len(fifaPlayersById))

    # Para leer y guardar los datos de los paises
    countryByPlayerId = {}
    countryFile = open(playerCountryPath, 'r')
    countryFile.readline()
    for line in countryFile:
        line = line.replace('\n', '').replace('\r', '').replace('"', '').split(',')
        idapi = int(line[0])
        countryByPlayerId[idapi] = (line[1], line[2])
    print('Jugadores con país:', len(countryByPlayerId))

    for playerid in fifaPlayersById:
        if playerid in countryByPlayerId:
            fifaPlayersById[playerid].country = countryByPlayerId[playerid][1]
        else:
            fifaPlayersById[playerid].country = 'Desconocido'


if __name__ == '__main__':
    # matchPath = 'tallerR/matches_full.csv'
    # inf = open(matchPath, 'r')
    # print(inf.readline().split(','))
    # print(inf.readline().split(',')[5])
    # # print(inf.readline().split(','))

    run()
