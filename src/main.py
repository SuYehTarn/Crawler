# -*- coding: utf-8 -*-
"""
.. module:: main
   :synopsis: This module is for user defining the custom script for running a :mod:`Crawler`.

.. moduleauthor:: Su, Yeh-Tarn

"""

from Extractor import Extractor
from UrlMatcher import UrlMatcher
from Crawler import Crawler
from urllib.parse import urlparse
import re

class Title(Extractor):

    def get_url(self, url, bs):
        data = url
        msg  = ''
        return data, msg

    def get_title(self, url, bs):
        data = bs.head.title.get_text()
        msg = ''
        return data, msg

args = {
    'scheme_pattern': r'http|https',
    'domain_pattern': r'.*',
    'path_pattern': r'.*',
    'extractors': [Title('title')],
    'workingList': [],
    'autoAddInternalLinks': True
}
c = Crawler(**args)
c.crawl()