# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaegraph.business_base import OriginsSearch
from facebook_tests import ExternalUserSearch
from gaepermission import facade
from gaepermission.model import MainUser, GoogleUser, PendingExternalToMainUser
from gaepermission.base_commands import ExternalToMainUser
from mock import Mock, patch
from mommygae import mommy




class GoogleLoginTests(GAETestCase):
    @patch('gaepermission.base_commands.log_main_user_in')
    def test_google_user_logged_for_the_first_time_with_no_conflict(self, log_main_user_in):
        google_account_user = self.mock_google_account_user()
        response = Mock()

        cmd = facade.login_google(google_account_user, response).execute()

        self.assertTrue(cmd.result)
        user = cmd.main_user_from_external
        self.assertEqual('foo@gmail.com', user.email)
        self.assertEqual('foo', user.name)
        self.assertEqual(MainUser.query().get(), user)
        google_user = ExternalUserSearch(user).execute().result[0]
        self.assertEqual('123', google_user.external_id)
        log_main_user_in.assert_called_once_with(user, response, 'userck')
        self.assertIsNone(cmd.pending_link)


    def mock_google_account_user(self):
        google_account_user = Mock()
        google_account_user.user_id = lambda: '123'
        google_account_user.email = lambda: 'foo@gmail.com'
        google_account_user.nickname = lambda: 'foo'
        return google_account_user

    def test_google_user_logged_for_the_second_time_with_conflict(self):
        GoogleUser(external_id='123').put()
        self.test_google_user_logged_for_the_first_time_with_conflict()

    @patch('gaepermission.base_commands.log_main_user_in')
    def test_google_user_logged_for_the_first_time_with_conflict(self, log_main_user_in):
        google_account_user = self.mock_google_account_user()
        main_user = mommy.save_one(MainUser, email='foo@gmail.com')

        cmd = facade.login_google(google_account_user, Mock()).execute()
        self.assertFalse(cmd.result)
        self.assertIsNone(cmd.main_user_from_external)

        self.assertEqual(1, len(GoogleUser.query().fetch()))
        self.assertEqual(1, len(MainUser.query().fetch()))
        self.assertIsNotNone(cmd.pending_link)
        self.assertEqual(PendingExternalToMainUser.query().get(), cmd.pending_link)
        self.assertEqual(cmd.external_user.key, cmd.pending_link.external_user)
        self.assertEqual(main_user.key, cmd.pending_link.main_user)
        self.assertEqual('123', cmd.external_user.external_id)
        self.assertFalse(log_main_user_in.called)

    @patch('gaepermission.base_commands.log_main_user_in')
    def test_google_user_logged_for_the_second_time(self, log_main_user_in):
        google_account_user = self.mock_google_account_user()
        g_key = GoogleUser(external_id='123').put()
        main_user = MainUser(name='foo', email='foo@gmail.com')
        main_user.put()
        ExternalToMainUser(origin=g_key, destination=main_user.key.id()).put()

        response = Mock()
        cmd = facade.login_google(google_account_user, response).execute()
        self.assertTrue(cmd.result)

        user = cmd.main_user_from_external
        self.assertEqual('foo@gmail.com', user.email)
        self.assertEqual('foo', user.name)
        self.assertEqual(main_user, user)
        self.assertEqual(1, len(GoogleUser.query().fetch()))
        self.assertEqual(1, len(MainUser.query().fetch()))
        self.assertIsNone(cmd.pending_link)
        log_main_user_in.assert_called_once_with(user, response, 'userck')

