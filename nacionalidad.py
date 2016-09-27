# -*- coding: utf-8 -*-
from player import Player, FifaPlayer, FullPlayer
from country import Country
import math
import numpy


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

    premierpath = 'tallerR/premierplayers2.csv'
    bundespath = 'tallerR/bundesplayers2.csv'
    serieapath = 'tallerR/serieaplayers2.csv'
    spainpath = 'tallerR/spainplayers2.csv'
    paths = [premierpath, bundespath, serieapath, spainpath]
    leagues = ['premier', 'bundes', 'seriea', 'spain']

    for path, league in zip(paths, leagues):

        infile = open(path, 'r')
        infile.readline()

        for line in infile:
            ids = line.replace('\n', '').split(',')
            season = ids[0]
            ids = ids[1:]
            for pid in ids:
                if pid != 'NA':
                    if (pid, season) in playerIds:
                        playerIds[(pid, season)].add(league)
                    else:
                        playerIds[(pid, season)] = {league}
        infile.close()

    outfile = open('Dataset/players_by_league.csv', 'w')
    outfile.write('id,premier,bundes,seriea,spain,season\n')
    lineskel = '%d,%d,%d,%d,%d,%d\n'
    players = {}

    for pid, season in playerIds:
        player = playerIds[(pid, season)]
        prem = 1 if 'premier' in player else 0
        bund = 1 if 'bundes' in player else 0
        serie = 1 if 'seriea' in player else 0
        spain = 1 if 'spain' in player else 0
        line = int(pid), prem, bund, serie, spain
        outfile.write(lineskel % line)
        outfile.flush()
        players[pid] = prem, bund, serie, spain, int(season[0:4])
    outfile.close()

    return players


def matchCountryCoords():

    players = []
    playerfile = open('jugadores_liga_pais.csv', 'r')
    playerfile.readline()
    for line in playerfile:
        idapi, name, country, age, league, season = line.replace('\n', '').split(',')
        players.append(FullPlayer(idapi, name, country, age, league, season))

    infile = open('Dataset/countries_mod.csv', 'r')
    infile.readline()
    countries = {}

    for line in infile:
        values = line.replace('\n', '').split(',')
        country = Country(values)
        countries[country.name] = country

    for player in players:
        if player.country in countries:
            player.lat = countries[player.country].lat
            player.lon = countries[player.country].lon
        else:
            print('no country for', player.name, player.country)

    return players


def matchCountryCoordsv2(players):

    infile = open('Dataset/countries_mod.csv', 'r')
    leagues = ['premier', 'bundes', 'seriea', 'spain']
    infile.readline()
    countries = {}
    finalTable = {}

    for line in infile:
        values = line.replace('\n', '').split(',')
        country = Country(values)
        countries[country.name] = country

    nocountryforoldman = []

    for player in players:
        pcountry = player.country
        if pcountry in countries:
            countryName = countries[pcountry].name
            for league in leagues:
                if player.__dict__[league]:
                    if (countryName, league) in finalTable:
                        finalTable[(countryName, league)].append(player.age)
                    else:
                        finalTable[(countryName, league)] = [player.age]
        else:
            nocountryforoldman.append((pcountry, player.name, player.idapi))

    for country, name, api in nocountryforoldman:
        print(country, name, api)

    outfile = open('tabla_final.csv', 'w')
    outfile.write('country,league,lat,long,age,players\n')
    lineskel = '%s,%s,%f,%f,%f,%d\n'

    for country in countries:
        for league in leagues:
            key = countries[country].name, league
            line = [countries[country].name, league, float(countries[country].lat), float(countries[country].lon)]
            if key in finalTable:
                line.extend([numpy.mean(finalTable[key]), len(finalTable[key])])
            else:
                line.extend([0, 0])
            outfile.write(lineskel % tuple(line))
            outfile.flush()


def readFullPlayers():

    infile = open('jugadores_con_pais.csv', 'r')
    infile.readline()
    players = []

    for line in infile:
        idapi, name, country, age, premier, bundes, seriea, spain = line.replace('\n', '').split(',')
        players.append(FifaPlayer(idapi=idapi, name=name, country=country, age=age, premier=int(premier),
                                  bundes=int(bundes), seriea=int(seriea), spain=int(spain)))

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


def readPlayersBySeasons():

    # Se leen y se guardan los jugadores con los paises
    countryfile = open('jugadores_con_pais_mod.csv', 'r')
    countryfile.readline()
    playersByIds = {}
    for line in countryfile:
        idapi, name, country, age, _, _, _, _ = line.replace('\n', '').split(',')
        playersByIds[int(idapi)] = name, country, int(age)
    countryfile.close()

    premierpath = 'tallerR/premierplayers2.csv'
    bundespath = 'tallerR/bundesplayers2.csv'
    serieapath = 'tallerR/serieaplayers2.csv'
    spainpath = 'tallerR/spainplayers2.csv'
    paths = [premierpath, bundespath, serieapath, spainpath]
    leagues = ['premier', 'bundes', 'seriea', 'spain']

    idseasonsleagues = set()
    for path, league in zip(paths, leagues):
        infile = open(path, 'r')
        infile.readline()
        for line in infile:
            ids = line.replace('\n', '').split(',')
            season = ids[0][1:5]
            ids = ids[1:]
            for pid in ids:
                if pid != 'NA':
                    idseasonsleagues.add((int(pid), int(season), league))

    seasonleaguesById = {}
    for idapi, season, league in idseasonsleagues:
        if idapi in seasonleaguesById:
            seasonleaguesById[idapi].append((season, league))
        else:
            seasonleaguesById[idapi] = [(season, league)]

    outfile = open('jugadores_liga_pais.csv', 'w')
    outfile.write('id,nombre,pais,edad,liga,temporada\n')
    lineskel = '%d,%s,%s,%d,%s,%d\n'
    for idapi in playersByIds:
        if idapi in seasonleaguesById:
            name, country, age = playersByIds[idapi]
            for season, league in seasonleaguesById[idapi]:
                ageaux = age + season - 2016
                line = idapi, name, country, ageaux, league, season
                outfile.write(lineskel % line)
                outfile.flush()
    outfile.close()


def run():
    players = readFullPlayers()
    matchCountryCoordsv2(players)

if __name__ == '__main__':

    # assignCountry()
    # run()
    readPlayersBySeasons()
    players = matchCountryCoords()

    leagues = ['premier', 'bundes', 'seriea', 'spain']
    seasons = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
