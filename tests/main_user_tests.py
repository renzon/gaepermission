# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import webapp2
from base import GAETestCase
from gaebusiness.business import CommandExecutionException
from gaepermission import facade
from gaepermission.base_commands import SaveUserCmd
from gaepermission.model import MainUser
from mock import patch, Mock
from mommygae import mommy


class LoggedUserTests(GAETestCase):
    @patch('gaepermission.facade.cookie_facade')
    def test_no_logged_user(self, cookie_facade):
        cmd_mock = Mock()
        cmd_mock.execute = Mock(return_value=cmd_mock)
        cmd_mock.result = None
        cookie_facade.retrive_cookie_data = Mock(return_value=cmd_mock)
        result = facade.logged_user(None).execute().result
        self.assertIsNone(result)

    @patch('gaepermission.facade.cookie_facade')
    def test_logged_user(self, cookie_facade):
        user = mommy.save_one(MainUser)
        cmd_mock = Mock()
        cmd_mock.execute = Mock(return_value=cmd_mock)
        cmd_mock.result = {'id': user.key.id()}
        cookie_facade.retrive_cookie_data = Mock(return_value=cmd_mock)
        result = facade.logged_user(None).execute().result
        self.assertEqual(user, result)


# workaroung for i18n

app = webapp2.WSGIApplication(
    [webapp2.Route('/', None, name='upload_handler')])

request = webapp2.Request({'SERVER_NAME': 'test', 'SERVER_PORT': 80,
                           'wsgi.url_scheme': 'http'})
request.app = app
app.set_globals(app=app, request=request)


class MainUserTests(GAETestCase):
    def test_save_error(self):
        cmd = facade.save_user_cmd(None)
        self.assertRaises(CommandExecutionException, cmd)
        self.assertTrue('email' in cmd.errors)

        cmd = facade.save_user_cmd('')
        self.assertRaises(CommandExecutionException, cmd)
        self.assertTrue('email' in cmd.errors)

        cmd = facade.save_user_cmd('asas')
        self.assertRaises(CommandExecutionException, cmd)
        self.assertTrue('email' in cmd.errors)

    def test_succes(self):
        saved_user = facade.save_user_cmd('foo@bar.com', 'foo', groups=['ADMIN'])()
        self.assertEqual(MainUser.query_email('foo@bar.com').get(), saved_user)

