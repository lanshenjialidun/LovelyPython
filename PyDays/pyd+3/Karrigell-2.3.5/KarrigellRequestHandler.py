"""Karrigell, a web programming framework in Python

Written by Pierre Quentel quentel.pierre@wanadoo.fr

Published under the BSD licence. See the file LICENCE.txt
"""

import sys, os, string, cStringIO, traceback, base64, time, copy
import Cookie, urlparse, mimetypes, BaseHTTPServer, cgi, urllib
import logging.handlers
# Karrigell-specific modules
from core import k_config
import Template, URLResolution, k_utils, k_script, modify_request
import debugger.k_debugger
from k_encodings import k_encoding_charsets, k_encoding
from k_stringio import KStringIO as StringIO
from LocalizedRequestHandler import LocalizedRequestHandler

# for imports
dirs = [ os.getcwd(),os.path.join(os.getcwd(),'databases') ]
for dir_ in dirs:
    if not dir_ in sys.path:
        sys.path.append(dir_)

import k_session

# compatibility with Python 2.3
try:
    set([])
except NameError:
    from sets import Set as set
    
__version__ = "2.3.5"

os.chdir(k_config.serverDir)

class ReloadError(Exception):
    pass

# update mime types
mimetypes.init()
mimetypes.types_map.update({
    '': 'application/octet-stream', # Default
    '.py' : 'text/html',
    '.pih': 'text/html',
    '.hip': 'text/html',
    '.pyk': 'text/html',
    '.ks' : 'text/html'
    })
mimetypes.types_map.update(k_config.extensions_map)


# set up logging
if k_config.loggingFile:
    _logdir = os.path.dirname(k_config.loggingFile)
    if not os.path.exists(_logdir):
        os.makedirs(_logdir)
    pars = eval(k_config.loggingParameters) # ugly way
    loghandler = logging.handlers.RotatingFileHandler(k_config.loggingFile, *pars)
    loghandler.setLevel(logging.INFO)
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger().addHandler(loghandler)

def content_type():
    "return content type for html texts"
    if not k_config.outputEncoding:
        ct="text/html"
    else:
        ct="text/html; charset="+k_encoding_charsets.encoding2mime_map.get(
            k_config.outputEncoding, k_config.outputEncoding)
    return ct

