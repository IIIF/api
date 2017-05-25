import os, sys
from iiif_prezi.factory import ManifestFactory
try:
	from collections import OrderedDict	
except:
	try:
		from ordereddict import OrderedDict
	except:
		print "You must: easy_install ordereddict"
		raise	

try:
	import pyld
except:
	print "WARNING: Not validating JSON-LD as pyld not available"
	pyld = None


BASEURL = "http://iiif.io/api/presentation/2.1/example/fixtures/"
HOMEDIR = "../source/api/presentation/2.1/example/fixtures/"
IMAGE_BASEURL = "http://iiif.io/api/image/2.1/example/reference/"
imageWidth = 1200
imageHeight = 1800

imageUris = [BASEURL + "resources/page1-full.png", BASEURL + "resources/page2-full.png"]
textUris = [BASEURL + "resources/page1.txt", BASEURL + "resources/page2.txt"]
htmlUris = [BASEURL + "resources/page1.html", BASEURL + "resources/page2.html"]
transcriptions = [ 
	["Top of First Page to Display", "Middle of First Page on Angle", "Bottom of First Page to Display"],
	["Top of Second Page to Display", "Middle of Second Page on Angle", "Bottom of Second Page on Angle"]
]

line1Dims = "225,70,750,150"

# Configure the factory
fac = ManifestFactory()
fac.set_base_prezi_uri(BASEURL)
fac.set_base_prezi_dir(HOMEDIR)
fac.set_base_image_uri(IMAGE_BASEURL)
fac.set_iiif_image_info(2.0, 1)
fac.set_debug('error')

