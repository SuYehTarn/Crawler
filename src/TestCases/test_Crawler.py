from collections import deque
from bs4 import BeautifulSoup
import unittest
import json
import sys
import io
import os
import re

from Crawler import Crawler
from Extractor import Extractor
from UrlMatcher import UrlMatcher
from Recorder import WorkingListManager

class TestCrawler(unittest.TestCase):
    """The test case of the module `Crawler`.

    Attributes:
    
    * testUrls (:obj:`list`): The list of urls for testing, containing three urls from ``http://www.pythonscraping.com``.
    * paths (:obj:`list`): The list of paths of files created during the test.
    """
    class Extractor_1(Extractor):
        """The testing extractor 1.
        """
        def get_title(self, url, bs):
            """The method of extracting the title from a web page.
            """
            data = bs.find('h1').get_text()
            msg  = ''
            return data, msg

    class Extractor_2(Extractor):
        """ The testing extractor 2.
        """
        def get_fakeLatin(self, url, bs):
            """The method of extracting the text of the tag having the id of `fakeLatin`.
            """
            data = bs.find(id='fakeLatin').get_text().replace('\n', '')
            msg  = ''
            return data, msg

        def get_classIsBody(self, url, bs):
            """The method of extracting the text of the tag having a class of `body`.
            """
            data = bs.find('', {'class': 'body'}).get_text().replace('\n', '')
            msg  = ''
            return data, msg

    class Extractor_3(Extractor):
        """ The testing extractor 3.
        """
        def get_gift1(self, url, bs):
            """The method of extracting the text of the tag having the id of `gift1`.
            """
            data = bs.find(id='gift1').get_text().strip('\n')
            data = data.replace('\n\n', '%*%').replace('\n', '').replace('%*%', '\n')
            msg  = ''
            return data, msg

    class Extractor_4(Extractor):
        """ The testing extractor 4.
        """
        def get_giftTitles(self, url, bs):
            """The method of extracting the text in each column of the tag having the id of `giftList`. It specifies the third testing url.
            """
            gifts = bs.find(id='giftList').findAll('tr', {'class': 'gift'})
            data = [g.td.get_text().strip('\n') for g in gifts]
            msg  = ''
            return data, msg

    testUrls = [
        'http://www.pythonscraping.com/pages/page1.html',
        'http://www.pythonscraping.com/pages/page2.html',
        'http://www.pythonscraping.com/pages/page3.html',
    ]

    paths = [
        'tmp/title.json',
        'tmp/para.json',
        'tmp/gift1.json',
        'tmp/giftTitles.json',
        'tmp/workingList.txt',
        'tmp/done.txt',
        'tmp/log.txt'
    ]

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it.

        * Directing the standard output to a :obj:`io.StringIO` object.
        * Checking the files assumed be created during test not exist before each test.
        """
        sys.stdout = self.strIO = io.StringIO()
        for path in self.paths:
            self.assertFalse(os.path.exists(path))

    def tearDown(self):
        """Hook method for deconstructing the test fixture after testing it.
        
        * Redirecting the standard output.
        * Removing the files created during esch test.
        """
        sys.stdout = sys.__stdout__
        for path in self.paths:
            if os.path.exists(path) and os.path.isfile(path):
                os.remove(path)

    def clean(self, string):
        return string.replace('\n',' ').replace('[', '\[').replace(']', '\]').replace('(', '\(').replace(')', '\)').replace('$', '\$')

    def test_attributes(self):
        """Test the setting of attributes.

        1. Test default attributes.
        2. Test user-defined attributes. All arguments are different from the default settings.
        """

        # Test default attributes
        patterns = {
            'scheme_pattern': r'http|https',
            'domain_pattern': r'.*',
            'path_pattern': r'.*',
        }
        c = Crawler()
        ## Test the WorkingListManager
        self.assertTrue(isinstance(c.WLM, WorkingListManager))
        self.assertFalse(c.WLM.workExists())

        ## Test the UrlMatcher
        self.assertTrue(isinstance(c.UM, UrlMatcher))
        for k, p in patterns.items():
            self.assertEqual(getattr(c.UM, k), p)

        ## Test other attributes
        self.assertFalse(c.curUrl)
        self.assertFalse(c.extractors)
        self.assertTrue(c.autoAddInternalLinks)

        #----------------------------#

        # Test user-defined attributes
        extractors = [self.Extractor_1('title'),
                    self.Extractor_2('para'),
                    self.Extractor_3('gift1'),
                    self.Extractor_4('giftTitles')]
        patterns = {
            'scheme_pattern': 'http',
            'domain_pattern': 'www.yahoo.com',
            'path_pattern': r'/path/page.*$',
        }
        c = Crawler(workingList=self.testUrls, **patterns, extractors=extractors, autoAddInternalLinks=False)

        ## Test the WorkingListManager
        self.assertTrue(c.WLM.workExists())
        self.assertEqual(c.WLM.records, deque(self.testUrls))

        ## Test the UrlMatcher
        self.assertTrue(isinstance(c.UM, UrlMatcher))
        for k, p in patterns.items():
            self.assertEqual(getattr(c.UM, k), p)

        ## Test other attributes
        self.assertFalse(c.curUrl)
        self.assertEqual(c.extractors, extractors)
        self.assertFalse(c.autoAddInternalLinks)

    def test_extendWorkingList(self):
        """Test the method of extending the working list.

        1. Test extending an empty working list.
        2. Test extending a none empty working list.
        """

        # Test extending an empty working list
        c = Crawler()
        self.assertFalse(c.WLM.records)
        c.extendWorkingList(self.testUrls[:2])
        self.assertTrue(c.WLM.records)
        self.assertEqual(c.WLM.records, deque(self.testUrls[:2]))

        # Test extending a none empty working list
        c = Crawler(workingList=self.testUrls[:1])
        self.assertTrue(c.WLM.records)
        c.extendWorkingList(self.testUrls[1:2])
        self.assertEqual(c.WLM.records, deque(self.testUrls[:2]))

    def test_addNewWorks(self):
        """Test the method of adding new works.

        1. Adding new works from a html document.
        2. Adding new work from a html document after getting a work for the working list.
        """
        c = Crawler()

        # Adding new works from a html document
        html1 = ('<!DOCTYPE html>'
                '<html>'
                '<head>'
                '    <title>aaa</title>'
                '</head>'
                '<body>'
                '    <div>'
                '        <a href="http://www.testurl.com/link1"></a>'
                '        <a href="/link2"></a>'
                '    </div>'
                '</body>'
                '</html>')
        expected = ['http://www.testurl.com/link1',
                    'http://www.testurl.com/link2']
        bs = BeautifulSoup(html1, 'html.parser')
        url = 'http://www.testurl.com'        
        c.addNewWorks(url, bs)
        self.assertTrue(c.WLM.workExists())
        self.assertEqual(c.WLM.records, deque(expected))

        # Adding new work from a html document after getting a work for the working list
        c.WLM.getWork()
        html2 = ('<!DOCTYPE html>'
                '<html>'
                '<head>'
                '    <title>aaa</title>'
                '</head>'
                '<body>'
                '    <div>'
                '        <a href="/link3"></a>'
                '    </div>'
                '</body>'
                '</html>')
        expected = ['http://www.testurl.com/link2',
                    'http://www.testurl.com/link3']
        bs = BeautifulSoup(html2, 'html.parser')
        url = 'http://www.testurl.com'
        c.addNewWorks(url, bs)
        self.assertTrue(c.WLM.workExists())
        self.assertEqual(c.WLM.records, deque(expected))

    def test_setUrlPattern(self):
        """Test setting url patterns for a crawler already be initialized
        """
        defaultPatterns = {
            'scheme_pattern': r'http|https',
            'domain_pattern': r'.*',
            'path_pattern': r'.*',
        }
        c = Crawler()
        for k, p in defaultPatterns.items():
            self.assertEqual(getattr(c.UM, k), p)

        patterns = {
            'scheme_pattern': 'http',
            'domain_pattern': 'www.yahoo.com',
            'path_pattern': r'/path/page.*$',
        }
        c.setUrlPattern(**patterns)
        for k, p in patterns.items():
            self.assertEqual(getattr(c.UM, k), p)

    def test_getPageBs(self):
        """Test the method of getting the :obj:`BeautifulSoup` object from a web page.
        
        1. Test getting page bs object from an available page
        2. Test getting page bs object from an unavailable page
        """
        c = Crawler()

        # Test getting page bs object from an available page
        bs = c.getPageBs(self.testUrls[0])
        self.assertTrue(isinstance(bs, BeautifulSoup))      # Returned data type correctness
        self.assertEqual(self.strIO.getvalue(), f'Getting: {self.testUrls[0]}\n')       # Standard output correctness
        self.assertTrue(c.curUrl)       # Current url existence
        self.assertEqual(c.curUrl, self.testUrls[0])        # Current url attribute correctness

        #----------------------------------------------------#

        # Test getting page bs object from an unavailable page
        sys.stdout = self.strIO = io.StringIO()
        bs = c.getPageBs('')
        self.assertFalse(c.curUrl)
        self.assertFalse(bs or isinstance(bs, BeautifulSoup))
        self.assertTrue(re.match(f'Getting: \nFailed to get : ', self.strIO.getvalue()))

    def test_extract1(self):
        """The testing method of extracting a string from a web page. In this case, all the targets of the extractors exist.
        """
        c = Crawler(extractors=[self.Extractor_1('title')])
        url  = self.testUrls[0]
        bs   = c.getPageBs(url)
        info = c.extract(url, bs)
        self.assertEqual(info, 'Get title: An Interesting Title')       # Returned information correctness
        
        expectDict = {'0': {'title': 'An Interesting Title'}}
        with open('tmp/title.json', 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expectDict)        # Record file correctness

    def test_extract2(self):
        """The testing method of extracting a string and a list of items from a web page. In this case, all the targets of the extractors exist.
        """

        # Expected results
        gift1 = 'Vegetable Basket\nThis vegetable basket is the perfect gift for your health conscious (or overweight) friends!Now with super-colorful bell peppers!\n$15.00'
        giftTitles = ['Vegetable Basket', 'Russian Nesting Dolls', 'Fish Painting', 'Dead Parrot', 'Mystery Box']

        c = Crawler(extractors=[self.Extractor_3('gift1'),self.Extractor_4('giftTitles')])
        url = self.testUrls[2]
        bs = c.getPageBs(url)
        info = c.extract(url, bs)
        
        self.assertEqual(info, f'Get gift1: {gift1}\nGet giftTitles: {giftTitles}')     # Correctness of returned message

        expectDict = {'0': {'gift1': gift1,}}
        with open('tmp/gift1.json', 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expectDict)        # Correctness of extracted data

        expectDict = {'0': {'giftTitles': giftTitles}}
        with open('tmp/giftTitles.json', 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expectDict)        # Correctness of extracted data

    def test_extract3(self):
        """The testing method of extracting with serveral extractors. In this case, some targets of the extractors do not extist.
        """
        self.assertEqual.__self__.maxDiff = None

        c = Crawler(extractors=[
                        self.Extractor_1('title'),
                        self.Extractor_2('para'),
                        self.Extractor_3('gift1'),
                        self.Extractor_4('giftTitles')
                        ])
        url = self.testUrls[1]
        bs = c.getPageBs(url)
        info = c.extract(url, bs)
        
        para = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

        pattern1 = self.clean(f'Get title: An Interesting Title\nGet fakeLatin: {para}\nGet classIsBody: {para}\nFailed to get gift1: .*\nFailed to get giftTitles: .*')
        pattern2 = self.clean(f'Get title: An Interesting Title\nGet classIsBody: {para}\nGet fakeLatin: {para}\nFailed to get gift1: .*\nFailed to get giftTitles: .*')
        self.assertTrue(re.match(f'({pattern1})|({pattern2})', info.replace('\n', ' ')))        # Returned information pattern correctness
        
        expectDict = {'0': {'title': 'An Interesting Title'}}
        with open('tmp/title.json', 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expectDict)        # Extracted record file correctness

        expectDict = {'0': {'fakeLatin': para, 'classIsBody': para}}
        with open('tmp/para.json', 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expectDict)        # Extracted record file correctness

        expectDict = {'0': {'gift1': ''}}
        with open('tmp/gift1.json', 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expectDict)        # Extracted record file correctness

        expectDict = {'0': {'giftTitles': ''}}
        with open('tmp/giftTitles.json', 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expectDict)        # Extracted record file correctness

    def test_saveLog(self):
        """Test the method of saving logs.
        """
        c = Crawler()
        c.log = ['first', 'second']
        c.saveLog()
        self.assertTrue(os.path.exists(c.logPath) and os.path.isfile(c.logPath))        # Log file existence
        with open(c.logPath, 'r') as fin:
            self.assertEqual(fin.read(), 'first\nsecond')       # Log file content correctness

    def test_printInfo(self):
        """Test the :obj:``printInfo`` method.
        """
        c = Crawler(workingList=self.testUrls)
        c.printInfo('this is a message')
        expectedStr = f'Result:\nthis is a message\nRemained Work Amount: 3\n{"-"*20}\n'
        self.assertEqual(self.strIO.getvalue(), expectedStr)        # Standard output string correctness

    def test_crawl(self):
        """Test the ``crawl`` method"""

        self.assertEqual.__self__.maxDiff = None

        para = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

        gift1 = 'Vegetable Basket\nThis vegetable basket is the perfect gift for your health conscious (or overweight) friends!Now with super-colorful bell peppers!\n$15.00'

        giftTitles = ['Vegetable Basket', 'Russian Nesting Dolls', 'Fish Painting', 'Dead Parrot', 'Mystery Box']

        # Defined the addNewWork method for testing through the testing urls
        l = self.testUrls[1:]
        class TestCrawler(Crawler):
            def addNewWorks(self, url, bs):
                if not l: return
                self.extendWorkingList([l.pop(0)])
        c = TestCrawler(
            workingList=self.testUrls[:1],
            extractors=[
                self.Extractor_1('title'),
                self.Extractor_2('para'),
                self.Extractor_3('gift1'),
                self.Extractor_4('giftTitles')
            ]
        )
        c.crawl()

        # Check records of wroking list
        self.assertFalse(c.WLM.workExists())
        self.assertTrue(os.path.exists(c.WLM.path) and os.path.isfile(c.WLM.path))
        with open(c.WLM.path, 'r') as fin:
            self.assertTrue(re.match(r'\s*', fin.read()))

        # Check records of extractor_1
        expected = {
            '0': {'title': 'An Interesting Title'},
            '1': {'title': 'An Interesting Title'},
            '2': {'title': 'Totally Normal Gifts'}
        }
        with open('tmp/title.json', 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expected)

        # Check records of extractor_2
        expected = {
            '0': {'fakeLatin': '', 'classIsBody': ''},
            '1': {'fakeLatin': para, 'classIsBody': para},
            '2': {'fakeLatin': '', 'classIsBody': ''}
        }
        with open('tmp/para.json', 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expected)

        # Check records of extractor_3
        expected = {
            '0': {'gift1': ''},
            '1': {'gift1': ''},
            '2': {'gift1': gift1}
        }
        with open('tmp/gift1.json', 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expected)

        # Check records of extractor_4
        expected = {
            '0': {'giftTitles': ''},
            '1': {'giftTitles': ''},
            '2': {'giftTitles': giftTitles}
        }
        with open('tmp/giftTitles.json', 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expected)

        returnedInfo = self.strIO.getvalue().split('\n' + '-'*20 + '\n')
        
        # Returned information pattern correctness of the extraction from page 1
        info = returnedInfo[0].strip('\n').replace('\n', ' ')
        pattern1 = self.clean(f'Getting: {self.testUrls[0]}\nResult:\nGet title: An Interesting Title\nFailed to get classIsBody: .*\nFailed to get fakeLatin: .*\nFailed to get gift1: .*\nFailed to get giftTitles: .*\nRemained Work Amount: 1')
        pattern2 = self.clean(f'Getting: {self.testUrls[0]}\nResult:\nGet title: An Interesting Title\nFailed to get fakeLatin: .*\nFailed to get gift1: .*\nFailed to get classIsBody: .*\nFailed to get giftTitles: .*\nRemained Work Amount: 1')        
        self.assertTrue(re.match(f'({pattern1})|({pattern2})', info))        # Returned information pattern correctness
        
        # Returned information pattern correctness of the extraction from page 2
        info = returnedInfo[1].strip('\n').replace('\n', ' ')
        pattern1 = self.clean(f'Getting: {self.testUrls[1]}\nResult:\nGet title: An Interesting Title\nGet fakeLatin: {para}\nGet classIsBody: {para}\nFailed to get gift1: .*\nFailed to get giftTitles: .*\nRemained Work Amount: 1')
        pattern2 = self.clean(f'Getting: {self.testUrls[1]}\nResult:\nGet title: An Interesting Title\nGet classIsBody: {para}\nGet fakeLatin: {para}\nFailed to get gift1: .*\nFailed to get giftTitles: .*\nRemained Work Amount: 1')        
        self.assertTrue(re.match(f'({pattern1})|({pattern2})', info))        # Returned information pattern correctness
        
        # Returned information pattern correctness of the extraction from page 3
        info = returnedInfo[2].strip('\n').replace('\n', ' ')
        pattern1 = self.clean(f'Getting: {self.testUrls[2]}\nResult:\nGet title: Totally Normal Gifts\nFailed to get classIsBody: .*\nFailed to get fakeLatin: .*\nGet gift1: {gift1}\nGet giftTitles: {giftTitles}\nRemained Work Amount: 0')
        pattern2 = self.clean(f'Getting: {self.testUrls[2]}\nResult:\nGet title: Totally Normal Gifts\nFailed to get fakeLatin: .*\nFailed to get classIsBody: .*\nGet gift1: {gift1}\nGet giftTitles: {giftTitles}\nRemained Work Amount: 0')        
        self.assertTrue(re.match(f'({pattern1})|({pattern2})', info))        # Returned information pattern correctness

        # Returned information pattern correctness of the finish of the crawler
        info = returnedInfo[3].strip('\n').replace('\n', ' ')
        pattern = self.clean('Working List is clear. Done.\n') + r'Time cost: (\d|\.)+$'
        self.assertTrue(re.match(pattern, info))        # Returned information pattern correctness


if __name__ == '__main__':
    unittest.main()