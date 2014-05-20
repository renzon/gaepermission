# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from gaecookie.decorator import no_csrf
from gaepermission.decorator import get_groups, login_not_required, permission_not_required, permissions
from tekton import router


def _helper(_write_tmpl, fcn):
    dct = {'groups': get_groups(fcn),
           'path': router.to_path(fcn),
           'sys_owner': users.is_current_user_admin()}
    _write_tmpl('permission.html', dct)


@no_csrf
def sysowner(_write_tmpl):
    _helper(_write_tmpl, sysowner)


@login_not_required
@no_csrf
def nologin(_write_tmpl):
    _helper(_write_tmpl, nologin)


@permission_not_required
@no_csrf
def nopermission(_write_tmpl):
    _helper(_write_tmpl, nopermission)


@permissions('ADMIN')
@no_csrf
def admin(_write_tmpl):
    _helper(_write_tmpl, admin)


@permissions('ADMIN', 'MANAGER')
@no_csrf
def admin_or_manager(_write_tmpl):
    _helper(_write_tmpl, nopermission)


@permissions('MANAGER')
@no_csrf
def manager(_write_tmpl):
    _helper(_write_tmpl, nopermission)

