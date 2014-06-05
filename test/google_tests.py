# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaegraph.business_base import OriginsSearch
from gaepermission import facade
from gaepermission.google.commands import FindMainUserFromGoogleUser, CheckMainUserGoogleEmailConflict
from gaepermission.model import MainUser, ExternalToMainUser, GoogleUser, PendingExternalToMainUser
from mock import Mock, patch
from mommygae import mommy


class FindMainUserFromGoogleUserTests(GAETestCase):
    def test_no_user(self):
        cmd = FindMainUserFromGoogleUser('google_id').execute()
        self.assertIsNone(cmd.result)
        self.assertIsNone(cmd.external_user)

    def test_google_user_only(self):
        google_user = mommy.save_one(GoogleUser, google_id='google_id')
        cmd = FindMainUserFromGoogleUser('google_id').execute()
        self.assertIsNone(cmd.result)
        self.assertEqual(google_user, cmd.external_user)

    def test_main_user(self):
        google_user = mommy.save_one(GoogleUser, google_id='google_id')
        main_user = mommy.save_one(MainUser)
        ExternalToMainUser(origin=google_user.key, destination=main_user.key).put()
        cmd = FindMainUserFromGoogleUser('google_id').execute()
        self.assertEqual(main_user, cmd.result)
        self.assertEqual(google_user, cmd.external_user)


class CheckMainUserGoogleEmailConflictTests(GAETestCase):
    def test_first_login_with_no_conflict(self):
        cmd = CheckMainUserGoogleEmailConflict('foo@gmail.com', 'google_id').execute()
        self.assertTrue(cmd.result)
        self.assertIsNone(cmd.external_user)
        self.assertIsNone(cmd.main_user_from_email)
        self.assertIsNone(cmd.main_user_from_external)

    def test_second_login_with_no_conflict(self):
        google_user = mommy.save_one(GoogleUser, google_id='google_id')
        cmd = CheckMainUserGoogleEmailConflict('foo@gmail.com', 'google_id').execute()
        self.assertTrue(cmd.result)
        self.assertEqual(google_user, cmd.external_user)
        self.assertIsNone(cmd.main_user_from_email)
        self.assertIsNone(cmd.main_user_from_external)

    def test_first_login_with_conflict(self):
        main_user = mommy.save_one(MainUser, email='foo@gmail.com')
        cmd = CheckMainUserGoogleEmailConflict('foo@gmail.com', 'google_id').execute()
        self.assertFalse(cmd.result)
        self.assertEqual(main_user, cmd.main_user_from_email)
        self.assertIsNone(cmd.external_user)
        self.assertIsNone(cmd.main_user_from_external)

    def test_already_linked_google_user(self):
        google_user = mommy.save_one(GoogleUser, google_id='google_id')
        main_user_from_external = mommy.save_one(MainUser)
        ExternalToMainUser(origin=google_user.key, destination=main_user_from_external.key).put()
        main_user_from_email = mommy.save_one(MainUser, email='foo@gmail.com')
        cmd = CheckMainUserGoogleEmailConflict('foo@gmail.com', 'google_id').execute()
        self.assertTrue(cmd.result)
        self.assertEqual(main_user_from_email, cmd.main_user_from_email)
        self.assertEqual(google_user, cmd.external_user)
        self.assertEqual(main_user_from_external, cmd.main_user_from_external)


class GoogleLoginTests(GAETestCase):
    @patch('gaepermission.google.commands.log_main_user_in')
    def test_google_user_logged_for_the_first_time_with_no_conflict(self, log_main_user_in):
        google_account_user = self.mock_google_account_user()
        response = Mock()

        cmd = facade.login_google(google_account_user, response).execute()

        self.assertTrue(cmd.result)
        user = cmd.main_user_from_external
        self.assertEqual('foo@gmail.com', user.email)
        self.assertEqual('foo', user.name)
        self.assertEqual(MainUser.query().get(), user)
        google_user = OriginsSearch(ExternalToMainUser, user).execute().result[0]
        self.assertEqual('123', google_user.google_id)
        log_main_user_in.assert_called_once_with(user, response, 'userck')
        self.assertIsNone(cmd.pending_link)


    def mock_google_account_user(self):
        google_account_user = Mock()
        google_account_user.user_id = lambda: '123'
        google_account_user.email = lambda: 'foo@gmail.com'
        google_account_user.nickname = lambda: 'foo'
        return google_account_user

    def test_google_user_logged_for_the_second_time_with_conflict(self):
        GoogleUser(google_id='123').put()
        self.test_google_user_logged_for_the_first_time_with_conflict()

    @patch('gaepermission.google.commands.log_main_user_in')
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
        self.assertEqual('123', cmd.external_user.google_id)
        self.assertFalse(log_main_user_in.called)

    @patch('gaepermission.google.commands.log_main_user_in')
    def test_google_user_logged_for_the_second_time(self, log_main_user_in):
        google_account_user = self.mock_google_account_user()
        g_key = GoogleUser(google_id='123').put()
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

