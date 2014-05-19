# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from tekton import router
from web.login import home


@no_csrf
def index(_write_tmpl):
    _write_tmpl('home.html', {'login_path': router.to_path(home.index)})
