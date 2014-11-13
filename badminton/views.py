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

def get_play_count(year):
    """
    Return the number of players played games for the given year
    """
    play_count = 0
    games = Game.objects.filter(play_date__year = year)
    for g in games: play_count += len(g.players.all())
    return play_count

def get_bal(year):
    """
    Return balance (contributions - costs) for the given year
    """
    bal = 0.
    contribs = Contribution.objects.filter(financial_year = year)
    for c in contribs: bal += c.amount
    costs = Cost.objects.filter(financial_year = year)
    for c in costs: bal -= c.amount
    return bal

def get_players(year):
    """
    Return a sorted list containing info below for the given year
    (first_name last_name, (play_count, balance))
    """
    games = Game.objects.filter(play_date__year = year)
    if len(games) == 0: return None

    player_count = {}
    player_name = {}
    for g in games:
        players = g.players.all()
        for p in players:
            if p.username in player_count: player_count[p.username] += 1
            else:
                player_count[p.username] = 1
                player_name[p.username] = p.first_name + ' ' + p.last_name

    player_bal = {}
    cost_per_play = get_bal(year) / get_play_count(year)
    for (k, v) in player_count.items():
        player_bal[player_name[k]] = (v, cost_per_play * v)
        contribs = Contribution.objects.filter(financial_year = year).filter(contributor__username = k)
        for c in contribs: player_bal[player_name[k]][0] += c.amount
    return sorted(player_bal.iteritems())

def get_user_bal_and_games(year, username):
    """
    Return a tuple (balance, games_player) for a given user in a given year
    """
    bal = get_bal(year)
    play_count = get_play_count(year)
    if play_count == 0: return (0., None)

    # Calculate user' balance
    user_bal = 0.
    contribs = Contribution.objects.filter(financial_year = year).filter(contributor__username = username)
    for c in contribs: user_bal += c.amount
    games = Game.objects.filter(play_date__year = year).filter(players__username = username)
    if len(games) > 0: user_bal += bal / play_count * len(games)
    return (user_bal, games)

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

    data = {'title'       : 'Friday badminton',
            'year'        : year,
            'current_year': date.today().year,
            'my_bal'      : bal_and_games[0],
            'my_games'    : bal_and_games[1]}
    return render(request, 'badminton/list.html', data)

@login_required(login_url = reverse_lazy('dryang-auth:login'))
@user_passes_test(is_user_in_group_badminton_organiser, login_url = '/auth/access-denied/')
def list_all(request):
    param = request.GET.get('p', None)
    if not param: param = 'game'
    logger.debug('p=' + param)
    year = request.GET.get('year', None)
    if not year: year = date.today().year
    else:
        year = int(year)
    logger.debug('Year: %d' % year)

    data = {'title'       : 'Friday badminton',
            'p'           : param,
            'year'        : year,
            'current_year': date.today().year,
            'bal'         : get_bal(year),
            'play_count'  : get_play_count(year),
            'is_player'   : is_user_in_group_badminton_player(request.user)}

    if param == 'game':
        data['games'] = Game.objects.filter(play_date__year = year)
    elif param == 'player':
        data['players'] = get_players(year)
    elif param == 'cost':
        data['costs'] = Cost.objects.filter(financial_year = year)
    elif param == 'contrib':
        data['contribs'] = Contribution.objects.filter(financial_year = year)
    elif param == 'mybal':
        bal_and_games = get_user_bal_and_games(year, request.user.username)
        data['my_bal'] = bal_and_games[0]
        data['my_games'] = bal_and_games[1]

    return render(request, 'badminton/list-all.html', data)
