import k_config
from HTMLTags import *

conf_vars = {}
for k in dir(k_config):
    if type(getattr(k_config,k)) in (str,bool,int,list) and not k.startswith("_"):
        conf_vars[k] = getattr(k_config,k)

print TABLE(Sum([ TR(TD(k)+TD(v)) for k,v in conf_vars.items() ]))
