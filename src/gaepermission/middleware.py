# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaepermission import facade
from tekton.gae.middleware import Middleware

LOGIN_PATH = '/login'
LOGOUT_PATH = '/logout'


class LoggedUser(Middleware):
    def set_up(self):
        user = facade.logged_user(self.handler.request).execute().result
        self.dependencies['_logged_user'] = user
        self.dependencies['_login_path'] = LOGIN_PATH
        self.dependencies['_logout_path'] = LOGOUT_PATH