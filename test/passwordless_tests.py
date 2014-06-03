# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import memcache
from base import GAETestCase
from gaepermission import facade
from gaepermission.commands import GetMainUserByEmail
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


class SendPasswordlessLoginLinkTests(GAETestCase):
    @patch('gaepermission.passwordless.commands.UrlFetchCommand')
    def test_no_app_data(self, fetch_command_cls):
        cmd = facade.send_passwordless_login_link('foo@gmail.com', 'http://www.yoursite/passworless/login',
                                                  'pt_BR').execute()
        self.assertDictEqual({'app_data': 'Must save Passwordless App Credentials before login calls'}, cmd.errors)
        self.assertFalse(fetch_command_cls.called)


    @patch('gaepermission.passwordless.commands.UrlFetchCommand')
    def test_success(self, fetch_command_cls):
        app = self._setup_app_data()
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


    def _setup_app_data(self):
        return mommy.save_one(PasswordlessApp, token='abc')


