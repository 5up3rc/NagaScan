# -*- coding: utf-8 -*-

""" Hack Requests

This module is a dedicated requests lib that supports cookie, headers, get/post, etc.

"""

import requests
import json
from selenium import webdriver


class HackRequests(object):
    def __init__(self, request_info, lib = 'REQUESTS'):
        self.request_info = request_info
        self.lib = lib
        self.url = "{}://{}{}".format(self.request_info['protocol'], self.request_info['host'], self.request_info['path'])
        self.TIME_OUT = 10 # timeout of requests

        # configurations for PhantomJS
        self.headers = {'User-Agent': self.request_info['user_agent'],
                 'Accept': self.request_info['accept'],
                 'Accept-Language': self.request_info['accept_language'],
                 'Accept-Encoding': self.request_info['accept_encoding'],
                 'Cookie': self.request_info['cookie'],
                 'Referer': self.request_info['referer']}
        self.executable_path='/home/ubuntu/phantomjs-2.1.1-linux-x86_64/bin/phantomjs' # Modify to your own phantomjs binary path
        self.service_args=[]
        self.service_args.append('--load-images=no')
        self.service_args.append('--disk-cache=yes')
        self.service_args.append('--ignore-ssl-errors=true')
        self.driver = self.init_phantomjs_driver(executable_path = self.executable_path, service_args = self.service_args)

    def get_request(self):
        if self.lib == "REQUESTS":
            headers = {'User-Agent': self.request_info['user_agent'],
                     'Accept': self.request_info['accept'],
                     'Accept-Language': self.request_info['accept_language'],
                     'Accept-Encoding': self.request_info['accept_encoding'],
                     'Referer': self.request_info['referer']}
            try:
                if self.request_info['cookie']:
                    cookies = self.get_cookie()
                    r = requests.get(self.url, headers = headers, cookies = cookies, timeout = self.TIME_OUT, verify=False).content
                else:
                    r = requests.get(self.url, headers = headers, timeout = self.TIME_OUT, verify=False).content
            except Exception, e:
                print str(e)
                r = ""
            return r
        elif self.lib == "PHANTOMJS":
            try:
                self.driver.get(self.url)
                r = self.driver.page_source
            except Exception, e:
                print str(e)
                r = ""
            return r

    def post_request(self):
        data = self.get_post_data()
        headers = {'User-Agent': self.request_info['user_agent'],
                 'Accept': self.request_info['accept'],
                 'Accept-Language': self.request_info['accept_language'],
                 'Accept-Encoding': self.request_info['accept_encoding'],
                 'Referer': self.request_info['referer']}
        try:
            if self.request_info['cookie']:
                cookies = self.get_cookie()
                r = requests.post(self.url, data = data, headers = headers, cookies = cookies, timeout = self.TIME_OUT, verify=False).content
            else:
                r = requests.post(self.url, data = data, headers = headers, timeout = self.TIME_OUT, verify=False).content
        except Exception, e:
            print str(e)
            r = ""
        return r

    def get_cookie(self):
        cookies = {}
        for line in self.request_info['cookie'].split(';'):
            name, value = line.strip().split('=', 1) # 1 means only split one time
            cookies[name] = value

        return cookies

    def get_post_data(self):
        if "application/x-www-form-urlencoded" in self.request_info['content_type']:
            post_data = {}
            for line in self.request_info['post_data'].split('&'):
                name, value = line.strip().split('=', 1) # 1 means only split one time
                post_data[name] = value
        elif "application/json" in self.request_info['content_type']:
            post_data = json.dumps(self.request_info['post_data'])
        else:
            post_data = ""

        return post_data

    def init_phantomjs_driver(self, *args, **kwargs):
        for key, value in self.headers.iteritems():
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
        driver =  webdriver.PhantomJS(*args, **kwargs)
        driver.set_page_load_timeout(self.TIME_OUT)
        return driver
