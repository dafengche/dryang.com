from __future__ import absolute_import

import matplotlib
matplotlib.use('Agg') # Non-interactive backend

import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import pytz
import socket

from datetime import datetime

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
    if 'plot_width' in params:
        width = params['plot_width'] / float(DPI)
    if 'plot_height' in params:
        height = params['plot_height'] / float(DPI)
    logger.debug('Plot size: width = ' + str(width) + ', height = ' + str(height))
    fig = plt.figure(figsize=(width, height))
    ax = fig.add_subplot(1, 1, 1) # Returns an Axes instance

    if 'mean_plot' == plot_type:
        pass
    elif 'score_map' == plot_type:
        pass 
    elif 'time_series' == plot_type:
        pass
    elif 'scatter_plot' == plot_type:
        pass
    elif 'histogram' == plot_type:
        pass

    N = 50
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = np.random.rand(N)
    area = np.pi * (15 * np.random.rand(N)) ** 2 # 0 to 15 point radiuses
    ax.scatter(x, y, s = area, c = colors, label = 'demo')
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
