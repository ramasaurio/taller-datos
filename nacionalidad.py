# -*- coding: utf-8 -*-
from player import Player, FifaPlayer


def run():

    # Todos los jugadores de dbpedia que nacieron después de 1967
    # y que han jugado en clubes de España, Italia, Alemania o Inglaterra
    players = getPlayers('Dataset/Nacionalidades/england-players.csv')
    players.extend(getPlayers('Dataset/Nacionalidades/england-players2.csv'))
    players.extend(getPlayers('Dataset/Nacionalidades/italy-players.csv'))
    players.extend(getPlayers('Dataset/Nacionalidades/germany-players.csv'))
    players.extend(getPlayers('Dataset/Nacionalidades/spain-players.csv'))

    # Todos los jugadores con distintos nombres completos
    playersByName = {}
    for player in players:
        if player.fullname not in playersByName:
            playersByName[player.fullname] = player
        elif ',' not in player.name:
            playersByName[player.fullname] = player
    print('total players:', len(playersByName))

    allPlayersFifa = getPlayersFifa('Dataset/Nacionalidades/players.csv', ',')
    print('total fifa players:', len(allPlayersFifa))

    playerIds = getFifaPlayersInLeagues()
    print('players Ids:', len(playerIds))

    playersFifa = [player for player in allPlayersFifa if player.idapi in playerIds]
    print('playersFifa', len(playersFifa))

    # Comienza el matcheo
    counter = 0
    counter2 = 0
    playernocountry = []
    for fplayer in playersFifa:
        words = fplayer.name.split(' ')
        for playername in playersByName:
            if not hasattr(fplayer, 'country'):
                if all([word in playername for word in words]):
                    fplayer.country = playersByName[playername].country
                    counter += 1
        if not hasattr(fplayer, 'country'):
            counter2 += 1
            playernocountry.append(fplayer)
            # print(fplayer.name)

    print(counter)
    print(counter2)
    for player in playernocountry:
        print(player.name)


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


def getFifaPlayersInLeagues():

    players = set()

    try:
        infile = open('Dataset/player_ids_in_leagues.csv', 'r')
        for line in infile:
            players = players.union([int(line.replace('\n', ''))])

    except FileNotFoundError:
        players = writeFifaPlayersInLeagues()

    return players


def writeFifaPlayersInLeagues():
    """
    lee los id de los jugadores de los partidos de las ligas y escribe en un archivo los distintos IDs
    :return: conjunto con los distintos IDs de los jugadores de los partidos
    """

    infile = open('tallerR/league-players.csv', 'r')
    infile.readline()
    playerIds = set()

    for line in infile:
        ids = line.replace('\n', '').split(',')
        for pid in ids:
            if pid != 'NA':
                playerIds = playerIds.union([int(pid)])

    outfile = open('Dataset/player_ids_in_leagues.csv', 'w')
    for pid in playerIds:
        outfile.write('%s\n' % pid)
        outfile.flush()

    outfile.close()
    infile.close()

    return playerIds


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
        values = line.replace('\n', '').replace('\r', '').replace('"', '').split(sep)
        if len(values) == 7:
            _, idapi, name, idapififa, bday, _, _ = values
        else:
            _, idapi, name, _, idapififa, bday, _, _ = values
        players.append(FifaPlayer(idapi, name, idapififa, bday))

    infile.close()
    return players


def checkWeirdLetters(path, sep=';'):
    infile = open(path, mode='r', encoding='utf-8')
    infile.readline()
    weirdLetters = set()

    for line in infile:
        name, fullname, _, _ = line.replace('\n', '').replace('\r', '').replace(', Jr', ' Jr').split(sep)
        # weirdLetters = weirdLetters.union(name)
        if '/' in fullname:
            print(fullname)
        fullname = fullname.lower()
        fullnamea = fullname.replace('á', 'a').replace('ā', 'a').replace('å', 'a').replace('ä', 'a').replace('â', 'a')
        fullnamea = fullnamea.replace('à', 'a').replace('ã', 'a').replace('ă', 'a').replace('ą', 'a')
        fullnamea = fullnamea.replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('ę', 'e')
        fullnamea = fullnamea.replace('ě', 'e').replace('ё', 'e').replace('ë', 'e').replace('ė', 'e')
        fullnamea = fullnamea.replace('í', 'i').replace('ì', 'i').replace('ï', 'i').replace('î', 'i').replace('õ', 'o')
        fullnamea = fullnamea.replace('ó', 'o').replace('ò', 'o').replace('ö', 'o').replace('ô', 'o').replace('ő', 'o')
        fullnamea = fullnamea.replace('ú', 'u').replace('ù', 'u').replace('ü', 'u').replace('û', 'u').replace('ū', 'u')
        fullnamea = fullnamea.replace('č', 'c').replace('ć', 'c').replace('ç', 'c')
        fullnamea = fullnamea.replace('š', 's').replace('ş', 's').replace('ś', 's').replace('ș', 's')
        fullnamea = fullnamea.replace('ž', 'z').replace('ż', 'z').replace('ź', 'z')
        fullnamea = fullnamea.replace('ń', 'n').replace('ņ', 'n').replace('ň', 'n')
        fullnamea = fullnamea.replace('ý', 'y')
        fullnamea = fullnamea.replace('ğ', 'g')
        fullnamea = fullnamea.replace('ř', 'r').replace('/', '')
        fullnamea = fullnamea.replace(' ', '').replace("'", "").replace('’', '').replace(',', '').replace('–', '-')
        weirdLetters = weirdLetters.union(fullnamea)
    aux = weirdLetters.difference('qwertyuiopasdfghjklzxcvbnñmQWERTYUIOPLKJHGFDSAZXCVBNÑM-')
    for char in aux:
        print(char)
    print(len(aux))

    infile.close()

if __name__ == '__main__':
    run()

    # checkWeirdLetters('Dataset/Nacionalidades/england-players.csv')
    # checkWeirdLetters('Dataset/Nacionalidades/italy-players.csv')
    # checkWeirdLetters('Dataset/Nacionalidades/germany-players.csv')
    # checkWeirdLetters('Dataset/Nacionalidades/spain-players.csv')
