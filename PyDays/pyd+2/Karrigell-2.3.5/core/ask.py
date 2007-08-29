from HTMLTags import *

def ask(title,action,*fields):
    print H2(title)
    print '<form action="%s" method="post">' %action
    print '<table>'
    for f in fields:
        if f[1]=='hidden':
            print INPUT(name=f[0],Type="hidden",value=f[2])
        else:
            prompt,name=f[:2]
            if len(f)>2:
                format = f[2]
                if format.lower() == 'textarea':
                    _input = TEXTAREA(name=name)
                elif format.lower() == 'password':
                    _input = INPUT(name=name,Type='password')
            else:
                _input = INPUT(name=name)
            print TR(TD(prompt)+TD(_input))
    print '</table>'
    print INPUT(Type="submit",value="Ok")
    print '</form>'