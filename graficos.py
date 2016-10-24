from mpl_toolkits.basemap import Basemap
from country import Country
import matplotlib.pyplot as plt
from matplotlib import ticker


def groupData(dataByCombo, leagues, seasons, banHome=False):

    countryToData = {}
    for (country, league, season) in dataByCombo:
        if league in leagues and season in seasons:
            if banHome and ((league == 'premier' and country == 'United Kingdom') or (
                            league == 'bundes' and country == 'Germany') or (
                            league == 'seriea' and country == 'Italy') or (
                            league == 'spain' and country == 'Spain')):
                continue

            lat, lon, age, players = dataByCombo[(country, league, season)]
            if country in countryToData:
                countryToData[country].append((float(age), int(players)))
            else:
                countryToData[country] = [(float(age), int(players))]

    return countryToData


def aggregateData(countryToData, countries):

    lats, lons = [], []
    ages, counts = [], []

    for country in countryToData:
        # if country == 'United Kingdom':
        #     continue
        meanage = 0
        totalplayers = 0
        for age, players in countryToData[country]:
            meanage += age * players
            totalplayers += players
        if totalplayers > 0:
            meanage /= totalplayers
        lats.append(countries[country].lat)
        lons.append(countries[country].lon)
        counts.append(totalplayers)
        ages.append(meanage)

    return lats, lons, ages, counts


def run():

    data = open('tabla_completa.csv', 'r')
    data.readline()
    dataByCombo = {}
    countries = {}

    # se leen los datos del archivo csv y se guardan en un diccionario para luego ser ordenados
    for line in data:
        country, lat, lon, age, league, season, players = line.replace('\n', '').split(',')
        dataByCombo[(country, league, int(season))] = lat, lon, age, players
        if country not in countries:
            countries[country] = Country(('NN', lat, lon, country))

    # se define la forma en que se agruparán los datos
    leagues = ['premier', 'seriea', 'spain', 'bundes']
    seasons = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]

    # se agrupan los datos
    countryToData = groupData(dataByCombo, ['bundes'], seasons, banHome=True)
    lats, lons, ages, counts = aggregateData(countryToData, countries)

    # Se grafican los datos
    # plt.figure(figsize=(25, 20))
    plt.figure(figsize=(30, 24))
    eq_map = Basemap(projection='merc', resolution='l', area_thresh=1000.0,
                     lat_0=0, lon_0=0, llcrnrlon=-120, llcrnrlat=-56,
                     urcrnrlon=+150, urcrnrlat=70)
    eq_map.drawcoastlines()
    eq_map.drawcountries()
    eq_map.fillcontinents(color='gray')
    # eq_map.drawmapboundary()

    xs, ys = [], []
    sizes, colors = [], []

    # Se obtienen las coordenadas y valores
    for lat, lon, age, count in zip(lats, lons, ages, counts):
        x, y = eq_map(lon, lat)
        xs.append(x)
        ys.append(y)
        colors.append(age)
        sizes.append(getMarkerSize(count))

    # para chequear q el tamaño del marcador represente el área y no el radio
    # x1, y1 = eq_map(-75, -35)
    # x2, y2 = eq_map(-75, -33.6)
    # x3, y3 = eq_map(-75, -36.5)
    # xs = [x1, x2, x3]
    # ys = [y1, y2, y3]
    # colors = [25, 27, 30]
    # sizes = [800, 200, 200]
    pathCollection = eq_map.scatter(xs, ys, marker='o', c=colors, cmap='jet', s=sizes)
    pathCollection.set_zorder(2)
    tick_locator = ticker.MaxNLocator(nbins=14)
    cbar = plt.colorbar(shrink=0.6)
    cbar.locator = tick_locator
    cbar.update_ticks()
    plt.clim(19, 33)
    cbar.set_label("Edades")

    # Título
    title_string = "Jugadores extranjeros en la Bundesliga\n"
    title_string += "Temporadas %d a %d" % (seasons[0], seasons[-1])
    plt.title(title_string, fontsize=25)
    plt.savefig('bundesliga3.pdf', orientation='landscape', format='pdf', dpi=1000, bbox_inches='tight')
    # plt.show()


def getMarkerSize(count):
    # maxradius = 500 está bien para el scatter
    # maxs = 324 está bien para las ligas individuales. Para el total usar 688
    maxradius = 500
    maxs = 324

    return count * maxradius / maxs


if __name__ == '__main__':
    run()
