# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaepermission.decorator import has_permission, permissions, login_required, login_not_required
from gaepermission.model import MainUser
from mommygae import mommy


class PermissionTests(GAETestCase):
    def test_login_not_required(self):
        @login_not_required
        def f():
            self.executed = True


        user = mommy.save_one(MainUser, groups=[])
        self.assertTrue(has_permission(user, f))
        self.assertTrue(has_permission(None, f))
        f()
        self.assertTrue(self.executed)

    def test_login_required(self):
        @login_required
        def f():
            self.executed = True


        user = mommy.save_one(MainUser)
        self.assertTrue(has_permission(user, f))
        f()
        self.assertTrue(self.executed)
        self.assertFalse(has_permission(None, f))


class GroupTests(GAETestCase):
    def test_white_list_security(self):
        # Only system adming has permission to not decorated functions
        def f():
            self.executed = True


        user = mommy.save_one(MainUser)
        self.assertFalse(has_permission(user, f))
        f()
        self.assertTrue(self.executed)

    def test_google_admin_access(self):
        # system admins have permission in any function
        self.testbed.setup_env(USER_IS_ADMIN='1')

        def f():
            self.executed = True

        @permissions('ADMIN')
        def adm():
            self.executed_adm = True

        user = mommy.save_one(MainUser)

        self.assertTrue(has_permission(user, f))
        f()
        self.assertTrue(self.executed)

        self.assertTrue(has_permission(user, adm))
        adm()
        self.assertTrue(self.executed_adm)


    def test_admin_group(self):
        @permissions('ADMIN')
        def adm():
            self.executed_adm = True

        user = mommy.save_one(MainUser)
        self.assertFalse(has_permission(user, adm))

        user = mommy.save_one(MainUser, groups=['MANAGER'])
        self.assertFalse(has_permission(user, adm))

        user = mommy.save_one(MainUser, groups=['ADMIN'])
        self.assertTrue(has_permission(user, adm))

        user = mommy.save_one(MainUser, groups=['ADMIN', 'MANAGER'])
        self.assertTrue(has_permission(user, adm))

