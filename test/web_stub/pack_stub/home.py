# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import permission_not_required


@no_csrf
@permission_not_required
def index():
    pass