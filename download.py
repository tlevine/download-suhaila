#!/usr/bin/env python3
import os
import re
from urllib.parse import urlsplit, urlunsplit

from requests import session
from lxml.html import fromstring

# Typing
import builtins
from requests.sessions import Session
from requests.models import Response
from typing import Tuple
from lxml.html import HtmlElement


USERNAME = 'tlevine'
PASSWORD = 'Onf5nVPgjyn3'

def url(href:str) -> str:
    '''
    >>> url('/videoadmin/category/suhaila-level-1.html')
    'http://www.suhailaonlineclasses.com/videoadmin/category/suhaila-level-1.html'

    >>> url('http://www.suhailaonlineclasses.com/videoadmin/category/suhaila-level-1.html')
    'http://www.suhailaonlineclasses.com/videoadmin/category/suhaila-level-1.html'
    '''
    _, _, path, query, _ = urlsplit(href)
    scheme = 'http'
    netloc = 'www.suhailaonlineclasses.com'
    fragment = '' # The part after the hash sign, like http://example.com#this-section
    return urlunsplit((scheme, netloc, path, query, fragment))

class Suhaila:
    def __init__(self, suhaila = None, username = USERNAME, password = PASSWORD):
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
    def cache(suhaila_url, func):
        _, *middle, last = urlsplit(suhaila_url.rstrip('/?')).path.split('/')

        # If the final thing doesn't have an extension,
        # call it index.html inside the directory.
        path_left = os.path.join('cache', *middle)
        if '.' in last:
            path_right = last
        else:
            path_right = os.path.join(last, 'index.html')
        path = os.path.join(path_left, path_right)

        if not os.path.exists(path):
            directory, _ = os.path.split(path)
            os.makedirs(directory, exist_ok = True)
            open(path, 'x').write(func())
        print(path)
        return open(path).read()

    def get(self, href) -> HtmlElement:
        raw = self.cache(href, lambda: self.s.get(url(href)).text)
        return fromstring(raw)

    def videoadmin(self) -> builtins.map:
        html = self.get('/videoadmin/')
        hrefs = map(str,html.xpath('//div[@class="conter"]/h4/a/@href'))
        return hrefs

def main():
    s = Suhaila()
    for href in s.videoadmin():
        pass


def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()