testInfo = {

# Done
1 : {"title": "Minimum Required Fields"},
2 : {"title": "Metadata Pairs", 'mfprops': [('metadata',{'date': 'some date'})]},
3 : {"title": "Metadata Pairs with Languages", 'mfprops': [('metadata', {'date': {'en':'some data','fr':'quelquetemps'}})]},
4 : {"title": "Metadata Pairs with Multiple Values in same Language", 'mfprops':[('metadata',{'date': ['some date', 'some other date']})]},
5 : {"title": "Description field", 'mfprops': [('description',"This is a description")]},
6 : {"title": "Multiple Descriptions", 'mfprops': [('description',["This is one description", {"en":"This is another"}])]},
7 : {"title": "Rights Metadata", 'mfprops': [('attribution', "Owning Institution"), ('license','http://creativecommons.org/licenses/by-nc/3.0/')]},
8 : {"title": "SeeAlso link / Manifest", 'mfprops':[('seeAlso','http://www.example.org/link/to/metadata')]},
9 : {"title": "Service link / Manifest", 'mfprops':[('service','http://www.example.org/link/to/searchService')]},
10 : {"title": "Service link as Object"},
11 : {"title": "ViewingDirection: l-t-r", 'ncanvas':2, 'mfprops':[('viewingDirection', 'left-to-right')]},
12 : {"title": "ViewingDirection: r-t-l", 'ncanvas':2, 'mfprops':[('viewingDirection', 'right-to-left')]},
13 : {"title": "ViewingDirection: t-t-b", 'ncanvas':2, 'mfprops':[('viewingDirection', 'top-to-bottom')]},
14 : {"title": "ViewingDirection: b-t-t", 'ncanvas':2, 'mfprops':[('viewingDirection', 'bottom-to-top')]},
15 : {"title": "ViewingHint: paged", 'ncanvas':2, 'mfprops':[('viewingHint','paged')]},
16 : {"title": "ViewingHint: continuous", 'ncanvas':2, 'mfprops':[('viewingHint','continuous')]},
17 : {"title": "ViewingHint: individuals", 'ncanvas':2, 'mfprops':[('viewingHint','individuals')]},
18 : {"title": "Non Standard Keys", 'mfprops':[('someProperty','someValue')]},
19 : {"title": "Multiple Canvases", 'ncanvas':2},
20 : {"title": "Multiple Sequences", 'nseqs':2},
21 : {"title": "Sequence with Metadata", 'seqprops':[('metadata', {'date':'some date'})]},
22 : {"title": "/Sequence/ with non l-t-r viewingDirection", 'seqprops':[('viewingDirection', 'right-to-left')]},
23 : {"title": "/Sequence/ with non paged viewingHint", 'seqprops':[('viewingHint','individuals')]},
24 : {"title": "Image with IIIF Service", 'iiif':True},
25 : {"title": "Image with IIIF Service, embedded info", 'iiif':True},
26 : {"title": "Image different size to Canvas", 'cvsprops': [('height', 900), ('width', 600)]},
27 : {"title": "No Image"},
28 : {"title": "Choice of Image"},
29 : {"title": "Choice of Image with IIIF Service", 'iiif':True},
30 : {"title": "Main + Detail Image"},
31 : {"title": "Detail with IIIF Service", 'iiif':True},
32 : {"title": "Multiple Detail Images"},
33 : {"title": "Detail Image with Choice"},
34 : {"title": "Detail Image with Choice, and 'no image' as option"},
35 : {"title": "Partial Image as Main Image"},
36 : {"title": "Partial Image as Main Image with IIIF Service", 'iiif':True},
37 : {"title": "Partial Image as Detail Image"},
38 : {"title": "Partial Image as Detail Image with IIIF Service", 'iiif':True},
39 : {"title": "Image with CSS Rotation"},
40 : {"title": "Multiple Languages for Metadata Labels", 'mfprops': [('metadata', {'label': {'fr':'date', 'en':'date'}, 'value': "2000"})]},
41 : {"title": "Main Image with Server side Rotation", 'iiif':True},
43 : {"title": "Embedded Transcription on Canvas", 'annoBody': fac.text('\n'.join(transcriptions[0]))},
44 : {"title": "Embedded Transcription on Fragment Segment", 'annoBody': fac.text(transcriptions[0][0]), 'annoTarget+': '#xywh='+line1Dims},
45 : {"title": "External text/plain Transcription on Canvas", 'annoBody': fac.text(ident=textUris[0])},
46 : {"title": "External text/plain Transcription on Segment", 'annoBody': fac.text(ident=BASEURL+"resources/line1.txt"), 'annoTarget+':'#xywh='+line1Dims},
47 : {"title": "Embedded HTML Transcription on Canvas", 'annoBody': fac.text('<span>' + "<br/>".join(transcriptions[0]) + '</span>', format='text/html')},
48 : {"title": "Embedded HTML Transcription on Segment", 'annoBody': fac.text("<b>"+transcriptions[0][0]+"</b>", format='text/html'), 'annoTarget+':'#xywh='+line1Dims},
51 : {"title": "Embedded Comment on a Canvas", 'annoBody': fac.text("Comment"), 'annoMotivation': 'oa:commenting'},
52 : {"title": "Embedded Comment on a Segment", 'annoBody': fac.text("Comment"), 'annoMotivation': 'oa:commenting', 'annoTarget+': "#xywh=100,100,200,200"},
54 : {"title": "Comment in HTML", 'annoBody': fac.text("<b>Comment</b>", format='text/html'), 'annoMotivation': 'oa:commenting'},
61 : {"title": "Embedded Transcription on Selector Segment", 'annoBody': fac.text(transcriptions[0][0])},
62 : {"title": "Label in Multiple Languages", 'mfprops': [('label', {'en':'62: some title','fr':'62: quelque titre'})]},
63 : {"title": "Description in Multiple Languages", 'mfprops': [('description', {'en':'description here','fr':'on le decrit ici'})]},
64 : {"title": "Description in HTML", 'mfprops':[('description', {'en html': '<span>Some HTML</span>'})]},
65 : {"title": "Sequence with startCanvas", 'seqprops':[('startCanvas', "http://iiif.io/api/presentation/2.0/example/fixtures/canvas/65/c1.json")]},

}


# To Do

todo = {
40 : {"title": "Partial Image with CSS Rotation"},
42 : {"title": "Non Rectangular Partial Image"},
49 : {"title": "XML with XPointer Transcription on Segment"},
50 : {"title": "Non Rectangular Transcription Segment"},
53 : {"title": "Embedded Comment on a Non-Rectangular Segment", 'annoBody': fac.text("Comment"), 'annoMotivation': 'oa:commenting'},

# Following need new resources
55 : {"title": "Audio Transcription on Segment"},
56 : {"title": "Video Transcription on Segment"},
57 : {"title": "Multiple Texts in Named Layers"},
58 : {"title": "Basic ToC via Ranges"},
59 : {"title": "Overlapping/Hierarchical Ranges"},
60 : {"title": "Range with Partial Canvas"}
}


