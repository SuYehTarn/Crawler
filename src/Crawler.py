# -*- coding: utf-8 -*-
"""
.. module:: Crawler
   :synopsis: This module contains the Crawler servering the main function.

.. moduleauthor:: Su, Yeh-Tarn

"""

from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import time
import re
import os

from Recorder import WorkingListManager
from UrlMatcher import UrlMatcher
from Extractor import Extractor
from Headers import getHeaders

class Crawler:
    """The main class of the crawler.

    It combines a working list manager, a url matcher, and one or mutiple extractors.    

    Attributes:

    * WLM (:obj:`WorkingListManager`): The working list manager handling the working list during crawling.
    * UM (:obj:`UrlMatcher`): The url matcher to match links in each page with patterns specified by the initialization arguments.
    * extractors (:obj:`list`): The list of user defined extractors used to extract data from each web request.
    * autoAddInternalLinks (:obj:`bool`): Handle auto adding links matched the specified scheme, domain, path pattern.
    * curUrl (:obj:`str`): Record the current page url for each request of web page.
    * startTime (:obj:`float`): Record the start time of crawling.
    * log (:obj:`list`): The list of information returned during crawling.
    * logPath (:obj:`str`): The path of log file. Default is `./tmp/log.txt`.

    Args:

        * workingList (:obj:`list`): A list of url strings. Default is an empty list.
        * scheme_pattern (:obj:`str`): The regular expression string of url scheme. For example, http, https, etc. Default is ``r'http|https'``.
        * domain_pattern (:obj:`str`): The regular expression string of url domain. Default is ``r'.*'``.
        * path_pattern (:obj:`str`): The regular expression string of url path. Default is ``r'.*'``.
        * extractors (:obj:`list`): A list of user defined extractors used to extract data from each web request. Default is an empty list.
        * autoAddInternalLinks (:obj:`bool`): Whether auto adding links matched the specified scheme, domain, path pattern or not. Default is True.

    Raise:

    * TypeError
        * `workingList`: The `workingList` argument is defined and not a list, or some elements of the list are not strings.
        * `extractors`: The `extractors` argument is defined and not a list, or some elements of the list are not extractors.
        * `scheme_pattern`: The `scheme_pattern` argument is defined and not a string.
        * `domain_pattern`: The `domain_pattern` argument is defined and not a string.
        * `path_pattern`: The `path_pattern` argument is defined and not a string.
        * `autoAddInternalLinks`: The `autoAddInternalLinks` argument is defined and not a bool value.
    """
    def __init__(self, workingList=None, scheme_pattern=r'http|https', domain_pattern=r'.*', path_pattern=r'.*', extractors=None, autoAddInternalLinks=True):
        """The initial method of a crawler.
        """
        if workingList is None:
            workingList = []
        self.WLM = WorkingListManager(workingList)
        
        if extractors is None:
            extractors = []
        elif isinstance(extractors, list):
            for extractor in extractors:
                if not isinstance(extractor, Extractor):
                    raise TypeError('Some element in extractors are not instances of extractor')
        else:
            raise TypeError('Extractors must be a list of extractors')        
        self.extractors = extractors

        if not isinstance(scheme_pattern, str):
            raise TypeError('Scheme pattern must be a string of regular expression')
        if not isinstance(domain_pattern, str):
            raise TypeError('Domain pattern must be a string of regular expression')
        if not isinstance(path_pattern, str):
            raise TypeError('Url pattern must be a string of regular expression')
        self.UM = UrlMatcher(scheme_pattern=scheme_pattern, domain_pattern=domain_pattern, path_pattern=path_pattern)

        if not isinstance(autoAddInternalLinks, bool):
            raise TypeError('Argument "autoAddInternalLinks" must be a boolean value')        
        self.autoAddInternalLinks = autoAddInternalLinks
        
        self.curUrl = ''
        self.startTime = time.time()
        self.log = []
        self.logPath = 'tmp/log.txt'
        
        try:
            os.mkdir('tmp')
        except FileExistsError:
            pass
        except Exception as e:
            print(e)

    def extendWorkingList(self, workingList):
        """The method of extending working list.
        
        Args:

        * workingList (:obj:`list`): A list of url strings.
        """
        self.WLM.addWorks(workingList)

    def setUrlPattern(self, scheme_pattern=r'http|https', domain_pattern=r'.*', path_pattern=r'.*'):
        """The method of setting patterns for url matcher.

        Args:

        * scheme_pattern (:obj:`str`): The regular expression string of url scheme. For example, http, https, etc. Default is ``r'http|https'``.
        * domain_pattern (:obj:`str`): The regular expression string of url domain. Default is ``r'.*'``.
        * path_pattern (:obj:`str`): The regular expression string of url path. Default is ``r'.*'``.
        """

        if not isinstance(scheme_pattern, str):
            print('Scheme pattern must be a string of regular expression')
            return
        if not isinstance(domain_pattern, str):
            print('Domain pattern must be a string of regular expression')
            return
        if not isinstance(path_pattern, str):
            print('Url pattern must be a string of regular expression')
            return
        self.UM.scheme_pattern = scheme_pattern
        self.UM.domain_pattern = domain_pattern
        self.UM.path_pattern = path_pattern

    def addExtractors(self, extractors):
        """The method of adding extractors.

        Args:

        * extractors (:obj:`list`): A list of extractors.
        """
        if not isinstance(extractors, list):
            print('Failed to add extractors: argument must be a list of extractor')
            return

        for e in extractors:
            if not isinstance(e, Extractor):
                print('Failed to add extractors: some elements are not extractors')
                return

        self.extractors += extractors

    def getPageBs(self, url):
        """The method of getting a BeautifulSoup object of a web page.

        Args:

        * url (:obj:`str`): The url string of the attempted web page.
        """
        print(f'Getting: {url}')
        self.curUrl = url
        pr = urlparse(url)
        try:
            req = requests.get(url, headers=getHeaders(pr.netloc, url))

        except Exception as e:
            print(f'Failed to get {url}: {e}')
            return None

        return BeautifulSoup(req.text, 'html.parser')

    def extract(self, url, bs):
        """The method of extracting data from BeartifulSoup object and corresponding url.

        Args:

        * url (:obj:`str`): The url string of the corresponding web page.
        * bs (:obj:`BeautifulSoup`) The BeautifulSoup object of the corresponding web page.
        """
        extractInfo = []

        for extractor in self.extractors:
            msg = extractor.extract(url, bs)
            extractInfo.append(msg)

        return '\n'.join(extractInfo)

    def addNewWorks(self, url, bs=''):
        """The method of adding new works.

        It works when the class attribute `autoAddInternalLinks` is set True.

        User can overwrite this method to defined the added links.

        Args:

        * url (:obj:`str`): The url string of the corresponding web page.
        * bs (:obj:`BeautifulSoup`) The BeautifulSoup object of the corresponding web page.
        """
        if not self.autoAddInternalLinks:
            return

        try:        
            links = (elem['href'] for elem in bs.findAll('a', href=re.compile(r'.+')))      # Get all href of all links from BeautifulSoup object.
            pr = urlparse(url)
            links = (f'{pr.scheme}://{pr.netloc}{link}' if link.startswith('/') else link for link in links)        # Complete the relatively notated urls.
            internalLinks = [link for link in links if self.UM.isIncluded(link)]        # Filt out the internal links
            self.extendWorkingList(internalLinks)
        except Exception as e:
            print(f'Failed to add new works: {e}')

    def printInfo(self, extractInfo=''):
        """The method of printing and recording information during crawling.

        The information includes the extracting result return from the extractors and the remained work amount.

        The record path is ``./tmp/log.txt`` by default.

        Args:

        * extractInfo (:obj:`str`): The extracting information returned from the extractors.
        """        
        text = '\n'.join([
            f'Result:\n{extractInfo}',
            f'Remained Work Amount: {self.WLM.remainedAmount()}',
            '-'*20
        ])
        print(text) 
        
        self.log.append(text)
        self.saveLog()
    
    def saveLog(self):
        """The method of saving logs.
        """
        try:
            with open(self.logPath, 'wt') as fout:
                fout.write('\n'.join(self.log))

        except Exception as e:
            print(f'Failed to save log: {e}')
        

    def crawl(self):
        """The main method of crawling.
        """
        while self.WLM.workExists():
            url = self.WLM.getWork()
            pageBs = self.getPageBs(url)
            extractInfo = self.extract(url, pageBs)
            self.addNewWorks(**{'url': url, 'bs': pageBs})
            self.printInfo(extractInfo)

        print('Working List is clear. Done.')
        print(f'Time cost: {time.time() - self.startTime}')