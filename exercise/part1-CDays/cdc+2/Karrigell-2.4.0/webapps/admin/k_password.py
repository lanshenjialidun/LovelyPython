"""New version written by Marcelo Santos Araujo"""

# forbid execution from Karrigell
try:
    SCRIPT_END
except NameError:
    pass
else:
    print "This script can't be executed by Karrigell"
    raise SCRIPT_END

import os
import sys
from getpass import getpass

# update sys.path to import PyDbLite
db_dir = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())),"databases")
sys.path.append(db_dir)
import PyDbLite

# create or open the users database
db = PyDbLite.Base("users.pdl")
db.create("login","password","role","session_key","nb_visits",
    "last_visit",mode="open")

print "Create a login/password for administrator"
login=raw_input("Login: ")
password=getpass("Password: ")
confirm_password = getpass("Password again (to confirm): ")
if password != confirm_password:
    print "Password mismatch!"
    sys.exit()
else:
    # remove existing admin if any
    db.delete(db(role="admin"))
    # insert new admin
    db.insert(login=login,password=password,role="admin",nb_visits=0)
    db.commit()
    print "Done..!"