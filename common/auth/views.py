from __future__ import absolute_import

from django.contrib import auth
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

import logging

logger = logging.getLogger(__name__)

def login(request):
    username = password = ''
    redirect_url = '/'
    if 'next' in request.GET: redirect_url = request.GET['next']
    if not redirect_url: redirect_url = '/'
    elif redirect_url == reverse('dryang-auth:logout'): redirect_url = '/'
    # TODO: Remove the line below
    if redirect_url == '/': redirect_url = '/verif/'
    logger.debug('next: ' + redirect_url)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        logger.debug('Authenticating started for ' + username)
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                logger.debug(username + ' logged in, redirecting to ' + redirect_url + '...')
                return redirect(redirect_url)
            else:
                # User account is disabled
                logger.debug(username + "'s account is disabled")
                # Go to the login page with warning message
                return render(request, 'auth/login.html', {'msg': 'You account has been disabled.'})
        else:
            # Go to the login page with warning message
            logger.debug(username + ' authentication failed')
            return render(request, 'auth/login.html', {'msg': 'Login failed, please try again.'})
    else:
        # Go to the login page
        try:
#            logger.debug(request.META['REMOTE_USER'])
            logger.debug(request.META['HTTP_X_PROXY_REMOTE_USER'])
        except KeyError:
            logger.debug('REMOTE_USER not found in request.META')
        logger.debug('Going to the login page...')
        return render(request, 'auth/login.html')

def logout(request):
    username = request.user.username
    logger.debug('Logging out ' + username + '...')
    auth.logout(request)
    logger.debug(username + ' logged out')
    return render(request, 'auth/logout.html')
