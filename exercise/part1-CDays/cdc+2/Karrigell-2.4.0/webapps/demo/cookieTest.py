if not SET_COOKIE.has_key('mylogin') or \
    not _is_valid(SET_COOKIE['mylogin']):
        raise SCRIPT_ERROR,'Unknown user'
