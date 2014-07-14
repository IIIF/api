
import os, sys
import commands
import urllib

sys.path.append(os.getcwd())
try:
	import ljson as json
except:
	print "Falling back to regular json"
	import json

try:
	from PIL import Image as pil_image
except:
	try:
		import Image as pil_image
	except:
		pil_image = None


try:
	from lxml import etree
except:
	etree = None

# TODO: New Python image library
# TODO: ImageMagick module
# TODO: VIPS


class ConfigurationError(Exception):
	pass

class MetadataError(Exception):
	pass


MAN_VIEWINGHINTS = ['individuals', 'paged', 'continuous']
CVS_VIEWINGHINTS = ['non-paged', 'start']
RNG_VIEWINGHINTS = ['top', 'individuals', 'paged', 'continuous']
VIEWINGDIRS = ['left-to-right', 'right-to-left', 'top-to-bottom', 'bottom-to-top']
RENAMED_PROPS = {'viewingHint':'viewing_hint', 'viewingDirection':'viewing_direction', 'seeAlso':'see_also'}

BAD_HTML_TAGS = ['script', 'style', 'object', 'form', 'input']
GOOD_HTML_TAGS = ['a', 'b', 'br', 'i', 'img', 'p', 'span']

class ManifestFactory(object):
	metadata_base = ""
	image_base = ""
	metadata_dir = ""
	add_lang = False

	def __init__(self, version="2.0", mdbase="", imgbase="", mddir="", lang="en"):
		""" mdbase: (string) URI to which identities will be appended for metadata
		imgbase: (string) URI to which image identities will be appended for IIIF Image API
		mddir: (string) Directory where metadata files will be written
		lang: (string) Language code to use by default if multiple languages given"""

		if mdbase:
			self.set_base_metadata_uri(mdbase)
		if imgbase:
			self.set_base_image_uri(imgbase)

		if mddir:
			self.set_base_metadata_dir(mddir)

		self.default_lang = lang
		if self.default_lang != "en":
			self.add_lang = True
		else:
			self.add_lang = False

		self.presentation_api_version = version
		if version[0] == "2":
			self.context_uri = "http://iiif.io/api/presentation/2/context.json"
		elif version[0] == "1":
			self.context_uri = "http://www.shared-canvas.org/ns/context.json"
		else:
			raise ConfigurationError("Unknown Presentation API Version: " + version )

		# Default Image API info
		self.default_image_api_version = -1
		self.default_image_api_level = -1
		self.default_image_api_context = ""
		self.default_image_api_profile = ""
		self.default_image_api_uri = ""
		self.default_image_api_dir = ""		

		self.debug_level = "warn"

		# Try to find ImageMagick's identify
		try:
			self.whichid = commands.getoutput('which identify')
		except:
			# No IM or not unix
			self.whichid = ""

	def set_debug(self, typ):
		if typ in ['error', 'warn', 'error_on_warning']:
			self.debug_level = typ
		else:
			raise ConfigurationError("Only levels are 'error', 'warn' and 'error_on_warning'")

	def assert_base_metadata_uri(self):
		if not self.metadata_base:
			raise ConfigurationError("Metadata API Base URI is not set")

	def assert_base_image_uri(self):
		if not self.image_base:
			raise ConfigurationError("IIIF Image API Base URI is not set")

	def set_base_metadata_dir(self, dir):
		if not os.path.exists(dir):
			raise ConfigurationError("Metadata API Base Directory does not exist")
		elif dir[-1] != "/":
			dir += "/"
		self.metadata_dir = dir

	def set_base_metadata_uri(self, uri):
		if not uri:
			raise ValueError("Must provide a URI to set the base URI to")
		elif uri[-1] != "/":
			uri += "/"
		self.metadata_base = uri

	def set_default_label_language(self, lang):
		self.default_lang = lang


	def set_base_image_dir(self, dr):
		if not dr:
			raise ValueError("Must provide a directory name to set the base directory to")			
		self.default_base_image_dir = dr

	def set_base_image_uri(self, uri):
		# No trailing / as that's what the base URI really is
		# Need to add it back all over the place though :(
		if not uri:
			raise ValueError("Must provide a URI to set the base URI to")	
		if uri[-1] == "/":
			uri = uri[:-1]
		self.default_base_image_uri = uri

	def set_iiif_image_info(self, version="2.0", lvl="1"):
		version = str(version)
		lvl = str(lvl)
		if not version in ['1.0', '1.1', '2.0']:
			raise ConfigurationError("Only versions 1.0, 1.1, 2.0 are known")
		if not lvl in ['0','1','2']:
			raise ConfigurationError("Level must be 0, 1 or 2")			
		self.default_image_api_version = version
		self.default_image_api_level = lvl
		if version == "1.0":
			self.default_image_api_profile = "http://library.stanford.edu/iiif/image-api/compliance.html#level" + lvl
			self.default_image_api_context = "http://library.stanford.edu/iiif/image-api/context.json"
		elif version == "1.1":
			self.default_image_api_profile = "http://library.stanford.edu/iiif/image-api/1.1/compliance.html#level" + lvl
			self.default_image_api_context = "http://library.stanford.edu/iiif/image-api/1.1/context.json"
		else:
			self.default_image_api_profile = "http://iiif.io/api/image/2/level%s.json" % lvl		
			self.default_image_api_context = "http://iiif.io/api/image/2/context.json"
	
	def set_iiif_image_conformance(self, version, lvl):
		return self.set_iiif_image_info(version, lvl)

	def collection(self, ident="collection", label="", mdhash={}):
		self.assert_base_metadata_uri()
		return Collection(self, ident, label, mdhash)

	def manifest(self, ident="manifest", label="", mdhash={}):
		self.assert_base_metadata_uri()
		return Manifest(self, ident, label, mdhash)

	def sequence(self,ident="", label="", mdhash={}):
		if ident:
			self.assert_base_metadata_uri()
		return Sequence(self, ident, label, mdhash)

	def canvas(self,ident="", label="", mdhash={}):
		if ident:
			self.assert_base_metadata_uri()
		return Canvas(self, ident, label, mdhash)

	def annotation(self, ident="", label="", mdhash={}):
		if ident:
			self.assert_base_metadata_uri()
		return Annotation(self, ident, label=label)

	def annotationList(self, ident="", label="", mdhash={}):
		if not ident:
			raise MetadataError("AnnotationLists must have a real identity")
		return AnnotationList(self, ident, label, mdhash)

	def image(self, ident, label="", iiif=False):
		if not ident:
			raise MetadataError("Images must have a real identity")			
		return Image(self, ident, label, iiif)

	def choice(self, default, rest):
		return Choice(self, default, rest)

	def text(self, txt="", ident="", language="", format=""):
		if not ident and not txt:
			raise ConfigurationError("Text must have either a URI or embedded text")
		elif txt:
			return Text(self, txt, language, format)
		else:
			return ExternalText(self, ident, language, format)

	def range(self, ident="", label="", mdhash={}):
		return Range(self, ident, label, mdhash)

	def layer(self, ident="", label="", mdhash={}):
		return Layer(self, ident, label, mdhash)


