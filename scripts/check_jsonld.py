
from pyld.jsonld import compact, frame, to_rdf, from_rdf, set_document_loader
import json, urllib, pprint
import os, sys

docCache = {}

def fetch(url):
	fh = urllib.urlopen(url)
	data = fh.read()
	fh.close()
	return data

def load_document_and_cache(url):
    if docCache.has_key(url):
        return docCache[url]

    doc = {
        'contextUrl': None,
        'documentUrl': None,
        'document': ''
    }
    data = fetch(url)
    doc['document'] = data;
    docCache[url] = doc
    return doc

set_document_loader(load_document_and_cache)

def clean_bnode_ids(js):
    new = {}
    for (k,v) in js.items():
        if k in ['@id', 'id'] and v.startswith("_:"):
            continue
        elif type(v) == dict:
            # recurse
            res = clean_bnode_ids(v)
            new[k] = res
        elif type(v) == list:
        	# iterate
        	newl = []
        	for i in v:
        		if type(i) == dict:
        			# recurse
        			newl.append(clean_bnode_ids(i))
        		else:
        			newl.append(i)
        	new[k] = newl	
        else:
            new[k] = v
    return new

def read_js(filepath):
	fh = open(filepath)
	data = fh.read()
	fh.close()
	try:
		jsd = json.loads(data)
	except:
		print "%s is not valid json" % filepath
		sys.exit(1)	
	return jsd

### Presentation

ctxtjs = read_js('source/api/presentation/2/context.json')
prezi_context_uri = "http://iiif.io/api/presentation/2/context.json"
docCache[prezi_context_uri] = {
	'contextUrl': None,
	'documentUrl': None,
	'document': json.dumps(ctxtjs)}

framejs = read_js('source/api/presentation/2/manifest_frame.json')
framejs['@context'] = ctxtjs['@context']

fixturedir = 'source/api/presentation/2.1/example/fixtures'
dirs = os.listdir(fixturedir)

# The extra property is dropped, as it should be
dirs.remove('18')

# Remove 24,25,29,31,36 as embedded @contexts will disappear
# This would be fixed in 3.0 by https://github.com/IIIF/iiif.io/issues/1121
dirs.remove('24')
dirs.remove('25')
dirs.remove('29')
dirs.remove('31')
dirs.remove('36')
dirs.remove('38')
dirs.remove('41')

# Remove 32, as duplicate resource is not described twice in compacted output.
# XXX Fix this in the manifest to use two different resources.
dirs.remove('32')

for d in dirs:
	if not d.isdigit():
		continue
	filepath = os.path.join(fixturedir, d, 'manifest.json')
	manifestjs = read_js(filepath)
	manifestjs['@context'] = ctxtjs['@context']
	# Convert example JSON-LD to RDF
	#rdf = to_rdf(manifestjs, {"format": "application/nquads"})
	# Convert back to JSON-LD
	#manifestjs2 = from_rdf(rdf)
	# Frame the JSON-LD
	try:
		framed = frame(manifestjs, framejs)
		# Compact it
		compacted = compact(framed, ctxtjs)
		# Except we want just the URI in the output
		compacted[unicode('@context')] = unicode(prezi_context_uri)
		# Strip bnode ids
		compacted = clean_bnode_ids(compacted)
		# And now should be the same.
		manifestjs[unicode('@context')] = unicode(prezi_context_uri)
		assert(compacted == manifestjs)
	except:
		print "Failed to process %s" % filepath
		raise

# print json.dumps(compacted, indent=2, sort_keys=True)

# Image 



# Search



# Auth



# Annexes


