# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import ModelSearchCommand
from gaecookie import facade as cookie_facade
from gaegraph.business_base import NodeSearch
from gaepermission import commands, inspector
from gaepermission.commands import FakeCommand, GoogleLogin, UpdateUserGroups
from gaepermission.model import MainUser
from gaepermission.passwordless.commands import SaveOrUpdateApp
from tekton import router

USER_COOKIE_NAME = 'userck'


def web_path_security_info():
    '''
    Returns a generator that returns all paths from the application if information about groups and csrf security
    '''
    return inspector.web_paths_security_info(router.package_base)


def logout(response):
    '''
    Returns a command that log the user out, removing her id from cookie
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


def update_user_groups(user_id, groups):
    '''
    Returns a command that updates user's groups of respective user_id.
    '''
    return UpdateUserGroups(user_id, groups)


def find_users_by_email_starting_with(email_prefix=None, cursor=None, page_size=30):
    '''
    Returns a command that retrieves users by its email_prefix, ordered by email.
    It returns a max number of users defined by page_size arg. Next result can be retrieved using cursor, in
    a next call. It is provided in cursor attribute from command.
    '''
    email_prefix = email_prefix or ''

    return ModelSearchCommand(MainUser.query_email_starts_with(email_prefix),
                              page_size, cursor, cache_begin=None)


def send_passwordless_login_link(email):
    '''
    :param email: The email where login link must be sent
    :return: command that communicate with passsworless to sent the email
    '''
    pass


def save_or_update_passwordless_app_data(id=None, token=None):
    '''
    :param id: The App's id
    :param token: The App's tokein
    :return: a command that save or update existing Passworoldless App Data
    See https://pswdless.appspot.com/api#register-sites
    '''
    return SaveOrUpdateApp(id, token)

