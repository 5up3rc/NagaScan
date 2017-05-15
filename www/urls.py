#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'avfisher'

import os, re, time, base64, hashlib, logging

from transwarp.web import get, post, ctx, view, interceptor, seeother, notfound

from apis import api, Page, APIError, APIValueError, APIPermissionError, APIResourceNotFoundError
from models import User, Request, ExclusionScan, ExclusionParse, ExclusionCookie, Sqlmap, Response
from config import configs

from utils import content_escape, html_encode


_COOKIE_NAME = 'NAGASCAN-ID'
_COOKIE_KEY = configs.session.secret

def _get_page_index():
    page_index = 1
    try:
        page_index = int(ctx.request.get('page', '1'))
    except ValueError:
        pass
    return page_index

def make_signed_cookie(id, password, max_age):
    # build cookie string by: id-expires-md5
    expires = str(int(time.time() + (max_age or 86400)))
    L = [id, expires, hashlib.md5('%s-%s-%s-%s' % (id, password, expires, _COOKIE_KEY)).hexdigest()]
    return '-'.join(L)

def parse_signed_cookie(cookie_str):
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        id, expires, md5 = L
        if int(expires) < time.time():
            return None
        user = User.get(id)
        if user is None:
            return None
        if md5 != hashlib.md5('%s-%s-%s-%s' % (id, user.password, expires, _COOKIE_KEY)).hexdigest():
            return None
        return user
    except:
        return None

def check_admin():
    user = ctx.request.user
    if user and user.admin:
        return
    raise APIPermissionError('No permission.')

def exclusion_validate(exclusion):
    for k, v in exclusion.items():
        if len(str(v)) > 255:
            return 'The length of {%s} cannot exceed 255 characters, please check!' % str(k)
        try:
            reg = '^[\w\s\|\.\?\;\=\-\/\@\&\:\(\)]*$'
            se = re.match(reg, str(v))
            if not se:
                return 'Incorrect {%s}, please check!' % str(k)
        except Exception:
            return 'Incorrect {%s}, please check!' % str(k)
    return 'success'

def sqlmap_validate(sqlmap):
    for k, v in sqlmap.items():
        if k in ["ip", "port", "status"]:
            try:
                if k == "ip":
                    reg = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
                if k == "port":
                    reg = '^\d{1,5}$'
                if k == "status":
                    reg = '^[1-2]$'
                se = re.match(reg, str(v))
                if not se:
                    return 'Incorrect {%s}, please check!' % str(k)
            except Exception:
                return 'Incorrect {%s}, please check!' % str(k)
    return 'success'

@interceptor('/')
def user_interceptor(next):
    logging.info('try to bind user from session cookie...')
    user = None
    cookie = ctx.request.cookies.get(_COOKIE_NAME)
    if cookie:
        logging.info('parse session cookie...')
        user = parse_signed_cookie(cookie)
        if user:
            logging.info('bind user <%s> to session...' % user.email)
    ctx.request.user = user
    return next()

@interceptor('/manage/')
def manage_interceptor(next):
    user = ctx.request.user
    if user and user.admin:
        return next()
    raise seeother('/signin')

@view('blogs.html')
@get('/')
def index():
    raise seeother('/manage/')

@view('signin.html')
@get('/signin')
def signin():
    return dict()

@get('/signout')
def signout():
    ctx.response.delete_cookie(_COOKIE_NAME)
    raise seeother('/')

@api
@post('/api/authenticate')
def authenticate():
    i = ctx.request.input(remember='')
    email = i.email.strip().lower()
    password = i.password
    remember = i.remember
    user = User.find_first('where email=?', email)
    if user is None:
        raise APIError('auth:failed', 'email', 'Invalid email.')
    elif user.password != password:
        raise APIError('auth:failed', 'password', 'Invalid password.')
    # make session cookie:
    max_age = 604800 if remember=='true' else None
    cookie = make_signed_cookie(user.id, user.password, max_age)
    ctx.response.set_cookie(_COOKIE_NAME, cookie, max_age=max_age)
    user.password = '******'
    return user

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')

