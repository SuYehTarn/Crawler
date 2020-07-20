from bs4 import BeautifulSoup
import unittest
import json
import sys
import re
import os
import io

from Recorder import JsonRecorder
from Extractor import Extractor

class TestExtractor(unittest.TestCase):
    """The test case of the module `Extractor`.

    Attributes:
    
    * html (:obj:`str`): The html string for testing.
    * bs (:obj:`BeautifulSoup`): The :obj:`BeautifulSoup` object retained from parsing the testing html string.
    * url (:obj:`str`): The url string for testing.
    """
    
    html = ('<!DOCTYPE html>'
            '<html>'
            '<head>'
            '    <title>aaa</title>'
            '</head>'
            '<body>'
            '    <div><a href="this.is.a.href"></a></div>'
            '</body>'
            '</html>')
    bs = BeautifulSoup(html, 'html.parser')
    url = 'http://www.test.com/path/page.html'            

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it.

        * Directing the standard output to a :obj:`io.StringIO` object.
        * Checking the file assumed be created during test not exist before each test.
        """
        sys.stdout = self.strIO = io.StringIO
        self.assertFalse(os.path.exists('tmp/testing.json'))

    def tearDown(self):
        """Hook method for deconstructing the test fixture after testing it.
        
        * Redirecting the standard output.
        * Removing the file created during esch test.
        """
        sys.stdout = sys.__stdout__
        if os.path.exists('tmp/testing.json'):
            os.remove('tmp/testing.json')

    def test_attributes2(self):
        """Test the setting of attributes.
        """
        e = Extractor('testing')
        self.assertEqual(e.name, 'testing')
        self.assertTrue(e.JsonRecorder and isinstance(e.JsonRecorder, JsonRecorder)) # The existence and type correctness of the json recorder.
        self.assertEqual(e.JsonRecorder.name, 'testing') # extractor.JsonRecorder has the same name as the extractor.

    def test_get(self):
        """Test the decorated method ``get``.
        """
        class myExtractor(Extractor):
            
            def get_url(self, url, bs):
                data = url
                msg  = ''
                return data, msg
            
            def get_title(self, url, bs):
                data = bs.head.title.get_text()
                msg  = 'titleMessage'
                return data, msg

        e = myExtractor('testing')

        # Case of successful extracting
        data1, msg1 = e.get_title(self.url, self.bs)
        data2, msg2 = e.get(e.get_title)(self.url, self.bs)
        self.assertEqual(data2, 'aaa')      # Correctness of extracted data
        self.assertEqual(data2, data1)      # Equality of returned data between original extracting method and decorated method.
        self.assertEqual(msg2, msg1 + '\nGet title: aaa')       # Correctness of returned message if set not empty returning message for the original method

        data1, msg1 = e.get_url(self.url, self.bs)
        data2, msg2 = e.get(e.get_url)(self.url, self.bs)
        self.assertEqual(msg2, msg1 + 'Get url: http://www.test.com/path/page.html')        # Correctness of returned message if remained empty returning message for the original method
        

        # Case of failing to extract
        with self.assertRaises(AttributeError):
            e.get_title('', '')

        data, msg = e.get(e.get_title)('', '')
        self.assertFalse(data)      # Empty string is returned due to an unsuccessful extraction.
        self.assertTrue(re.match(r'Failed to get .*: ', msg))       # Correctness of returned message of an unsuccessful extraction.

    def test_extract2(self):

        class myExtractor(Extractor):
            
            def get_url(self, url, bs):
                data = url
                msg  = ''
                return data, msg
            
            def get_title(self, url, bs):
                data = bs.head.title.get_text()
                msg  = ''
                return data, msg

        expectedDict = {'0': {'title': 'aaa', 'url': 'http://www.test.com/path/page.html'}}
        e = myExtractor('testing')
        msg = e.extract(self.url, self.bs)
        self.assertEqual(msg, 'Get title: aaa\nGet url: http://www.test.com/path/page.html') # Return correct message

        path = e.JsonRecorder.path
        self.assertTrue(os.path.exists(path) and os.path.isfile(path)) # JsonRecorder create a record file
        with open(path, 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expectedDict) # Correct file content

    



if __name__ == "__main__":
    unittest.main()