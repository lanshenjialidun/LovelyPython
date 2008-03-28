"""A script to generate the code to handle a database from
a configuration script

This script is a Python script which must define at least 2 variables :
- name   : the name of the database
- fields : a list of strings of the form "name:type" where name is the
           name of the field and type, its type
           Example : fields = ['name:str','author:str','issued:datetime.date']

Additional variables can be defined :
- dbmodule       : a string with the database module name. Defaults to 
                   'gadfly'. Must be one of 'gadfly','kirbybase','sqlite'
- data_directory : the directory where database will be stored (defaults to 
                   the same directory as the configuration script)
- pageTitle      : the title printed on top of the HTML pages (defaults to
                   the variable name)
- stylesheet     : the stylesheet url applied to all HTML pages (defaults to
                   default.css in this directory)
- security       : the security level. 3 possible values :
                   'low' : anyone can edit and remove records
                   'standard' : only logged in users can manage the base, only
                   the administrator can manage the users' base
                   'high' : only the administrator can manage the base
                   Default is 'low'
"""

try:
    SCRIPT_END
except NameError:
    pass
else:
    print "This script can't be executed by Karrigell"
    raise SCRIPT_END

import os
import cStringIO
import datetime
import sys
import md5

try:
    # if Tkinter is available, make a gui application
    from Tkinter import *
    import tkFileDialog
    import tkMessageBox
    gui = True
except:
    # otherwise, use raw_input()
    gui = False

from records_skeleton import *
import db_specifics

def save_admin_info(admin_file,login,password):
    out = open(admin_file,'w')
    out.write(login+'\n')
    # save md5 digest of the password
    out.write(md5.new(password).digest())

def selectConfigFile():
# select the configuration file
    if gui:
        configFile=tkFileDialog.askopenfilename(master = root,parent=None,
           filetypes=[("Configuration file",".py")])
    else:
        print "Configuration file :",
        configFile = raw_input()
    if not configFile:
        sys.exit()
    generate_script(configFile)

