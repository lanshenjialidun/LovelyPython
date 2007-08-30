#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import log
import re
import sys

_sample_whois = """
inetnum:      202.96.63.97 - 202.96.63.127
netname:      CAIMARNET

domain:       123.93.203.in-addr.arpa
descr:        Reverse zone for 203.93.123.0/24

domain:       140.4.221.in-addr.arpa
descr:        reverse delegation for 221.4.140/24

domain:       250.5.221.in-addr.arpa
descr:        China Network Communications Group Co. ChongQing
"""

def read_chunk(whois_file):
    """read one chunk from whois file once

    >>> from StringIO import StringIO
    >>> list(read_chunk(StringIO(_sample_whois)))
    [('inetnum', ['202.96.63.97', '202.96.63.127']), ('descr', '203.93.123.0/24'), ('descr', '221.4.140/24'), ('domain', '250.5.221')]
    """
    while True:
        line = whois_file.readline()
        if not line:
            break
        if line == '\n':
            line = whois_file.readline()
            if line.startswith('inetnum:'):
                inetnum = line[len('inetnum:'):].strip()
                inetnum = inetnum.replace(' ', '').split('-')
                yield ('inetnum', inetnum)
            elif line.startswith('domain:'):
                domain = line[len('domain:'):].strip()
                domain = domain.replace('.in-addr.arpa', '')
                line = whois_file.readline()
                if line.startswith('descr:'):
                    descr = line[len('descr:'):].strip()
                    segm = re.findall('[0-9.]+/[0-9]+', descr)
                    if segm and len(segm) == 1:
                        segm = segm[0]
                        yield('descr', segm)
                        continue
                yield ('domain', domain)

def network_segment(whois_file):
    """read network segments from whois file

    >>> from StringIO import StringIO
    >>> list(network_segment(StringIO(_sample_whois)))
    ['202.96.63.0/24', '203.93.123.0/24', '221.4.140.0/24', '221.5.250.0/24']
    """
    if isinstance(whois_file, str):
        whois = file(whois_file)
    else:
        whois = whois_file
    for chunk in read_chunk(whois):
        name, segment = chunk
        if name=='descr':
            yield fix_segment(segment)
        elif name=='domain':
            yield reverse_segment(segment)
        elif name=='inetnum':
            ip1, ip2 = segment
            yield max_mask24(get_network(ip1, ip2))
        else:
            yield chunk

def fix_segment(segment):
    """
    >>> fix_segment('221.4.140/24')
    '221.4.140.0/24'
    >>> fix_segment('127/8')
    '127.0.0.0/8'
    """
    list_segm = segment.split('/')[0].split('.')
    if len(list_segm) < 4:
        segment = "%s%s/%s" % (
                segment.split('/')[0],
                '.0' * (4-len(list_segm)),
                segment.split('/')[1],
                )
    return segment

def reverse_segment(inverted_network):
    """
    >>> reverse_segment('250.5.221')
    '221.5.250.0/24'
    >>> reverse_segment('127')
    '127.0.0.0/8'
    """
    segment = inverted_network.split('.')[::-1]
    lr = len(segment)
    segment = '.'.join(segment) + '.0'*(4-lr) + '/' + str(lr*8)
    return segment

def get_network(ip1, ip2):
    """
    >>> get_network('218.106.0.0', '218.106.255.255')
    '218.106.0.0/16'
    >>> get_network('218.106.1.0', '218.106.1.255')
    '218.106.1.0/24'
    >>> get_network('219.158.32.0', '219.158.63.255')
    '219.158.32.0/19'
    >>> get_network('218.106.96.0', '218.106.99.255')
    '218.106.96.0/22'
    >>> get_network('218.106.208.0', '218.106.223.255')
    '218.106.208.0/20'
    >>> get_network('202.96.63.97', '202.96.63.127')
    '202.96.63.96/28'
    """

    ip1 = [int(i) for i in ip1.split('.')]
    ip2 = [int(i) for i in ip2.split('.')]

    def same_bit_length(i1, i2):
        return int(log((i2-i1+1), 2))

    same = 0
    for i1, i2 in zip(ip1, ip2):
        if i1==i2:
            same += 1
        else:
            break

    same_bit = same_bit_length(ip1[same], ip2[same])
    bit_mask_len = 2**same_bit
    mask_len = 8*same+(8-same_bit)

    ip = '.'.join([str(i) for i in ip1[:same]])
    ip += '.' + str(ip1[same]/(bit_mask_len)*(bit_mask_len))
    ip += '.0' * (4-same-1)
    return ip + '/' + str(mask_len)

def max_mask24(segment):
    """
    >>> max_mask24('202.96.63.96/28')
    '202.96.63.0/24'
    """
    network, mask = segment.split('/')
    if int(mask) > 24:
        return '%s.0/24' % '.'.join(network.split('.')[:3])
    else:
        return segment

def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'test':
        test()
        sys.exit()
    whois_filename = sys.argv[1]
    for segm in network_segment(whois_filename):
        print segm
