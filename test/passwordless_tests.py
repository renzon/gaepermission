# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from google.appengine.api import memcache
from base import GAETestCase
from gaebusiness.business import CommandExecutionException
from gaegraph.business_base import SingleDestinationSearh
from gaepermission import facade
from gaepermission.base_commands import GetMainUserByEmail
from gaepermission.model import PasswordlessUser, MainUser, ExternalToMainUser
from gaepermission.passwordless.commands import GetApp
from gaepermission.passwordless.model import PasswordlessApp
from mock import patch, Mock
from mommygae import mommy


class AppDataTests(GAETestCase):
    def test_save_or_update(self):
        get_app = GetApp()
        self.assertIsNone(get_app.execute().result)
        facade.save_or_update_passwordless_app_data('1', 't').execute()
        self.assertIsNone(memcache.get(get_app._cache_key()))
        app = GetApp().execute().result
        self.assertEqual('1', app.app_id)
        self.assertEqual('t', app.token)

        facade.save_or_update_passwordless_app_data('2').execute()
        self.assertIsNone(memcache.get(get_app._cache_key()))
        app2 = GetApp().execute().result
        self.assertEqual('2', app2.app_id)
        self.assertEqual('t', app2.token)
        self.assertEqual(app, app2)

        facade.save_or_update_passwordless_app_data(token='t2').execute()
        self.assertIsNone(memcache.get(get_app._cache_key()))
        app3 = GetApp().execute().result
        self.assertEqual('2', app3.app_id)
        self.assertEqual('t2', app3.token)
        self.assertEqual(app, app3)

        facade.save_or_update_passwordless_app_data('1', 't').execute()
        self.assertIsNone(memcache.get(get_app._cache_key()))
        app4 = GetApp().execute().result
        self.assertEqual('1', app4.app_id)
        self.assertEqual('t', app4.token)
        self.assertEqual(app, app4)


def _setup_app_data():
    return mommy.save_one(PasswordlessApp, token='abc')


class SendPasswordlessLoginLinkTests(GAETestCase):
    @patch('gaepermission.passwordless.commands.UrlFetchCommand')
    def test_no_app_data(self, fetch_command_cls):
        cmd = facade.send_passwordless_login_link('foo@gmail.com', 'http://www.yoursite/passworless/login',
                                                  'pt_BR')
        self.assertRaises(CommandExecutionException, cmd)
        self.assertDictEqual({'app_data': 'Must save Passwordless App Credentials before login calls'}, cmd.errors)
        self.assertFalse(fetch_command_cls.called)


    @patch('gaepermission.passwordless.commands.UrlFetchCommand')
    def test_success(self, fetch_command_cls):
        app = _setup_app_data()
        fetch_cmd_obj = Mock()
        fetch_command_cls.return_value = fetch_cmd_obj
        facade.send_passwordless_login_link('foo@gmail.com', 'http://www.yoursite/passworless/login', 'pt_BR').execute()
        main_user = GetMainUserByEmail('foo@gmail.com').execute().result
        self.assertIsNone(main_user)
        self.assertIsNone(PasswordlessUser.query().get())
        fetch_command_cls.assert_called_once_with('https://pswdless.appspot.com/rest/login',
                                                  {'email': 'foo@gmail.com',
                                                   'app_id': app.app_id,
                                                   'token': app.token,
                                                   'hook': 'http://www.yoursite/passworless/login',
                                                   'lang': 'pt_BR'},
                                                  method='POST')
        fetch_cmd_obj.execute.assert_called_once_with()


