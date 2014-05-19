# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node, Arc


class MainUser(Node):
    name = ndb.StringProperty()
    email = ndb.StringProperty()


# Users from external providers

class ExternalToMainUser(Arc):
    destination = ndb.KeyProperty(MainUser, required=True)


class GoogleUser(Node):
    google_id = ndb.StringProperty(required=True)

    @classmethod
    def query_by_google_id(cls, google_id):
        return cls.query(cls.google_id == google_id)


