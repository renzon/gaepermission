# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from gaecookie.decorator import no_csrf
from gaepermission import facade


@no_csrf
def index(_handler, _resp):
    user = users.get_current_user()
    if user:
        facade.login_google(user, _resp).execute()
    _handler.redirect('/')