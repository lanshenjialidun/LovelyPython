# reads the Configuration File
# the variable 'base' is set to current directory
import ConfigParser
import os
import sys
import getopt
import traceback
import urllib
import re

# set default values
initFile = "Karrigell.ini"
port = 80  # the standard HTTP port, can be set in command line
reload_modules = 1
debug = 1
silent = False
gzip = False
persistentSession = 0
base = '' # base URL (used for Xitami)
ignore = []
allow_directory_listing = "none"
hide_extensions = []
hide_paths = []
language=""
outputEncoding = 'ISO-8859-1'

encodeFormData = False
loggingFile = ''
loggingParameters = '"a",0,10'

class ConfigError(Exception):
    pass

def usage():
    print "Usage : python Karrigell.py [-P port] [-D] [-S] [-H] [initFile]"
    print "\n\tport = HTTP port"
    print "\n\tR = reload (always reloads imported modules)"
    print "\n\tS = silent (no output written to console)"
    print "\n\tH = help (shows this message)"
    print "\n\tinitFile = the initialization file to be used"

# get the command-line options (parsed later, after the configuration file)
try:
    _opts, _args = getopt.getopt(sys.argv[1:], "hP:L:SR")
except getopt.GetoptError:
    # print usage information and exit:
    usage()
    sys.exit(2)

if _args:
    if len(_args) == 1:
        initFile = _args[0]
    else:
        usage()
        sys.exit(2)

# server directory
if len (sys.argv) > 0:
    serverDir=os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    serverDir=os.getcwd()

for o, a in _opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    if o in ("-S", "--silent"):
        silent=1
    if o in ("-R", "--reload"):
        reload_modules=1
    if o in ("-P", "--port"):
        try:
            port=int(a)
        except ValueError:
            raise ConfigError, _("Error - port must be an integer")

conf=ConfigParser.ConfigParser({'base':serverDir})
try:
    conf.read(initFile)
except ConfigParser.ParsingError,message:
    parsingErrorMsg=_("Parsing error")
    print parsingErrorMsg,message
    print type(message)
    print message.__dict__
    for item in message._args:
        print item[1]
    sys.exit(2)

# Server
try:
    port=int(conf.get("Server","port"))
except ValueError:
    raise ConfigError, _("Error - port must be an integer")
except (ConfigParser.NoOptionError,ConfigParser.NoSectionError):
    pass
except:
    traceback.print_exc(file=sys.stderr)

# reload_modules level
# 1 = reloads imported files every time
try:
    reload_modules = conf.getint("Server","reload_modules")
except:
    pass

# debug level
# 1 = show the "Debug" button on error pages
try:
    debug = conf.getint("Server","debug")
except:
    pass

# silent mode
try:
    silent=conf.getboolean("Server","silent")
except:
    pass

# gzip support
try:
    gzip=conf.getboolean("Server","gzip")
except:
    pass

# persistent sessions
persistentSession = False
try:
    persistentSession=conf.getboolean("Server","persistentSession")
except:
    pass

# urls to ignore
try:
    ignore=conf.get("Server","ignore").split(';')
except:
    pass

# user-defined values
globalScripts=[]
try:
    _globalScriptsList=conf.get("Server","global").split(";")
    for _globalScript in _globalScriptsList:
        _gPath,_gName=os.path.dirname(_globalScript),os.path.basename(_globalScript)
        _gPath = os.path.normpath(_gPath)
        if not _gPath in sys.path:
            sys.path.append(_gPath)
        _gName=os.path.splitext(_gName)[0]
        exec ('import '+os.path.basename(_gName))
        globalScripts.append(_gName)
except (ConfigParser.NoSectionError,ConfigParser.NoOptionError):
    pass

# output encoding
try:
    outputEncoding=conf.get("Server","outputEncoding")
except (ConfigParser.NoSectionError,ConfigParser.NoOptionError):
    pass

try:
    unicode('a',outputEncoding)
except LookupError:
    print "Unknown outputEncoding in configuration file : %s" %outputEncoding
    sys.exit()

# form data encoding
try:
    encodeFormData = conf.getboolean("Server","encodeFormData")
except (ConfigParser.NoSectionError,ConfigParser.NoOptionError):
    pass

# Root Directory, default to server directory
rootDir=os.path.join(serverDir,"webapps")
try:
    rootDir=conf.get("Directories","root")
except (ConfigParser.NoOptionError,ConfigParser.NoSectionError):
    pass
except:
    traceback.print_exc(sys.stderr)

if not os.path.isdir(rootDir):
    raise ConfigError, "root directory not found : %s" %rootDir

