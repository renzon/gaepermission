# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaepermission import facade
from gaepermission.model import MainUser
from mock import patch, Mock


class LoggedUserTests(GAETestCase):
    @patch('gaepermission.facade.cookie_facade')
    def test_no_logged_user(self, cookie_facade):
        cookie_facade.retrive_cookie_data = Mock(return_value=None)
        result = facade.logged_user(None).execute().result
        self.assertIsNone(result)

    @patch('gaepermission.facade.cookie_facade')
    def test_no_logged_user(self, cookie_facade):
        user = MainUser()
        user.put()
        cookie_facade.retrive_cookie_data = Mock(return_value={'id': user.key.id()})
        result = facade.logged_user(None).execute().result
        self.assertEqual(user, result)
