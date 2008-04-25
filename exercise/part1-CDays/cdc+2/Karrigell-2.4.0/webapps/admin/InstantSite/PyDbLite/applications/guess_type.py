import re
import datetime
import locale

locale.setlocale(locale.LC_ALL,'')

# guess locale date format
d = datetime.date(2000,1,2)
d_str = d.strftime("%x")
vals = [ int(x) for x in re.match("(\d+)[/-](\d+)[/-](\d+)$",d_str).groups() ]
date_fmt = {"m" : vals.index(1), # month
    "d" : vals.index(2) # day
    }

ix_year = [ i for i in range(3) if not i in date_fmt.values() ][0]
date_fmt["y"] = ix_year # year

def _date(s,elts):
    vals = [ int(x) for x in elts ]
    y = vals[date_fmt["y"]]
    m = vals[date_fmt["m"]]
    d = vals[date_fmt["d"]]
    try:
        return datetime.date(y,m,d)
    except:
        return s

patterns = [
    ("-?\d+$",int),
    ("-?\d*\.\d+$",float),
    ("-?\d+\.\d*$",float),
    ("(\d+)[/-](\d+)[/-](\d+)$",_date)
    ]

def guess_type(s):
    for (pattern,conv_func) in patterns:
        mo = re.match(pattern,s)
        if mo:
            if conv_func is _date:
                return _date(s,mo.groups())
            else:
                return conv_func(s)
    if s.startswith("'"):
        for p,c in [ (p,c) for (p,c) in patterns if c in [int,float] ]:
            if re.match(p,s[1:]):
                return s[1:]
    return s

if __name__=="__main__":

    for v in ["abcd","123","-125","--55","1.02","-12.","'123","'1.23","--12.","-1a",
        "2008/10/2","6/10/1958","11-12-1964"]:
        print v,guess_type(v),guess_type(v).__class__
        