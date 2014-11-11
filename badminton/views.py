import json
import logging

from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render

from common.auth.utils import is_user_in_group

from badminton.models import Contribution, Cost, Game

logger = logging.getLogger(__name__)

def is_user_in_group_badminton_player(user):
    return is_user_in_group(user, 'badminton_player')

def is_user_in_group_badminton_organiser(user):
    return is_user_in_group(user, 'badminton_organiser')

def get_total_play_count(year):
    total_play_count = 0
    games = Game.objects.filter(play_date__year = year)
    for g in games: total_play_count += len(g.players.all())
    return total_play_count

def get_total_bal(year):
    # Calculate the total balance (contributions - costs)
    total_bal = 0.
    contribs = Contribution.objects.filter(financial_year = year)
    for c in contribs: total_bal += c.amount
    costs = Cost.objects.filter(financial_year = year)
    for c in costs: total_bal -= c.amount
    return total_bal

def get_user_bal_and_games(year, username):
    total_bal = get_total_bal(year)
    total_play_count = get_total_play_count(year)

    # Calculate user' balance
    bal = 0.
    contribs = Contribution.objects.filter(financial_year = year).filter(contributor__username = username)
    for c in contribs: bal += c.amount
    games = Game.objects.filter(play_date__year = year).filter(players__username = username)
    if len(games) > 0: bal += total_bal / total_play_count * len(games)
    return (bal, games)

def index(request):
    data = {'title': 'Friday badminton'}
    if request.user.is_authenticated():
        if is_user_in_group_badminton_organiser(request.user):
            logger.debug(request.user.username + ' is a member of group badminton_organiser')
            return redirect(reverse('dryang-badminton:list-all'), data)
        elif is_user_in_group_badminton_player(request.user):
            logger.debug(request.user.username + ' is a member of group badminton_player')
            return redirect(reverse('dryang-badminton:list'), data)
    else:
        return render(request, 'badminton/index.html', data)

@login_required(login_url = reverse_lazy('dryang-auth:login'))
@user_passes_test(is_user_in_group_badminton_player, login_url = '/auth/access-denied/')
def list(request):
    year = request.GET.get('year', None)
    if not year: year = date.today().year
    else:
        logger.debug("Found parameter 'year' in request")
        year = int(year)
    logger.debug('Year: %d' % year)

    bal_and_games = get_user_bal_and_games(year, request.user.username)

    data = {'title': 'Friday badminton',
            'year': year,
            'current_year': date.today().year,
            'bal': bal_and_games[0],
            'games': bal_and_games[1]}
    return render(request, 'badminton/list.html', data)

@login_required(login_url = reverse_lazy('dryang-auth:login'))
@user_passes_test(is_user_in_group_badminton_organiser, login_url = '/auth/access-denied/')
def list_all(request):
    year = request.GET.get('year', None)
    if not year: year = date.today().year
    else:
        logger.debug("Found parameter 'year' in request")
        year = int(year)
    logger.debug('Year: %d' % year)

    data = {'title': 'Friday badminton',
            'year': year,
            'current_year': date.today().year,
            'bal': get_total_bal(year),
            'total_play_count': get_total_play_count(year)}
    return render(request, 'badminton/list-all.html', data)
