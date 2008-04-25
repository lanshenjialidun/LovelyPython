"""Fonctionnal testing for "Python In HTML" (PIH) and "HTML In Python" (HIP).
"""
__author__ = "Didier Wenzek (didier.wenzek@free.fr)"

# The code under test is in the .. directory.
import sys
sys.path.append('..')

# We use the Python unit testing framework
import unittest
import thread, time
from util import *

class TemplateTest(unittest.TestCase):
	"""Testing the Karrigell Scripting languages.
	
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

	def test_PIH_InsertPython(self):
		"""<% and %> tags are used to insert python code in HTML."""
		import time
		addScript("time.pih")
		page = getPage("/time.pih")
		today = time.strftime("%d:%m:%y",time.localtime(time.time()))
		expected = getGoldenFile("time.out", date=today)
		self.assertEqual(page.status, 200)
		self.assertEqual(page.content, expected)

	def test_PIH_PrintValue(self):
		"""<%= an %> tags are used to print python value."""
		addScript("value.pih")
		page = getPage("/value.pih")
		expected = getGoldenFile("value.out")
		self.assertEqual(page.status, 200)
		self.assertEqual(page.content + '\n', expected)

	def test_PIH_Indentation(self):
		"""Python indentation is managed using the <% end %> tag."""
		addScript("indent.pih")
		page = getPage("/indent.pih", 'POST', params={'hour':'22'})
		expected = getGoldenFile("indent.out")
		self.assertEqual(page.status, 200)
		self.assertEqual(page.content, expected)

	def test_PIH_IndentTag(self):
		"""Within <indent> tag HTML must follow Python indentation."""
		addScript("indent_tag.pih")
		page = getPage("/indent_tag.pih", 'POST', params={'hour':'22'})
		expected = getGoldenFile("indent_tag.out")
		self.assertEqual(page.status, 200)
		self.assertEqual(page.content, expected)

	def test_PIH_EmbeddedBlocks(self):
		"""Python blocks may be embedded."""
		addScript("embedded.pih")
		page = getPage("/embedded.pih")
		expected = getGoldenFile("embedded.out")
		self.assertEqual(page.status, 200)
		self.assertEqual(page.content, expected)

	def test_HIP_Principes(self):
		"""Literal text in python are printed to the response stream"""
		addScript("the_smiths.hip")
		page = getPage("/the_smiths.hip")
		expected = getGoldenFile("the_smiths.out")
		self.assertEqual(page.status, 200)
		self.assertEqual(page.content, expected)

if __name__ == "__main__":
	unittest.main()

