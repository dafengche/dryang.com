from __future__ import absolute_import

from django.contrib import auth
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

import logging

logger = logging.getLogger(__name__)

def login(request):
    username = password = ''
    redirect_url = settings.LOGIN_REDIRECT_URL
    if 'next' in request.GET: redirect_url = request.GET['next']
    if redirect_url == reverse('dryang-auth:logout'):
        redirect_url = settings.LOGIN_REDIRECT_URL
    logger.debug('next: ' + redirect_url)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        logger.debug('Authenticating started for ' + username)
        user = auth.authenticate(username = username, password = password)
        return login_user(request, user, redirect_url)
    else:
        try:
#            remote_user = request.META['REMOTE_USER']
            remote_user = request.META['HTTP_X_PROXY_REMOTE_USER']
            if remote_user and remote_user != '(null)':
                logger.debug('Client submitted a certificate\n\t' + remote_user)
                user = auth.authenticate(remote_user = remote_user)
                return login_user(request, user, redirect_url)
        except KeyError:
            logger.debug('REMOTE_USER not found in request.META')
        # Go to the login page
        logger.debug('Going to the login page...')
        return render(request, 'auth/login.html')

def logout(request):
    username = request.user.username
    logger.debug('Logging out ' + username + '...')
    auth.logout(request)
    logger.debug(username + ' logged out')
    return render(request, 'auth/logout.html')

def login_user(request, user, redirect_url):
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            logger.debug(user.username + ' logged in, redirecting to ' + redirect_url + '...')
            return redirect(redirect_url)
        else:
            # User account is disabled
            logger.debug(user.username + "'s account is disabled")
            # Go to the login page with warning message
            return render(request, 'auth/login.html', {'msg': 'You account has been disabled.'})
    else:
        # Go to the login page with warning message
        logger.debug('Login failed')
        return render(request, 'auth/login.html', {'msg': 'Login failed, please try again.'})

def access_denied(request):
    return render(request, 'auth/access-denied.html')
