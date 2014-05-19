# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie import facade as cookie_facade
from gaegraph.business_base import NodeSearch
from gaepermission import commands
from gaepermission.commands import FakeCommand, GoogleLogin

USER_COOKIE_NAME = 'userck'


def logout(response):
    '''
    Returns a command that logout the user out removing her id from cookie
    '''
    return cookie_facade.delete_cookie(response, USER_COOKIE_NAME)


def logged_user(request):
    '''
    Returns a command that retrieves the current logged user based on secure cookie
    If there is no logged user, the result from command is None
    '''
    dct = cookie_facade.retrive_cookie_data(request, USER_COOKIE_NAME).execute().result
    if dct is None:
        return FakeCommand()
    return NodeSearch(dct['id'])


def login_google(google_user, response):
    '''
    Googe user must be the user returnet from get_current_user from users module provided by App Engine
    Returns a command that log user in based on her google account credentials.
    The logged user (MainUser) is provides on result or None if the user is not logged with her Google Account
    '''

    return commands.GoogleLogin(google_user, response, USER_COOKIE_NAME)