def removeExtraLabels(manifest):
	for s in manifest.sequences:
		s.label = ""

def addEmbedInfo(manifest):
	for s in manifest.sequences:
		for c in s.canvases:
			for a in c.images:
				svc = a.resource.service
				svc.height = imageHeight
				svc.width = imageWidth
				svc.tiles = [{"width":512,"scaleFactors":[1,2,4,8,16]}]
				profile = OrderedDict([("formats", ["gif", "tif", "pdf"]), 
					("qualities", ["color", "gray"]), 
					("supports", ["canonicalLinkHeader", "mirroring", "rotationArbitrary", "sizeAboveFull"])])
				svc.profile = ["http://iiif.io/api/image/2/level2.json", profile]

def removeImages(manifest):
	for s in manifest.sequences:
		for c in s.canvases:
			c.images = []

def addTxnSegment(manifest):
	for s in manifest.sequences:
		for c in s.canvases:
			l = c.other_content[0]
			a = l.resources[0]
			a.on = c.make_selection("xywh="+line1Dims, summarize=True)

def makeImageChoice(manifest):
	# Make choice of image for the canvas
	for s in manifest.sequences:
		for c in s.canvases:
			for a in c.images:
				color = a.resource;
				color.label = "Color"
				grey = fac.image(ident=IMAGE_BASEURL+"page1-full/full/full/0/gray.jpg", label="Greyscale")
				grey.set_hw(imageHeight, imageWidth)
				a.choice(color, [grey])

def addDetailImage(manifest):
	for s in manifest.sequences:
		for c in s.canvases:
			# Add a detail image
			a = c.annotation()
			img = a.image(ident=BASEURL + "resources/detail.jpg", label="Detail Image", iiif=False)
			img.set_hw(173,173)
			a.on += "#xywh=%s,%s,173,173" % (200 * len(c.images), 200 * len(c.images))

def addDetailImageIIIF(manifest):
	for s in manifest.sequences:
		for c in s.canvases:
			# Add a detail image
			a = c.annotation()
			img = a.image(ident="detail", label="Detail Image", iiif=True)
			img.set_hw(173,173)
			a.on += "#xywh=%s,%s,173,173" % (200 * len(c.images), 200 * len(c.images))

def makeDetailChoice(manifest):
	# Make choice of image for the canvas
	for s in manifest.sequences:
		for c in s.canvases:
			for a in c.images[1:]:
				color = a.resource;
				color.label = "Color"
				grey = fac.image(ident=IMAGE_BASEURL+"detail/full/full/0/gray.jpg", label="Greyscale")
				grey.set_hw(173,173)
				a.choice(color, [grey])

def makeNilChoice(manifest):
	for s in manifest.sequences:
		for c in s.canvases:
			for a in c.images[1:]:
				a.resource.item.append("rdf:nil")

def makePartialImage(manifest):
	for s in manifest.sequences:
		for c in s.canvases:
			c.height -= 200
			c.width -= 200
			img = c.images[0].resource
			img.height -= 200
			img.width -= 200
			img.id += "#xywh=100,100,%s,%s" % (img.width, img.height)

def makePartialImageIIIF(manifest):
	for s in manifest.sequences:
		for c in s.canvases:
			c.height -= 200
			c.width -= 200
			img = c.images[0].resource
			region = "100,100,1000,1600"
			try:
				sel = OrderedDict([("@type", "iiif:ImageApiSelector"), ("region", region)])
			except:
				sel = {"@type":"iiif:ImageApiSelector", "region":region}
			sr = img.make_selection(sel)
			sr.id = img.id.replace("/full", "/" + region, 1)
			c.images[0].resource = sr

def makePartialDetail(manifest):
	for s in manifest.sequences:
		for c in s.canvases:
			for a in c.images[1:]:
				img = a.resource
				img.height -= 20
				img.width -= 20
				img.id += "#xywh=10,10,%s,%s" % (img.width, img.height)
				a.on = a.on.replace('173', '153')

def makePartialDetailIIIF(manifest):
	for s in manifest.sequences:
		for c in s.canvases:
			for a in c.images[1:]:
				img = a.resource
				img.height -= 20
				img.width -= 20
				region = "10,10,%s,%s" % (img.width, img.height)
				try:
					sel = OrderedDict([("@type", "iiif:ImageApiSelector"), ("region", region)])
				except:
					sel = {"@type":"iiif:ImageApiSelector", "region":region}
				sr = img.make_selection(sel)
				sr.id = img.id.replace('/full', '/'+region, 1)
				a.resource = sr
				
