# -*- coding: utf-8 -*-

from player import Player


def run():

    # # Todos los jugadores de dbpedia que nacieron después de 1967
    # # y que han jugado en clubes de España, Italia, Alemania o Inglaterra
    # players = getPlayers('Dataset/Nacionalidades/england-players.csv')
    # players.extend(getPlayers('Dataset/Nacionalidades/italy-players.csv'))
    # players.extend(getPlayers('Dataset/Nacionalidades/germany-players.csv'))
    # players.extend(getPlayers('Dataset/Nacionalidades/spain-players.csv'))
    # print(len(players))
    #
    # # Todos los jugadores con distintos nombres completos
    # playersByName = {}
    # for player in players:
    #     if player.fullname not in playersByName:
    #         playersByName[player.fullname] = player
    #     elif ',' not in player.name:
    #         playersByName[player.fullname] = player
    # print(len(playersByName))

    playersFifa = getPlayersFifa('Dataset/Nacionalidades/players.csv', ',')
    print(len(playersFifa))


def test():
    englandplayers = getPlayers('Dataset/Nacionalidades/england-teams.csv')
    italyplayers = getPlayers('Dataset/Nacionalidades/italy-teams.csv')
    germanyplayers = getPlayers('Dataset/Nacionalidades/germany-teams.csv')
    spainplayers = getPlayers('Dataset/Nacionalidades/spanish-teams.csv')
    englandplayers2 = getPlayers('Dataset/Nacionalidades/england-teams2.csv')
    italyplayers2 = getPlayers('Dataset/Nacionalidades/italy-teams2.csv')
    germanyplayers2 = getPlayers('Dataset/Nacionalidades/germany-teams2.csv')
    spainplayers2 = getPlayers('Dataset/Nacionalidades/spanish-teams2.csv')

    englandDict = {}
    italyDict = {}
    germanyDict = {}
    spainDict = {}

    for player in englandplayers:
        if player.name not in englandDict:
            englandDict[player.name] = player
    for player in englandplayers2:
        if player.name not in englandDict:
            englandDict[player.name] = player

    for player in italyplayers:
        if player.name not in italyDict:
            italyDict[player.name] = player
    for player in italyplayers2:
        if player.name not in italyDict:
            italyDict[player.name] = player

    for player in germanyplayers:
        if player.name not in germanyDict:
            germanyDict[player.name] = player
    for player in germanyplayers2:
        if player.name not in germanyDict:
            germanyDict[player.name] = player

    for player in spainplayers:
        if player.name not in spainDict:
            spainDict[player.name] = player
    for player in spainplayers2:
        if player.name not in spainDict:
            spainDict[player.name] = player

    print('Inglaterra: %d %d' % (len(englandplayers), len(englandDict)))
    print('Italia: %d %d' % (len(italyplayers), len(italyDict)))
    print('Alemania: %d %d' % (len(germanyplayers), len(germanyDict)))
    print('España: %d %d' % (len(spainplayers), len(spainDict)))

    totalDict = {}
    for name in englandDict:
        player = englandDict[name]
        if player.name not in totalDict:
            totalDict[player.name] = player
    for name in italyDict:
        player = italyDict[name]
        if player.name not in totalDict:
            totalDict[player.name] = player
    for name in germanyDict:
        player = germanyDict[name]
        if player.name not in totalDict:
            totalDict[player.name] = player
    for name in spainDict:
        player = spainDict[name]
        if player.name not in totalDict:
            totalDict[player.name] = player

    print(len(englandDict) + len(italyDict) + len(germanyDict) + len(spainDict))
    print(len(totalDict))


def getPlayers(path, sep=';'):

    infile = open(path, mode='r', encoding='utf-8')
    infile.readline()
    players = []
    for line in infile:
        try:
            name, fullname, country, bday = line.replace('\n', '').replace('\r', '').replace(', Jr', ' Jr').split(sep)
            players.append(Player(name, fullname, country, bday))
        except ValueError:
            print(line)

    infile.close()
    return players


# "id", "player_api_id", "player_name"       , "player_fifa_api_id", "birthday"           ,"height","weight"
#  1  , 505942         , "Aaron Appindangoye", 218353              , "1992-02-29 00:00:00",182.88  ,187

def getPlayersFifa(path, sep=','):
    infile = open(path, mode='r', encoding='utf-8')
    infile.readline()
    players = []
    for line in infile:
        try:
            _, idapi, name, idapififa, bday, _, _ = line.replace('\n', '').replace('\r', '').split(sep)
        except ValueError:
            print(line)

    infile.close()
    return players


if __name__ == '__main__':
    run()
