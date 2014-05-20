# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router
from web import permission
from web.login import home


@login_not_required
@no_csrf
def index(_write_tmpl):
    _write_tmpl('home.html', {'login_path': router.to_path(home.index),
                              'no_login_path': router.to_path(permission.nologin),
                              'no_permission_path': router.to_path(permission.nopermission),
                              'adm_path': router.to_path(permission.admin),
                              'adm_or_manager_path': router.to_path(permission.admin_or_manager),
                              'manager_path': router.to_path(permission.manager),
                              'sys_owner_path': router.to_path(permission.sysowner)})