@api
@post('/api/users')
def register_user():
    i = ctx.request.input(name='', email='', password='')
    name = i.name.strip()
    email = i.email.strip().lower()
    password = i.password
    if not name:
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not _RE_MD5.match(password):
        raise APIValueError('password')
    user = User.find_first('where email=?', email)
    if user:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    user = User(name=name, email=email, password=password, image='http://avfisher.win/wp-content/uploads/2015/10/avfisher.jpg' % hashlib.md5(email).hexdigest())
    user.insert()
    # make session cookie:
    cookie = make_signed_cookie(user.id, user.password, None)
    ctx.response.set_cookie(_COOKIE_NAME, cookie)
    return user

@view('register.html')
@get('/register')
def register():
    return dict()

@get('/manage/')
def manage_index():
    raise seeother('/manage/requests')

@view('manage_request_list.html')
@get('/manage/requests')
def manage_requests():
    return dict(page_index=_get_page_index(), user=ctx.request.user)

@view('manage_vulns_list.html')
@get('/manage/vulns/:type/list')
def manage_vulns_list(type):
    return dict(type=content_escape(type), page_index=_get_page_index(), user=ctx.request.user)

@view('manage_request_view.html')
@get('/manage/requests/:request_rid/view')
def manage_request_view(request_rid):
    return dict(url='/api/requests/%s/view' % request_rid, user=ctx.request.user)

@view('manage_user_list.html')
@get('/manage/users')
def manage_users():
    return dict(page_index=_get_page_index(), user=ctx.request.user)

@view('manage_exclusion_view.html')
@get('/manage/exclusions/:type/view')
def manage_exclusion_view(type):
    return dict(type=content_escape(type), user=ctx.request.user)

@view('manage_scan_view.html')
@get('/manage/scan/:type/view')
def manage_scan_view(type):
    return dict(page_index=_get_page_index(), type=content_escape(type), user=ctx.request.user)

@view('manage_scan_edit.html')
@get('/manage/scan/:type/:id/edit')
def manage_scan_edit(type, id):
    return dict(url='/api/scan/%s/%s/edit' % (content_escape(type), content_escape(id)), user=ctx.request.user)

@view('manage_scan_add.html')
@get('/manage/scan/:type/add')
def manage_scan_add(type):
    return dict(url='/api/scan/%s/add' % content_escape(type), type=content_escape(type), user=ctx.request.user)

@api
@get('/api/requests')
def api_get_requests():
    total = Request.count_all()
    page = Page(total, _get_page_index())
    requests = Request.find_by('order by id desc limit ?,?', page.offset, page.limit)
    return dict(requests=content_escape(requests), page=page)

@api
@get('/api/vulns/:type/list')
def api_list_vulns(type):
    check_admin()
    if type == "xss":
        total = Request.count_by('where result_xss = ?', 'vulnerable')
        page = Page(total, _get_page_index())
        requests = Request.find_by('where result_xss = ? order by id desc limit ?,?', 'vulnerable', page.offset, page.limit)
    elif type == "sqli":
        total = Request.count_by('where result_sqli = ?', 'vulnerable')
        page = Page(total, _get_page_index())
        requests = Request.find_by('where result_sqli = ? order by id desc limit ?,?', 'vulnerable', page.offset, page.limit)
    elif type == "fi":
        total = Request.count_by('where result_fi = ?', 'vulnerable')
        page = Page(total, _get_page_index())
        requests = Request.find_by('where result_fi = ? order by id desc limit ?,?', 'vulnerable', page.offset, page.limit)
    else:
        raise notfound()
    return dict(type=content_escape(type), requests=content_escape(requests), page=page)

@api
@get('/api/requests/:request_rid/view')
def api_view_request(request_rid):
    check_admin()
    request = Request.find_by('where rid = ?', request_rid)
    response = Response.find_by('where rid = ?', request_rid)
    if request is None or response is None:
        raise notfound()
    return dict(request=content_escape(request), response=html_encode(response))

@api
@get('/api/users')
def api_get_users():
    total = User.count_all()
    page = Page(total, _get_page_index())
    users = User.find_by('order by created_at desc limit ?,?', page.offset, page.limit)
    for u in users:
        u.password = '******'
    return dict(users=users, page=page)

