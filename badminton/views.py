import json
import logging

from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render

from common.auth.utils import is_user_in_group

from badminton.models import Contribution, Cost, Record

logger = logging.getLogger(__name__)

def index(request):
    data = {'title': 'Friday badminton'}
    if request.user.is_authenticated():
        return redirect(reverse('dryang-badminton:list'))
    else:
        return render(request, 'badminton/index.html', data)

def is_user_in_group_badminton_player(user):
    return is_user_in_group(user, 'badminton_player')

@login_required(login_url = reverse_lazy('dryang-auth:login'))
@user_passes_test(is_user_in_group_badminton_player, login_url = '/auth/access-denied/')
def list(request):
    # TODO: Get year from request
    year = date.today().year

    # Get total play count
    total_play_count = 0
    records = Record.objects.filter(play_date__year = year)
    for r in records: total_play_count += len(r.players.all())

    # Calculate the total cost (costs - contributions)
    total_cost = 0.
    costs = Cost.objects.filter(financial_year = year)
    for c in costs: total_cost += c.amount
    contribs = Contribution.objects.filter(financial_year = year)
    for c in contribs: total_cost -= c.amount

    # Calculate cost for the current user
    records = records.filter(players__username = request.user.username)
    cost = 0.
    if len(records) > 0: cost = total_cost / total_play_count * len(records)

    data = {'year': date.today().year, 'records': records, 'cost': cost}
    return render(request, 'badminton/list.html', data)

'''
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
                result = request.broker.execute('services.compute.compute.' + o, *args, **kwargs)
                logger.debug('Result: ' + str(result))
                return HttpResponse(json.dumps(result), content_type = 'application/json')
            except Exception as ex:
                logger.error(ex)
                return HttpResponse(json.dumps({'error': 'Request failed!'}), content_type = 'application/json')

    return HttpResponse(json.dumps({'error': 'Request unsupported!'}), content_type = 'application/json')
'''
