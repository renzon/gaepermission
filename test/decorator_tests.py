# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaepermission.decorator import has_permission
from gaepermission.model import MainUser
from mommygae import mommy


class NoPermissionRequiredTests(GAETestCase):
    def test_white_list_securIty(self):
        def f():
            pass

        user = mommy.save_one(MainUser)
        self.assertFalse(has_permission(user, f))

    def test_google_admin_access(self):
        self.testbed.setup_env(USER_EMAIL='usermail@gmail.com',USER_ID='1', USER_IS_ADMIN='1')
        def adm():
            pass

        user = mommy.save_one(MainUser)
        self.assertTrue(has_permission(user, adm))