class BaseMetadataObject(object):

	_properties = ['id', 'type', 'label', 'metadata', 'description', 'thumbnail',
		'attribution', 'license', 'logo', 'service', 'see_also', 'within', 'related',
		'viewing_hint', 'viewing_direction']
	_extra_properties = []

	def __init__(self, factory, ident="", label="", mdhash={}, **kw):
		self._factory = factory
		if ident:
			if ident.startswith('http'):
				self.id = ident
			else:
				self.id = factory.metadata_base + self.__class__._uri_segment + ident
				if not self.id.endswith('.json'):
					self.id += '.json'
		else:
			self.id = ""
		self.type = self.__class__._type
		self.label = ""
		if label:
			self.set_label(label)
		self.metadata = []
		if mdhash:
			self.set_metadata(mdhash)

		self.description = ""
		self.thumbnail = ""

		self.attribution = ""
		self.license = ""
		self.logo = ""

		self.service = ""
		self.see_also = ""
		self.within = ""
		self.related = ""

	def __setattr__(self, which, value):
		if RENAMED_PROPS.has_key(which):
			which = RENAMED_PROPS[which]
		if which[0] != "_" and not which in self._properties and not which in self._extra_properties:
			self.maybe_warn("Setting non-standard field '%s' on resource of type '%s'" % (which, self._type))
		if hasattr(self, which) and hasattr(self, 'set_%s' % which):
			fn = getattr(self, 'set_%s' % which)
			return fn(value)
		else:
			object.__setattr__(self, which, value)

	def maybe_warn(self, msg):
		msg = "WARNING: " + msg
		if self._factory.debug_level == "warn":
			print msg
		elif self._factory.debug_level == "error_on_warning":
			raise MetadataError(msg)

	def langhash_to_jsonld(self, lh, html=True):
		# {"fr": "something in french", "en": "something in english", "de html" : "<span>German HTML</span>"}
		# --> [{"@value": "something in french", "@language": "fr"}, ...]
		l = []
		for (k,v) in lh.items():
			if 'html' in k:
				k = k.replace("html", '').strip()
				if not html:
					raise MetadataError("Cannot have HTML in '%s', only plain text" % v)
				# process HTML here
				if v[0] != '<' or v[-1] != '>':
					raise MetadataError("First and last characters of HTML value must be '<' and '>' respectively, in '%r'" % v)
				if etree:
					try:
						dom = etree.XML(v)
					except Exception, e:
						raise MetadataError("Invalid XHTML in '%s':  %s" % (v, e))
					for elm in dom.iter():
						if elm.tag in BAD_HTML_TAGS:
							raise MetadataError("HTML vulnerability '%s' in '%s'" % (elm.tag, v))
						elif elm.tag in [etree.Comment, etree.ProcessingInstruction]:
							raise MetadataError("HTML Comment vulnerability '%s'" % elm)
						elif elm.tag == 'a':
							for x in elm.attrib.keys():
								if x != "href":
									raise MetadataError("Vulnerable attribute '%s' on a tag" % x)
						elif elm.tag == 'img':
							for x in elm.attrib.keys():
								if not x in ['src', 'alt']:
									raise MetadataError("Vulnerable attribute '%s' on img tag" % x)
						else:
							if elm.attrib:
								raise MetadataError("Attributes not allowed on %s tag" % (elm.tag))
							if not elm.tag in GOOD_HTML_TAGS:
								self.maybe_warn("Risky HTML tag '%s' in '%s'" % (elm.tag, v))
						# Cannot keep CDATA sections separate from text when parsing in LXML :(

				h = {"@value":v, "@type":"rdf:XMLLiteral"}
				if k:
					h['@language'] = k
				l.append(h)				
			else:
				l.append({"@value":v, "@language":k})
		return l

	def set_metadata(self, mdhash):
		# In:  {label:value}
		# Set: {"label":label, "value":value}
		# Really add_metadata, as won't overwrite
		
		if type(mdhash) != dict:
			raise ValueError("set_metadata takes a dict()")

		# by reference, not value, so can modify in place without
		# triggering __setattr__  ;)
		md = self.metadata
		for (k,v) in mdhash.items():
			if type(v) in [str, unicode] and self._factory.add_lang:
				v = self.langhash_to_jsonld({self._factory.default_lang : v})
			elif type(v) == dict:
				# "date":{"en:"Circa 1400",fr":"Environ 1400"}
				v = self.langhash_to_jsonld(v)
			md.append({"label":k, "value":v})

	def _set_magic(self, which, value, html=True):
		if type(value) in [str, unicode] and self._factory.add_lang:
			value = self.langhash_to_jsonld({self._factory.default_lang : value}, html)
		elif type(value) == dict:
			# {"en:"Something",fr":"Quelque Chose"}
			value = self.langhash_to_jsonld(value, html)
		object.__setattr__(self, which, value)

	def set_label(self, value):
		return self._set_magic('label', value, False)
	def set_description(self, value):
		return self._set_magic('description', value)
	def set_attribution(self, value):
		return self._set_magic('attribution', value)

	def toJSON(self, top=False):
		d = self.__dict__.copy()
		if d.has_key('id') and d['id']:
			d['@id'] = d['id']
			del d['id']
		d['@type'] = d['type']
		del d['type']
		for (k, v) in d.items():
			if not v or k[0] == "_":
				del d[k]
		for e in self._required:
			if not d.has_key(e):
				raise MetadataError("Resource type '%s' requires '%s' to be set" % (self._type, e))
		debug = self._factory.debug_level
		if debug.find("warn") > -1:
			for e in self._warn:
				if not d.has_key(e):
					msg = "Resource type '%s' should have '%s' set" % (self._type, e)
					self.maybe_warn(msg)
		if top:
			d['@context'] = self._factory.context_uri

		if d.has_key('viewing_hint'):
			if hasattr(self, '_viewing_hints'):
				if not d['viewing_hint'] in self._viewing_hints:
					msg = "'%s' not a known viewing hint for type '%s': %s" % (d['viewing_hint'], self._type, ' '.join(self._viewing_hints))
					self.maybe_warn(msg)
			else:
				msg = "Resource type '%s' does not have any known viewing_hints; '%s' given" % (self._type, d['viewing_hint'])
				self.maybe_warn(msg)
			if self._factory.presentation_api_version[0] == '1':
				d['viewingHint'] = d['viewing_hint']
				del d['viewing_hint']

		if d.has_key('viewing_direction'):
			if hasattr(self, '_viewing_directions'):
				if not d['viewing_direction'] in self._viewing_directions:
					msg = "'%s' not a known viewing hint for type '%s': %s" % (d['viewing_direction'], self._type, ' '.join(self._viewing_directions))
					self.maybe_warn(msg)
			else:
				msg = "Resource type '%s' does not have any known viewing_directions; '%s' given" % (self._type, d['viewing_direction'])
				self.maybe_warn(msg)
			if self._factory.presentation_api_version[0] == '1':
				d['viewingDirection'] = d['viewing_direction']
				del d['viewing_direction']

		if self._factory.presentation_api_version[0] == '1' and d.has_key('see_also'):
			d['seeAlso'] = d['see_also']
			del d['see_also']

		return d

	def toString(self, compact=True):
		js = self.toJSON(top=True)
		if compact:
			return json.dumps(js, sort_keys=True, separators=(',',':'))
		else:
			return json.dumps(js, sort_keys=True, indent=2)

	def toFile(self, compact=True):
		mdd = self._factory.metadata_dir
		if not mdd:
			raise ConfigurationError("Metadata Directory on Factory must be set to write to file")

		js = self.toJSON(top=True)
		# Now calculate file path based on URI of top object
		# ... which is self for those of you following at home
		myid = js['@id']
		mdb = self._factory.metadata_base
		if not myid.startswith(mdb):
			raise ConfigurationError("The @id of that object is not the base URI in the Factory")

		fp = myid[len(mdb):]	
		bits = fp.split('/')
		if len(bits) > 1:
			mydir = os.path.join(mdd, '/'.join(bits[:-1]))		
			try:
				os.makedirs(mydir)
			except OSError, e:
				pass

		fh = file(os.path.join(mdd, fp), 'w')
		if compact:
			json.dump(js, fh, sort_keys=True, separators=(',',':'))
		else:
			json.dump(js, fh, sort_keys=True, indent=2)
		fh.close()

