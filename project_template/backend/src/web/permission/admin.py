# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import permissions
from tekton import router


@permissions('ADMIN')
@no_csrf
def index(_write_tmpl):
    dct = {'list_users_path': router.to_path(list_users)}
    _write_tmpl('/permission/admin.html', dct)


@permissions('ADMIN')
def list_users(_json, email_prefix='', cursor=None):
    cmd = facade.find_users_by_email_starting_with(email_prefix, cursor, 2)
    users = cmd.execute().result
    users = [u.to_dict(include=['id', 'email', 'name', 'roles']) for u in users]
    cursor_str = cmd.cursor.urlsafe() if cmd.cursor else ''
    next_page = router.to_path(list_users, email_prefix=email_prefix, cursor=cursor_str)
    _json({'users': users, 'next_page': next_page, 'more': cmd.more})

