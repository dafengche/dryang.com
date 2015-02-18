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

from services import celery_worker_config as cfg
from services.celery import app
from services.servicelib.cache import CacheControl
from services.servicelib.db import query_db

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.task
def make_plot_mpl(params):
    logger.debug('make_plot_mpl() called')
    logger.debug(params)

    return _make_plot(params)

@CacheControl(host = cfg.cache['host'], port = cfg.cache['port'], time = cfg.cache['time'])
def _make_plot(params):
    dataset = params['dataset']
    if dataset not in ['boe', 'emep', 'gaw']:
        return {'error': 'Unsupported dataset: ' + dataset}

    plot_type = params['plot_type']
    if plot_type not in ['score_map', 'time_series']:
        return {'error': 'Unsupported plot type: ' + plot_type}

    if dataset == 'boe' and plot_type != 'time_series':
        return {'error': 'Unsupported plot type for dataset boe: ' + plot_type}

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

    if 'score_map' == plot_type:
        sw_lat = -90.
        sw_lon = -180.
        ne_lat = 90.
        ne_lon = 180.
#        # Europe
#        sw_lat = 27.636311
#        sw_lon = -31.266001
#        ne_lat = 81.008797
#        ne_lon = 39.869301
        if 'sw_lat' in params: sw_lat = params['sw_lat']
        if 'sw_lon' in params: sw_lon = params['sw_lon']
        if 'ne_lat' in params: ne_lat = params['ne_lat']
        if 'ne_lon' in params: ne_lon = params['ne_lon']
        logger.debug('(sw_lat, sw_lon): (' + str(sw_lat) + ', ' + str(sw_lon) + ')')
        logger.debug('(ne_lat, ne_lon): (' + str(ne_lat) + ', ' + str(ne_lon) + ')')

        # Retrieve data from database
        # TODO: Get obs and mod values
        query = None
        if dataset == 'emep':
            query = ('SELECT id, station_latitude_deg, station_longitude_deg '
                    'FROM gac_emep_stations')
        else: # GAW
            query = ('SELECT id, lat, lon FROM gac_gaw_stations')
        data = query_db(query, host = cfg.plot['db_host'],
                    port = cfg.plot['db_port'],
                    dbname = cfg.plot['db_name'],
                    user = cfg.plot['db_user'],
                    password = cfg.plot['db_pass'])
        if 'error' in data: return data
        logger.debug(str(data['number_of_results']) + ' record(s) retrieved')
        stn_id_list = []
        stn_lat_list = []
        stn_lon_list = []
        for d in data['data']:
            stn_id_list.append(d[0])
            stn_lat_list.append(d[1])
            stn_lon_list.append(d[2])

#        stn_lat_list = [47.8, -54.85, 47.0544, 44.18, 47.42, 46.55]
#        stn_lon_list = [11.02, -68.32, 12.9583, 10.7, 10.98, 7.99]
#        scores = [4.93657698397, -31.0626756529, 35.2049971001, 23.1060270438, 12.5139213403, 17.3946319493]

        # TODO: Set resolution according to area dimension
        map = Basemap(projection = 'cyl',
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
        # TODO: Set parallels and meridians intervals according to area dimension
        # labels = [left, right, top, bottom]
        map.drawmeridians(np.arange(0, 360, 20), labels = [0, 0, 1, 1])
        map.drawparallels(np.arange(-90, 90, 10), labels = [1, 1, 0, 0])

        x, y  = map(stn_lon_list, stn_lat_list) # Notice x = lon, y = lat
#        scat = map.scatter(x, y, marker = 'o',
#                s = 100,
#                c = scores,
#                cmap = plt.get_cmap('rainbow')
#                )
        scat = map.scatter(x, y, marker = 'o', s = 20, c = 'r')

#        plt.title('Verification score map')

#        map.colorbar(scat, 'bottom', size = '5%', pad = '2%')
#        ax.legend()
    elif 'time_series' == plot_type:
#        x = np.array([datetime(2013, m, 20, 0, 0) for m in range(1, 13)])
#        y = np.random.randint(100, size = x.shape)
# You may load data from CSV files using np.loadtxt method
#        x, y = np.loadtxt('/path/to/date-against-value.csv',
#                    unpack = True,
#                    converters = { 0: dates.strpdate2num('%Y-%m-%d') }
#                    )

        # Retrieve data from database
        query = 'SELECT ddate, rate FROM boe_base_rate'
        if 'start_date' in params and 'end_date' in params:
            start_date = params['start_date']
            end_date = params['end_date']
            logger.debug('start_date: ' + str(start_date))
            logger.debug('end_date: ' + str(end_date))
            query += " WHERE ddate BETWEEN '" + start_date + "' AND '" + end_date + "'"
        data = query_db(query, host = cfg.plot['db_host'],
                    port = cfg.plot['db_port'],
                    dbname = cfg.plot['db_name'],
                    user = cfg.plot['db_user'],
                    password = cfg.plot['db_pass'])
        if 'error' in data: return data
        logger.debug(str(data['number_of_results']) + ' record(s) retrieved')

        x = []
        y = []
        for d in data['data']:
            x.append(d[0]) # ddate
            y.append(d[1]) # rate

        ax.plot_date(x, y, fmt = 'r-', label = 'base rate')
        ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation = 20)
        ax.grid(True)
        ax.legend()

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
    full_name = '%s/%s' % (cfg.plot['output_dir'], file_name)
    logger.debug('Output: ' + full_name)
    plt.savefig(full_name, dpi = DPI)

    # Set additional info
    output = {}
    output['metadata'] = metadata
    output['url'] = cfg.plot['url_prefix'] + '/' + file_name

    return output
