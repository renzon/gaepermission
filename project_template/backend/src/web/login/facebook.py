# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.tmpl_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse
from web.login import pending


@login_not_required
def index(_resp, token, ret_path='/'):
    cmd = facade.login_facebook(token, _resp)
    cmd.execute()
    if cmd.pending_link:
        pending_path = router.to_path(pending.index, cmd.pending_link.key.id())
        user_email = cmd.main_user_from_email.email
        facade.send_passwordless_login_link(user_email,
                                            'https://gaepermission.appspot.com' + pending_path).execute()
        return TemplateResponse({'provider': 'Facebook', 'email': user_email}, 'login/pending.html')
    return RedirectResponse(ret_path)


@no_csrf
def form():
    app = facade.get_facebook_app_data().execute().result
    dct = {'save_app_path': router.to_path(save), 'app': app}
    return TemplateResponse(dct, 'login/facebook_form.html')


def save(app_id, token):
    facade.save_or_update_facebook_app_data(app_id, token).execute()
    return RedirectResponse('/')