@api
@get('/api/exclusions/:type/view')
def api_view_exclusion(type):
    check_admin()
    if type == "parse":
        exclusion = ExclusionParse.find_all()[0]
    elif type == "xss":
        exclusion = ExclusionScan.find_by('where type=0')[0]
    elif type == "sqli":
        exclusion = ExclusionScan.find_by('where type=1')[0]
    elif type == "fi":
        exclusion = ExclusionScan.find_by('where type=2')[0]
    elif type == "cookie":
        exclusion = ExclusionCookie.find_all()[0]
    else:
        raise notfound()
    return dict(type=content_escape(type), exclusion=content_escape(exclusion))

@api
@post('/api/exclusions/:type/update')
def api_update_exclusion(type):
    check_admin()
    now = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    i = ctx.request.input()
    if type == "parse":
        exclusion_parse = ExclusionParse.find_all()[0]
        exclusion_parse.exclusion = content_escape(i.exclusion.strip().lower())
        exclusion_parse.update_time = now
        res = exclusion_validate(exclusion_parse)
        if res == 'success':
            exclusion_parse.update()
        else:
            return dict(result='failed', error=res)
    elif type == "cookie":
        exclusion_cookie = ExclusionCookie.find_all()[0]
        exclusion_cookie.exclusion = content_escape(i.exclusion.strip().lower())
        exclusion_cookie.update_time = now
        res = exclusion_validate(exclusion_cookie)
        if res == 'success':
            exclusion_cookie.update()
        else:
            return dict(result='failed', error=res)
    elif type == "xss":
        exclusion_scan = ExclusionScan.find_by('where type=0')[0]
        exclusion_scan.method = content_escape(i.method.strip().lower())
        exclusion_scan.protocol = content_escape(i.protocol.strip().lower())
        exclusion_scan.host = content_escape(i.host.strip().lower())
        exclusion_scan.ip = content_escape(i.ip.strip().lower())
        exclusion_scan.port = content_escape(i.port.strip().lower())
        exclusion_scan.path = content_escape(i.path.strip().lower())
        exclusion_scan.accept = content_escape(i.accept.strip().lower())
        exclusion_scan.accept_language = content_escape(i.accept_language.strip().lower())
        exclusion_scan.accept_encoding = content_escape(i.accept_encoding.strip().lower())
        exclusion_scan.referer = content_escape(i.referer.strip().lower())
        exclusion_scan.user_agent = content_escape(i.user_agent.strip().lower())
        exclusion_scan.cookie = content_escape(i.cookie.strip().lower())
        exclusion_scan.content_type = content_escape(i.content_type.strip().lower())
        exclusion_scan.post_data = content_escape(i.post_data.strip().lower())
        exclusion_scan.update_time = now
        res = exclusion_validate(exclusion_scan)
        if res == 'success':
            exclusion_scan.update()
        else:
            return dict(result='failed', error=res)
    elif type == "sqli":
        exclusion_scan = ExclusionScan.find_by('where type=1')[0]
        exclusion_scan.method = content_escape(i.method.strip().lower())
        exclusion_scan.protocol = content_escape(i.protocol.strip().lower())
        exclusion_scan.host = content_escape(i.host.strip().lower())
        exclusion_scan.ip = content_escape(i.ip.strip().lower())
        exclusion_scan.port = content_escape(i.port.strip().lower())
        exclusion_scan.path = content_escape(i.path.strip().lower())
        exclusion_scan.accept = content_escape(i.accept.strip().lower())
        exclusion_scan.accept_language = content_escape(i.accept_language.strip().lower())
        exclusion_scan.accept_encoding = content_escape(i.accept_encoding.strip().lower())
        exclusion_scan.referer = content_escape(i.referer.strip().lower())
        exclusion_scan.user_agent = content_escape(i.user_agent.strip().lower())
        exclusion_scan.cookie = content_escape(i.cookie.strip().lower())
        exclusion_scan.content_type = content_escape(i.content_type.strip().lower())
        exclusion_scan.post_data = content_escape(i.post_data.strip().lower())
        exclusion_scan.update_time = now
        res = exclusion_validate(exclusion_scan)
        if res == 'success':
            exclusion_scan.update()
        else:
            return dict(result='failed', error=res)
    elif type == "fi":
        exclusion_scan = ExclusionScan.find_by('where type=2')[0]
        exclusion_scan.method = content_escape(i.method.strip().lower())
        exclusion_scan.protocol = content_escape(i.protocol.strip().lower())
        exclusion_scan.host = content_escape(i.host.strip().lower())
        exclusion_scan.ip = content_escape(i.ip.strip().lower())
        exclusion_scan.port = content_escape(i.port.strip().lower())
        exclusion_scan.path = content_escape(i.path.strip().lower())
        exclusion_scan.accept = content_escape(i.accept.strip().lower())
        exclusion_scan.accept_language = content_escape(i.accept_language.strip().lower())
        exclusion_scan.accept_encoding = content_escape(i.accept_encoding.strip().lower())
        exclusion_scan.referer = content_escape(i.referer.strip().lower())
        exclusion_scan.user_agent = content_escape(i.user_agent.strip().lower())
        exclusion_scan.cookie = content_escape(i.cookie.strip().lower())
        exclusion_scan.content_type = content_escape(i.content_type.strip().lower())
        exclusion_scan.post_data = content_escape(i.post_data.strip().lower())
        exclusion_scan.update_time = now
        res = exclusion_validate(exclusion_scan)
        if res == 'success':
            exclusion_scan.update()
        else:
            return dict(result='failed', error=res)
    else:
        return dict(result='failed', error='unknown scan type!')
    return dict(result='success')

