#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-12-29 上午10:45
# @Author  : Arvin
# @Site    : 
# @File    : HttpTools.py
# @Software: PyCharm


import urllib.request


class HtmlUtil():
    __def_ua = "***"

    __proxy = None
    __user_name = None
    __password = None

    def __init__(self, proxy=None, user_name=None, password=None):
        self.__proxy = proxy
        self.__user_name = user_name
        self.__password = password

    def get(self, url, ua=None):
        if url is None or len(url) == 0:
            raise Exception("url不可为空")
        if ua is None or len(ua) == 0:
            ua = self.__def_ua
        headers = {'User-Agent': ua, 'Connection': 'keep-alive', "Accept": "*/*", "Referer": "http://www.baidu.com"}
        handler = None
        proxy = self.__proxy
        if proxy is not None:
            if self.__user_name is not None and self.__password is not None:
                proxy = self.__user_name + ":" + self.__password + "@" + proxy
            handler = urllib.request.ProxyHandler({'http': 'http://' + proxy + '/'})
        else:
            handler = urllib.request.BaseHandler()
        opener = urllib.request.build_opener(handler)
        get_request = urllib.request.Request(url, None, headers=headers, method="GET")
        get_response = opener.open(get_request)
        html_str = get_response.read().decode()
        return html_str

    def post(self, url, data, ua=None):
        if url is None or len(url) == 0:
            raise Exception("url不可为空")
        if data is None:
            data = {}
        postdata = urllib.parse.urlencode(data).encode()
        if ua is None or len(ua) == 0:
            ua = self.__def_ua
        headers = {'User-Agent': ua, 'Connection': 'keep-alive', "Accept": "*/*", "Referer": "http://www.baidu.com"}
        handler = None
        proxy = self.__proxy
        if proxy is not None:
            if self.__user_name is not None and self.__password is not None:
                proxy = self.__user_name + ":" + self.__password + "@" + proxy
            handler = urllib.request.ProxyHandler({'http': 'http://' + proxy + '/'})
        else:
            handler = urllib.request.BaseHandler()
        opener = urllib.request.build_opener(handler)
        get_request = urllib.request.Request(url, postdata, headers=headers, method="POST")
        get_response = opener.open(get_request)
        html_str = get_response.read().decode()
        return html_str