#!/bin/python
#coding:utf-8
'''cdays+1-exercise-1.py
    @note: 使用os.stat获取相关信息, os.walk遍历,
    @see: help(os)
    @author: U{shengyan<mailto:shengyan1985@gmail.com>}
    @version: $Id$
'''
import sys
import os

def get_top_three(path):
    ''' 获取给定路径中文件大小最大的三个
    @param path: 指定路径
    @return 返回一个list，每项为 (size, filename)
    '''
    all_file = {}
    for root, dirs, files in os.walk(path):             #遍历path
        for onefile in files:
            fname = os.path.join(root, onefile)         #获得当前处理文件的完整名字
            fsize = os.stat(fname).st_size              #获得当前处理文件大小
            if all_file.has_key(fsize):                 #按照文件大小存储
                all_file[fsize].append(fname)
            else:
                all_file[fsize] = [fname]
    fsize_key = all_file.keys()                         #得到所有的文件大小
    fsize_key.sort()                                    #排序，从小到大
    result = []
    for i in [-1, -2, -3]:                              #依次取最大的三个
        for j in all_file[fsize_key[i]]:                #保存
            result.append((fsize_key[i], j))
    return result[:3]                                   #返回前三个
    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'usage:\n\tpython cdays+1-exercise-1.py path'
    else:
        abs_path = os.path.abspath(sys.argv[1])         #得到绝对路径
        if not os.path.isdir(abs_path):                 #判断所给的路径是否存在
            print '%s is not exist' % abs_path
        else:
            top = get_top_three(abs_path)
            for (s, f) in top:
                print '%s\t->\t%s' % (f, s)
            
            
