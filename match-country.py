from nacionalidad import getPlayersFifa
from match import Matches
import numpy as np

positions = {'GK', 'DEF', 'MID', 'FWD'}
regionNames = ['brazil', 'argentina', 'united kingdom', 'spain', 'italy', 'france', 'germany', 'netherland', 'uruguay',
               'sudamerica', 'norteamerica', 'asia', 'oceania', 'yugoslavia', 'checoslovaquia', 'africa', 'europa_Oc',
               'eurioa_Or', 'Otro']
local = ['home', 'away']


def run():
    playerCountryPath = 'Dataset/jugadores_con_pais.csv'
    playerPath = 'tallerR/players.csv'
    matchPath = 'tallerR/matches_no_xml.csv'
    homePos = 'tallerR/PosL.csv'
    awayPos = 'tallerR/PosV.csv'
    outpath = 'Dataset/matches_edad_region.csv'

    # Para leer y guardar los partidos
    homePlayers = []
    awayPlayers = []
    for i in range(11):
        homePlayers.append('home_player_' + str(i + 1))
        awayPlayers.append('away_player_' + str(i + 1))
    matches = Matches(matchPath, idM='id', league='league_id', date='date', home=homePlayers, away=awayPlayers,
                      homePos=homePos, awayPos=awayPos)
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

    # Se le asigna el país y la región a todos los jugadores
    regions, regionsByCountry = getRegions()
    for playerid in fifaPlayersById:
        if playerid in countryByPlayerId:
            country = countryByPlayerId[playerid][1]
            fifaPlayersById[playerid].country = country
            fifaPlayersById[playerid].region = regionsByCountry[country]
        else:
            fifaPlayersById[playerid].country = 'No Country'
            fifaPlayersById[playerid].region = 'Otro'

    for match in matches:

        matchRegions = {'home': {}, 'away': {}}
        matchAgesByPositions = {'home': {}, 'away': {}}

        # Nacionalidades
        matchids = match.homeId, match.awayId
        for mids, loc in zip(matchids, local):
            for playerId in mids:
                player = fifaPlayersById[playerId]
                if player.region in matchRegions[loc]:
                    matchRegions[loc][player.region] += [playerId]
                else:
                    matchRegions[loc][player.region] = [playerId]

        # Edades
        matchpos = match.homePos, match.awayPos
        for mids, mpos, loc in zip(matchids, matchpos, local):
            for playerid, playerpos in zip(mids, mpos):
                player = fifaPlayersById[playerid]
                age = match.year - player.byear - 1
                age += 1 if match.month > player.bmonth else 0
                age += 1 if player.bmonth == match.month and match.day > player.bday else 0
                if playerpos in matchAgesByPositions[loc]:
                    matchAgesByPositions[loc][playerpos] += [age]
                else:
                    matchAgesByPositions[loc][playerpos] = [age]

        match.ages = matchAgesByPositions
        match.regions = matchRegions

    # se escribe el nuevo archivo
    infile = open(matchPath, 'r')
    header = infile.readline().replace('\n', '')
    lineskel = '%s'
    for loc in local:
        for region in regionNames:
            header += ',%s_%s' % (loc, region)
            lineskel += ',%f'
        for position in positions:
            header += ',%s_%s_%s' % ('edad', loc, position)
            lineskel += ',%f'
    header += '\n'
    lineskel += '\n'

    outfile = open(outpath, 'w')
    outfile.write(header)

    for match in matches:
        line = [infile.readline().replace('\n', '')]

        for loc in local:
            for region in regionNames:
                if region in match.regions[loc]:
                    line.append(len(match.regions[loc][region]) / 11)
                else:
                    line.append(0)
            for position in positions:
                if position in match.ages[loc]:
                    line.append(np.mean(match.ages[loc][position]))
                else:
                    line.append(0)

        line = tuple(line)
        outfile.write(lineskel % line)
        outfile.flush()

    outfile.close()

    # # Check para ver si están todos los jugadores de los matches
    # for match in matches:
    #     for homeid in match.homeId:
    #         if homeid not in fifaPlayersById:
    #             print(homeid)
    #     for awayid in match.awayId:
    #         if awayid not in fifaPlayersById:
    #             print(awayid)


def getRegions():

    regions = {'brazil': ['Brazil'],
               'argentina': ['Argentina'],
               'united kingdom': ['United Kingdom'],
               'spain': ['Spain'],
               'italy': ['Italy'],
               'france': ['France'],
               'germany': ['Germany'],
               'netherland': ['Netherlands'],
               'uruguay': ['Uruguay'],
               'sudamerica': ['Chile', 'Colombia', 'Peru', 'Paraguay', 'Venezuela', 'Ecuador', 'Bolivia', 'Panama',
                              'Suriname'],
               'norteamerica': ['Mexico', 'United States', 'Costa Rica', 'Canada', 'Honduras', 'El Salvador', 'Jamaica',
                                'Trinidad and Tobago'],
               'asia': ['Japan', 'South Korea', 'China', 'Turkey', 'Israel', 'Ukraine', 'Iran', 'Lebanon', 'Iraq',
                        'Georgia', 'Kazakhstan', 'Uzbekistan', 'Syria', 'Tajikistan', 'Oman', 'Azerbaijan', 'Armenia'],
               'oceania': ['Australia'],
               'yugoslavia': ['Croatia', 'Bosnia and Herzegovina', 'Slovenia', 'Macedonia', 'Serbia and Montenegro',
                              'Kosovo'],
               'checoslovaquia': ['Czech Republic', 'Slovakia', 'Hungary'],
               'africa': ['Senegal', 'Nigeria', 'Ivory Coast', 'Cameroon', 'Congo [DRC]', 'Morocco', 'Mali',
                          'South Africa', 'Tunisia', 'Egypt', 'Sierra Leone', 'Mozambique', 'Central African Republic',
                          'Zimbabwe', 'Zambia', 'Angola', 'Togo', 'Kenya', 'Guinea', 'Algeria', 'Uganda', 'Gambia',
                          'Guinea-Bissau', 'Ghana', 'Liberia', 'Burkina Faso', 'Burundi', 'Cape Verde', 'Gabon',
                          'Benin',
                          'Namibia'],
               'europa_Oc': ['Switzerland', 'Sweden', 'Belgium', 'Poland', 'Austria', 'Portugal', 'Denmark', 'Greece',
                             'Ireland', 'Norway', 'Iceland', 'Finland', 'Monaco'],
               'eurioa_Or': ['Romania', 'Belarus', 'Russia', 'Bulgaria', 'Estonia', 'Albania', 'Latvia', 'Lithuania']}

    regionsByCountry = dict([(country, region) for region in regions for country in regions[region]])

    return regions, regionsByCountry


if __name__ == '__main__':

    run()
