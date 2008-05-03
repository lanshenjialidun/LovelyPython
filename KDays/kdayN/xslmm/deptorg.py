# $Id: deptorg.py 325 2005-12-30 04:23:49Z  $
# deptorg.py 快捷mm XML 理解处理

#!/usr/bin/env python
# coding:utf-8

import sys,os,string,re
#import time,datetime
#from elementtree.ElementTree import *
from elementtree import ElementTree
from HTMLTags import *
from dict4ini import DictIni


orgxml		= "deptorg.xml"



def listDeptStaff(elem):
    """列选分部成员节点
    """
    staffdict = {}
    for e in elem:
        if "staff" == e.attrib["TEXT"].encode("utf8"):
            #print e.attrib["TEXT"].encode("utf8")
            staff = e.findall("./node")
            for s in staff:
                name = s.attrib["TEXT"].encode("utf8")     
                #print name
                mem = getStaffUser(s)
                #print "".join([mem[i] for i in mem.keys()])
                for k in mem.keys():
                    if "mail" == k:
                        #print mem[k]
                        staffdict[mem[k]] = name
                    else:
                        pass
                
                
        else:
            pass
    #print staffdict
    return staffdict

def getStaffUser(elem):
    """列选成员所有信息
    """
    user = {}
    usr = elem.findall("./node")
    for u in usr:
        key =u.attrib["TEXT"]
        user[key]=u.find('./node').attrib["TEXT"].encode("utf8")       
    #print user[user.keys()[1]]
    
    return user


#通告包含成功
#print open(orgxml,"r").read()
print HR()
tree = ElementTree.parse(orgxml)
elem = tree.getroot()
#print elem
dept = elem.findall("node/node")

deptall = {}
deptree = []
for d in dept:
    if "DeptOrgVersion" == d.attrib["TEXT"]:
        pass
    else:
        #print LI(d.attrib["TEXT"].encode("utf8"))
        staff = d.findall("./node")
        staffdict=listDeptStaff(staff)
        deptall.update(staffdict)
        deptree.append({d.attrib["TEXT"]:staffdict})

"""将XML 处理结果通过 sessoin 对象传递回引用页面！
"""
sess.usr["dept"]=deptall
sess.usr["deptree"]=deptree

#print dir()