class ContentResource(BaseMetadataObject):

	def make_selection(self, selector, summarize=False):
		if summarize:
			full = {"@id":self.id, "@type": self.type}
			if self.label:
				full['label'] = self.label
		else:
			full = self

		sr = SpecificResource(self._factory, full)
		if type(selector) == str:
			selector = {"@type": "oa:FragmentSelector", "value": selector}
		sr.selector = selector
		return sr

	def make_fragment(self, fragment):
		return self.id + "#" + fragment


class Collection(BaseMetadataObject):
	_type = "sc:Collection"
	_uri_segment = ""
	_required = ["@id", 'label']
	_warn = []
	_extra_properties = ['collections', 'manifests']
	collections = []
	manifests = []

	def __init__(self, *args, **kw):
		super(Collection, self).__init__(*args, **kw)
		self.collections = []
		self.manifests = []

	def add_collection(self, coll):
		self.collections.append(coll)

	def add_manifest(self, manifest):
		self.manifests.append(manifest)

	def collection(self, *args, **kw):
		coll = self._factory.collection(*args, **kw)
		self.add_collection(coll)
		return coll

	def manifest(self, *args, **kw):
		mn = self._factory.manifest(*args, **kw)
		self.add_manifest(mn)
		mn.within = self.id
		return mn

	def toJSON(self, top=True):
		json = super(Collection, self).toJSON(top)
		newcolls = []
		newmans = []
		if json.has_key('collections'):
			# Add in only @id, @type, label
			for c in json['collections']:
				newcolls.append({"@id": c.id, '@type': 'sc:Collection', 'label': c.label})
			json['collections'] = newcolls
		if json.has_key('manifests'):
			# Add in only @id, @type, label
			for c in json['manifests']:
				newmans.append({"@id": c.id, '@type': 'sc:Manifest', 'label': c.label})
			json['manifests'] = newmans
		return json

