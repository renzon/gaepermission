# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import permissions
from tekton import router


@permissions('ADMIN')
@no_csrf
def list_users(_json, email_prefix='', cursor=None):
    cmd = facade.find_users_by_email_starting_with(email_prefix, cursor)
    users = cmd.execute().result
    users = [u.to_dict(include=['id', 'email', 'name', 'roles']) for u in users]
    cursor_str = cmd.cursor.urlsafe() if cmd.cursor else ''
    next_page = router.to_path(list_users, email_prefix=email_prefix, cursor=cursor_str)
    _json({'users': users, 'next_page': next_page})

