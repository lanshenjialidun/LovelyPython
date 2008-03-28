"""The methods modify_path and modify_headers are called after all the 
elements of the original HTTP request have been received by the request 
handler
modify_query is called in prepare_env()

They return the modified arguments. This module can be edited to tune Karrigell
to particular needs
"""

def modify_path(path):
    return path
    
def modify_headers(headers):
    #HEADERS['host'] = HEADERS['x-forwarded-host']
    return headers

def modify_query(query):
    return query
    