class LoginTests(GAETestCase):
    @patch('gaecookie.facade.write_cookie')
    @patch('gaepermission.passwordless.commands.UrlFetchCommand')
    def test_success_with_no_user(self, fetch_command_cls, write_cookie):
        app, fetch_cmd_obj, response = self.setup_base_mock(fetch_command_cls)
        main_user = facade.login_passwordless('0123', response,
                                              'https://pswdless.appspot.com/rest/detail').execute().result
        self.assertIsNotNone(main_user)

        self.assertEqual('foo@bar.com', main_user.email)
        self.assertEqual('foo@bar.com', main_user.name)
        self.assert_base_execution(app, fetch_cmd_obj, fetch_command_cls, main_user, PasswordlessUser.query().get(),
                                   write_cookie, response)

    @patch('gaecookie.facade.write_cookie')
    @patch('gaepermission.passwordless.commands.UrlFetchCommand')
    def test_success_with_main_user(self, fetch_command_cls, write_cookie):
        app, fetch_cmd_obj, response = self.setup_base_mock(fetch_command_cls)

        main_user_on_db = mommy.save_one(MainUser, email="foo@bar.com")

        main_user = facade.login_passwordless('0123', response,
                                              'https://pswdless.appspot.com/rest/detail').execute().result

        self.assertEqual(main_user_on_db, main_user)

        p_user = PasswordlessUser.query().get()
        self.assertIsNotNone(p_user)
        self.assert_base_execution(app, fetch_cmd_obj, fetch_command_cls, main_user, p_user, write_cookie, response)


    @patch('gaecookie.facade.write_cookie')
    @patch('gaepermission.passwordless.commands.UrlFetchCommand')
    def test_success_with_passwordless_user(self, fetch_command_cls, write_cookie):
        app, fetch_cmd_obj, response = self.setup_base_mock(fetch_command_cls)

        main_user_on_db = mommy.save_one(MainUser, email="foo@bar.com")
        p_user_on_db = mommy.save_one(PasswordlessUser, external_id="654321")
        ExternalToMainUser(origin=p_user_on_db.key, destination=main_user_on_db.key).put()

        main_user = facade.login_passwordless('0123',
                                              response,
                                              'https://pswdless.appspot.com/rest/detail').execute().result

        self.assertEqual(main_user_on_db, main_user)

        p_user = PasswordlessUser.query().get()
        self.assertEqual(p_user_on_db, p_user)
        self.assert_base_execution(app, fetch_cmd_obj, fetch_command_cls, main_user, p_user, write_cookie, response)

    @patch('gaecookie.facade.write_cookie')
    @patch('gaepermission.passwordless.commands.UrlFetchCommand')
    def test_success_with_passwordless_user_related_to_main_user_referenced_by_another_email(self, fetch_command_cls,
                                                                                             write_cookie):
        app, fetch_cmd_obj, response = self.setup_base_mock(fetch_command_cls)

        main_user_same_email_but_not_related_to_passwordless = mommy.save_one(MainUser, email="foo@bar.com")
        main_user_related_to_passwordless = mommy.save_one(MainUser, email="another@bar.com")
        p_user_on_db = mommy.save_one(PasswordlessUser, external_id="654321")
        ExternalToMainUser(origin=p_user_on_db.key, destination=main_user_related_to_passwordless.key).put()

        main_user = facade.login_passwordless('0123', response,
                                              'https://pswdless.appspot.com/rest/detail').execute().result

        self.assertEqual(main_user_related_to_passwordless, main_user)
        self.assertNotEqual(main_user_same_email_but_not_related_to_passwordless, main_user)
        p_user = PasswordlessUser.query().get()
        self.assertEqual(p_user_on_db, p_user)
        self.assert_base_execution(app, fetch_cmd_obj, fetch_command_cls, main_user, p_user, write_cookie, response)


    def setup_base_mock(self, fetch_command_cls):
        app = _setup_app_data()
        fetch_cmd_obj = Mock()
        fetch_cmd_obj.errors = {}
        fetch_cmd_obj.execute = Mock(return_value=fetch_cmd_obj)
        fetch_cmd_obj.result.content = json.dumps({'id': "654321", 'email': "foo@bar.com"})
        fetch_command_cls.return_value = fetch_cmd_obj
        return app, fetch_cmd_obj, Mock()

    def assert_base_execution(self, app, fetch_cmd_obj, fetch_command_cls, main_user, p_user, write_cookie, response):
        self.assertEqual('654321', p_user.external_id)
        self.assertEqual(main_user, SingleDestinationSearh(ExternalToMainUser, p_user).execute().result)
        fetch_command_cls.assert_called_once_with('https://pswdless.appspot.com/rest/detail',
                                                  {'ticket': '0123', 'app_id': app.app_id, 'token': app.token},
                                                  'POST')
        fetch_cmd_obj.execute.assert_called_once_with()
        write_cookie.assert_called_once_with(response, 'userck', {'id': main_user.key.id()})
