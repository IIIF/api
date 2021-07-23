#!/usr/bin/env python
"""Check JSON examples in IIIF specs.

See help string below for description
Simeon Warner - 2016-02-25
"""
import json
import os
import argparse
import re
import sys

p = argparse.ArgumentParser(description='''
Check the JSON examples included in IIIF specifications. Looks for
all *.md files under --basedir and parses them line by line looking for code
blocks starting with "``` json" and ending with "```". Removes both comment
lines that have \\ as the first non-whitespace and comments that have end
with \\ followed by chars not including a double quote. Substitutes valid
dummy JSON for { ... } and [ ... ]. Also removes lines that contain only
an ellipsis and whitespace.''',
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

p.add_argument('--basedir', '-b', action='store', default='source',
               help='directory under which to look for *.md files')
p.add_argument('--verbose', '-v', action='store_true',
               help='be vebose, show files examined and bad code blacks (after munging)')
args = p.parse_args()


def check_json_in_file(file):
    """Check the JSON blocks in file."""
    if args.verbose:
        print("%s ..." % (file))
    errors = 0
    in_json = 0  # 0 for not, else line num of start
    json_str = ''
    n = 0
    for line in open(file, 'r'):
        n += 1
        if (in_json):
            if line.startswith('```'):
                # Got all of JSON, check it
                try:
                    jj = json.loads(json_str)
                except Exception as e:
                    print("%s: bad JSON starting at line %d\n==> %s" % (file, in_json, str(e)))
                    if args.verbose:
                        print(json_str)
                    errors += 1
                json_str = ''
                in_json = 0
            elif (not re.match(r'''\s*//''', line)                  # start of line comments
                  and not re.search(r'''\s//[^"]+$''', line)        # end of line comments
                  and not re.search(r'''^\s+\.\.\.\s*$''', line)):  # line with only ellipsis
                # comments are illegal in JSON :-( but be have them in examples
                # we also have unfilled array and object blocks with an ellipsis, in both
                # cases substitute and valid dummy array
                json_str += re.sub(r'''[\[\{]\s+...\s+[\]\}]''', ' [ ] ', line)
        elif re.match(r'''```\s?json''', line):
            in_json = n
    return(errors)


errors = 0
for dir, dirs, files in os.walk(args.basedir):
    for file in files:
        if file.endswith(".md"):
            errors += check_json_in_file(os.path.join(dir, file))
if (errors):
    sys.stderr.write("Found %d bad json examples :-(\n" % errors)
    sys.exit(1)
sys.exit(0)
