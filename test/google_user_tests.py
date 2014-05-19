# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaegraph.business_base import OriginsSearch
from gaepermission import facade
from gaepermission.model import MainUser, ExternalToMainUser, GoogleUser
from mock import Mock


class GoogleLoginTests(GAETestCase):
    def test_no_google_user_logged(self):
        user = facade.login_google(None, Mock()).execute().result
        self.assertIsNone(user)

    def test_google_user_logged_for_the_first_time(self):
        google_account_user = Mock()
        google_account_user.user_id = lambda: '123'
        google_account_user.email = lambda: 'foo@gmail.com'
        google_account_user.nickname = lambda: 'foo'
        user = facade.login_google(google_account_user, Mock()).execute().result
        self.assertEqual('foo@gmail.com', user.email)
        self.assertEqual('foo', user.name)
        self.assertEqual(MainUser.query().get(), user)
        google_user = OriginsSearch(ExternalToMainUser, user).execute().result[0]
        self.assertEqual('123', google_user.google_id)

    def test_google_user_logged_for_the_second_time(self):
        google_account_user = Mock()
        google_account_user.user_id = lambda: '123'
        g_key = GoogleUser(google_id='123').put()
        main_user = MainUser(name='foo', email='foo@gmail.com')
        main_user.put()
        ExternalToMainUser(origin=g_key, destination=main_user.key.id()).put()

        user = facade.login_google(google_account_user, Mock()).execute().result
        self.assertEqual('foo@gmail.com', user.email)
        self.assertEqual('foo', user.name)
        self.assertEqual(main_user, user)
        self.assertEqual(1, len(GoogleUser.query().fetch()))
        self.assertEqual(1, len(MainUser.query().fetch()))


