# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from google.appengine.ext import ndb

from gaepermission.base_commands import FindMainUserFromExternalUserId, CheckMainUserEmailConflict, log_main_user_in
from gaepermission.model import GoogleUser, ExternalToMainUser, MainUser, PendingExternalToMainUser


class FindMainUserFromGoogleUser(FindMainUserFromExternalUserId):
    def __init__(self, id):
        super(FindMainUserFromGoogleUser, self).__init__(GoogleUser.query_by_google_id(id))


class CheckMainUserGoogleEmailConflict(CheckMainUserEmailConflict):
    def __init__(self, email, google_id):
        super(CheckMainUserGoogleEmailConflict, self).__init__(email, FindMainUserFromGoogleUser(google_id))


class GoogleLogin(CheckMainUserGoogleEmailConflict):
    def __init__(self, google_api_user, response, user_cookie):
        super(GoogleLogin, self).__init__(google_api_user.email(), google_api_user.user_id())
        self.google_api_user = google_api_user
        self.user_cookie = user_cookie
        self.response = response
        self._arc = None
        self.pending_link = None

    def do_business(self, stop_on_error=True):
        super(GoogleLogin, self).do_business(stop_on_error)

        # if no conflict
        if self.result:
            if self.external_user is None and self.main_user_from_external is None:
                self.external_user = GoogleUser(google_id=self.google_api_user.user_id())
                self.main_user_from_external = MainUser(name=self.google_api_user.nickname(),
                                                        email=self.google_api_user.email())
                external_user_key, main_user_key = ndb.put_multi([self.external_user, self.main_user_from_external])
                self._arc = ExternalToMainUser(origin=external_user_key, destination=main_user_key)
            log_main_user_in(self.main_user_from_external, self.response, self.user_cookie)
        else:
            if self.external_user is None:
                self.external_user = GoogleUser(google_id=self.google_api_user.user_id())
                self.external_user.put()
            self.pending_link = PendingExternalToMainUser(external_user=self.external_user.key,
                                                          main_user=self.main_user_from_email.key)

    def commit(self):
        return [m for m in [self._arc, self.pending_link] if m]


