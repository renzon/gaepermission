# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaepermission import facade
from gaepermission.model import MainUser
from mommygae import mommy


class GetUserByEmailTests(GAETestCase):
    def test_get_user(self):
        user = mommy.save_one(MainUser, email='foo@bar.com')
        cmd = facade.get_user_by_email('foo@bar.com')
        self.assertEqual(user, cmd())

    def test_not_get_user(self):
        cmd = facade.get_user_by_email('foo@bar.com')
        self.assertIsNone(cmd())

