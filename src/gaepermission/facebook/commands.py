# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from google.appengine.api import memcache

from gaebusiness.gaeutil import ModelSearchCommand
from gaepermission.facebook.model import FacebookApp


class GetFacebookApp(ModelSearchCommand):
    def __init__(self):
        super(GetFacebookApp, self).__init__(FacebookApp.query(), 1)

    def do_business(self, stop_on_error=True):
        super(GetFacebookApp, self).do_business(stop_on_error)
        if self.result:
            self.result = self.result[0]
        else:
            self.result = None


class SaveOrUpdateFacebookApp(GetFacebookApp):
    def __init__(self, id=None, token=None):
        super(SaveOrUpdateFacebookApp, self).__init__()
        self.token = token
        self.id = id

    def do_business(self, stop_on_error=True):
        super(SaveOrUpdateFacebookApp, self).do_business(stop_on_error)
        if not self.result:
            self.result = FacebookApp()
        else:
            memcache.delete(self._cache_key())
        if self.id:
            self.result.app_id = self.id
        if self.token:
            self.result.token = self.token

    def commit(self):
        return self.result


