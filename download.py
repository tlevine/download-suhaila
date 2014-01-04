#!/usr/bin/env python3
from requests import session
from lxml.html import fromstring

# Typing
from requests.sessions import Session
from requests.models import Response
from typing import Tuple
from lxml.html import HtmlElement

s = session()

USERNAME = 'tlevine'
PASSWORD = 'Onf5nVPgjyn3'

def url(absolute_href:str) -> str:
    return 'http://www.suhailaonlineclasses.com' + absolute_href

def login(username, password) -> Tuple[Session,Response]:
    action = '/amember/member.php'

    r = s.get(url(action))
    html = fromstring(r.text)

    names = map(str, html.xpath('//form[@action="/amember/login"]/descendant::input/@name'))
    values = map(str, html.xpath('//form[@action="/amember/login"]/descendant::input/@value'))
    data = dict(zip(names, values))
    data['amember_login'] = username
    data['amember_pass']  = password

    r = s.post(url(action), data = data)
    return s,r
