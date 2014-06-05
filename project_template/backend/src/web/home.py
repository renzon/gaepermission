# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router
from web import groups
from web.login import home, passwordless, facebook
from web.permission import home as permission_home, admin


@login_not_required
@no_csrf
def index(_write_tmpl):
    _write_tmpl('home.html', {'login_path': router.to_path(home.index),
                              'security_table_path': router.to_path(permission_home.index),
                              'permission_admin_path': router.to_path(admin),
                              'passwordless_admin_path': router.to_path(passwordless.form),
                              'facebook_admin_path': router.to_path(facebook.form),
                              'no_login_path': router.to_path(groups.nologin),
                              'no_permission_path': router.to_path(groups.login_required),
                              'adm_path': router.to_path(groups.admin),
                              'adm_or_manager_path': router.to_path(groups.admin_or_manager),
                              'manager_path': router.to_path(groups.manager),
                              'sys_owner_path': router.to_path(groups.sysowner)})
