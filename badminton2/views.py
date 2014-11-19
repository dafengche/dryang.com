from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render

import json
import logging

from badminton.models import Contribution, Cost, Game
from common.auth.utils import is_user_in_group

logger = logging.getLogger(__name__)

def get_play_count(year):
    """
    Return the number of players played games of the given year
    """
    play_count = 0
    games = Game.objects.filter(play_date__year = year)
    for g in games: play_count += len(g.players.all())
    return play_count

def get_costs(year):
    """
    Return costs of the given year
    """
    sum = 0.
    costs = Cost.objects.filter(financial_year = year)
    for c in costs: sum += c.amount
    return sum

def get_contribs(year):
    """
    Return contributions of the given year
    """
    sum = 0.
    contribs = Contribution.objects.filter(financial_year = year)
    for c in contribs: sum += c.amount
    return sum

def get_cost_per_play(year):
    """
    Return cost per play for a given year
    """
    play_count = get_play_count(year)
    if play_count == 0: return 0
    else: return (get_costs(year) - get_contribs(year)) / play_count

def get_players_bal(year):
    """
    Return a dictioinary containing info below of the given year
    {'cost_per_play': cost per play,
     'player_records' [
        {'username': username,
         'first_name': first_name,
         'last_name': last_name,
         'contrib': contributions this player made,
         'game_dates': [games this player played],
        },
        {
        }
     ],
    }
    """
    games = Game.objects.filter(play_date__year = year)
    if len(games) == 0: return None

    player_count = {}
    for g in games:
        players = g.players.all()
        for p in players:
            if p not in player_count:
                player_count[p] = []
#            player_count[p].append(g.play_date) # Non-serializable
            player_count[p].append(g.play_date.isoformat())

    cost_per_play = get_cost_per_play(year)
    
    players_bal = {
        'cost_per_play': get_cost_per_play(year),
        'player_records': []
    }
    for (k, v) in player_count.items():
        ctb = 0.
        contribs = Contribution.objects.filter(financial_year = year) \
                        .filter(contributor__username = k.username)
        for c in contribs: ctb += c.amount
        d = k.as_json()
        d.update({'contrib': ctb, 'game_dates': v})
        players_bal['player_records'].append(d)
    return players_bal

def get_player_bal(year, username):
    """
    Return a list of info below for a given user in a given year
    {'cost_per_play': cost per play,
     'contrib': contributions this player made,
     'game_list': [games this player played],
    }
    """
    games = Game.objects.filter(play_date__year = year) \
                        .filter(players__username = username)
    if len(games) == 0: return None

#    game_dates = [g.play_date for g in games] # Non-serializable
    game_dates = [g.play_date.isoformat() for g in games]

    cost_per_play = get_cost_per_play(year)

    ctb = 0.
    contribs = Contribution.objects.filter(financial_year = year) \
                        .filter(contributor__username = username)
    for c in contribs: ctb += c.amount

    return {'cost_per_play': cost_per_play,
            'contrib': ctb,
            'game_dates': game_dates}

def index(request):
    if request.user.is_authenticated():
        logger.debug('User is authenticated')
        if is_user_in_group(request.user, 'badminton_organiser') or \
                    is_user_in_group(request.user, 'badminton_player'):
            return render(request, 'badminton2/badminton.html',
                    {'title': 'Friday badminton'})
        else:
            return redirect(reverse('dryang-auth:access-denied'),
                    {'title': 'Friday badminton'})
    else:
        return render(request, 'badminton2/index.html',
                    {'title': 'Friday badminton'})

@login_required(login_url = reverse_lazy('dryang-auth:login'))
def get_data(request):
    if request.is_ajax():
        if request.method == 'POST':
            params = json.loads(request.body)
            logger.debug('Parameters: ' + str(params))
            if not 'r' in params:
                return HttpResponse(
                    json.dumps({'error': "Parameter 'r' not found!"}),
                    content_type = 'application/json')
            if not 'y' in params: return HttpResponse(
                    json.dumps({'error': "Parameter 'y' not found!"}),
                    content_type = 'application/json')
            r = params['r']
            y = params['y']
            if r not in ['b', 'g', 'p', 'c', 'ctb']:
                return HttpResponse(
                    json.dumps({'error': 'Unsupported parameter r: ' + r}),
                    content_type = 'application/json')

            data = None
            if r == 'b':
                if not is_user_in_group(request.user, 'badminton_player'):
                    logger.warning('%s is not a member of group \
                        badminton_player' % request.user.username)
                    return HttpResponse(
                        json.dumps({'error': 'Access denied'}),
                        content_type = 'application/json')
                data = get_player_bal(y, request.user.username) 
            else:
                if not is_user_in_group(request.user, 'badminton_organiser'):
                    logger.warning('%s is not a member of group \
                        badminton_organiser' % request.user.username)
                    return HttpResponse(
                        json.dumps({'error': 'Access denied'}),
                        content_type = 'application/json')
                if r == 'g':
                    data = Game.objects.filter(play_date__year = y)
                    data = [g.as_json() for g in data]
                elif r == 'p':
                    data = get_players_bal(y)
                elif r == 'c':
                    data = Cost.objects.filter(financial_year = y)
                    data = [c.as_json() for c in data]
                else: # ctb
                    data = Contribution.objects.filter(financial_year = y)
                    data = [c.as_json() for c in data]

            # At this point, data should be JSON serialisable
            if data: logger.debug(data)
            return HttpResponse(
                json.dumps({'data': data}),
                content_type = 'application/json')

    return HttpResponse(
            json.dumps({'error': 'Request failed!'}),
            content_type = 'application/json')
