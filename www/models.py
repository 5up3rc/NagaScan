#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'avfisher'

'''
Models for user, blog, comment.
'''

import time, uuid

from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField, DatetimeField, LongTextField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(updatable=False, ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(updatable=False, default=time.time)

class Request(Model):
    __table__ = 'requests'

    id = StringField(primary_key=True, ddl='int(32)')
    rid = StringField(updatable=False, ddl='varchar(64)')
    ip = StringField(ddl='varchar(40)')
    port = StringField(ddl='varchar(40)')
    protocol = StringField(ddl='varchar(40)')
    host = StringField(ddl='varchar(255)')
    method = StringField(ddl='varchar(40)')
    user_agent = TextField()
    accept = StringField(ddl='varchar(255)')
    accept_language = StringField(ddl='varchar(255)')
    accept_encoding = StringField(ddl='varchar(255)')
    cookie = TextField()
    referer = TextField()
    content_type = StringField(ddl='varchar(255)')
    post_data = TextField()
    path = TextField()
    scan_xss = StringField(ddl='int(4)')
    scan_sqli = StringField(ddl='int(4)')
    result_xss = StringField(ddl='varchar(40)')
    result_sqli = StringField(ddl='varchar(40)')
    poc_xss = TextField()
    poc_sqli = TextField()
    time = StringField(ddl='varchar(255)')
    update_time = StringField(ddl='varchar(255)')

class Response(Model):
    __table__ = 'responses'

    id = StringField(primary_key=True, ddl='int(32)')
    rid = StringField(updatable=False, ddl='varchar(64)')
    response_xss = LongTextField()
    response_fi = LongTextField()
    update_time = StringField(ddl='varchar(255)')

class ExclusionScan(Model):
    __table__ = 'exclusions_scan'

    id = StringField(primary_key=True, ddl='int(50)')
    type = StringField(ddl='int(4)')
    ip = StringField(ddl='varchar(40)')
    port = StringField(ddl='varchar(40)')
    protocol = StringField(ddl='varchar(40)')
    host = StringField(ddl='varchar(255)')
    method = StringField(ddl='varchar(40)')
    user_agent = TextField()
    accept = StringField(ddl='varchar(255)')
    accept_language = StringField(ddl='varchar(255)')
    accept_encoding = StringField(ddl='varchar(255)')
    cookie = TextField()
    referer = TextField()
    content_type = StringField(ddl='varchar(255)')
    post_data = TextField()
    path = TextField()
    update_time = StringField(ddl='varchar(255)')

class ExclusionParse(Model):
    __table__ = 'exclusions_parse'

    id = StringField(primary_key=True, ddl='int(50)')
    exclusion = StringField(ddl='varchar(255)')
    update_time = StringField(ddl='varchar(255)')

class ExclusionCookie(Model):
    __table__ = 'exclusions_cookie'

    id = StringField(primary_key=True, ddl='int(50)')
    exclusion = TextField()
    update_time = StringField(ddl='varchar(255)')

class Sqlmap(Model):
    __table__ = 'sqlmap'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    ip = StringField(ddl='varchar(40)')
    port = StringField(ddl='varchar(40)')
    status = StringField(ddl='int(4)')
    update_time = StringField(ddl='varchar(255)')