# cgi Directory, default to root/cgi-bin
cgi_directories = [os.path.join(rootDir,"cgi-bin")]
try:
    cgi_directories=conf.get("Directories","cgi").split(';')
    cgi_directories = [os.path.normpath(d) for d in cgi_directories ]
except (ConfigParser.NoOptionError,ConfigParser.NoSectionError):
    pass
except:
    traceback.print_exc(sys.stderr)
    
# protected zones : for all scripts, include AuthentScript.py
protectedDirs=[]
try:
    protectedDirs = conf.get("Directories","protected").split(";")
    protectedDirs = [ os.path.normpath(_p) for _p in protectedDirs ]
except (ConfigParser.NoOptionError,ConfigParser.NoSectionError):
    pass
except:
    traceback.print_exc(sys.stderr)
    sys.exit()

# files with extension in hide_extensions won't be shown
try:
    hide_extensions = conf.get("Directories","hide_extensions")
    hide_extensions = [ _h.strip() for _h in hide_extensions.split(";") ]
except (ConfigParser.NoOptionError,ConfigParser.NoSectionError):
    pass

# files matching the patterns in hide_paths won't be shown
try:
    hide_paths = conf.get("Directories","hide_paths")
    hide_paths = [ re.compile(_h.strip()) for _h in hide_paths.split(";") ]
except (ConfigParser.NoOptionError,ConfigParser.NoSectionError):
    pass

# logging directory
try:
    loggingFile=conf.get("Directories","loggingFile")
except (ConfigParser.NoOptionError,ConfigParser.NoSectionError):
    pass

# logging parameters
try:
    loggingParameters=conf.get("Directories","loggingParameters")
except (ConfigParser.NoOptionError,ConfigParser.NoSectionError):
    pass


# Applications
extensions_map={}
try:
    extensions=conf.options("Applications")
    for _extension in extensions:
        extensions_map["."+_extension]=conf.get("Applications",_extension)
except ConfigParser.NoSectionError:
    pass

# Aliases
alias={}
try:
    _aliases=conf.options("Alias")
    for _al in _aliases:
        _path=conf.get("Alias",_al)
        alias[_al]=os.path.normpath(urllib.unquote(_path))
    if not 'base' in _al:
        del alias['base']
except ConfigParser.NoSectionError:
    pass
    
# default language (added by Sylvain Ramousse)
try:
    language=conf.get("Translation","lang")
except (ConfigParser.NoSectionError,ConfigParser.NoOptionError):
    pass

# virtual hosts
virtual_hosts = {}

# default
virtual_hosts[0] = {
    'silent' : silent,
    'reload_modules' : reload_modules,
    'port' : port,
    'gzip' : gzip,
    'persistentSession' : persistentSession,
    'ignore': ignore,
    'globalScripts' : globalScripts,
    'rootDir' : rootDir,
    'protectedDirs' : protectedDirs,
    'allow_directory_listing' : allow_directory_listing,
    'hide_extensions' : hide_extensions,
    'extensions_map' : extensions_map,
    'alias' : alias,
    'language' : language
    }

def get_allow_dir_list(adl,host):
    if not adl in ['all','none']:
        raise ConfigError, "Error in configuration file %s : " \
            "allow_directory_listing = %s for virtual host %s"\
            '(must be "all" or "none")' %(initFile,adl,
                host)
    return adl

# determine who can read directory listings
try:
    allow_directory_listing = conf.get("Directories",
        "allow_directory_listing")
except (ConfigParser.NoOptionError,ConfigParser.NoSectionError):
    pass

virtual_hosts[0]['allow_directory_listing'] = \
    get_allow_dir_list(allow_directory_listing,0)

for section in conf.sections():
    if section.strip().lower().startswith('virtualhost'):
        host = section.split()[1]
        virtual_hosts[host] = {}
        for option in conf.options(section):
            if option == 'root':    
                if os.path.isdir(conf.get(section,option)):
                    virtual_hosts[host]['rootDir'] = conf.get(section,option)
                else:
                    raise IOError,'Root directory for virtual host %s' \
                    ' not found : %s' %(host,conf.get(section,option))
            elif option == 'allow_directory_listing':
                adl = conf.get(section,option)
                virtual_hosts[host]['allow_directory_listing'] = \
                    get_allow_dir_list(adl,host)

# import modules to handle scripts
handled_extensions = []
for path in ["core","modules","debugger"]:
    p = os.path.join(serverDir,path)
    if not p in sys.path:
        sys.path.append(p)
for f in os.listdir(os.path.join(serverDir,"modules")):
    if f.startswith('mod_') and f.endswith('.py'):
        module_name = os.path.splitext(f)[0]
        handled_extensions.append(module_name[4:].lower())

if __name__=="__main__":
    for k,v in globals().items():
        print "%s : %s" %(k,v)