class Manifest(BaseMetadataObject):
	_type = "sc:Manifest"
	_uri_segment = ""
	_required = ["@id", "label", "sequences"]
	_warn = ["description"]
	_viewing_hints = MAN_VIEWINGHINTS
	_viewing_directions = VIEWINGDIRS
	_extra_properties = ['sequences', 'structures']

	sequences = []
	structures = []

	def __init__(self, *args, **kw):
		super(Manifest, self).__init__(*args, **kw)
		self.sequences = []
		self.structures = []

	def add_sequence(self, seq):
		# verify identity doesn't conflict with existing sequences
		if seq.id:
			for s in self.sequences:
				if s.id == seq.id:
					raise MetadataError("Cannot have two Sequences with the same identity")
		self.sequences.append(seq)

	def add_range(self, rng):
		# verify identity doesn't conflict with existing ranges
		if rng.id:
			for r in self.structures:
				if r.id == rng.id:
					raise MetadataError("Cannot have two Ranges with the same identity")
		self.structures.append(rng)

	def sequence(self, *args, **kw):
		seq = self._factory.sequence(*args, **kw)
		self.add_sequence(seq)
		return seq

	def range(self, *args, **kw):
		rng = self._factory.range(*args, **kw)
		self.add_range(rng)
		return rng

	def toJSON(self, top=True):
		json = super(Manifest, self).toJSON(top)
		newseqs = []

		for s in json['sequences']:			
			if isinstance(s, Sequence):
				newseqs.append(s.toJSON(False))
			elif type(s) == dict and dict['@type'] == 'sc:Sequence':
				newseqs.append(s)
			else:
				raise MetadataError("Non-Sequence in Manifest['sequences']")
		json['sequences'] = newseqs
		if json.has_key('structures'):
			newstructs = []
			for s in json['structures']:
				newstructs.append(s.toJSON(False))
			json['structures'] = newstructs
		return json


