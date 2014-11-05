from __future__ import absolute_import

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render

import json
import logging

logger = logging.getLogger(__name__)

@login_required(login_url = reverse_lazy('dryang-auth:login'))
def index(request):
    return render(request, 'verif/index.html', {'title': 'Verification'})

@login_required(login_url = reverse_lazy('dryang-auth:login'))
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
                return HttpResponse(json.dumps(result['result']), content_type = 'application/json')
            except Exception as ex:
                logger.error(ex)
                return HttpResponse(json.dumps({'error': 'Request failed!'}), content_type = 'application/json')

@login_required(login_url = reverse_lazy('dryang-auth:login'))
def get_stations(request):
    if request.is_ajax():
        if request.method == 'POST':
            params = json.loads(request.body)
            logger.debug('Parameters: ' + str(params))
            args = [params]
            kwargs = {}
            try:
                result  = request.broker.execute('services.station.station.get_stations', *args, **kwargs)
                logger.debug('Result: ' + str(result))
                return HttpResponse(json.dumps(result['result']), content_type = 'application/json')
            except Exception as ex:
                logger.error(ex)
                return HttpResponse(json.dumps({'error': 'Request failed!'}), content_type = 'application/json')

def is_user_in_group_tester(user):
    if user:
        return user.groups.filter(name = 'tester').count() == 1
    return False

@login_required(login_url = reverse_lazy('dryang-auth:login'))
#@user_passes_test(is_user_in_group_tester, login_url = reverse_lazy('dryang-auth:access-denied'))
@user_passes_test(is_user_in_group_tester, login_url = '/auth/access-denied/')
def test(request):
    return render(request, 'verif/test.html', {'title': 'Verification'})
