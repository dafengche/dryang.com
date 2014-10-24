from __future__ import absolute_import

from django.http import HttpResponse
from django.shortcuts import render

import json
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'verif/index.html', {'title': 'Verification'})

def get_plot(request):
    if request.is_ajax():
        if request.method == 'POST':
            params = json.loads(request.body)
            logger.debug('Parameters: ' + str(params))
            args = [params]
            kwargs = {}
            try:
                result  = request.broker.execute('services.plot.plot.make_plot_mpl', *args, **kwargs)
                logger.debug('Result: ' + str(result))
                return HttpResponse(json.dumps(result), content_type = 'application/json')
            except Exception as ex:
                logger.error(ex)
                return HttpResponse(json.dumps({'error': 'Request failed!'}), content_type = 'application/json')