class Sequence(BaseMetadataObject):
	_type = "sc:Sequence"
	_uri_segment = "sequence/"
	_required = ["canvases"]
	_warn = ["@id", "label"]
	_viewing_directions = VIEWINGDIRS
	_viewing_hints = MAN_VIEWINGHINTS
	_extra_properties = ['canvases']
	canvases = []

	def __init__(self, *args, **kw):
		super(Sequence, self).__init__(*args, **kw)
		self.canvases = []

	def add_canvas(self, cvs):
		if cvs.id:
			for c in self.canvases:
				if c.id == cvs.id:
					raise MetadataError("Cannot have two Canvases with the same identity")
		self.canvases.append(cvs)

	def canvas(self, *args, **kw):
		cvs = self._factory.canvas(*args, **kw)
		self.add_canvas(cvs)
		return cvs

	def toJSON(self, top=True):
		json = super(Sequence, self).toJSON(top)
		newcvs = []
		for c in json['canvases']:
			if isinstance(c, Canvas):
				newcvs.append(c.toJSON(False))
			elif type(c) == dict and c['@type'] == 'sc:Canvas':
				newcvs.append(c)
			else:
				# break
				raise MetadataError("Non Canvas as part of Sequence")
		json['canvases'] = newcvs
		return json

class Canvas(ContentResource):
	_type = "sc:Canvas"
	_uri_segment = "canvas/"	
	_required = ["@id", "label", "height", "width"]
	_warn = ["images"]
	_viewing_hints = CVS_VIEWINGHINTS
	_extra_properties = ['height', 'width', 'images', 'other_content']
	height = 0
	width = 0
	images = []
	other_content = []

	def __init__(self, *args, **kw):

		super(Canvas, self).__init__(*args, **kw)
		self.images = []
		self.other_content = []
		self.height = 0
		self.width = 0

	def set_hw(self, h,w):
		self.height = h
		self.width = w

	def add_annotation(self, imgAnno):
		self.images.append(imgAnno)
	def add_annotationList(self, annoList):
		self.other_content.append(annoList)

	def annotation(self, *args, **kw):
		anno = self._factory.annotation(*args, **kw)
		anno.on = self.id
		self.add_annotation(anno)
		return anno

	def annotationList(self, *args, **kw):
		annol = self._factory.annotationList(*args, **kw)
		annol._canvas = self
		self.add_annotationList(annol)
		return annol

	def toJSON(self, top=True):
		json = super(Canvas, self).toJSON(top)
		if json.has_key('images'):
			newimgs = []
			for c in json['images']:
				newimgs.append(c.toJSON(False))
			json['images'] = newimgs
		if json.has_key('other_content'):
			newlists = []
			for c in json['other_content']:
				newlists.append(c.toJSON(False))
			json['other_content'] = newlists
		elif json.has_key('otherContent'):
			newlists = []
			for c in json['otherContent']:
				newlists.append(c.toJSON(False))
			json['otherContent'] = newlists
		return json


