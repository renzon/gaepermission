# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from tekton import router

_security_permission_group_map = {}


def permissions(*groups):
    pass


def permission_not_required():
    pass


def has_permission(user, fcn):
    path = router.to_path(fcn)
    groups = _security_permission_group_map.get(path)
    if groups:
        pass
    return users.is_current_user_admin()
