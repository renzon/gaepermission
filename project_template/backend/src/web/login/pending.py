# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
@login_not_required
def index(_resp, pending_id, ticket):
    facade.login_checking_email(pending_id, ticket, _resp).execute()
    return RedirectResponse('/')