class KarrigellRequestHandler(LocalizedRequestHandler):

    server_version = "Karrigell/" + __version__
    cachemanaged   = 1     # httpd optimization
    imported = {}
    accepted_languages = []

    if k_config.language:
        accepted_languages.append(k_config.language)

    # dictionnary holding already loaded code
    # key=name of the file's full path
    # value=[time of last modification when loaded, Script object]
    # when a Python, pih, hip or ks file is required, if the file exists in
    # loadedScripts and has not been modified since it was loaded,
    # use the content in loadedScripts instead of loading from the file
    # system and parse the code
    loadedScripts={}

    def prepare_env(self):
        """Prepare environment for dynamic scripts"""

        # cgi scripts
        d,depth = k_utils.urlInPaths(self.fileName,
            k_config.cgi_directories)
        self.cgi_info = None
        if d:
            self.cgi_info = d,self.fileName[len(d)+1:]
            self.make_cgi_env()
            return    

        # initialize the cookie objects
        # COOKIE = cookies received from the browser
        if self.HEADERS.has_key("cookie"):
            self.COOKIE=Cookie.SimpleCookie(self.HEADERS["cookie"])
        else:
            self.COOKIE=Cookie.SimpleCookie()
        # check if cookie logged_user is set
        self.LOGGED_USER = None
        if self.COOKIE.has_key('logged_user'):
            self.LOGGED_USER = self.COOKIE['logged_user'].value
        # SET_COOKIE = cookies sent back to the browser            
        self.SET_COOKIE=Cookie.SimpleCookie()

        # if there is a Query String, decode it in a QUERY dictionary
        # handle the query string, if any
        self.QUERY = cgi.parse_qs(self.qs,1)

        # all unicode management written by Radovan Garabik 
        # and Laurent Pointal
        if k_config.encodeFormData:
            # try encoding the query string
            qs_encoding = k_encoding.try_encoding(urllib.unquote(self.qs), 
               ['ascii', k_config.outputEncoding, 'utf-8', 'iso8859_1_ncc', 
               'cp1252', 'macroman'])

            # if qs_encoding is None, encoding could not have been determined
            # most likely it is gibberish, or a malicious user entered invalid 
            # sequence intentionally
            # in any case, we just have no idea what to do with the QUERY, so 
            # we might as well discard it....
            if qs_encoding is None:
                self.QUERY = {}
        
            # now fix the query, convert it to unicode using our guessed 
            # encoding
            for key, val in self.QUERY.items():
                for i, v in enumerate(val): 
                    try:
                        # if it is just an ascii string, leave it in peace
                        unicode(v, 'ascii')
                        continue
                    except UnicodeDecodeError:
                        # modify val list in-place
                        val[i] = unicode(v, qs_encoding)

        if self.command == 'POST' and not isinstance(self.body.value,str):
            # test if self.body.value is a string, which is the case when
            # enctype is text/plain
            for key in self.body.keys():
                self.QUERY[key] = self.body[key]
                if not isinstance(self.body[key],list):
                    self.QUERY[key] = [self.body[key]]
                for i,elt in enumerate(self.QUERY[key]):
                    if not elt.filename:
                        # convert FieldStorage to string if not file upload
                        s = elt.value
                        # elt.value SHOULD be in the same encoding as 
                        # outputEncoding, but unfortunately there are some 
                        # broken browsers so we have to do the test...
                        # for backward compatibility, if outputEncoding=='',
                        # don't use unicode at all
                        if k_config.encodeFormData:
                            s_encoding = k_encoding.try_encoding(s, 
                                ['ascii', k_config.outputEncoding, 'utf-8', 
                                'iso8859_1_ncc', 'cp1252', 'macroman'])
                        else:
                            s_encoding = 'ascii'
                        if s_encoding == 'ascii':
                            self.QUERY[key][i] = s
                        elif s_encoding:
                            self.QUERY[key][i] = unicode(s, s_encoding)
                        else: # gibberish
                            self.QUERY[key][i] = '' # or would it be better 
                                                    # to delete it?

        self.QUERY = modify_request.modify_query(self.QUERY)
        self.QUERY=k_utils.applyQueryConvention(self.QUERY)
        
        self.ctype=content_type()  # default content-type

        # replace standard output by a StringIO
        # the "print" statements in scripts will write to this StringIO
        self.outputStream=StringIO()

        # select language
        self.get_language()

        # read an Authorization header if any
        # and decode it in AUTH_USER and AUTH_PASSWORD
        self.AUTH_USER,self.AUTH_PASSWORD=None,None
        if self.HEADERS.has_key('authorization'):
            basic_credentials=self.HEADERS["authorization"]
            basic_cookie=basic_credentials.split()[1]
            self.AUTH_USER,self.AUTH_PASSWORD=\
                base64.decodestring(basic_cookie).split(":")

        # create the namespace in which the script is going to run
        self.nameSpace.update({
            "RESPONSE":self.RESPONSE,"HEADERS":self.HEADERS,
            "AUTH_USER":self.AUTH_USER,"AUTH_PASSWORD":self.AUTH_PASSWORD,
            "QUERY":self.QUERY,"REQUEST":self.QUERY, 
            "COOKIE":self.COOKIE, "SET_COOKIE":self.SET_COOKIE,
            "PATH":self.path,
            "ACCEPTED_LANGUAGES":self.accepted_languages,
            "SERVER_DIR":k_config.serverDir,
            "CONFIG":k_config,
            "Session":self.Session,"Authentication":self.Authentication,
            "RestrictToAdmin":self.RestrictToAdmin,
            "Login":self.Login,"LOGGED_USER":self.LOGGED_USER,
            "os":os,"Cookie":Cookie,"string":string})
            # frequently used modules needn't be imported in scripts

    def make_cgi_env(self):
        # set environment for cgi scripts
        # copied from CGIHTTPServer
        dir_, rest = self.cgi_info
        query = self.qs
        i = rest.find('/')
        if i >= 0:
            script, rest = rest[:i], rest[i:]
        else:
            script, rest = rest, ''
        scriptname = dir_ + '/' + script
        env = {}
        env['SERVER_SOFTWARE'] = self.version_string()
        env['SERVER_NAME'] = self.server.server_name
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['SERVER_PROTOCOL'] = self.protocol_version
        env['SERVER_PORT'] = str(self.server.server_port)
        env['REQUEST_METHOD'] = self.command
        uqrest = urllib.unquote(rest)
        env['PATH_INFO'] = uqrest
        env['PATH_TRANSLATED'] = self.translate_path(uqrest)
        env['SCRIPT_NAME'] = scriptname
        if query:
            env['QUERY_STRING'] = query
        host = self.address_string()
        if host != self.client_address[0]:
            env['REMOTE_HOST'] = host
        env['REMOTE_ADDR'] = self.client_address[0]
        authorization = self.headers.getheader("authorization")
        if authorization:
            authorization = authorization.split()
            if len(authorization) == 2:
                import base64, binascii
                env['AUTH_TYPE'] = authorization[0]
                if authorization[0].lower() == "basic":
                    try:
                        authorization = base64.decodestring(authorization[1])
                    except binascii.Error:
                        pass
                    else:
                        authorization = authorization.split(':')
                        if len(authorization) == 2:
                            env['REMOTE_USER'] = authorization[0]
        # XXX REMOTE_IDENT
        if self.headers.typeheader is None:
            env['CONTENT_TYPE'] = self.headers.type
        else:
            env['CONTENT_TYPE'] = self.headers.typeheader
        length = self.headers.getheader('content-length')
        if length:
            env['CONTENT_LENGTH'] = length
        accept = []
        for line in self.headers.getallmatchingheaders('accept'):
            if line[:1] in "\t\n\r ":
                accept.append(line.strip())
            else:
                accept = accept + line[7:].split(',')
        env['HTTP_ACCEPT'] = ','.join(accept)
        ua = self.headers.getheader('user-agent')
        if ua:
            env['HTTP_USER_AGENT'] = ua
        co = filter(None, self.headers.getheaders('cookie'))
        if co:
            env['HTTP_COOKIE'] = ', '.join(co)
        # XXX Other HTTP_* headers
        # Since we're setting the env in the parent, provide empty
        # values to override previously set values
        for k in ('QUERY_STRING', 'REMOTE_HOST', 'CONTENT_LENGTH',
                  'HTTP_USER_AGENT', 'HTTP_COOKIE'):
            env.setdefault(k, "")
        os.environ.update(env)

    def handle_data(self):
        """Wrap in a try/except clause for uncaught exceptions 
        to prevent crashing the server"""
        try:
            self.try_handle_data()
        except k_script.AUTH_ABORT:
            pass
        except:
            traceback.print_exc(file=sys.stderr)

    def log_date_time_string(self):
        """Return the current time formatted for logging."""
        now = time.time()
        year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
        tzh = -(time.timezone/3600)
        tzm = (time.timezone%3600)/60
        s = "%02d/%3s/%04d:%02d:%02d:%02d %+03d%02d" % (
                day, self.monthname[month], year, hh, mm, ss, tzh, tzm)
        return s

    def log_error(self, format, *args):
        """Log an error.

        This is called when a request cannot be fulfilled.  By
        default it passes the message on to log_message().

        Arguments are the same as for log_message().
        
        Put the error message only to stderr.

        """
        if not k_config.silent:
            msg = ("%s - - [%s] %s" %
                             (self.address_string(),
                              self.log_date_time_string(),
                              format%args))

            sys.stderr.write(msg)
            sys.stderr.write('\n')

    def log_message(self, format, *args):
        """Log an arbitrary message.

        This is used by all other logging functions.  Override
        it if you have specific logging wishes.

        The first argument, FORMAT, is a format string for the
        message to be logged.  If the format string contains
        any % escapes requiring parameters, they should be
        specified as subsequent arguments (it's just like
        printf!).

        The client host and current date/time are prefixed to
        every message.

        """

        msg = ("%s - - [%s] %s" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))
        if not k_config.silent:
            BaseHTTPServer.BaseHTTPRequestHandler.log_message(self, format, *args)

        if k_config.loggingFile:
            logging.info(msg)
        
    def translate_path(self,path):
        return URLResolution.translate_path(path)

    def try_handle_data(self):
        """Handle a GET or POST request"""
        sys.stdout = k_utils.Stdout(self.client_address)
        self.HEADERS = k_utils.CI_dict(self.headers)
            
        # a hook to modify the path and request headers
        self.path = modify_request.modify_path(self.path)
        self.HEADERS = modify_request.modify_headers(self.HEADERS)

        self.RESPONSE=k_utils.CI_dict({'Content-Type':content_type()})  # default value
        parsed_path = urlparse.urlparse(self.path)
        self.qs = parsed_path[4]
        
        path_without_qs = parsed_path[2]

        self.path_without_qs = path_without_qs

        # virtual hosts
        self.host = self.HEADERS.get('host',0)
        if self.host !=0 and ':' in self.host:
            self.host = self.host.split(':')[0]
        if not k_config.virtual_hosts.has_key(self.host):
            self.host = 0
        for k in k_config.virtual_hosts[self.host].keys():
            setattr(k_config,k,k_config.virtual_hosts[self.host][k])
        URLResolution.k_config = k_config

        fileName=URLResolution.translate_path(self.path_without_qs)
        self.fileName = fileName
        baseurl,subpath = URLResolution.getScriptElements(self.path_without_qs)
        self.COOKIE = Cookie.SimpleCookie()
        self.SET_COOKIE=Cookie.SimpleCookie()
        self.nameSpace={"REQUEST_HANDLER":self}
        self.outputStream = StringIO()

        # save current directory (it may be modified inside scripts)
        saveDir=os.getcwd()

        # if file doesn't exist, search for a file with same name and
        # an extension .py, .pih, .hip, .ks
        if not k_utils.exists(fileName):
            # I don't use os.path.exists() because on Windows, trailing dots
            # at the end of a file name are ignored
            if self.path in k_config.ignore:
                self.karrigellSendResponse(204,'No content')
                return
            try:
                ext=URLResolution.search(self.path_without_qs,fileName)
                fileName+=ext
                self.path_without_qs+=ext
            except IOError:
                self.install_translations()
                self.send_error(404,_("No file matching url ")+self.path_without_qs)
                return
            except URLResolution.DuplicateExtensionError,msg:
                self.send_error(300,msg)
                return

        # if fileName is a directory, search an index file and redirect
        elif os.path.isdir(fileName):
            try:
                indexFile = URLResolution.indexFile(fileName)
                fileName=os.path.join(fileName,indexFile)
            except URLResolution.DuplicateIndexError,msg:
                self.send_error(300, "More than one index file : %s" %msg)
                return
            except URLResolution.NoIndexError:
                # no index found : print directory listing
                if k_config.allow_directory_listing == 'none':
                    self.send_error(403,"Directory listing not allowed")
                    return
                try:
                    f = StringIO()
                    f.write(
                        Template.list_directory(self.path_without_qs,fileName))
                    self.ctype = content_type()
                except:
                    f = StringIO()
                    traceback.print_exc(file = f)
                    self.ctype = content_type()
                self.outputStream = f
                self.outputStream.read()    # so that tell() returns the length
                self.karrigellSendResponse(200,"Ok")
                return
            if not self.path_without_qs.endswith('/'):
                self.path=self.path_without_qs+'/'
                # make http redirection to destination file
                self.redirect(self.path)
                return
            else:
                self.path = self.path_without_qs = \
                    urlparse.urljoin(self.path_without_qs,indexFile)
                
        # if file is a ks script with no method, redirect to method 'index'
        if os.path.isfile(fileName) and fileName.lower().endswith('.ks'):
            if not len(subpath):
                if not self.path_without_qs.endswith('/'):
                    self.path=self.path_without_qs+'/index'
                else:
                    self.path=self.path_without_qs+'index'

                # make http redirection to index file
                self.redirect(self.path)
                return

        # file exists, now work on it
        base,extension=os.path.splitext(fileName)
        extension=extension[1:]
        
        # check if extension is authorized
        # hidden extensions are specified in [Directories] hidden_extensions
        # in the configuration file
        if extension in k_config.hide_extensions:
            self.send_error(403,"You are not allowed to see " \
                "the files with this extension")
            return
            
        # check if path authorized
        # hidden paths are regular expression patterns specified in 
        # [Directories] hidden_extensions in the configuration file
        for hidden_path in k_config.hide_paths:
            if hidden_path.match(self.path_without_qs):
                self.send_error(403,"You are not allowed to see " \
                "the files with the pattern %s" %hidden_path.pattern)
                return

        self.base_ctype, self.encoding = mimetypes.guess_type(fileName)
        self.ctype = self.base_ctype
        if self.base_ctype=='text/html':
            self.ctype = content_type()
        self.RESPONSE['Content-Type']=self.ctype

        os.chdir(os.path.dirname(fileName))

        script = None
        # cache
        if self.cache(fileName):
            script = self.loadedScripts[fileName][1]
        # process the script according to its extension
        elif extension.lower() in k_config.handled_extensions:
            # Python, pih or hip script : prepare environment and namespace
            try:
                script=Template.getScript(fileName)
                self.loadedScripts[fileName]=(os.path.getmtime(fileName),
                    script)
            except k_script.ParseError,error:
                # parse error : show traceback and file content
                tb=StringIO()
                traceback.print_exc(file=tb)
                error_info = [self.path,fileName,tb.getvalue(),
                    error.errorLine]
                errorFileName = os.path.join(k_config.serverDir,
                    "debugger/parseErrorShow.pih")
                try:
                    err_script = Template.getScript(errorFileName)
                    out = err_script.render({'error_info':error_info}).value
                except:
                    out = StringIO()
                    traceback.print_exc(file=out)
                    out = out.getvalue()
                self.outputStream = StringIO()
                self.outputStream.write(out)
                self.karrigellSendResponse(200,'Ok')
                return

        if script:
            self.prepare_env()
            # add attributes to the script object
            script.url=self.path_without_qs
            script.path=self.path
            script.parent=None
            script.subpath = subpath
            script.baseurl = baseurl
            # execution
            self.execute(script)
        elif k_utils.pathInDirs(fileName,k_config.protectedDirs)[0]:
            # static file in a protected directory
            self.prepare_env()
            self.nameSpace['fileName'] = fileName
            depth = k_utils.pathInDirs(fileName,k_config.protectedDirs)[1]
            script = Template.getScript(
                os.path.join(k_config.serverDir,'core','dump.py'))
            script.code = 'Include("'+'../'*depth + 'AuthentScript.py");' \
                + script.code
            self.execute(script)
        else:
            # for all other extensions, just read data and send it as is
            self.testGzip()
            if not self.send_static(fileName):
                self.send_response(200,"Ok")
                f = open(fileName,'rb')
                # for html document that have a META http-equiv content-type
                # just send the Content-type header text/html without encoding
                if self.base_ctype == "text/html":
                    if k_utils.has_meta_ct(f.read()):
                        self.RESPONSE['Content-type'] = self.base_ctype
                    f.seek(0) # rewind
                if self.testGzip():
                    f = self.doGzip(f.read())
                    self.RESPONSE['Content-Length'] = f.tell()
                    f.seek(0)
                # send response headers
                for item in self.RESPONSE.keys():
                    self.send_header(item,self.RESPONSE[item])
                self.end_headers()
                if not self.command == "HEAD":
                    self.copyfile(f, self.wfile)

        # in any case, restore current directory
        os.chdir(saveDir)

    def cache(self,fileName):
        # cache :
        # if file was already loaded and source has not been modified
        # since it was loaded, uses loaded code (prevents from reading
        # and parsing again)
        if self.loadedScripts.has_key(fileName):
            try:
                fileMTime=os.path.getmtime(fileName)
            except:
                return
            if self.loadedScripts[fileName][0]==fileMTime:
                return True
            elif fileName.lower().endswith('.ks'):
                # for ks script, if source has changed, remove the module
                moduleName=os.path.splitext(os.path.basename(fileName))[0]
                try:
                    del sys.modules[moduleName]
                except KeyError:
                    pass

    def send_static(self,fileName):
        """
        25/01/2005 Luca Montecchian <l.montecchiani@teamsystem.com>
        Http optimization, cache and headers for static files
        """
        # Disabled by configuration ?
        if self.cachemanaged == 0:
            return False

        s = os.stat(fileName)
        mdt = time.gmtime(s.st_mtime)
        lastModified = time.strftime("%a, %d %b %Y %H:%M:%S GMT", mdt)
        size = str(s.st_size)
        ims = self.HEADERS.get('if-modified-since',None)

        if lastModified and ims == lastModified :
            self.send_response(304)
            return True
        else:
            # populate the header  ;) 
            self.RESPONSE["Last-Modified"] = lastModified
            self.RESPONSE["Content-Length"] = size
        return False

    def execute(self,script):
        """Create an output stream and execute the script. Handle exceptions"""

        # add script directory in sys.path, so that the script can
        # import modules in the same directory
        dirname=os.path.dirname(script.name)
        if not dirname in sys.path:
            sys.path.append(dirname)    # for imports

        if not self.imported.has_key(self.host):
            self.imported[self.host] = {}
        else:
            for m in self.imported[self.host].keys():
                sys.modules[m] = self.imported[self.host][m][0]

        # self.execution is used in Include()
        self.execution=Template.ExecContext(script,self.nameSpace,
            self.path, self)

        # delete the imported modules whose source code has changed
        self.reload_modules()

        # for security reasons, hide some modules
        # for virtual hosts, prevents scripts to access session information
        save_modules = {}
        for m in ['k_session','KarrigellRequestHandler']:
            save_modules[m] = sys.modules[m]
            del sys.modules[m]

        try:
            try:
                self.outputStream.write(self.execution())
            finally:
                # restore saved modules
                for m in save_modules.keys():
                    sys.modules[m] = save_modules[m]
        # catches defined exceptions
        except k_script.HTTP_REDIRECTION,url:    
            # HTTP redirection towards a given URL
            self.redirect(url)
        except k_script.HTTP_ERROR,error:
            self.send_error(error.code,error.message)
        except k_script.HTTP_RESPONSE,(code,message):
            self.karrigellSendResponse(code,message)
        except k_script.AUTH_ABORT:
            pass
        else:
            # if everything's ok, send response
            if not self.cgi_info:
                try:
                    self.karrigellSendResponse(200,"Ok")
                except:
                    traceback.print_exc(file=sys.stderr)
            else:
                self.send_response(200,"Ok")
                self.outputStream.seek(0)
                if not self.command == "HEAD":
                    self.copyfile(self.outputStream, self.wfile)
        
        # save session object
        if hasattr(self,"sessionObject"):
            k_session.store(self.sessionId,self.sessionObject)
        
        # find new modules (those in sys.modules
        # that were not in the initial modules)
        newModules = set(sys.modules.keys())-set(initialModules)

        # store new modules in self.imported[self.host]
        for m in newModules:
            if m =='__main__':
                pass
            elif not m in self.imported[self.host].keys() and \
                hasattr(sys.modules[m],'__file__'):
                pyfile = sys.modules[m].__file__
                if pyfile.endswith('.pyc'):
                    pyfile = pyfile[:-1]
                if pyfile.endswith('.py'):
                    try:
                        self.imported[self.host][m] = [sys.modules[m],
                            pyfile,os.stat(pyfile)[8]]
                    except OSError:
                        print 'problem with module %s' %m
                        print 'file %s' %pyfile

        # remove new modules from sys.modules
        for m in newModules:
            # may seem strange, but *must* set the module to None first
            sys.modules[m] = None
            del sys.modules[m]

        # restore sys.path
        sys.path = copy.copy(initial_path)

    def reload_modules(self):
        # if k_config.reload_modules is set, force reloading of the imported 
        # modules if at least one has been modified since last request
        if k_config.reload_modules:
            _reload = False
            for m in self.imported[self.host].keys():
                if _reload:
                    break
                try:
                    mtime = os.stat(self.imported[self.host][m][1])[8]
                    if mtime != self.imported[self.host][m][2]:
                        _reload = True
                except OSError:
                    _reload = True
            if _reload:
                for module in self.imported[self.host].keys():
                    sys.modules[module] = None
                    del sys.modules[module]
                    del self.imported[self.host][module]

    def redirect(self,url):
        """HTTP redirection to url"""
        self.send_response(302,"Found")
        # don't forget cookies !
        for morsel in self.SET_COOKIE.values():
            self.send_header('Set-Cookie', morsel.output(header='').lstrip())
        self.send_header('Location',url)
        self.end_headers()

    def Authentication(self,testFunction,realm="Protected zone",
        errorMessage="Authentication error"):
        """Utility function for authentication
        testFunction is a user-defined function taking no argument and
        returning true if the couple (AUTH_USER,AUTH_PASSWORD) is allowed,
        false otherwise
        Example :
            def testFunction():
                return AUTH_USER=="holden" and AUTH_PASSWORD=="caulfield"

        errorMessage is the message displayed if user cancels authentication
        """
        if self.AUTH_USER:
            if not testFunction():
                self.authenticate(realm,errorMessage)
        else:
            self.authenticate(realm,errorMessage)

    def authenticate(self,realm,errorMessage):
        self.send_response(401,"Authorization")
        self.send_header("WWW-Authenticate",'Basic realm="%s"' %realm)
        self.send_header("Content-type",content_type())
        self.end_headers()
        self.wfile.write(k_encoding.encode(errorMessage, k_config.outputEncoding))
        # message if user cancels authentication request
        raise k_script.AUTH_ABORT

    def RestrictToAdmin(self,admin_file=None):
        """Used to restrict access to the administrator
        Uses a file with the admin's login and password md5 hashes"""
        if admin_file is None:
            admin_file = os.path.join(k_config.serverDir,'admin','admin.ini')
        import md5
        digest=open(admin_file,"rb").read()
        userDigest=digest[:16]
        passwordDigest=digest[16:]

        def authTest():
            return (md5.new(self.AUTH_USER).digest()==userDigest \
                and md5.new(self.AUTH_PASSWORD).digest()==passwordDigest)

        self.Authentication(authTest,
            realm=_("Administration"),
            errorMessage=_("Authentication error"))

    def Login(self,script=None):
        if script is None:
            script = os.path.join(k_config.serverDir,'core','login.py')
        print Template.getScript(script).render(self.nameSpace).value
        
    def setSessionObject(self):
        """Internal method, initializes the session object
        If the client has sent a cookie named sessionId, takes its value and
        returns the corresponding SessionElement objet, stored in
        k_session.sessionDict
        Otherwise creates a new SessionElement objet and generates a random
        8-letters value sent back to the client as the value for a cookie
        called sessionId
        """
        if self.HEADERS.has_key("cookie"):
            ck=Cookie.SimpleCookie(self.HEADERS["cookie"])
            if ck.has_key("sessionId"):
                sessionId=ck["sessionId"].value
            else:
                self.SET_COOKIE=Cookie.BaseCookie()
                sessionId=k_utils.generateRandom(8)
                self.SET_COOKIE["sessionId"]=sessionId
        else:
            self.SET_COOKIE=Cookie.BaseCookie()
            sessionId=k_utils.generateRandom(8)
            self.SET_COOKIE["sessionId"]=sessionId
        self.sessionObject = k_session.getSessionObject(sessionId)
        self.sessionId = sessionId

    def Session(self):
        """Function called in scripts, retrieves the session object"""
        if not hasattr(self,"sessionObject"):
            self.setSessionObject()
        return self.sessionObject

    def send_error(self, code, message=None):
        """Overrides BaseHTTPServer.BaseHTTPRequestHandler's send_error with
        additional output : server version and date/time"""
        self.install_translations()
        self.translateClassAttributes()
        try:
            short, long = self.responses[code]
        except KeyError:
            short, long = '???', '???'
        if not message:
            message = short
        explain = long
        self.log_error("code %d, message %s", code, message)
        self.send_response(code, message)
        self.send_header("Content-Type", content_type())
        self.end_headers()
        err_msg = (self.error_message_format %
                         {'code': code,
                          'message': message,
                          'explain': explain,
                          'version': __version__,
                          'time':self.date_time_string()})
        self.wfile.write(k_encoding.encode(err_msg, k_config.outputEncoding))

    def address_string(self):
        """Overrides address_string to remove hostname resolution"""
        return self.client_address[0] 
    
    def testGzip(self):
        """Test if content should be gzipped"""
        if not k_config.gzip:
            return False
        if not gzip_support:
            return False
        accept_encoding = self.HEADERS.get('accept-encoding','').split(',')
        accept_encoding = [ x.strip() for x in accept_encoding ]
        # if gzip is supported by the user agent,
        # and if the option gzip in the [Server] section of the
        # configuration file is set, 
        # and content type is text/ or javascript, 
        # set Content-Encoding to 'gzip' and return True
        if 'gzip' in accept_encoding and \
            self.ctype and (self.ctype.startswith('text/') or 
            self.ctype=='application/x-javascript'):
            self.RESPONSE['Content-Encoding']='gzip'
            return True
        return False

    def doGzip(self,data):
        """gzip data and return a StringIO holding the gzipped data"""
        sio = cStringIO.StringIO()
        gzf = gzip.GzipFile(fileobj = sio, mode = "wb")
        gzf.write(data)
        gzf.close()
        return sio

    def karrigellSendResponse(self,code,message):
        self.send_response(code,message)
        # sends the cookie before the other headers, seems to be required ?
        if self.SET_COOKIE.has_key("sessionId") \
            and not self.sessionId in k_session.sessions:
            # if session was closed, set expiration time of cookie to 0
            self.SET_COOKIE["sessionId"]=self.sessionId
            self.SET_COOKIE["sessionId"]["expires"]=0
        if self.SET_COOKIE:
            # Cookies should be header items, rather than pushed out to the
            # main stream.
            for morsel in self.SET_COOKIE.values():
                self.send_header('Set-Cookie', morsel.output(header='').lstrip())
        # test if content should be gzipped
        if code == 200 and self.testGzip():
            self.outputStream = self.doGzip(self.outputStream.getvalue())
        # set Content-Length header
        self.RESPONSE['Content-Length']=self.outputStream.tell()
        # send response headers
        for item in self.RESPONSE.keys():
            self.send_header(item,self.RESPONSE[item])
        self.end_headers()
        if not self.command == "HEAD":
            # output stream is written on the socket fileobject
            self.outputStream.seek(0)
            self.copyfile(self.outputStream, self.wfile)

# Python may not have gzip support
gzip_support = False
try:
    import gzip
    gzip_support = True
except ImportError:
    print "Warning - gzip is not supported"
    pass

initial_path = copy.copy(sys.path)
initialModules = copy.copy(sys.modules.keys())
initialModules.sort()
