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


class SaveUserTests(GAETestCase):
    def test_save(self):
        facade.save_user_cmd('renzo@gmail.com', 'Renzo Nuccitelli', locale='pt_BR', timezone='America/Sao_Paulo')()
        user = facade.get_user_by_email('renzo@gmail.com')()
        self.assertEqual('renzo@gmail.com', user.email)
        self.assertEqual('Renzo Nuccitelli', user.name)
        self.assertEqual('pt_BR', user.locale)
        self.assertEqual('America/Sao_Paulo', user.timezone)
        self.assertListEqual([], user.groups)


class FindUsersByGroup(GAETestCase):
    def test_find_user_without_group(self):
        users = facade.find_users_by_email_and_group()()
        self.assertListEqual([], users)
        saved_users = []
        saved_users.append(facade.save_user_cmd('a@a.com', 'a')())
        saved_users.append(facade.save_user_cmd('b@b.com', 'b', groups=['G1'])())
        saved_users.append(facade.save_user_cmd('c@c.com', 'c', groups=['G2'])())
        saved_users.append(facade.save_user_cmd('c@c.com', 'c', groups=['G1', 'G2'])())
        users = facade.find_users_by_email_and_group()()
        self.assertListEqual(saved_users[:1], users)
        users = facade.find_users_by_email_and_group('a')()
        self.assertListEqual(saved_users[:1], users, users)

    def test_find_user_with_group(self):
        users = facade.find_users_by_email_and_group(group='G1')()
        self.assertListEqual([], users)
        saved_users = []
        saved_users.append(facade.save_user_cmd('a@a.com', 'a')())
        saved_users.append(facade.save_user_cmd('b@b.com', 'b', groups=['G1'])())
        saved_users.append(facade.save_user_cmd('c@c.com', 'c', groups=['G2'])())
        saved_users.append(facade.save_user_cmd('d@c.com', 'd', groups=['G1', 'G2'])())
        users = facade.find_users_by_email_and_group(group='G1')()
        self.assertListEqual(saved_users[1::2], users)
        users = facade.find_users_by_email_and_group(group='G2')()
        self.assertListEqual(saved_users[2:], users)
        users = facade.find_users_by_email_and_group('b@', group='G2')()
        self.assertListEqual([], users)
        users = facade.find_users_by_email_and_group('c@', group='G2')()
        self.assertListEqual(saved_users[2:3], users)


