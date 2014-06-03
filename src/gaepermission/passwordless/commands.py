# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import memcache
from gaebusiness.business import Command
from gaebusiness.gaeutil import ModelSearchCommand, UrlFetchCommand
from gaegraph.business_base import SingleOriginSearh
from gaepermission.commands import GetMainUserByEmail
from gaepermission.model import MainUser, ExternalToMainUser
from gaepermission.passwordless.model import PasswordlessApp


class GetApp(ModelSearchCommand):
    def __init__(self):
        super(GetApp, self).__init__(PasswordlessApp.query(), 1)

    def do_business(self, stop_on_error=True):
        super(GetApp, self).do_business(stop_on_error)
        if self.result:
            self.result = self.result[0]
        else:
            self.result = None


class SaveOrUpdateApp(GetApp):
    def __init__(self, id=None, token=None):
        super(SaveOrUpdateApp, self).__init__()
        self.token = token
        self.id = id

    def do_business(self, stop_on_error=True):
        super(SaveOrUpdateApp, self).do_business(stop_on_error)
        if not self.result:
            self.result = PasswordlessApp()
        else:
            memcache.delete(self._cache_key())
        if self.id:
            self.result.app_id = self.id
        if self.token:
            self.result.token = self.token

    def commit(self):
        return self.result


class SengLoginEmail(GetApp):
    def __init__(self, email, return_url, lang, url_passwordless_login):
        super(SengLoginEmail, self).__init__()
        self.url_passwordless_login = url_passwordless_login
        self.email = email
        self.return_url = return_url
        self.lang = lang


    def do_business(self, stop_on_error=True):
        super(SengLoginEmail, self).do_business(stop_on_error)
        app = self.result
        if app:
            fetch_command = UrlFetchCommand(self.url_passwordless_login,
                                            {'email': self.email,
                                             'app_id': app.app_id,
                                             'token': app.token,
                                             'hook': self.return_url,
                                             'lang': self.lang},
                                            method='POST')
            fetch_command.execute()
        else:
            self.add_error('app_data','Must save Passwordless App Credentials before login calls')