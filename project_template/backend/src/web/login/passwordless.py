# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.tmpl_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
@login_not_required
def index():
    return TemplateResponse(template_path='login/passwordless_info.html')


@login_not_required
def send_email(email, ret_path='/'):
    url = 'https://gaepermission.appspot.com' + router.to_path(check, ret_path=ret_path)
    facade.send_passwordless_login_link(email, url).execute()
    return RedirectResponse(index)


@no_csrf
@login_not_required
def check(_resp, ticket, ret_path='/'):
    facade.login_passwordless(ticket, _resp).execute()
    return RedirectResponse(ret_path)


@no_csrf
def form():
    app = facade.get_passwordless_app_data().execute().result
    dct = {'save_app_path': router.to_path(save), 'app': app}
    return TemplateResponse(dct, 'login/passwordless_form.html')


def save(_handler, app_id, token):
    facade.save_or_update_passwordless_app_data(app_id, token).execute()
    _handler.redirect('/')