@api
@get('/api/scan/:type/view')
def api_view_scan(type):
    check_admin()
    if type == "sqlmap":
        total = Sqlmap.count_all()
        page = Page(total, _get_page_index())
        sqlmaps = Sqlmap.find_by('order by update_time desc limit ?,?', page.offset, page.limit)
        return dict(type=content_escape(type), sqlmaps=content_escape(sqlmaps), page=page)
    else:
        raise notfound()

@api
@get('/api/scan/:type/:id/edit')
def api_edit_scan(type, id):
    check_admin()
    if type == "sqlmap":
        sqlmap = Sqlmap.find_by('where id = ?', content_escape(id))
        return dict(type=content_escape(type), id=content_escape(id), sqlmap=content_escape(sqlmap))
    else:
        raise notfound()

@api
@post('/api/scan/:type/:id/update')
def api_update_scan(type, id):
    check_admin()
    now = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    i = ctx.request.input()
    if type == "sqlmap":
        sqlmap = Sqlmap.get(content_escape(id))
        sqlmap.ip = content_escape(i.ip.strip().lower())
        sqlmap.port = content_escape(i.port.strip().lower())
        sqlmap.status = i.status.strip().lower()
        sqlmap.update_time = now
        res = sqlmap_validate(sqlmap)
        if res == 'success':
            sqlmap.update()
        else:
            return dict(result='failed', error=res)
    else:
        return dict(result='failed', error='unknown scan type!')
    return dict(result='success')

@api
@post('/api/scan/:type/add')
def api_add_scan(type):
    check_admin()
    now = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    i = ctx.request.input()
    if type == "sqlmap":
        sqlmap = Sqlmap()
        sqlmap.ip = content_escape(i.ip.strip().lower())
        sqlmap.port = content_escape(i.port.strip().lower())
        sqlmap.status = i.status.strip().lower()
        sqlmap.update_time = now
        res = sqlmap_validate(sqlmap)
        if res == 'success':
            sqlmap.insert()
        else:
            return dict(result='failed', error=res)
    else:
        return dict(result='failed', error='unknown scan type!')
    return dict(result='success')

@api
@get('/api/scan/:type/:id/delete')
def api_delete_scan(type, id):
    check_admin()
    if type == "sqlmap":
        sqlmap = Sqlmap(id=content_escape(id))
        sqlmap.delete()
    else:
        return dict(result='failed', error='unknown scan type!')
    return dict(result='success')
