from __future__ import absolute_import

import matplotlib
matplotlib.use('Agg') # Non-interactive backend

import logging
import matplotlib.dates as dates
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import numpy as np
import os
import pytz
import socket

from datetime import datetime
from mpl_toolkits.basemap import Basemap

from services.celery import app
from services.servicelib.cache import CacheControl

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

OUTPUT_DIR = '/var/share/download_data'
URL_PREFIX = 'http://web01:8008'

@app.task
def make_plot_mpl(params):
    logger.debug('make_plot_mpl() called')
    logger.debug(params)

    return _make_plot(params)

@CacheControl(time = 600)
def _make_plot(params):
    plot_type = params['plot_type']
    if plot_type not in ['histogram', 'mean_plot', 'scatter_plot', 'score_map', 'time_series']:
        return {'error': 'Unsupported plot type: ' + plot_type}

    # Plot, default size: 660x480px, 100dpi
    DPI = 100
    width = 6.6
    height = 4.8
    if 'score_map' == plot_type:
        width = 8.
        height = 4.5
    if 'plot_width' in params:
        width = params['plot_width'] / float(DPI)
    if 'plot_height' in params:
        height = params['plot_height'] / float(DPI)
    logger.debug('Plot size: width = ' + str(width) + ', height = ' + str(height))
    fig = plt.figure(figsize = (width, height))
    ax = fig.add_subplot(1, 1, 1) # Returns an Axes instance

    # TODO: Get bounding box from client (score map)
    sw_lat = -90.
    sw_lon = -180.
    ne_lat = 90.
    ne_lon = 180.
#    # Europe
#    sw_lat = 27.636311
#    sw_lon = -31.266001
#    ne_lat = 81.008797
#    ne_lon = 39.869301

    if 'mean_plot' == plot_type:
        x = np.linspace(-2, 2, 100)

        ax.plot(x, x, label = 'linear')
        ax.plot(x, x**2, label = 'quadratic')
        ax.plot(x, x**3, label = 'cubic')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Simple plot')
        #ax.set_xlim(-2, 2)
        ax.set_ylim(-8, 8)
        ax.grid(True)
        ax.legend()
    elif 'score_map' == plot_type:
        lats = [47.8, -54.85, 47.0544, 44.18, 47.42, 46.55]
        lons = [11.02, -68.32, 12.9583, 10.7, 10.98, 7.99]
        scores = [4.93657698397, -31.0626756529, 35.2049971001, 23.1060270438, 12.5139213403, 17.3946319493]

        # TODO: Set resolution according to area dimension
        map = Basemap(projection = 'mill',
                llcrnrlon  = sw_lon,
                llcrnrlat  = sw_lat,
                urcrnrlon  = ne_lon,
                urcrnrlat  = ne_lat,
                fix_aspect = False,
                resolution = 'l'
                )
        map.drawcoastlines()
#        map.drawcountries()
#        map.fillcontinents(color = 'gray')
        map.drawmapboundary()
        map.drawmeridians(np.arange(0, 360, 20))
        map.drawparallels(np.arange(-90, 90, 10))

        x, y  = map(lons, lats) # Notice x = lon, y = lat
        scat = map.scatter(x, y, marker = 'o',
                s = 100,
                c = scores,
                cmap = plt.get_cmap('rainbow')
                )

#        plt.title('Verification score map')

#        map.colorbar(scat, 'bottom', size = '5%', pad = '2%')
#        ax.legend()
    elif 'time_series' == plot_type:
#        x = np.array([datetime(2013, m, 20, 0, 0) for m in range(1, 13)])
#        y = np.random.randint(100, size = x.shape)
        x, y = np.loadtxt(OUTPUT_DIR + '/date-against-value.csv',
                    unpack = True,
                    converters = { 0: dates.strpdate2num('%Y-%m-%d') }
                    )
        ax.plot_date(x, y, fmt = 'r-', label = 'obs')
        ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation = 20)
        ax.grid(True)
        ax.legend()
    elif 'scatter_plot' == plot_type:
        N = 50
        x = np.random.rand(N)
        y = np.random.rand(N)
        colors = np.random.rand(N)
        area = np.pi * (15 * np.random.rand(N)) ** 2 # 0 to 15 point radiuses
        ax.scatter(x, y, s = area, c = colors, label = 'demo')
        ax.legend()
    elif 'histogram' == plot_type:
        xl = []
        mu, sigma = 100, 15
        x = mu + sigma * np.random.randn(10000)
        xl.append(x)

        mu, sigma = 100, 20
        x = mu + sigma * np.random.randn(10000)
        xl.append(x)

        n, bins, patches = ax.hist(xl, bins = 50, normed = True,
                    alpha = 0.75, histtype='step',
                    color = ['b', 'r'],
                    label = [r'$\sigma=15$', '$\sigma=20$']
                    )

        # The default legend of histogram shows boxes rather than lines. To show lines,
        # custom artists are required
        #artist_0 = plt.Line2D((0, 1), (0, 0), color = 'b')
        #artist_1 = plt.Line2D((0, 1), (0, 0), color = 'r')
        artist_0 = lines.Line2D((0, 1), (0, 0), color = 'b')
        artist_1 = lines.Line2D((0, 1), (0, 0), color = 'r')

        # Create legend from custom artist/label lists
        ax.legend([artist_0, artist_1], [r'$\sigma=15$', '$\sigma=20$'])

        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.set_title(r'$\mathrm{Standard\ normal\ distribution:}\ \mu=100$')
        ax.set_xlim(40, 160)
        ax.set_ylim(0, 0.03)
        ax.grid(True)

    # Get metadata
    metadata = {}
    metadata['width'] = fig.get_figwidth() * DPI
    metadata['height'] = fig.get_figheight() * DPI
    metadata['subplot_left'] = fig.subplotpars.left
    metadata['subplot_right'] = fig.subplotpars.right
    metadata['subplot_bottom'] = fig.subplotpars.bottom
    metadata['subplot_top'] = fig.subplotpars.top
    metadata['x_min'], metadata['x_max'] = ax.get_xlim()
    metadata['y_min'], metadata['y_max'] = ax.get_ylim()
    if 'time_series' == plot_type:
        metadata['x_min'] = dates.num2date(metadata['x_min'], tz = pytz.utc).strftime('%Y-%m-%d')
        metadata['x_max'] = dates.num2date(metadata['x_max'], tz = pytz.utc).strftime('%Y-%m-%d')
    elif 'score_map' == plot_type:
        metadata['x_min'] = sw_lon
        metadata['y_min'] = sw_lat
        metadata['x_max'] = ne_lon
        metadata['y_max'] = ne_lat
    logger.debug(metadata)

    prefix = 'plot_make_plot'
    ts = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    suffix = '.png'
    file_name = '%s-%s-%s-%04d%s' % (socket.gethostname(), prefix, ts, os.getpid(), suffix)
    full_name = '%s/%s' % (OUTPUT_DIR, file_name)
    logger.debug('Output: ' + full_name)
    plt.savefig(full_name, dpi = DPI)

    # Set additional info
    output = {}
    output['metadata'] = metadata
    output['url'] = URL_PREFIX + '/' + file_name

    return output
