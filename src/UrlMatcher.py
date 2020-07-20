# -*- coding: utf-8 -*-
"""
.. module:: UrlMatcher
   :synopsis: This module contains the url matcher.

.. moduleauthor:: Su, Yeh-Tarn

"""

from urllib.parse import urlparse
import re

class UrlMatcher:
    """The device to check if given url matched the specified patterns.

    Attributes:

    * scheme_pattern (:obj:`str`): The regular expression string for matching the scheme of a given url.
    * domain_pattern (:obj:`str`): The regular expression string for matching the domain of a given url.
    * path_pattern (:obj:`str`): The regular expression string for matching the path of a given url.

    Args:

    * scheme_pattern (:obj:`str`): The regular expression string of url scheme. For example, http, https, etc. Default is ``r'http|https'``.
    * domain_pattern (:obj:`str`): The regular expression string of url domain. Default is ``r'.*'``.
    * path_pattern (:obj:`str`): The regular expression string of url path. Default is ``r'.*'``.
    """
    def __init__(self, scheme_pattern=r'http|https', domain_pattern=r'.*', path_pattern=r'.*'):
        """The initial method of a url matcher.
        """
        self.scheme_pattern = scheme_pattern
        self.domain_pattern = domain_pattern
        self.path_pattern = path_pattern

    def isIncluded(self, url):
        """The method of checking if a given url matched the specified patterns.

        Args:

        * url (:obj:`str`): The url attempted to check.

        Returns:

        :obj:`bool`: True if the url is matched the patterns, False otherwise.
        """
        parseResult = urlparse(url)

        if not re.match(self.scheme_pattern, parseResult.scheme):
            return False

        if not re.match(self.domain_pattern, parseResult.netloc):
            return False

        if not re.match(self.path_pattern, parseResult.path):
            return False

        return True