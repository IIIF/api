#!/usr/bin/env python
# Check JSON examples in IIIF specs, see help string below
# Simeon Warner - 2016-02-25
import json, os, optparse, re, sys

p = optparse.OptionParser(usage='''usage: %prog [options]

Check to JSON examples included in IIIF specifications. Looks for
all *.md files under --basedir and line-parses them looking for code
blocks starting with "``` json" and ending with "```", e.g.:

``` json-doc
{ "JSON": "here" }
```

Removes both comment lines that have \\ as the first non-whitespace
and comments that have end with \\ followed by chars not including a double 
quote. Also removes lines that contain only an ellipsis and whitespace.''')

p.add_option('--basedir', '-b', action='store', default='source',
             help='directory under which to look for *.md files [default %default]')
p.add_option('--verbose','-v', action='store_true',
             help='be vebose, show files examined and bad code blacks (after munging)')
(opts,args) = p.parse_args()
if (len(args)>0):
    p.error("No arguments allowed")

def check_json_in_file(file):
    if (opts.verbose):
        print("%s ..." % (file))
    errors = 0
    in_json = 0 # 0 for not, else line num of start
    json_str = ''
    n = 0
    for line in open(file,'r'):
        n += 1
        if (in_json):
            if (line.startswith('```')):
                # Got all of JSON, check it
                try:
                    jj = json.loads(json_str)
                except Exception as e:
                    print("%s: bad JSON starting at line %d\n==> %s" % (file,in_json,str(e)))
                    if (opts.verbose):
                        print(json_str)
                    errors += 1
                json_str = ''
                in_json = 0
            elif (not re.match(r'''\s*//''',line) and         # start of line comments
                  not re.search(r'''\s//[^"]+$''',line) and   # end of line comments
                  not re.search(r'''^\s+\.\.\.\s*$''',line)): # line with only ellipsis
                # comments are illegal in JSON :-( but be have them in examples
                json_str += re.sub( r'''\[\s+...\s+\]''','[ "dummy" ]', line)
        elif (line.startswith('``` json')):
            in_json = n
    return(errors)
    
errors = 0
for dir, dirs, files in os.walk(opts.basedir):
    for file in files:
        if file.endswith(".md"):
           errors += check_json_in_file(os.path.join(dir,file))
if (errors):
    sys.stderr.write("Found %d bad json examples :-(\n" % errors)
    sys.exit(1)
sys.exit(0)
