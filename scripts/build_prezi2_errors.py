import json
import urllib, os
import copy

from factory import ManifestFactory

BASEURL = "http://iiif.io/api/presentation/2.0/example/errors/"
HOMEDIR = "../source/api/presentation/2.0/example/errors/"
IMAGE_BASEURL = "http://iiif.io/api/image/2.0/example/"

# Configure a factory for the fake Manifests
fac = ManifestFactory()
fac.set_base_metadata_uri(BASEURL)
fac.set_base_metadata_dir(HOMEDIR)
fac.set_base_image_uri(IMAGE_BASEURL)
fac.set_iiif_image_info(2.0, 1)
fac.set_debug('error')

coll = fac.collection(label="Collection of Errors")
TEST_ID = 0	

mf = fac.manifest(label="manifest")
s = mf.sequence()
c = s.canvas(ident="c1", label="canvas")
c.set_hw(1,1)
basejs = mf.toJSON(top=True)

anno = c.annotation()
anno.image(ident="http://example.net/image.jpg", iiif=False)
basejs_image = mf.toJSON(top=True)


def make_test(data, name):
	global TEST_ID, BASEURL, HOMEDIR, coll
	name = "%s: %s" % (TEST_ID, name)
	myid = BASEURL + "%s/manifest.json" % TEST_ID
	mf = coll.manifest(ident=myid, label = name)

	try:
		os.mkdir(HOMEDIR+str(TEST_ID))
	except:
		pass
	fn = HOMEDIR + '%s/manifest.json' % TEST_ID
	fh = file(fn, 'w')
	fh.write(data)
	fh.close()

	TEST_ID += 1


