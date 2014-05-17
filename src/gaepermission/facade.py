# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie import facade as cookie_facade
from gaegraph.business_base import NodeSearch
from gaepermission.commands import FakeCommand

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
    dct = cookie_facade.retrive_cookie_data(request, USER_COOKIE_NAME)
    if dct is None:
        return FakeCommand()
    return NodeSearch(dct['id'])


