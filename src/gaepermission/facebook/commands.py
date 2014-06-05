# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json

from google.appengine.api import memcache
from google.appengine.ext import ndb

from gaebusiness.gaeutil import ModelSearchCommand, UrlFetchCommand
from gaecookie import facade
from gaegraph.business_base import SingleDestinationSearh
from gaepermission.facebook.model import FacebookApp
from gaepermission.model import FacebookUser, ExternalToMainUser, MainUser


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


class GetFacebookUser(ModelSearchCommand):
    def __init__(self, facebook_id):
        super(GetFacebookUser, self).__init__(FacebookUser.query_by_facebook_id(facebook_id), 1)

    def do_business(self, stop_on_error=True):
        super(GetFacebookUser, self).do_business(stop_on_error)
        self.result = self.result[0] if self.result else None


class FetchFacebook(UrlFetchCommand):
    def __init__(self, token):
        super(FetchFacebook, self).__init__('https://graph.facebook.com/v2.0/me',
                                            {'fields': 'id,email,name',
                                             'access_token': token})
        self._to_commit = None

    def do_business(self, stop_on_error=True):
        super(FetchFacebook, self).do_business(stop_on_error)
        if not self.errors:
            dct = json.loads(self.result.content)
            self.result = None
            facebook_user = GetFacebookUser(dct['id']).execute().result
            if facebook_user:
                self.result = SingleDestinationSearh(ExternalToMainUser, facebook_user).execute().result
            else:
                self.result = MainUser(name=dct['name'], email=dct['email'])
                main_user = self.result
                facebook_user = FacebookUser(facebook_id=dct['id'])
                ndb.put_multi([main_user, facebook_user])
                self._to_commit = ExternalToMainUser(origin=facebook_user.key, destination=main_user.key)

    def commit(self):
        return self._to_commit


class LogFacebookUserIn(FetchFacebook):
    def __init__(self, token, response, user_cookie_name):
        super(LogFacebookUserIn, self).__init__(token)
        self.user_cookie_name = user_cookie_name
        self.response = response

    def do_business(self, stop_on_error=True):
        super(LogFacebookUserIn, self).do_business(stop_on_error)
        facade.write_cookie(self.response, self.user_cookie_name, {'id': self.result.key.id()}).execute()