def addRotation(manifest):
	for s in manifest.sequences:
		for c in s.canvases:
			for a in c.images:
				# add stylesheet that does 180 rotation of image
				a.stylesheet(".rotated {transform: rotate(180deg)}", "rotated")

def addServerRotation(manifest):
	for s in manifest.sequences:
		for c in s.canvases:
			for a in c.images:
				img = a.resource
				rot = "180"

				try:
					sel = OrderedDict([("@type", "iiif:ImageApiSelector"), ("rotation", rot)])
				except:
					sel = {"@type":"iiif:ImageApiSelector", "rotation":rot}
				sr = img.make_selection(sel)
				sr.id = img.id.replace("/0/", "/180/", 1)
				c.images[0].resource = sr

def addServiceObject(manifest):
	svc = manifest.add_service(ident="http://example.org/path/to/service")
	svc.format = "text/html"

# n : list of functions to call on manifest
extraFuncs = {	
1 : [removeExtraLabels],
10 : [addServiceObject],
25 : [addEmbedInfo],
27: [removeImages],
28: [makeImageChoice],
29: [makeImageChoice],  # XXX Demonstrates grey zooming issue!
30: [addDetailImage],
31: [addDetailImageIIIF],
32: [addDetailImage, addDetailImage],
33: [addDetailImage, makeDetailChoice],
34: [addDetailImage, makeDetailChoice, makeNilChoice],
35: [makePartialImage],
36: [makePartialImageIIIF],
37: [addDetailImage, makePartialDetail],
38: [addDetailImageIIIF, makePartialDetailIIIF],
39: [addRotation],
41: [addServerRotation]
}

manifests = {}


coln = fac.collection(label="Collection of Test Cases")

for (idn, info) in testInfo.items():

	print "Building %s" % info['title']
	# Build the Manifest
	mf = coln.manifest(ident="%s/manifest" % idn, label="Test %s Manifest: %s" % (idn, info['title']))
	annolists = []
	if info.has_key('mfprops'):
		for (p,v) in info['mfprops']:
			setattr(mf, p, v)

	for sx in range(info.get('nseqs', 1)):
		if sx > 0:
			seq = mf.sequence(ident="%s/s%s"%(idn, sx), label="Test %s Sequence %s" % (idn, sx+1))
		else:
			seq = mf.sequence(label="Test %s Sequence %s" % (idn, sx+1))
		if info.has_key('seqprops'):
			for (p,v) in info['seqprops']:
				setattr(seq,p,v)

		imageWithIIIF = info.has_key('iiif')
		for cx in range(info.get('ncanvas', 1)):
			cvs = seq.canvas(ident="%s/c%s" % (idn, cx+1), label="Test %s Canvas: %s" % (idn, cx+1))
			cvs.set_hw(imageHeight, imageWidth)
			anno = cvs.annotation()
			imguri = imageUris[cx]

			if imageWithIIIF:
				img = anno.image(ident=imguri[imguri.rfind('/')+1:-4], iiif=True)
			else:
				img = anno.image(ident=imguri, iiif=False)
			img.set_hw(imageHeight, imageWidth)

			if info.has_key('cvsprops'):
				for (p,v) in info['cvsprops']:
					setattr(cvs, p, v)
		
		# Maybe make an annotation list with an annotation...
		if info.has_key('annoBody'):
			annolist = cvs.annotationList(ident="%s/list1" % idn, label="Test %s List 1" % idn)
			anno = annolist.annotation()
			anno.resource = info['annoBody']
			if info.has_key('annoTarget+'):
				anno.on += info['annoTarget+']
			if info.has_key('annoMotivation'):
				anno.motivation = info['annoMotivation']
			annolists.append(annolist)

	for fn in extraFuncs.get(idn, []):
		fn(mf)

	if pyld:
		# This will raise an error on invalid JSON-LD
		rdf = pyld.jsonld.expand(mf.toJSON(top=True))

	for annolist in annolists:
		annolist.toFile(compact=False)

	for sx in range(1, len(mf.sequences)):
		mf.sequences[sx].toFile(compact=False)

	mf.toFile(compact=False)
	manifests[idn] = mf


coln.toFile(compact=False)
