import re
import os

for f in os.listdir('.'):
    fname, fext = os.path.splitext(f)
    if fext != '.rst':
        continue
    newlines = []
    with open(f, 'r') as fi:
        for l in fi:
            if re.search('(\:show\-inheritance\:)', l):
                continue
            if re.search('(\:undoc\-members\:)', l):
                continue
            newlines.append(l)
    with open(f, 'w') as fo:
        for l in newlines:
            fo.write(l)
