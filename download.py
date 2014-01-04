#!/usr/bin/env python3
import os
import re
from urllib.parse import urlsplit, urlunsplit

from time import sleep
from random import betavariate

from requests import session
from lxml.html import fromstring

# Typing
from requests.sessions import Session
from requests.models import Response
try:
    from typing import Sequence
except ImportError:
    # Hack in case mypy isn't available
    from builtins import map as Sequence
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
            self.s.headers['user-agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0'
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
        'func must take nothing and return bytes.'
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
            open(path, 'xb').write(func())
        return open(path, 'rb').read()

    def get(self, href, parse_html = True) -> HtmlElement:
        'Download a URL, and optionally parse it as HTML.'
        absolute_url = url(href)
        if parse_html:
            raw = self.cache(href, lambda: self.s.get(absolute_url).content)
            html = fromstring(raw.decode('utf-8'))
            html.make_links_absolute(absolute_url)
            return html
        else:
            self.cache(href, lambda: self.s.get(absolute_url).content)

    def videoadmin(self) -> Sequence:
        'Download and parse the /videoadmin page.'
        html = self.get('/videoadmin/')
        hrefs = map(str,html.xpath('//div[@class="conter"]/h4/a/@href'))
        return hrefs

    def category(self, href) -> Sequence:
        'Download and parse a /videoadmin/category page.'
        html = self.get(href)
        return (x.replace('videoadmin/../', '') for x in
                html.xpath('//a[contains(@href,".mp4")]/@href'))

def randomsleep():
    'Sleep between zero and 100 seconds.'
    sleep(100 * betavariate(0.7, 8))

def main():
    s = Suhaila()
    for a in s.videoadmin():
        print(a)
        for b in s.category(a):
            print(b)
            s.get(b, parse_html = False)
            randomsleep()

def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()
    main()
