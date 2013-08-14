#!/bin/env python

#iconv -f CP1250 -t UTF8 $1 | tr ',' ':' > $1.utf8.pydic.txt
import sys

for line in sys.stdin:
    line = line.decode('CP1250').strip().split(',')
    if line:
        if not line[0].startswith(u'nie'):
            line = filter(lambda x: not x.startswith(u'nie'),
                          map(lambda y: y.strip(), line))
        print ','.join(line).encode('utf-8')