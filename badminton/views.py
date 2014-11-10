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
        return redirect(reverse('dryang-badminton:list'), data)
    else:
        return render(request, 'badminton/index.html', data)

def is_user_in_group_badminton_player(user):
    return is_user_in_group(user, 'badminton_player')

@login_required(login_url = reverse_lazy('dryang-auth:login'))
@user_passes_test(is_user_in_group_badminton_player, login_url = '/auth/access-denied/')
def list(request):
    year = request.GET.get('year', None)
    if not year: year = date.today().year
    else:
        logger.debug("Found parameter 'year' in request")
        year = int(year)
    logger.debug('Year: %d' % year)

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

    data = {'title': 'Friday badminton',
            'year': year,
            'records': records,
            'cost': cost}
    return render(request, 'badminton/list.html', data)
