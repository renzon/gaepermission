# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from config.tmpl_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import get_groups, login_not_required, login_required, permissions
from tekton import router


def _helper(fcn):
    dct = {'groups': get_groups(fcn),
           'path': router.to_path(fcn),
           'sys_owner': users.is_current_user_admin()}
    return TemplateResponse(dct, 'groups.html')


@no_csrf
def sysowner():
    return _helper(sysowner)


@login_not_required
@no_csrf
def nologin():
    return _helper(nologin)


@login_required
@no_csrf
def login_required():
    return _helper(login_required)


@permissions('ADMIN')
@no_csrf
def admin():
    return _helper(admin)


@permissions('ADMIN', 'MANAGER')
@no_csrf
def admin_or_manager():
    return _helper(admin_or_manager)


@permissions('MANAGER')
@no_csrf
def manager():
    return _helper(manager)

