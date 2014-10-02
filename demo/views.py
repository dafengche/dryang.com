from django.http import HttpResponse
from django.shortcuts import render
import json
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'demo/index.html')

def calc(request):
    if request.is_ajax():
        if request.method == 'POST':
            params = json.loads(request.body)
            logger.debug('Parameters: ' + str(params))
            a = float(params['a'])
            b = float(params['b'])
            o = params['o']
            args = [a, b]
            kwargs = {}
            try:
                result = request.broker.execute('compute.compute.' + o, *args, **kwargs)
                logger.debug('Result: ' + str(result))
                return HttpResponse(json.dumps(result), content_type = 'application/json')
            except Exception as ex:
                logger.error(ex)
                return HttpResponse(json.dumps({'error': 'Request failed!'}), content_type = 'application/json')

    return HttpResponse(json.dumps({'error': 'Request unsupported!'}), content_type = 'application/json')
