# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from itertools import izip
import unittest
from gaepermission import inspector
from tekton import router


class InspectorTests(unittest.TestCase):
    def setUp(self):
        router.package_base = 'web_stub'

    def test_web_paths_generator(self):
        generator = inspector.web_paths('web_stub')
        expected_paths = ['/pack_stub/stub/adm',
                          '/pack_stub/stub/adm_or_manager',
                          '/pack_stub/stub/manager',
                          '/pack_stub/stub/sysowner',
                          '/pack_stub',
                          '/']
        self.assertListEqual(expected_paths, [t for t in generator])

    def test_web_paths_security_info(self):
        path_infos = inspector.web_paths_security_info('web_stub')
        expected_paths = ['/pack_stub/stub/adm',
                          '/pack_stub/stub/adm_or_manager',
                          '/pack_stub/stub/manager',
                          '/pack_stub/stub/sysowner',
                          '/pack_stub',
                          '/']
        expected_groups = ['ADMIN', 'ADMIN, MANAGER', 'MANAGER', 'SYS_OWNER', 'Permission not Required',
                           'Login not Required']

        expected_csrf = [True, True, True, True, False, False]

        for exp_path_info, exp_path, exp_groups, exp_csrf in izip(path_infos, expected_paths, expected_groups,
                                                                  expected_csrf):
            self.assertEqual(exp_path, exp_path_info.path)
            self.assertEqual(exp_groups, exp_path_info.groups)
            self.assertEqual(exp_csrf, exp_path_info.csrf)

    def tearDown(self):
        router.package_base = 'web_stub'