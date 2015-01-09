# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaepermission.decorator import permissions


def sysowner():
    pass


@permissions('ADMIN')
def adm():
    pass


@permissions('MANAGER')
def manager():
    pass


@permissions('ADMIN', 'MANAGER')
def adm_or_manager():
    pass
