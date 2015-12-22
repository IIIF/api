
import json
import csv
import urllib
import os, sys, re

schemes = "http://www.iana.org/assignments/uri-schemes/uri-schemes-1.csv"

context = sys.argv[1]

if context.startswith('http'):
	cfh = urllib.urlopen(context)
else:
	cfh = file(context)

data = cfh.read()
cfh.close()
js = json.loads(data)
keys = js['@context']
if type(keys) == list:
	keys = keys[0]

fh = urllib.urlopen(schemes)
rows = csv.reader(fh)
for row in rows:
	scheme = row[0]
	if keys.has_key(scheme):
		print "Collision: %s (expands to %s)" % (scheme, keys[scheme])

fh.close()