# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from itertools import izip
import unittest
from gaepermission import inspector
from tekton import router


class InspectorTests(unittest.TestCase):
    def test_web_paths_generator(self):
        generator = inspector.web_paths('web')
        expected_paths = ['/pack_stub/stub/adm',
                          '/pack_stub/stub/adm_or_manager',
                          '/pack_stub/stub/manager',
                          '/pack_stub/stub/sysowner',
                          '/pack_stub',
                          '/']
        self.assertListEqual(expected_paths, [t for t in generator])

    def test_web_paths_security_info(self):
        path_infos = [(t.path, t.groups, t.csrf) for t in inspector.web_paths_security_info('web')]
        expected_paths = ['/pack_stub/stub/adm',
                          '/pack_stub/stub/adm_or_manager',
                          '/pack_stub/stub/manager',
                          '/pack_stub/stub/sysowner',
                          '/pack_stub',
                          '/']
        expected_groups = ['ADMIN', 'ADMIN, MANAGER', 'MANAGER', 'SYS_OWNER', 'Login Required',
                           'Login not Required']

        expected_csrf = [True, True, True, True, False, False]

        expected_path_infos = zip(expected_paths, expected_groups, expected_csrf)
        expected_path_infos.sort(key=lambda e: e[0])

        path_infos.sort(key=lambda e: e[0])
        self.assertListEqual(expected_path_infos, path_infos)
