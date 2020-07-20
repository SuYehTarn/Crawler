import unittest

from UrlMatcher import UrlMatcher

class TestUrlMatcher(unittest.TestCase):
    """The test case of the module `UrlMatcher`.
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_attributes(self):
        """Testing the attributes setting after initialization.
        """
        # Test defualt settings
        UM = UrlMatcher()
        self.assertEqual(UM.scheme_pattern, r'http|https')
        self.assertEqual(UM.domain_pattern, r'.*')
        self.assertEqual(UM.path_pattern, r'.*')

        # Test user defined arguments
        UM = UrlMatcher(**{
            'scheme_pattern': 'http',
            'domain_pattern': 'www.yahoo.com',
            'path_pattern': r'/path/page.*$',
        })
        self.assertNotEqual(UM.scheme_pattern, r'http|https')
        self.assertNotEqual(UM.domain_pattern, r'.*')
        self.assertNotEqual(UM.path_pattern, r'.*')
        self.assertEqual(UM.scheme_pattern, 'http')
        self.assertEqual(UM.domain_pattern, 'www.yahoo.com')
        self.assertEqual(UM.path_pattern, r'/path/page.*$')

    def test_isIncluded(self):
        """Testing the ``isIncluded()`` method.
        """
        # Test defualt settings
        UM = UrlMatcher()
        url = 'http://www.google.com'
        self.assertTrue(UM.isIncluded(url))
        url = 'ftp://www.google.com'
        self.assertFalse(UM.isIncluded(url))

        # Test user defined arguments
        UM = UrlMatcher(**{
            'scheme_pattern': 'http',
            'domain_pattern': 'www.yahoo.com',
            'path_pattern': r'/path/page.*$',
        })
        url = 'http://www.google.com'
        self.assertFalse(UM.isIncluded(url))
        url = 'http://www.yahoo.com'
        self.assertFalse(UM.isIncluded(url))
        url = 'http://www.yahoo.com/path'
        self.assertFalse(UM.isIncluded(url))
        url = 'http://www.yahoo.com/path/page'
        self.assertTrue(UM.isIncluded(url))        
        url = 'http://www.yahoo.com/path/page/11233.html'
        self.assertTrue(UM.isIncluded(url))

if __name__ == "__main__":
    unittest.main()