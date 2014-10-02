import matplotlib
matplotlib.use('Agg') # Non-interactive backend

from celery import Celery
from datetime import datetime

import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import pytz
import socket

from cache import CacheControl

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# First argument is the name of the current module
# redis://:password@hostname:port/db_number, all fields after the scheme are
# optional, and will default to localhost on port 6379, using database 0
app = Celery('plot', broker = 'amqp://', backend = 'redis://')

OUTPUT_DIR = '/var/share/download_data'

@app.task
def make_plot_mpl(params):
    logger.debug('make_plot_mpl() called')
    logger.debug(params)

    return _make_plot(params)

@CacheControl(time = 600)
def _make_plot(params):
    plot_type = params['plot_type']
    if plot_type not in ['histogram', 'mean_plot', 'scatter_plot', 'time_series']:
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
        N = 50
        x = np.random.rand(N)
        y = np.random.rand(N)
        colors = np.random.rand(N)
        area = np.pi * (15 * np.random.rand(N)) ** 2 # 0 to 15 point radiuses
        ax.scatter(x, y, s = area, c = colors, label = 'demo')
        ax.legend()
    elif 'histogram' == plot_type:
        pass

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
    name = '%s/%s-%s-%s-%04d%s' % (OUTPUT_DIR, socket.gethostname(), prefix, ts, os.getpid(), suffix)
    logger.debug('Output: ' + name)
    plt.savefig(name, dpi = DPI)

    # Set additional info
    output = {}
    output['metadata'] = metadata
    output['url'] = 'some_where' # TODO

    return output
