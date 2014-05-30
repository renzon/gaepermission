# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaepermission import facade
from gaepermission.decorator import has_permission
from tekton.gae.middleware import Middleware

LOGIN_PATH = '/login'
LOGOUT_PATH = '/logout'


class LoggedUserMiddleware(Middleware):
    def set_up(self):
        user = facade.logged_user(self.handler.request).execute().result
        self.dependencies['_logged_user'] = user
        self.dependencies['_login_path'] = LOGIN_PATH
        self.dependencies['_logout_path'] = LOGOUT_PATH


class PermissionMiddleware(Middleware):
    def set_up(self):
        fcn = self.dependencies['_fcn']
        user = self.dependencies['_logged_user']
        if not has_permission(user, fcn):
            if user is None:
                self.handler.redirect(LOGIN_PATH)
            else:
                self.handler.response.status_int = 403
                self.handler.response.write('You have no access permission')
            return True