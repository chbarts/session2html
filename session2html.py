#!/usr/bin/env python3

# Chris Barts 2019

import os
import sys
import time
import json

# https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# https://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string

def remove_prefix(str, prefix):
    if str.startswith(prefix):
        return str[len(prefix):]
    return str

# [SessionManager v2]
# name=Build Your Own Text Editor | Hacker News-2017-04-06
# timestamp=1491538580086
# autosave=false  count=1/104     screensize=1920x1080

def getheader(fp):
    name = ''
    timestamp = ''
    ln = fp.readline().rstrip()
    if ln != '[SessionManager v2]':
        raise Exception('Not a SessionManager v2 file!')
    ln = fp.readline().rstrip()
    if not ln.startswith('name='):
        raise Exception("Can't find name!")
    name = remove_prefix(ln, 'name=')
    ln = fp.readline().rstrip()
    if not ln.startswith('timestamp='):
        raise Exception("Can't find timestamp!")
    timestamp = remove_prefix(ln, 'timestamp=')
    local_time = time.localtime(int(timestamp[0:len(timestamp)-3]))
    fp.readline()
    return (name, local_time)

# Mon Jul 22 14:07:00 MDT 2019

# windows.tabs.entries.title

def write_file(fp, name, ltime, obj):
    fp.write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>' + name + '</title></head>\n')
    fp.write('<body><h1>' + name + ' # ' + time.strftime("%a %b %d %H:%M:%S %Z %Y", ltime) + '</h1>\n')
    fp.write('<ul>\n')
    for window in obj['windows']:
        for tab in window['tabs']:
            fp.write('<li><ol>\n')
            for entry in tab['entries']:
                if entry['title']:
                    fp.write("<li><a href=\"{0}\">{1}</a></li>\n".format(entry['url'], entry['title']))
                else:
                    fp.write("<li><a href=\"{0}\">{1}</a></li>\n".format(entry['url'], entry['url']))
            fp.write('</ol></li>\n')
    fp.write('</ul>\n')
    fp.write('</body></html>\n')

fname = None
name = None
ltime = None
obj = None

if (__name__ == '__main__') and (len(sys.argv) == 1):
    eprint(sys.argv[0] + ': convert a Firefox SessionManager .session file to HTML')
    eprint('Takes a file named foo.bar for any extension .bar and writes it to foo.html in the current directory')
    eprint('Exits if the output file exists')
    sys.exit(0)

with open(sys.argv[1], 'r') as fp:
    fname = os.path.splitext(sys.argv[1])[0] + '.html'
    if os.path.exists(fname):
        eprint(sys.argv[0] + ': ' + fname + ': file exists!')
        sys.exit(1)
    try:    
        (name, ltime) = getheader(fp)
        obj = json.load(fp)
    except Exception as inst:
        eprint(sys.argv[0] + ': An exception occurred on ' + sys.argv[1] + ': ' + inst)
        sys.exit(1)

with open(fname, 'w') as fp:
    write_file(fp, name, ltime, obj)
