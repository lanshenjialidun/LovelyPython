import os
import sys
import traceback

import k_config
import k_translation

class LocalizedRequestHandler:

    current_language="" # current language
    accepted_languages=[]
    forbiddenListMsg="Directory list forbidden"
    fileNotFoundMsg="File not found"

    def install_translations(self):
        # translation 
        self.get_language()
        k_translation.install(k_config.serverDir,
                self.accepted_languages,k_config.outputEncoding) 

    # modifies BaseHTTPServer class attributes for internationalization
    def translateClassAttributes(self):
        self.weekdayname = [_('Mon'), _('Tue'), _('Wed'), _('Thu'), _('Fri'),
            _('Sat'), _('Sun')]

        self.monthname = [None,
            _('Jan'), _('Feb'), _('Mar'), _('Apr'), _('May'), _('Jun'),
            _('Jul'), _('Aug'), _('Sep'), _('Oct'), _('Nov'), _('Dec')]

        self.responses = {
            200: ('OK', _('Request fulfilled, document follows')),
            201: ('Created', _('Document created, URL follows')),
            202: ('Accepted',
                  _('Request accepted, processing continues off-line')),
            203: ('Partial information', _('Request fulfilled from cache')),
            204: ('No response', _('Request fulfilled, nothing follows')),

            301: ('Moved', _('Object moved permanently -- see URI list')),
            302: ('Found', _('Object moved temporarily -- see URI list')),
            303: ('Method', _('Object moved -- see Method and URL list')),
            304: ('Not modified',
                  _('Document has not changed since given time')),

            400: ('Bad request',
                  _('Bad request syntax or unsupported method')),
            401: ('Unauthorized',
                  _('No permission -- see authorization schemes')),
            402: ('Payment required',
                  _('No payment -- see charging schemes')),
            403: ('Forbidden',
                  _("Request forbidden -- authorization will not help")),
            404: ('Not found', _('Nothing matches the given URI')),

            500: ('Internal error', _('Server got itself in trouble')),
            501: ('Not implemented',
                  _('Server does not support this operation')),
            502: ('Service temporarily overloaded',
              _('The server cannot process the request due to a high load')),
            503: ('Gateway timeout',
                  _('The gateway server did not receive a timely response')),
            }
        self.error_message_format="<head><title>"+_("Error response")+\
            "</title></head><body><h1>"+_("Error response")+"</h1>"+\
            "<p>"+_("Error code")+" %(code)d."+\
            "<p>"+_("Message: ")+"%(message)s."+\
            "<p>"+_("Error code explanation: ")+"%(code)s = %(explain)s."+\
            "<p><i>Karrigell %(version)s - %(time)s</i></body>"
        self.forbiddenListMsg=_("Directory list forbidden")
        self.fileNotFoundMsg=_("File not found")
        self.execErrMsg=_("Error for")+' %s'

    def send_head(self):
        """Overrides BaseHTTPServer's send_head for internationalization of 
        the 404 error and adding index.pih and index.hip as default"""
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            for index in "index.html", "index.htm", "index.pih", "index.hip":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        if ctype.startswith('text/'):
            mode = 'r'
        else:
            mode = 'rb'
        try:
            f = open(path, mode)
            self.send_response(200)
            self.send_header("Content-type", ctype)
            self.end_headers()
            return f
        except IOError:
            self.send_error(404, self.fileNotFoundMsg)
            return None
        except:
            traceback.print_exc(file=sys.stderr)
            return None

    def get_language(self):
        """Parses accept-language header if any and initializes the 
        accepted_languages list. If a language option has been defined
        in the configuration file it is used regardless of the browser
        options ; if this option is "default" then no translation is
        made"""
        if len(self.accepted_languages):
            if self.accepted_languages[0] == "default":
                self.accepted_languages=[]
        elif not hasattr(self,"HEADERS"):
            self.accepted_languages=[]                    
        else:
            if not self.HEADERS.has_key("accept-language"):
                self.accepted_languages=[]
                return
            languageHeader=self.HEADERS["accept-language"]
            languageList=languageHeader.split(",")
            langs=[]
            for item in languageList:
                l=item.split(";")[0][:2]
                if not l in langs:
                    langs.append(l)
            self.accepted_languages = langs

    def trace(self,data):
        sys.stderr.write('%s\n' %data)
