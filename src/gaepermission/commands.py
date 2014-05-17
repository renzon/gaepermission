# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import Command


class FakeCommand(Command):
    '''
    This command is used when there is only the need to keep the Command contract
    '''

    def do_business(self, stop_on_error=True):
        pass