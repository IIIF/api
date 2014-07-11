
from pyld.jsonld import compact, frame, to_rdf, from_rdf
import json, urllib, pprint

framejs = json.load(urllib.urlopen('http://localhost:4000/api/presentation/2/manifest_frame.json'))
manifestjs = json.load(urllib.urlopen('http://localhost:4000/api/presentation/2.0/example/manifest1.json'))
contextjs = json.load(urllib.urlopen('http://localhost:4000/api/presentation/2/context.json'))
contextURI = "http://iiif.io/api/presentation/2/context.json"

# Convert example JSON-LD to RDF
rdf = to_rdf(manifestjs)
# Convert back to JSON-LD
manifestjs2 = from_rdf(rdf)
# Frame the JSON-LD
framed = frame(manifestjs2, framejs)
# Compact it
compacted = compact(framed, contextjs)

# Except we want just the URI in the output
compacted = compact(framed, contextURI)

# And print it
pprint.pprint(compacted)


