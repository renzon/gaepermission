# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node, Arc


class MainUser(Node):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    groups = ndb.StringProperty(repeated=True)

    @classmethod
    def query_email_starts_with(cls, prefix=''):
        last_str_with_prefix = prefix + unichr(0x110000 - 1)
        return cls.query(cls.email >= prefix, cls.email < last_str_with_prefix).order(cls.email)

    @classmethod
    def query_email(cls, email):
        return cls.query(cls.email == email)


# Users from external providers

class ExternalToMainUser(Arc):
    destination = ndb.KeyProperty(MainUser, required=True)


class GoogleUser(Node):
    google_id = ndb.StringProperty(required=True)

    @classmethod
    def query_by_google_id(cls, google_id):
        return cls.query(cls.google_id == google_id)


class PasswordlessUser(Node):
    pswdless_id = ndb.StringProperty(required=True)  # id on Passwordless

    @classmethod
    def query_by_passworless_id(cls, id):
        return cls.query(cls.pswdless_id == id)