class Annotation(BaseMetadataObject):
	_type = "oa:Annotation"
	_uri_segment = "annotation/"
	_required = ["motivation", "resource", "on"]
	_warn = ["@id"]
	_extra_properties = ['motivation', 'on', 'resource', 'stylesheet']

	def __init__(self, *args, **kw):
		super(Annotation, self).__init__(*args, **kw)
		self.motivation = "sc:painting"
		self.on = ""
		self.resource = {}

	def image(self, ident="", label="", iiif=False):
		img = self._factory.image(ident, label, iiif)
		self.resource = img
		return img

	def text(self, text, language="", format="text/plain"):
		txt = self._factory.text(text, language, format)
		self.resource = txt
		return txt

	def audio(self, ident="", label=""):
		aud = self._factory.audio(ident, label)
		self.resource = aud
		return aud

	def choice(self, default, rest):
		chc = self._factory.choice(default, rest)
		self.resource = chc
		return chc

	def stylesheet(self, css, cls):
		# This has to go here, as need to modify both Annotation and Resource
		ss = { "@type": ["oa:CssStyle", "cnt:ContentAsText"], "format": "text/css", "chars" : css}
		self.stylesheet = ss
		if not self.resource:
			raise MetadataError("Cannot set a stylesheet without first creating the body")
		if isinstance(self.resource, SpecificResource):
			self.resource.style = cls
		else:
			sr = SpecificResource(self._factory, self.resource)
			sr.style = cls
			self.resource = sr

	def toJSON(self, top=True):
		json = super(Annotation, self).toJSON(top)
		json['resource'] = json['resource'].toJSON(top=False)
		if isinstance(json['on'], BaseMetadataObject):
			json['on'] = json['on'].toJSON(top=False)
		return json


class SpecificResource(BaseMetadataObject):
	_type = "oa:SpecificResource"
	_required = ['full']
	_warn = []
	_extra_properties = ['style', 'selector', 'full']
	style = ""
	selector = ""
	full = None

	def __init__(self, factory, full):
		self._factory = factory
		self.type = self.__class__._type
		self.full=full

	def toJSON(self, top=False):
		json = super(SpecificResource, self).toJSON(top)
		if isinstance(json['full'], BaseMetadataObject):
			json['full'] = json['full'].toJSON()
		return json



