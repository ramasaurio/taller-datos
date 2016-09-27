# -*- coding: utf-8 -*-
from player import Player, FifaPlayer
from country import Country
import math


def assignCountry():

    # Todos los jugadores de dbpedia que nacieron después de 1967
    # y que han jugado en clubes de España, Italia, Alemania o Inglaterra
    players = getPlayers('Dataset/Nacionalidades/england-players.csv')
    players.extend(getPlayers('Dataset/Nacionalidades/england-players2.csv'))
    players.extend(getPlayers('Dataset/Nacionalidades/italy-players.csv'))
    players.extend(getPlayers('Dataset/Nacionalidades/italy-players2.csv'))
    players.extend(getPlayers('Dataset/Nacionalidades/germany-players.csv'))
    players.extend(getPlayers('Dataset/Nacionalidades/germany-players2.csv'))
    players.extend(getPlayers('Dataset/Nacionalidades/spain-players.csv'))
    players.extend(getPlayers('Dataset/Nacionalidades/spain-players2.csv'))
    players.extend(getPlayers('Dataset/Nacionalidades/bundesliga_players.csv'))
    players.extend(getPlayers('Dataset/Nacionalidades/serieA_players.csv'))
    players.extend(getPlayers('Dataset/Nacionalidades/premierleague_players.csv'))
    players.extend(getPlayers('Dataset/Nacionalidades/laliga_players.csv'))

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

    # playerIds = getFifaPlayersInLeagues()
    playerIds = getFifaPlayersByLeagues()
    print('players Ids:', len(playerIds))
    playersFifa = []
    for fplayer in allPlayersFifa:
        if fplayer.idapi in playerIds:
            prem, bund, serie, spa = playerIds[fplayer.idapi]
            fplayer.premier = prem
            fplayer.bundes = bund
            fplayer.seriea = serie
            fplayer.spain = spa
            playersFifa.append(fplayer)
    print('playersFifa', len(playersFifa))

    # contadores para los match
    counter = 0

    playernocountry = []
    for fplayer in playersFifa:

        words = fplayer.name.split(' ')
        tocayoplayers = []
        for playername in playersByName:
            # if not hasattr(fplayer, 'country'):
            if all([word in playername for word in words]):

                # se verifica que la fecha de nacimiento sea la misma
                potp = playersByName[playername]
                days = 0
                if potp.byear is not None:
                    days += (potp.byear - fplayer.byear) * 365
                if potp.bmonth is not None:
                    days += (potp.bmonth - fplayer.bmonth) * 30
                if potp.bday is not None:
                    days += potp.bday - fplayer.bday
                tocayoplayers.append((potp, math.fabs(days)))

        if len(tocayoplayers) > 0:
            tocayoplayers = sorted(tocayoplayers, key=lambda pl: pl[1])
            fplayer.country = tocayoplayers[0][0].country.replace('_', ' ')
            counter += 1

        # jugadores que no tuvieron match
        if not hasattr(fplayer, 'country'):
            playernocountry.append(fplayer)

    print(counter)
    print(len(playernocountry))
    for player in playernocountry:
        print(player.name)

    writeFifaPlayers('jugadores-con-pais.csv', [p for p in playersFifa if hasattr(p, 'country')])


def writeFifaPlayers(path, playersFifa):

    fwriter = open(path, 'w')
    fwriter.write('id,name,country,age,premier,bundes,seriea,spain\n')
    lineskel = '%d,%s,%s,%i,%d,%d,%d,%d\n'

    for player in playersFifa:
        line = player.idapi, player.name, player.country, player.age, player.premier, player.bundes, player.seriea, player.spain
        fwriter.write(lineskel % line)
        fwriter.flush()

    fwriter.close()


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
            players.add(int(line.replace('\n', '')))

    except FileNotFoundError:
        players = writeFifaPlayersInLeagues()

    return players


def getFifaPlayersByLeagues():

    players = {}

    try:
        infile = open('Dataset/players_by_league.csv', 'r')
        infile.readline()
        for line in infile:
            pid, premier, bundes, seriea, spain = line.replace('\n', '').split(',')
            players[int(pid)] = int(premier), int(bundes), int(seriea), int(spain)
        infile.close()

    except FileNotFoundError:
        players = writeFifaPlayersByLeagues()

    return players


def writeFifaPlayersByLeagues():
    """
    lee los id de los jugadores de los partidos de las ligas y escribe en un archivo los distintos IDs
    :return: conjunto con los distintos IDs de los jugadores de los partidos
    """

    playerIds = {}

    premierpath = 'tallerR/premierplayers.csv'
    bundespath = 'tallerR/bundesplayers.csv'
    serieapath = 'tallerR/serieaplayers.csv'
    spainpath = 'tallerR/spainplayers.csv'
    paths = [premierpath, bundespath, serieapath, spainpath]
    leagues = ['premier', 'bundes', 'seriea', 'spain']

    for path, league in zip(paths, leagues):

        infile = open(path, 'r')
        infile.readline()

        for line in infile:
            ids = line.replace('\n', '').split(',')
            for pid in ids:
                if pid != 'NA':
                    if pid in playerIds:
                        playerIds[pid].add(league)
                    else:
                        playerIds[pid] = {league}
        infile.close()

    outfile = open('Dataset/players_by_league.csv', 'w')
    outfile.write('id,premier,bundes,seriea,spain\n')
    lineskel = '%d,%d,%d,%d,%d\n'
    players = {}

    for pid in playerIds:
        player = playerIds[pid]
        prem = 1 if 'premier' in player else 0
        bund = 1 if 'bundes' in player else 0
        serie = 1 if 'seriea' in player else 0
        spain = 1 if 'spain' in player else 0
        line = int(pid), prem, bund, serie, spain
        outfile.write(lineskel % line)
        outfile.flush()
        players[pid] = prem, bund, serie, spain
    outfile.close()

    return players


def matchCountryCoords(players):

    infile = open('Dataset/countries.csv', 'r')
    infile.readline()
    countries = []

    for line in infile:
        values = line.replace('\n', '').split(',')
        country = Country(values)
        countries.append(country)

    for player in players:
        country = player.country
        country = country.replace('_', '')


def readFullPlayers():

    infile = open('jugadores_con_pais.csv', 'r')
    infile.readline()
    players = []

    for line in infile:
        idapi, name, country, age, premier, bundes, seriea, spain = line.replace('\n', '').split(',')
        players.append(FifaPlayer(idapi=idapi, name=name, country=country, age=age, premier=premier, bundes=bundes,
                                  seriea=seriea, spain=spain))

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
    assignCountry()

    readFullPlayers()
    matchCountryCoords(players)
