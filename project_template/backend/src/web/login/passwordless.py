# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required
from tekton import router


@no_csrf
@login_not_required
def index(_write_tmpl):
    _write_tmpl('login/passwordless_info.html')


@login_not_required
def send_email(_handler, email):
    facade.send_passwordless_login_link(email, 'https://gaepermission.appspot.com' + router.to_path(check)).execute()
    _handler.redirect(router.to_path(index))


@no_csrf
@login_not_required
def check(_handler, _resp, ticket):
    facade.login_passwordless(ticket, _resp).execute()
    _handler.redirect('/')


@no_csrf
def form(_write_tmpl):
    app = facade.get_passwordless_app_data().execute().result
    dct = {'save_app_path': router.to_path(save), 'app': app}
    _write_tmpl('login/passwordless_form.html', dct)


def save(_handler, app_id, token):
    facade.save_or_update_passwordless_app_data(app_id, token).execute()
    _handler.redirect('/')