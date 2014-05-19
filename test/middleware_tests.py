# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaepermission import middleware
from gaepermission.model import MainUser
from mock import Mock, patch


class LoggedUserTests(GAETestCase):
    @patch('gaepermission.middleware.facade', )
    def test_no_logged_user(self, facade):
        cmd_mock = Mock()
        cmd_mock.execute = Mock(return_value=cmd_mock)
        cmd_mock.result = None
        facade.logged_user = Mock(return_value=cmd_mock)
        dependency = {}
        middleware.LoggedUser(Mock(), dependency, Mock()).set_up()
        self.assertEqual({'_login_path': '/login',
                          '_logout_path': '/logout',
                          '_logged_user': None}, dependency)

    @patch('gaepermission.middleware.facade', )
    def test_logged_user(self, facade):
        user = MainUser()
        user.put()
        cmd_mock = Mock()
        cmd_mock.execute = Mock(return_value=cmd_mock)
        cmd_mock.result = user
        facade.logged_user = Mock(return_value=cmd_mock)
        dependency = {}
        middleware.LoggedUser(Mock(), dependency, Mock()).set_up()
        self.assertEqual({'_login_path': '/login',
                          '_logout_path': '/logout',
                          '_logged_user': user}, dependency)