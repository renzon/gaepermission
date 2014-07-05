# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaepermission import middleware
from gaepermission.model import MainUser
from mock import Mock, patch
from mommygae import mommy


class LoggedUserTests(GAETestCase):
    @patch('gaepermission.middleware.facade', )
    def test_no_logged_user(self, facade):
        cmd_mock = Mock()
        cmd_mock.execute = Mock(return_value=cmd_mock)
        cmd_mock.result = None
        facade.logged_user = Mock(return_value=cmd_mock)
        dependency = {}
        handler = Mock()
        handler.request.path_qs='/foo?param1=1&param2=2'
        middleware.LoggedUserMiddleware(handler, dependency, Mock()).set_up()
        self.assertEqual({'_login_path': '/login?ret_path=%2Ffoo%3Fparam1%3D1%26param2%3D2',
                          '_logout_path': None,
                          '_logged_user': None}, dependency)

    @patch('gaepermission.middleware.facade', )
    def test_logged_user(self, facade):
        user = mommy.save_one(MainUser)
        user.put()
        cmd_mock = Mock()
        cmd_mock.execute = Mock(return_value=cmd_mock)
        cmd_mock.result = user
        facade.logged_user = Mock(return_value=cmd_mock)
        dependency = {}
        middleware.LoggedUserMiddleware(Mock(), dependency, Mock()).set_up()
        self.assertEqual({'_login_path': None,
                          '_logout_path': '/logout',
                          '_logged_user': user}, dependency)