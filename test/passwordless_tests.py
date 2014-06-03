# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import memcache
from base import GAETestCase
from gaepermission import facade
from gaepermission.passwordless.commands import GetApp


class AppDateTests(GAETestCase):
    def test_save_or_update(self):
        get_app = GetApp()
        self.assertIsNone(get_app.execute().result)
        facade.save_or_update_passwordless_app_data('1', 't').execute()
        self.assertIsNone(memcache.get(get_app._cache_key()))
        app = GetApp().execute().result
        self.assertEqual('1', app.app_id)
        self.assertEqual('t', app.token)

        facade.save_or_update_passwordless_app_data('2').execute()
        self.assertIsNone(memcache.get(get_app._cache_key()))
        app2 = GetApp().execute().result
        self.assertEqual('2', app2.app_id)
        self.assertEqual('t', app2.token)
        self.assertEqual(app, app2)

        facade.save_or_update_passwordless_app_data(token='t2').execute()
        self.assertIsNone(memcache.get(get_app._cache_key()))
        app3 = GetApp().execute().result
        self.assertEqual('2', app3.app_id)
        self.assertEqual('t2', app3.token)
        self.assertEqual(app, app3)

        facade.save_or_update_passwordless_app_data('1','t').execute()
        self.assertIsNone(memcache.get(get_app._cache_key()))
        app4 = GetApp().execute().result
        self.assertEqual('1', app4.app_id)
        self.assertEqual('t', app4.token)
        self.assertEqual(app, app4)

