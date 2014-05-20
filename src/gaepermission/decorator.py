# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from tekton import router

_security_permission_group_map = {}


class _PermissionNotRequiredHelper(object):
    '''
    Class that aways returns True for in operation
    '''

    def __init__(self, msg):
        self.msg = msg

    def __contains__(self, item):
        return True

    def __unicode__(self):
        return self.msg


_permission_not_required_helper = _PermissionNotRequiredHelper('Permission not Required')
_login_not_required_helper = _PermissionNotRequiredHelper('Login not Required')


def permissions(*groups):
    def decorator(fcn):
        path = router.to_path(fcn)
        _security_permission_group_map[path] = frozenset(groups)
        return fcn

    return decorator


def login_not_required(fcn):
    path = router.to_path(fcn)
    _security_permission_group_map[path] = _login_not_required_helper
    return fcn


def permission_not_required(fcn):
    path = router.to_path(fcn)
    _security_permission_group_map[path] = _permission_not_required_helper
    return fcn


def get_groups_by_path(path):
    return _security_permission_group_map.get(path)


def get_groups(fcn):
    path = router.to_path(fcn)
    return get_groups_by_path(path)


def has_permission(user, fcn):
    groups = get_groups(fcn)
    if user is None:
        return groups is _login_not_required_helper
    if groups:
        #testing for login or permission not required
        if None in groups:
            return True
        for g in user.groups:
            if g in groups:
                return True

    return users.is_current_user_admin()