class ExternalText(ContentResource):
	_type = "dcterms:Text"
	_required = []
	_factory = None
	_warn = ["format"]
	_uri_segment = "resources"
	_extra_properties = ['format', 'language']
	format = ""
	language = ""

	def __init__(self, factory, ident, language="", format=""):
		self._factory = factory
		self.format = format
		self.language = language
		self.type = self.__class__._type
		if ident.startswith('http'):
			self.id = ident
		else:
			self.id = self.id = factory.metadata_base + self.__class__._uri_segment + ident


class Text(ContentResource):
	_type = "cnt:ContentAsText"
	_required = ["chars"]
	_warn = ["format"]
	_extra_properties = ['format', 'chars', 'language']
	chars = ""
	format = ""
	language = ""

	def __init__(self, factory, text, language="", format="text/plain"):
		self._factory = factory
		self.type = self.__class__._type
		self.chars = text
		self.format = format
		if language:
			self.language = language

class Audio(ContentResource):
	_type = "dctypes:Sound"
	_required = ["@id"]
	_warn = ["format"]
	_uri_segment = "res"
	_extra_properties = ['format']

class Image(ContentResource):
	_type = "dctypes:Image"
	_required = ["@id"]
	_warn = ["format", "height", "width"]
	_extra_properties = ['format', 'height', 'width']

	def __init__(self, factory, ident, label, iiif=False):
		self._factory = factory
		self.type = self.__class__._type
		self.label = ""
		self.format = ""
		self.height = 0
		self.width = 0
		self._identifier = ""
		if label:
			self.set_label(label)

		if iiif:
			# add IIIF service -- iiif is version or bool
			# ident is identifier
			self.service = {
				"@id": factory.default_base_image_uri + '/' + ident,
			}
			if factory.default_image_api_version[0] == '1':
				self.id = factory.default_base_image_uri + '/' + ident + '/full/full/0/native.jpg'				
			else:
				self.id = factory.default_base_image_uri + '/' + ident + '/full/full/0/default.jpg'
				self.service["@context"] = factory.default_image_api_context
			self._identifier = ident
			self.format = "image/jpeg"

			if factory.default_image_api_level != -1:
				self.service['profile'] = factory.default_image_api_profile

		else:
			# Static image
			# ident is either full URL or filename
			if ident.startswith('http://') or ident.startswith('https://'):
				self.id = ident
			else:
				self.id = factory.image_base + ident

	def set_hw(self, h,w):
		self.height = h
		self.width = w

	def set_hw_from_iiif(self):
		if not self._identifier:
			raise ConfigurationError("Image is not configured with IIIF support")

		requrl = self._factory.image_base + self._identifier + '/info.json';
		try:
			fh = urllib.urlopen(requrl)
			data = fh.read()
			fh.close()
		except:
			raise ConfigurationError("Could not get IIIF Info from %s" % requrl)

		try:
			js = json.loads(data)
			self.height = int(js['height'])
			self.width = int(js['width'])
		except:
			print data
			raise ConfigurationError("Response from IIIF server did not have mandatory height/width")


	def set_hw_from_file(self, fn):
		# Try to do it automagically
		if not os.path.exists(fn):
			raise ValueError("Could not find image file: %s" % fn)

		cmd = self._factory.whichid
		if cmd:
			# Try IM
			try:
				info = commands.getoutput(cmd + ' -ping -format "%h %w" ' + fn)
				(h, w) = info.split(" ")
				self.height = int(h)
				self.width = int(w)
				return
			except:
				pass

		if pil_image:
			# Try PIL
			try:
				img = pil_image.open(fn)
				(w,h) = img.size
				self.height = h
				self.width = w
				try:
					img.close()
				except:
					pass
				return
			except:
				pass

		raise ConfigurationError("No identify from ImageMagick and no PIL, you have to set manually")

