# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router
from web import groups
from web.login import home
from web.permission import home as permission_home


@login_not_required
@no_csrf
def index(_write_tmpl):
    _write_tmpl('home.html', {'login_path': router.to_path(home.index),
                              'security_tabe_path': router.to_path(permission_home.index),
                              'no_login_path': router.to_path(groups.nologin),
                              'no_permission_path': router.to_path(groups.nopermission),
                              'adm_path': router.to_path(groups.admin),
                              'adm_or_manager_path': router.to_path(groups.admin_or_manager),
                              'manager_path': router.to_path(groups.manager),
                              'sys_owner_path': router.to_path(groups.sysowner)})
