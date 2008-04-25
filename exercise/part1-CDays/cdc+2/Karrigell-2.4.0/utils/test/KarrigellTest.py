"""Fonctionnal testing for the Karrigell server
"""

__author__ = "Didier Wenzek (didier.wenzek@free.fr)"

# The code under test is in the .. directory.
import sys, os
sys.path.append('..')

# We use the Python unit testing framework
import unittest
import thread, time
from util import *

class KarrigellTest(unittest.TestCase):
    """Testing the Karrigell server.
    
    A test is prepared with the addScript() and removeScript() methods.
    which are used to set up the root directory with scripts picked from
    the data directory.
    
    The Karrigell response is returned by the getPage() method
    as a Page object with a status and a content attribute.
    
    The expected response can be retrieved from the data repository with the
    getGoldenFile() method.
    
    The Karrigell response can then be tested against the expected response,
    using any of the unittest methods like assertEqual().
    
    """

    def setUp(self):
        launchKarrigell()

    def test_IsRunning(self):
        """Karrigell is an http server."""
        addScript("hello.py", "index.py")
        addScript("hello.py", "hello.py")
        addScript("hello.py", "subdir/hello.py")
        expected = getGoldenFile("hello.out")
        page = getPage("/")
        self.assertEqual(page.status, 302)
        self.assertEqual(page.content, '')
        page = getPage("/hello.py")
        self.assertEqual(page.status, 200)
        self.assertEqual(page.content, expected)
        page = getPage("/subdir/hello.py")
        self.assertEqual(page.status, 200)
        self.assertEqual(page.content, expected)
        removeScript("xoxox.html")
        page = getPage("/xoxox.html")
        self.assertEqual(page.status, 404)  # file not found gives an error page

    def test_Static(self):
        """Karrigell serve any static file from the root directory."""
        addScript("karrigell.html")
        expected = getGoldenFile("karrigell.html",mode='rb')
        page = getPage("/karrigell.html")
        self.assertEqual(page.status, 200)
        self.assertEqual(page.content, expected)
        addScript("karrigell.gif")
        expected = getGoldenFile("karrigell.gif",mode="rb")
        page = getPage("/karrigell.gif")
        self.assertEqual(page.status, 200)
        self.assertEqual(page.content, expected)

    def test_Alias(self):
        """An alias url can be given to a directory."""
        addScript("hello.py", "doc_directory/index.py")
        expected = getGoldenFile("hello.out")
        page = getPage("doc/index.py")
        self.assertEqual(page.status, 200)
        self.assertEqual(page.content, expected)

    def test_PythonScripting(self):
        """Karrigell display the output of python scripts"""
        addScript("using_query.py")
        addScript("using_query_shortcut.py")
        parameters = { 'spam':'foo', 'animal': ('dog') }
        expected = getGoldenFile("using_query.out", spam='foo',animal='dog')
        page = getPage("/using_query.py", "POST", parameters)
        self.assertEqual(page.status, 200)
        self.assertEqual(page.content, expected)
        page = getPage("/using_query_shortcut.py", "POST", parameters)
        self.assertEqual(page.status, 200)
        self.assertEqual(page.content, expected)

    def test_Exception(self):
        """Karrigell handles exceptions to stop or redirect the output""" 
        addScript("script_end.py")
        expected = getGoldenFile("script_end.out")
        page = getPage("/script_end.py")
        self.assertEqual(page.status, 200)
        self.assertEqual(page.content, expected)

        addScript("http_error.py")
        page = getPage("/http_error.py")
        self.assertEqual(page.status, 501)

        addScript("http_redirect.py")
        page = getPage("/http_redirect.py")
        self.assertEqual(page.status, 302)

    def test_Error(self):
        """Karrigell catches errors and builds an error page.""" 
        addScript("script_error.py")
        expected = getGoldenFile("script_error.out")
        page = getPage("/script_error.py")
        self.assertEqual(page.status, 200)
        # can't compare last lines because of random parameter "key"
        self.assertEqual(page.content[:-150], expected[:-150])

    def test_PIH(self):
        """Karrigell script can mix python and html with PIH.""" 
        import time
        addScript("time.pih")
        page = getPage("/time.pih")
        today = time.strftime("%d:%m:%y",time.localtime(time.time()))
        expected = getGoldenFile("time.out", date=today)
        self.assertEqual(page.status, 200)
        self.assertEqual(page.content, expected)

    def test_HIP(self):
        """Karrigell script can mix python and html with HIP.""" 
        import time
        addScript("time.hip")
        page = getPage("/time.hip")
        today = time.strftime("%d:%m:%y",time.localtime(time.time()))
        expected = getGoldenFile("time.out", date=today)
        self.assertEqual(page.status, 200)
        self.assertEqual(page.content, expected)

    def test_Include(self):
        """Scripts can include other scripts""" 
        addScript("include.py")
        addScript("header.htm")
        addScript("footer.py")
        page = getPage("/include.py")
        expected = getGoldenFile("include.out")
        self.assertEqual(page.status, 200)
        self.assertEqual(page.content, expected)

        addScript("include_parameters.py")
        addScript("menu.py")
        page = getPage("/include_parameters.py")
        expected = getGoldenFile("include_parameters.out")
        self.assertEqual(page.status, 200)
        self.assertEqual(page.content, expected)

    def test_Session(self):
        """Karrigell handles a session object using a cookie.""" 
        addScript("session_set.pih")
        addScript("session_use.pih")
        page_1 = getPage("/session_set.pih", "POST",
                         {'name': 'Karrigell', 'firstname': 'Python'},
                         expected_headers = ('Set-Cookie',))
        page_2 = getPage("/session_use.pih",
                         sent_headers = {'Cookie':page_1.headers['Set-Cookie']})
        expected = getGoldenFile("session_use.out",
                                 name='Karrigell', firstname='Python')
        self.assertEqual(page_2.status, 200)
        self.assertEqual(page_2.content , expected)        

    def test_SetResponse(self):
        """RESPONSE changes the HTTP response headers"""
        addScript("set_response.py")
        page = getPage("/set_response.py",expected_headers=('Content-Type',))
        self.assertEqual(page.headers['Content-Type'],'text/plain')

    def test_Protected(self):
        """For protected directories, ask HTTP authentication"""
        page = getPage("protected/hello.htm")
        #self.assertEqual(page.status,401)
        sys.stderr.write(page.content)

if __name__ == "__main__":
    saveSdtout=sys.stdout
    sys.stdout=open("testResult.txt","w")
    unittest.main()
    sys.stdout.close()
