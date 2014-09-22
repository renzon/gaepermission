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