def make_tests():

	# Some baseline nonsense
	make_test('asdf', 'Non-JSON')
	make_test('{}', 'Empty JSON')
	make_test('{"@id":"foo"}', 'JSON without @context')
	make_test('{"@context":""}', 'JSON with empty @context')
	make_test('{"@context":"http://example.com/context.json"}', 'JSON with unknown @context')
	n = {"@context":"http://iiif.io/api/presentation/2/context.json"}
	make_test(json.dumps(n, sort_keys=True, indent=2), 'JSON without a @type')
	n['@type'] = "fish"
	make_test(json.dumps(n, sort_keys=True, indent=2), 'JSON with a nonsense @type')	

	# Config as ident defaults to manifest.json but needs a base URI to be set
	#n['@type'] = "sc:Manifest"

	n = copy.deepcopy(basejs)
	del n['@id']
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Manifest without an @id')
	n['@id'] = "fish"
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Manifest with a nonsense @id')

	n = copy.deepcopy(basejs)
	del n['label']
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Manifest without a label')	
	n['label'] = 1.0
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Manifest with a non-string label')	

	n = copy.deepcopy(basejs)
	del	n['sequences']
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Manifest without any Sequences (not present)')
	n['sequences'] = []
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Manifest without any Sequences (empty)')	
	n['sequences'] = [1]
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Manifest with broken Sequence')	
	n['sequences'] = {1:2}
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Manifest with non Sequence')	
	n['sequences'] = [{'@type':'fish'}]
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Manifest with non Sequence in list')		
	n['sequences'] = {'@type':'sc:Sequence'}
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Manifest with Sequence not in list')	
	n['sequences'] = [{'@type':"sc:Sequence"}]
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Manifest with empty Sequence')
	n['sequences'] = [{'@type':"sc:Sequence", 'canvases': []}]
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Manifest with empty Sequence')

	n = copy.deepcopy(basejs)	
	n['sequences'][0]['canvases'] = "asdf"
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Sequence with non Canvas / non list')	
	n['sequences'][0]['canvases'] = ["asdf"]
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Sequence with non Canvas in a list')	

	n = copy.deepcopy(basejs)
	n['sequences'][0]['canvases'] = n['sequences'][0]['canvases'][0]
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Sequence with Canvas not in a list')		

	n = copy.deepcopy(basejs)
	del n['sequences'][0]['canvases'][0]['@id']
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Canvas without id')
	n['sequences'][0]['canvases'][0]['@id'] = 'asdf'
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Canvas without real URI')

	n = copy.deepcopy(basejs)
	del n['sequences'][0]['canvases'][0]['label']
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Canvas without label')
	n['sequences'][0]['canvases'][0]['label'] = 1.0
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Canvas with nonstring label')

	n = copy.deepcopy(basejs)
	del n['sequences'][0]['canvases'][0]['height']
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Canvas without height')
	n['sequences'][0]['canvases'][0]['height'] = "two"
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Canvas with non integer height')	

	n = copy.deepcopy(basejs)
	del n['sequences'][0]['canvases'][0]['width']
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Canvas without width')
	n['sequences'][0]['canvases'][0]['width'] = "two"
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Canvas with non integer width')

	n = copy.deepcopy(basejs)
	n['sequences'][0]['canvases'][0]['images'] = "asdfasdf"	
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Canvas with non list images')	
	n['sequences'][0]['canvases'][0]['images'] = ["asdfasdf"]	
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Canvas with list of non annotations in images')


	n = copy.deepcopy(basejs_image)
	n['sequences'][0]['canvases'][0]['images'] = n['sequences'][0]['canvases'][0]['images'][0]
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Canvas with annotation directly in images')

	n = copy.deepcopy(basejs_image)
	del n['sequences'][0]['canvases'][0]['images'][0]['motivation']
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Annotation without a motivation')

	# This is a difficult error to detect, as it's only wrong in images, not everywhere
	n['sequences'][0]['canvases'][0]['images'][0]['motivation'] = "somethingElse"
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Annotation with a nonsense motivation')

	n = copy.deepcopy(basejs_image)
	del n['sequences'][0]['canvases'][0]['images'][0]['on']
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Annotation without a target/on')
	n['sequences'][0]['canvases'][0]['images'][0]['on'] = 1.0
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Annotation with a nonsense target/on')

	n = copy.deepcopy(basejs_image)
	del n['sequences'][0]['canvases'][0]['images'][0]['resource']
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Annotation without a body/resource')
	n['sequences'][0]['canvases'][0]['images'][0]['resource'] = 1.0
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Annotation with a nonsense body/resource')

	n = copy.deepcopy(basejs_image)
	del n['sequences'][0]['canvases'][0]['images'][0]['resource']['@type']
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Annotation resource without a type')
	n['sequences'][0]['canvases'][0]['images'][0]['resource'] = {'@type' : 'dctypes:Audio', '@id':'http://foo.bar.com/baz'}
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Annotation resource in images that isn\'t an Image')

	n = copy.deepcopy(basejs_image)
	del n['sequences'][0]['canvases'][0]['images'][0]['resource']['@id']
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Image without an id')
	n['sequences'][0]['canvases'][0]['images'][0]['resource']['@id'] = "asdf"	
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Image without a real id')

	n = copy.deepcopy(basejs_image)
	n['sequences'][0]['canvases'][0]['images'][0]['resource']['height'] = "six"
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Image with broken height')	

	n = copy.deepcopy(basejs_image)
	n['sequences'][0]['canvases'][0]['images'][0]['resource']['width'] = "six"
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Image with broken width')
		
	# Bad property values
	n = copy.deepcopy(basejs)	
	n['description'] = {"@value": "<x> <y> <plain text>"}
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Non HTML with < and > in description')		
	n['description'] = {"@language": "en"}
	make_test(json.dumps(n, sort_keys=True, indent=2), 'No Value in description')	
	n['description'] = "<span onmouseover='ownzor()'>Naughty</span>"
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Vulnerable HTML attribute in description')	
	n['description'] = "<span><script>function ownzor() {}</script>Naughty</span>"
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Vulnerable HTML tag in description')
	n['description'] = "<span><!-- &lt;script>function ownzor() {}&lt;/script>-->Naughty</span>"
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Vulnerable HTML comment in description')

	n = copy.deepcopy(basejs)
	n['viewingDirection'] = "upside-down"
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Invalid viewingDirection value')	

	# Bad startCanvas to non-canvas
	n = copy.deepcopy(basejs)
	n['sequences'][0]['startCanvas'] = "http://example.net/not/a/canvas"
	make_test(json.dumps(n, sort_keys=True, indent=2), 'Invalid startCanvas value')


make_tests()		
coll.toFile(compact=False)