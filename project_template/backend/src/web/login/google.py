# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required


@login_not_required
@no_csrf
def index(_handler, _resp, _write_tmpl):
    user = users.get_current_user()
    if user:
        cmd = facade.login_google(user, _resp).execute()
        if cmd.pending_link:
            _write_tmpl('login/pending.html', {'provider': 'Google', 'email': user.email()})
            return
    _handler.redirect('/')