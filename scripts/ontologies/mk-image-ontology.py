#!/home/cheshire/install/bin/python -i

import sys, os, re
import json

from rdflib import Namespace
from rdfsObj import Class, Property, Ontology, ontologies, ontologyNamespaces
from rdfObject import namespaces as NS, types

onto = Ontology(str(NS['iiif']))
onto._owl.versionInfo = "2015-12-13 23:00:00Z"

ontologies['iiif'] = onto
ontologyNamespaces[NS['iiif']] = onto

lst = Class(NS['rdf']['List'])
sc = types['sc']
iiif = types['iiif']
#xsd = types['xsd']
#xint = xsd['integer']
#xstr = xsd['string']

### Classes

image = Class(NS['iiif']['Image'])
image.comment = ""

profile = Class(NS['iiif']['ImageProfile'])
profile.comment = ""

feature = Class(NS['iiif']['Feature'])
feature.comment = ""

size = Class(NS['iiif']['Size'])
size.comment = ""

tile = Class(NS['iiif']['Tile'])

### Properties

scaleFactor = Property(NS['iiif']['scaleFactor'])
scaleFactor.domain = tile
#scaleFactor.range = xint

format = Property(NS['iiif']['format'])
format.domain = profile
#format.range = xstr

quality = Property(NS['iiif']['quality'])
quality.domain = profile
#quality.range = xstr

supports = Property(NS['iiif']['supports'])
supports.domain = profile
supports.range = feature

psize = Property(NS['iiif']['size'])
psize.domain = image
psize.range = size

ptile = Property(NS['iiif']['tile'])
ptile.domain = image
ptile.range = tile

### Instances

features = []
fh = file('image_context.json')
data = fh.read()
fh.close()
img_ctxt = json.loads(data)['@context']
for k in img_ctxt.keys():
	try:
		if img_ctxt[k]['@type'] == "iiif:Feature":
			uri = img_ctxt[k]['@id']
			uri = uri.replace('iiif:', '')
			features.append(uri)
	except:
		pass

for f in features:
	ftr = iiif.Feature(getattr(NS['iiif'], f))
	onto.add_object(ftr)

srlz = onto.serialize('pretty-xml')
print srlz.data
