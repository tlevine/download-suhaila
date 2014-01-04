#!/usr/bin/env python3
import os
from urllib.parse import urlsplit

from requests import session
from lxml.html import fromstring

# Typing
from requests.sessions import Session
from requests.models import Response
from typing import Tuple
from lxml.html import HtmlElement


USERNAME = 'tlevine'
PASSWORD = 'Onf5nVPgjyn3'

def url(absolute_href:str) -> str:
    return 'http://www.suhailaonlineclasses.com' + absolute_href

class Suhaila:
    def __init__(self, suhaila = None, username = USERNAME, password = PASSWORD):
        self._mkcache()

        if suhaila != None:
            # Use the existing session.
            # This is helpful for development
            # so you don't have to log in
            # every time you change something.
            self.s = suhaila.s
        else:
            self.s = session()
            action = '/amember/member.php'

            r = self.s.get(url(action))
            html = fromstring(r.text)

            names = map(str, html.xpath('//form[@action="/amember/login"]/descendant::input/@name'))
            values = map(str, html.xpath('//form[@action="/amember/login"]/descendant::input/@value'))
            data = dict(zip(names, values))
            data['amember_login'] = username
            data['amember_pass']  = password

            self.s.post(url(action), data = data)

    @staticmethod
    def _mkcache():
        try:
            os.mkdir('cache')
        except OSError:
            pass

    @staticmethod
    def cache(suhaila_url, func):
        _, *urlparts = urlsplit(suhaila_url.rstrip('/?')).path.split('/')
        path = os.path.join('cache', *urlparts)
        if not os.path.exists(path):
            open(path, 'x').write(func())
        return open(path).read()

    def videoadmin(self):
        href = '/videoadmin/'
        raw = self.cache(href, lambda: self.s.get(url(href)).text)
        html = fromstring(raw)
        return html