class Choice(BaseMetadataObject):
	_type = "oa:Choice"
	_uri_segment = "annotation" # not really necessary
	_required = ["item"]
	_warn = ["default"]
	_extra_properties = ['default', 'item']
	default = {}
	item = []

	def __init__(self, factory, default, rest):
		super(Choice, self).__init__(factory, indent="", label="", mdhash={})
		self.default = default
		if type(rest) != list:
			rest = [rest]
		self.item = rest


	def toJSON(self, top=True):
		json = super(Choice, self).toJSON(top)
		json['default'] = json['default'].toJSON(top=False)
		newitem = []
		for c in json['item']:
			if isinstance(c, BaseMetadataObject):
				newitem.append(c.toJSON(False))
			else:
				newitem.append(c)
		json['item'] = newitem		
		return json

class AnnotationList(BaseMetadataObject):
	_type = "sc:AnnotationList"
	_uri_segment = "list/"	
	_required = ["@id"]
	_warn = []
	_canvas = None
	_extra_properties = ["resources"]

	resources = []
	within = {}

	def __init__(self, *args, **kw):
		self.resources = []
		self.within = []
		self._canvas = None
		return super(AnnotationList, self).__init__(*args, **kw)

	def add_annotation(self, imgAnno):
		self.resources.append(imgAnno)

	def annotation(self, *args, **kw):
		anno = self._factory.annotation(*args, **kw)
		if self._canvas:
			anno.on = self._canvas.id
		self.add_annotation(anno)
		return anno

	def layer(self, *args, **kw):
		lyr = self._factory.layer(*args, **kw)
		self.within = lyr
		return lyr


	def toJSON(self, top=True):
		# if top == false, only include @id, @type, label
		# else, include everything
		json = super(AnnotationList, self).toJSON(top)
		if top:
			newl = []
			for c in json['resources']:
				newl.append(c.toJSON(False))
			json['resources'] = newl
		else:
			try:
				del json['resources']
			except:
				# Could be just pointer to service
				pass
		return json

class Range(BaseMetadataObject):
	_type = "sc:Range"
	_uri_segment = "range/"	
	_required = ["@id", "label", "canvases"]
	_warn = []
	_viewing_hints = RNG_VIEWINGHINTS
	_viewing_directions = VIEWINGDIRS
	_extra_properties = ['canvases', 'ranges']

	canvases = []
	ranges = []

	def __init__(self, factory, ident="", label="", mdhash={}):
		super(Range, self).__init__(factory, ident, label, mdhash)
		self.canvases = []	
		self.ranges = []

	def add_canvas(self, cvs, frag=""):
		cvsid = cvs.id
		if frag:
			cvsid += frag
		self.canvases.append(cvsid)

	def range(self, ident="", label="", mdhash={}):
		r = self._factory.range(ident, label, mdhash)
		self.add_range(r)
		return r

	def add_range(self, rng):
		self.ranges.append(rng.id)		


class Layer(BaseMetadataObject):
	_type = "sc:Layer"		
	_uri_segment = "layer/"
	_required = ["@id", "label"]
	_warn = []


if __name__ == "__main__":
	factory = ManifestFactory()	
	factory.set_base_metadata_uri("http://www.example.org/metadata/")

	factory.set_base_image_uri("http://www.example.org/iiif/")
	factory.set_iiif_image_info(version="2.0", lvl="2")

	mf = factory.manifest(label="Manifest")
	mf.viewingHint = "paged"

	seq = mf.sequence() 
	for x in range(2):
		# Mostly identity will come from incrementing number (f1r, f1v,...)
		# or the image's identity

		cvs = seq.canvas(ident="c%s" % x, label="Canvas %s" % x)  
		cvs.set_hw(1000,1000)
		anno = cvs.annotation() 
		# al = cvs.annotationList("foo") 

		img = factory.image("f1r.c", iiif=True)
		img.set_hw_from_file("/Users/azaroth/Box Sync/SharedCanvasData/m804/images/f1r.c.jpg")
		img2 = factory.image("f1r", iiif=True)
		img2.set_hw_from_file("/Users/azaroth/Box Sync/SharedCanvasData/m804/images/f1r.jpg")

		chc = anno.choice(img, [img2])


	print mf.toString(compact=False)
