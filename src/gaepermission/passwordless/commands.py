# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import memcache
from gaebusiness.gaeutil import ModelSearchCommand
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


