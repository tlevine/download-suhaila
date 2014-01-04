#!/usr/bin/env python3
import os

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
    def __init__(self, username, password):
        self._mkcache()

        self.s = session()
        action = '/amember/member.php'

        r = self.s.get(url(action))
        html = fromstring(r.text)

        names = map(str, html.xpath('//form[@action="/amember/login"]/descendant::input/@name'))
        values = map(str, html.xpath('//form[@action="/amember/login"]/descendant::input/@value'))
        data = dict(zip(names, values))
        data['amember_login'] = username
        data['amember_pass']  = password

        r = self.s.post(url(action), data = data)

    @staticmethod
    def _mkcache():
        try:
            os.mkdir('cache')
        except OSError:
            pass

    @staticmethod
    def cache(filename, func):
        path = os.path.join('cache',filename)
        if not os.path.exists(path):
            open(path, 'x').write(func())
        return open(path).read()

    def videoadmin(self):
        raw = self.cache('videoadmin', lambda: self.s.get(url('/videoadmin/')).text)
        html = fromstring(raw)
        return html
