# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required
from tekton import router


@login_not_required
def index(_handler, _resp, token):
    facade.login_facebook(token, _resp).execute()
    _handler.redirect('/')


@no_csrf
def form(_write_tmpl):
    app = facade.get_facebook_app_data().execute().result
    dct = {'save_app_path': router.to_path(save), 'app': app}
    _write_tmpl('login/facebook_form.html', dct)


def save(_handler, app_id, token):
    facade.save_or_update_facebook_app_data(app_id, token).execute()
    _handler.redirect('/')