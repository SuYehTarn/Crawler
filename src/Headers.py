# -*- coding: utf-8 -*-
"""
.. module:: headers
   :synopsis: This module contains a method of creating headers for web request.

.. moduleauthor:: Su, Yeh-Tarn

"""

from itertools import chain
import random

def getHeaders(domain='', referer=''):
    """The method of creating headers for web request. The user agents data are collected on 2020/07/04, from: ``https://www.whatismybrowser.com/guides/the-latest-user-agent/?utm_source=whatismybrowsercom&utm_medium=internal&utm_campaign=breadcrumbs``

    Args:

    * domain (:obj:`str`): A specific url domain string.
    * referer (:obj:`str`): A specific referer url string.

    Return:
    
    * :obj:`dict`: The header dict.

    """

    firefox_user_agents_desktop = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0", # Windows desktop
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0", # Macos desktop
        "Mozilla/5.0 (X11; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0", #Linux desktop
        "Mozilla/5.0 (Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", #Linux desktop
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0", #Linux desktop
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", #Linux desktop
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", #Linux desktop
    ]

    firefox_user_agents_mobile = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/27.0 Mobile/15E148 Safari/605.1.15", # Iphone
        "Mozilla/5.0 (iPad; CPU OS 10_15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/27.0 Mobile/15E148 Safari/605.1.15", # Ipad
        "Mozilla/5.0 (iPod touch; CPU iPhone OS 10_15_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) FxiOS/27.0 Mobile/15E148 Safari/605.1.15", # Ipod
        "Mozilla/5.0 (Android 10; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0", # Android (standard)
        "Mozilla/5.0 (Android 10; Mobile; LG-M255; rv:68.0) Gecko/68.0 Firefox/68.0", # Android (Lg)
    ]

    chrome_user_agents_desktop = [    
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36", # Windows desktop
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36", # Windows desktop
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36", # Windows desktop
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36", # Macos desktop
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36", #Linux desktop
    ]

    chrome_user_agents_mobile = [    
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4103.88 Mobile/15E148 Safari/604.1", # Iphone
        "Mozilla/5.0 (iPad; CPU OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4103.88 Mobile/15E148 Safari/604.1", # Ipad
        "Mozilla/5.0 (iPod; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4103.88 Mobile/15E148 Safari/604.1", # Ipod
        "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36", # Android (standard)
        "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36", # Android (Samsung)
        "Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36", # Android (Samsung)
        "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36", # Android (Samsung)
        "Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36", # Android (Samsung)    
        "Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36", # Android (Lg)
        "Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36", # Android (Lg)
        "Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36", # Android (Lg)
    ]

    user_agents_desktop = list(chain(firefox_user_agents_desktop, chrome_user_agents_desktop))
    user_agents_mobile = list(chain(firefox_user_agents_mobile, chrome_user_agents_mobile))
    headers = {
        'Host': domain,
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-agent': random.choice(user_agents_desktop),
        'Referer': referer if referer else domain,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    }
    return headers