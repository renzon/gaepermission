# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaegraph.business_base import OriginsSearch
from gaepermission import facade
from gaepermission.model import MainUser, FacebookUser, PendingExternalToMainUser
from gaepermission.base_commands import ExternalToMainUser
from mock import patch, Mock
from mommygae import mommy


class ExternalUserSearch(OriginsSearch):
    arc_class = ExternalToMainUser


class FacebookLoginTests(GAETestCase):
    def setup_fetch_mock(self):
        fetch_mock = Mock()
        fetch_mock.result = {'id': '123', 'email': 'foo@gmail.com', 'name': 'foo'}
        fetch_mock.errors = {}
        return fetch_mock

    @patch('gaepermission.base_commands.log_main_user_in')
    def test_facebook_user_logged_for_the_first_time_with_no_conflict(self, log_main_user_in):
        response = Mock()
        fetch_mock = self.setup_fetch_mock()
        cmd = facade.login_facebook('', response)

        cmd._fetch_facebook = fetch_mock
        cmd.execute()

        self.assertTrue(cmd.result)
        user = cmd.main_user_from_external
        self.assertEqual('foo@gmail.com', user.email)
        self.assertEqual('foo', user.name)
        self.assertEqual(MainUser.query().get(), user)
        facebook_user = ExternalUserSearch(user).execute().result[0]
        self.assertEqual('123', facebook_user.external_id)
        log_main_user_in.assert_called_once_with(user, response, 'userck')
        self.assertIsNone(cmd.pending_link)


    def test_facebook_user_logged_for_the_second_time_with_conflict(self):
        FacebookUser(external_id='123').put()
        self.test_facebook_user_logged_for_the_first_time_with_conflict()

    @patch('gaepermission.base_commands.log_main_user_in')
    def test_facebook_user_logged_for_the_first_time_with_conflict(self, log_main_user_in):
        main_user = mommy.save_one(MainUser, email='foo@gmail.com')

        response = Mock()
        fetch_mock = self.setup_fetch_mock()
        cmd = facade.login_facebook('', response)

        cmd._fetch_facebook = fetch_mock
        cmd.execute()
        self.assertFalse(cmd.result)
        self.assertIsNone(cmd.main_user_from_external)

        self.assertEqual(1, len(FacebookUser.query().fetch()))
        self.assertEqual(1, len(MainUser.query().fetch()))
        self.assertIsNotNone(cmd.pending_link)
        self.assertEqual(PendingExternalToMainUser.query().get(), cmd.pending_link)
        self.assertEqual(cmd.external_user.key, cmd.pending_link.external_user)
        self.assertEqual(main_user.key, cmd.pending_link.main_user)
        self.assertEqual('123', cmd.external_user.external_id)
        self.assertFalse(log_main_user_in.called)

    @patch('gaepermission.base_commands.log_main_user_in')
    def test_facebook_user_logged_for_the_second_time(self, log_main_user_in):
        f_key = FacebookUser(external_id='123').put()
        main_user = MainUser(name='foo', email='foo@gmail.com')
        main_user.put()
        ExternalToMainUser(origin=f_key, destination=main_user.key.id()).put()

        response = Mock()
        fetch_mock = self.setup_fetch_mock()
        cmd = facade.login_facebook('', response)

        cmd._fetch_facebook = fetch_mock
        cmd.execute()

        self.assertTrue(cmd.result)

        user = cmd.main_user_from_external
        self.assertEqual('foo@gmail.com', user.email)
        self.assertEqual('foo', user.name)
        self.assertEqual(main_user, user)
        self.assertEqual(1, len(FacebookUser.query().fetch()))
        self.assertEqual(1, len(MainUser.query().fetch()))
        self.assertIsNone(cmd.pending_link)
        log_main_user_in.assert_called_once_with(user, response, 'userck')