def generate_script(configFile):
    # initialize the variables
    conf_vars = {}
    execfile(configFile,conf_vars)
    
    # check if 'name' and 'fields' are defined in the config file
    if not conf_vars.has_key('name'):
        print "Error - configuration script must specify a variable 'name'"
    else:
        name = conf_vars['name']

    if not conf_vars.has_key('fields'):
        print "Error - configuration script must specify a variable 'fields'"
    else:
        fields = conf_vars['fields']

    script_directory = os.path.dirname(configFile)
    # defaults
    security = conf_vars.get('security','low')
    stylesheet = conf_vars.get('stylesheet','../default.css')
    data_directory = conf_vars.get('data_directory',script_directory)
    pageTitle = conf_vars.get('pageTitle', 'Managing base %s' %name)

    # default for database module if undefined
    if not conf_vars.has_key('dbmodule'):
        try:
            import kirbybase
            dbmod_name = 'kirbybase'
        except:
            print "Error - no database module specified in configuration " \
                "script and KirbyBase not installed"
    else:
        dbmod_name = conf_vars['dbmodule']

    # if security level is not 'low', there must be a login/password file
    # for the administrator, created later in the script
    if security != 'low':
        abspath = os.path.join(os.path.normpath(data_directory),name)
        admin_file = '%s.ini' %abspath

        users_name = conf_vars.get("users_name",'%s_users' %name)
        users_fields = conf_vars.get("users_fields",['login:str','password:str'])

    else:
        users_name = ""

    def make_script(name,
        fields,
        pageTitle,
        security,
        stylesheet):
        """Generate the ks script to manage the database called 'name'
        See parameters above
        If authent is True, an HTTP basic authentication test is made for
        every access to the management script
        """
        if security not in ['low','standard','high']:
            print "Invalid value for security : %s\n"
            print "Must be in ['low','standard','high']"

        authent = (security == 'high')

        def field_names(fields):
            return [ field.split(":")[0] for field in fields ]

        # initialize variables used in the db_specifics module
        db_specifics.fieldDefs(dbmod_name,data_directory,name,fields,users_name)

        # open the generated ks script
        out = open(os.path.join(script_directory,'%s.ks' %name),'w')

        # write header, imports, database module
        out.write('"""'+hdr1 %(name,datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))+'"""')
        out.write(imports)
        out.write("# database-specific modules\n")
        out.write(db_specifics.modulesToImport(dbmod_name))

        if authent:
            out.write(admin %{'admin_file':admin_file})
            # if only the administrator can run the script, no need for additional
            # security
            security = 'low'

        # write configuration variables
        out.write("\n#parameters\n")
        params = ['name','pageTitle']
        for param in params:
            val = locals()[param]
            if isinstance(val,str):
                out.write('%s = "%s"\n' %(param,locals()[param]))
            else:
                out.write('%s = %s\n' %(param,locals()[param]))
        out.write('field_names = %s\n' %db_specifics.field_names)
        out.write('field_types = %s\n' %db_specifics.field_types)
        if security != 'low':
            out.write("users = r'%s'\n" %db_specifics.users_base)
            out.write('admin_file = r"%s"\n' %admin_file)    

        # code to open an existing base, or create it with the specified fields
        out.write(db_specifics.createCode(dbmod_name))

        if security != 'low':
            # generate code to open the users base
            out.write(db_specifics.openUsersCode(dbmod_name))

        # generate html HEAD part
        out.write('\n#header\nheader=')
        out.write(header %{'stylesheet':stylesheet,'title':pageTitle})
        out.write('\n')

        # default user test is True if security level is 'low', False otherwise
        out.write(hdr2 %{'default_user_test':(security=='low')})

        if security == 'standard':
            out.write(index_if_users1)
            out.write(db_specifics.selectByUserId(dbmod_name))
            out.write(index_if_users2)

        # generate code to select all records and print them in a table
        out.write(db_specifics.selectAllAsDict(dbmod_name,name))
        out.write(index_security_not_high)
        print_code = ['print TD(record["%s"],Class="main")' \
            %field for field in db_specifics.field_names]

        out.write(('\n'+' '*12).join(print_code))
        out.write(index_security_not_high_2)

        out.write(index_end)

        # generate code to edit an existing record or create a new one
        out.write(edit_1 %(db_specifics.selectByRecordId(dbmod_name),
            db_specifics.field_names))
        input_code = []
        for field in field_names(fields):
            input_code.append('print TR(TD("%s")+'
                'TD(INPUT(name="%s",size="40",value=record["%s"])))'
                    %(field,field,field))

        out.write(('\n'+' '*4).join(input_code))
        out.write(edit_2)

        # generate code to insert or remove a record, check users login/password
        out.write(rest %(db_specifics.insert(dbmod_name),
                        db_specifics.remove(dbmod_name),
                        db_specifics.selectUserByLogin(dbmod_name)))

        # generate code to redirect to the admin page
        if security != 'low':
            out.write(admin_method %users_name)

        out.close()

    # generate main script
    make_script(name, 
        fields,
        pageTitle,
        security,
        stylesheet)

    if security == 'low':
        sys.exit()
    else:
        print "security %s "%security   
        # ask for administrator login/password
        # if an admin file already exists and nothing is
        # entered, keep existing values
 
        test = os.path.exists(admin_file)
        
        def enter_admin_info():
            login = w_login.get()
            password = w_password.get()
            if not login:
                tkMessageBox.showerror(title = "Missing login",
                    message = 'You must enter a login')
                return
            if not len(password)>5:
                tkMessageBox.showerror(title = "Invalid password",
                    message = 'You must enter a password of length > 5')
                return            
            save_admin_info(admin_file,login,password)
            root.destroy()
        
        if gui:
            b_select.destroy()
            Label(root,text="Security level is %s. \nYou must enter " \
                "a login and password for the administrator" %security)\
                .grid(row=1,column=0,columnspan=2)
            Label(root,text="Login").grid(row=2,column=0)
            w_login = Entry(root)
            w_login.grid(row=2,column=1)
            Label(root,text="Password").grid(row=3,column=0)
            w_password = Entry(root)
            w_password.grid(row=3,column=1)
            Button(root,text="Ok",command=enter_admin_info).grid(row=4,column=0)
            Button(root,text="Cancel",command=root.destroy).grid(row=4,column=1)
        else:
            print "Security level is %s. \nYou must enter " \
                "a login and password for the administrator" %security
            print "Login :",
            login = raw_input()
            print "Password :",
            password = raw_input()
            save_admin_info(admin_file,login,password)

        # generate users management script
        make_script(users_name,
            users_fields,
            "%s users" %name,
            "high",
            stylesheet)

if gui:
    root = Tk()
    root.title("Script generator for Karrigell")
    root.geometry("300x100")
    b_select = Button(root,text="Select configuration file",command=selectConfigFile)
    b_select.grid(row=1,column=0)
    root.mainloop()
else:
    print "Script generator for Karrigell"
    selectConfigFile()
