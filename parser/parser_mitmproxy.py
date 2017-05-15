# -*- coding: utf-8 -*-

""" Parse mitmproxy Request Log

This module is used to parse mitmproxy Requests and insert into MySQL DB.

Usage:
    python parser_mitmproxy.py logs.txt

"""

import sys
import re
import MySQLdb
import hashlib
import time
from lib.db_operation import db_insert, db_query, fetch_exclusion_parse, get_parse_exclusion_info
from lib.utils import highlight, escape_content


ENVIRONMENT = "Linux"
#ENVIRONMENT = "Windows"

def is_duplicate(table, rid):
    try:
        sql = "SELECT COUNT(*) FROM {} where rid ='{}'".format(table, rid.strip())
        query_result = db_query(sql)
        count = [row[0] for row in query_result]
        if count[0] >= 1:
            return True
        else:
            return False
    except Exception, e:
        print highlight('[!] {}'.format(str(e)), 'red')
        return False

def insert_request(request):
    try:
        feeds = []
        for key, value in request.items():
            if key != 'time':
                feeds.append(escape_content(value))
        feeds_str = ",".join(feeds)
        rid = hashlib.sha256(feeds_str).hexdigest()
        if not is_duplicate('requests', rid):
            now = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            table_request = 'requests'
            request['rid'] = rid
            request['update_time'] = now

            table_response = 'responses'
            args_response = {}
            args_response['rid'] = rid
            args_response['update_time'] = now

            flag = 'insert'
        else:
            now = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            table_request = 'requests'
            args_request = {}
            args_request['update_time'] = now
            cons_request = {}
            cons_request['rid'] = rid

            table_response = 'responses'
            args_response = {}
            args_response['update_time'] = now
            cons_response = {}
            cons_response['rid'] = rid

            flag = 'update'
        if flag == 'insert':
            if db_insert(table_request, request) and db_insert(table_response, args_response):
                print highlight('[+] {} request rid: {}, url: {}://{}{}'.format(flag, rid, request['protocol'], request['host'], request['path']), 'green')
                return True
            else:
                return False
    except Exception, e:
        print highlight('[!] {}'.format(str(e)), 'red')
        return False

def get_item_info(line, item, delim):
    if item in line:
        item_info = line.split(delim, 1)[1].strip()
        reg = '^b\'(.*?)\'$'
        match = re.search(reg, item_info)
        if match:
            item_info = match.group(1)
    else:
        item_info = ''
    return item_info

def is_contained(rtext, excludes):
    if len(excludes):
        excludes_str = '|'.join(excludes)
        reg = '.*({}).*'.format(excludes_str)
        res = re.search(reg, rtext)
        if res:
            return True
        else:
            return False
    else:
        return False

def get_file_to_array(log_file):
    with open(log_file, 'rb') as f:  # Note: Here is 'rb' rather than 'r'
        contents = f.readlines()
    num_of_delim = 0
    requests = []
    request_str = ''
    for i in range(len(contents)):
        if num_of_delim == 1:
            requests.append(request_str.strip('\r\n'))
            request_str = ''
            num_of_delim = 0
        if '======================================================' in contents[i]:
            num_of_delim += 1
        request_str += contents[i]
    return requests

def parse_request_info(request_info):
    if ENVIRONMENT == "Linux":
        lines = request_info.split('\n') # For Linux
    elif ENVIRONMENT == "Windows":
        lines = request_info.split('\n') # For Windows
    requestinfo = {}
    for line in lines:
        time = get_item_info(line, 'time:', ': ')
        protocol = get_item_info(line, 'protocol:', ': ')
        host = get_item_info(line, 'host:', ': ')
        path = get_item_info(line, 'path:', ': ')
        method = get_item_info(line, 'method:', ': ')
        port = get_item_info(line, 'port:', ': ')
        user_agent = get_item_info(line, 'user_agent:', ': ')
        accept = get_item_info(line, 'accept:', ': ')
        accept_language = get_item_info(line, 'accept_language:', ': ')
        accept_encoding = get_item_info(line, 'accept_encoding:', ': ')
        content_type = get_item_info(line, 'content_type:', ': ')
        referer = get_item_info(line, 'referer:', ': ')
        cookie = get_item_info(line, 'cookie:', ': ')
        post_data = get_item_info(line, 'post_data:', ': ')
        if time:
            requestinfo['time'] = time
        if protocol:
            requestinfo['protocol'] = protocol
        if port:
            requestinfo['port'] = port
        if method:
            requestinfo['method'] = method
        if path:
            requestinfo['path'] = path
        if host:
            requestinfo['host'] = host
        if user_agent:
            requestinfo['user_agent'] = user_agent
        if accept:
            requestinfo['accept'] = accept
        if accept_language:
            requestinfo['accept_language'] = accept_language
        if accept_encoding:
            requestinfo['accept_encoding'] = accept_encoding
        if content_type:
            requestinfo['content_type'] = content_type
        if referer:
            requestinfo['referer'] = referer
        if cookie:
            requestinfo['cookie'] = cookie
        if post_data:
            requestinfo['post_data'] = post_data
    return requestinfo

def parse_log(log_file, excludes):
    requests = get_file_to_array(log_file)
    for request in requests:
        if not is_contained(request, excludes):
            request_info = request.split('======================================================')[0]
            request_info_parsed = parse_request_info(request_info)
            insert_request(request_info_parsed) # Insert Mitmproxy requests into Database

def main():
    log_file = sys.argv[1]
    excludes = get_parse_exclusion_info(fetch_exclusion_parse()[0])
    parse_log(log_file, excludes)

if __name__ == "__main__":
    while True:
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        delim = '.............................................'
        print "[*][{}] Time: {}\n{}".format('Requests Analysis', highlight(str(now), 'green'), delim)
        main()
        time.sleep(5)
        print delim, '\n'
