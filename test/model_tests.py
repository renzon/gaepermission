# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaepermission.model import MainUser
from mommygae import mommy


class UserTests(GAETestCase):
    def test_query_email_starts_with(self):
        users_ordered_by_unicode = [mommy.save_one(MainUser, email='%s@foo.com' % b) for b in 'a b c'.split(' ')]
        db_users = MainUser.query_email_starts_with().fetch()
        self.assertListEqual(users_ordered_by_unicode, db_users)

        db_users = MainUser.query_email_starts_with('a').fetch()
        self.assertListEqual(users_ordered_by_unicode[:1], db_users)

        db_users = MainUser.query_email_starts_with('aa@').fetch()
        self.assertListEqual([], db_users)

        abc_user = mommy.save_one(MainUser, email='abc@foo.com')
        db_users = MainUser.query_email_starts_with('aa').fetch()
        self.assertListEqual([], db_users)
        db_users = MainUser.query_email_starts_with('ab').fetch()
        self.assertListEqual([abc_user], db_users)

