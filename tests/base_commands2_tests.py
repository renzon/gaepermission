# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaegraph.business_base import SingleDestinationSearh
from gaepermission import facade
from gaepermission.model import MainUser, GoogleUser, PendingExternalToMainUser, ExternalToMainUser
from gaepermission.passwordless.commands import Login
from mock import patch, Mock
from mommygae import mommy


class LoginCheckingEmailTests(GAETestCase):
    def setup_call_stat(self, LoginClassMock):
        login_obj = Login(None, None, None, None)
        main_user = mommy.save_one(MainUser, email='foo@gmail.com')
        login_obj.result = main_user
        login_obj.set_up = Mock()
        login_obj.do_business = Mock()
        login_obj.commit = lambda: None
        LoginClassMock.return_value = login_obj
        external_user = mommy.save_one(GoogleUser)
        pending_key = PendingExternalToMainUser(external_user=external_user.key, main_user=main_user.key).put()
        return external_user, main_user, pending_key

    @patch('gaepermission.base_commands2.Login')
    def test_success(self, LoginClassMock):
        external_user, main_user, pending_key = self.setup_call_stat(LoginClassMock)

        cmd = facade.login_checking_email(str(pending_key.id()), 'ticket', 'response').execute()

        self.assertTrue(cmd.checked)
        self.assertEqual(main_user, SingleDestinationSearh(ExternalToMainUser, external_user).execute().result)

    @patch('gaepermission.base_commands2.Login')
    def test_not_existing_pending_id(self, LoginClassMock):
        external_user, main_user, pending_key = self.setup_call_stat(LoginClassMock)

        self.assertRaises(ValueError,facade.login_checking_email,'not existing', 'ticket', 'response')

        self.assertIsNone(SingleDestinationSearh(ExternalToMainUser, external_user).execute().result)


    @patch('gaepermission.base_commands2.Login')
    def test_not_creating_link_if_there_is_one_already(self, LoginClassMock):
        external_user, main_user, pending_key = self.setup_call_stat(LoginClassMock)
        linked_main_user = mommy.save_one(MainUser)
        ExternalToMainUser(origin=external_user.key, destination=linked_main_user).put()
        cmd = facade.login_checking_email(str(pending_key.id()), 'ticket', 'response').execute()

        self.assertFalse(cmd.checked)
        self.assertEqual(1, len(ExternalToMainUser.query().fetch()))


