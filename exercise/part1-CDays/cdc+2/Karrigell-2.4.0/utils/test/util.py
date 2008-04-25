"""Functions used to setup a test suite for the Karrigell server
"""

__author__ = "Didier Wenzek (didier.wenzek@free.fr)"

import thread, httplib, urllib, os, shutil, time, Tkinter

data_src = "data"
root_dir = "root"

def launchKarrigell():
	"""Launch Karrigell in the test environnement"""
	addScript("hello.py", "index.py")
	# when launching Karrigell, current directory must be that of
	# Karrigell.py for good resolution of (root) in the .ini file
	saveDir=os.getcwd()
	os.chdir('..')
	try:
		getPage("/")
	except:
		thread.start_new_thread(os.system,
			(r"python Karrigell.py test/KarrigellTest.ini",))
		time.sleep(3)
	os.chdir(saveDir)

def addScript(src, dest=None):
	"""Add a new script (piked from the data directory)
	in the root directory served by the test server.
	
	If no dest is given, the src path is taken for dest"""
	if dest == None:
		dest = src
	src = os.path.join(data_src, src)
	dest = os.path.join(root_dir, dest)
	dir, _ = os.path.split(dest)
	if not os.path.isdir(dir):
		os.makedirs(dir)
	shutil.copyfile(src, dest)

def removeScript(path):
	"""Removes the named script
	from the root directory served by the test server."""
	path = os.path.join(root_dir, path)
	if os.path.isdir(path):
		os.rmdir(path)
	else:
		try:
			os.remove(path)
		except OSError:
			pass

def getGoldenFile(src, mode="r", **args):
	"""Get the expected output from a golden file
	(piked from the data directory)."""
	src = os.path.join(data_src, src)
	if args:
		return file(src,mode).read() % args
	else:
		return file(src,mode).read()

class Page:
	"""A page returned by the test server."""
	def __init__(self):
		self.status = 404
		self.headers = {}
		self.content = ""
	
def getPage(url, method="GET", params={}, sent_headers={}, expected_headers=()):
	"""Get the requested page from the test server."""
	conn = httplib.HTTPConnection("localhost:8888")
	if method == "GET":
		conn.request(method, url, params, sent_headers)
	elif method == "POST":
		params = urllib.urlencode(params)
		headers = {"Content-type": "application/x-www-form-urlencoded",
				   "Content-length": str(len(params))}
		headers.update(sent_headers)
		conn.request(method, url, params, headers)
	else:
		return None
	response = conn.getresponse()
	page = Page()
	page.status = response.status
	page.headers = {}
	for h in expected_headers:
		v = response.getheader(h)
		v = response.getheader(h)
		page.headers[h] = v
	page.content = response.read()
	conn.close()
	return page

