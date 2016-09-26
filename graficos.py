from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

# make sure the value of resolution is a lowercase L,
#  for 'low', not a numeral 1
my_map = Basemap(projection='merc', lat_0=0, lon_0=-100, resolution='h', area_thresh=0.1,
                 llcrnrlon=-136.25, llcrnrlat=56,
                 urcrnrlon=-134.25, urcrnrlat=57.75)

my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color='coral')
my_map.drawmapboundary()

my_map.drawmeridians(np.arange(0, 360, 30))
my_map.drawparallels(np.arange(-90, 90, 30))

lons = [-135.3318, -134.8331, -134.6572]
lats = [57.0799, 57.0894, 56.2399]
x, y = my_map(lons, lats)
my_map.plot(x, y, 'bo', markersize=10)

plt.show()
