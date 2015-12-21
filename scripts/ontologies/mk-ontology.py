#!/home/cheshire/install/bin/python -i

import sys, os, re
import commands

from rdflib import Namespace
from rdfsObj import Class, Property, Ontology, ontologies, ontologyNamespaces
from rdfObject import namespaces as NS, types

onto = Ontology(str(NS['sc']))
onto._owl.versionInfo = "2015-12-13 23:00:00Z"

ontologies['sc'] = onto
ontologyNamespaces[NS['sc']] = onto

anno = Class(NS['oa']['Annotation'])
lst = Class(NS['rdf']['List'])

oa = types['oa']
sc = types['sc']

### Classes

coll = Class(NS['sc']['Collection'])
coll.comment = "Collections are used to list the manifests available for viewing, and to describe the structures, hierarchies or collections that the physical objects are part of."

manifest = Class(NS['sc']['Manifest'])
manifest.comment = "The manifest resource represents a single object and any intellectual work or works embodied within that object"

seq = Class(NS['sc']['Sequence'])
seq.comment = "The sequence conveys the ordering of the views of the object."

rng = Class(NS['sc']['Range'])
rng.comment = "Ranges describe additional structure within an object, such as newspaper articles that span pages, the range of non-content-bearing pages at the beginning of a work, or chapters within a book"

cvs = Class(NS['sc']['Canvas'])
cvs.comment = "The canvas represents an individual page or view and acts as a central point for laying out the different content resources that make up the display."

alst = Class(NS['sc']['AnnotationList'])
alst.comment = "AnnotationLists are an ordered list of Annotation objects. Typically all Annnotations in a list target the same Canvas"

layer = Class(NS['sc']['Layer'])
layer.comment = "Layers are lists of AnnotationLists to group them together, for example to create the set of lists that make up a particular translation/edition of a text"

zone = Class(NS['sc']['Zone'])
zone.comment = "Used to group annotations together in an area of a Canvas, for example to model columns, foldouts or palimpsests; Note that Zones are not currently used in the IIIF Presentation API."
zone.subClassOf = cvs

vh = Class(NS['sc']['ViewingHint'])
vd = Class(NS['sc']['ViewingDirection'])

### Properties

#### Structural Properties

hcl = Property(NS['sc']['hasCollections'])
hcl.range = lst
hcl.domain = coll

hm = Property(NS['sc']['hasManifests'])
hm.range = lst
hm.domain = coll

hs = Property(NS['sc']['hasSequences'])
hs.range = lst
hs.domain = manifest

hc = Property(NS['sc']['hasCanvases'])
hc.range = lst

ha = Property(NS['sc']['hasAnnotations'])
ha.range = lst

hia = Property(NS['sc']['hasImageAnnotations'])
hia.subPropertyOf = ha
hia.range = lst

hl = Property(NS['sc']['hasLists'])
hl.range = lst

hr = Property(NS['sc']['hasRanges'])
hr.range = lst

#### Relationships

sr = Property(NS['sc']['hasStartCanvas'])
sr.comment = "A link from a Manifest or Sequence to the Canvas that the rendering agent should initialize their view with."
sr.range = cvs

cl = Property(NS['sc']['hasContentLayer'])
cl.comment = "A link from a Range to a Layer that provides the content resources of that Range"
cl.range = layer
cl.domain = rng

#### Properties

hml = Property(NS['sc']['metadataLabels'])
hml.comment = "An rdf:List of label/value pairs providing descriptive metadata about the resource, intended for human audience"
hml.range = lst

pal = Property(NS['sc']['attributionLabel'])
pal.comment = "A string containing an attribution description that must be displayed when using the resource"

pvd = Property(NS['sc']['viewingDirection'])
pvd.range = vd
pvd.comment = "References the sc:ViewingDirection that defines the direction that the resource should be viewed in"

pvh = Property(NS['sc']['viewingHint'])
pvh.range = vh
pvh.comment = "A hint to a user agent as to how to render the resource"

### Instances

paint = oa.Motivation(NS['sc'].painting)
onto.add_object(paint)

ltr = sc.ViewingDirection(NS['sc'].leftToRightDirection)
ltr.comment = "Left-to-Right Viewing Direction"
onto.add_object(ltr)

rtl = sc.ViewingDirection(NS['sc'].rightToLeftDirection)
rtl.comment = "Right-to-Left Viewing Direction"
onto.add_object(rtl)

ttb = sc.ViewingDirection(NS['sc'].topToBottomDirection)
ttb.comment = "Top-to-Bottom Viewing Direction"
onto.add_object(ttb)

btt = sc.ViewingDirection(NS['sc'].bottomToTopDirection)
btt.comment = "Bottom-to-Top Viewing Direction"
onto.add_object(btt)

paged = sc.ViewingHint(NS['sc'].pagedHint)
paged.comment = "Viewing Hint that object has canvases that represent pages that can be turned"
onto.add_object(paged)

nonpaged = sc.ViewingHint(NS['sc'].nonPagedHint)
nonpaged.comment = "Viewing Hint that the Canvas MUST NOT be presented in a page turner"
onto.add_object(nonpaged)

continuous = sc.ViewingHint(NS['sc'].continuousHint)
continuous.comment = "Each canvas represents a segment of a continuous object such as a long scroll"
onto.add_object(continuous)

indivs = sc.ViewingHint(NS['sc'].individualsHint)
indivs.comment = "Each canvas represents a separate individual object, and should not have transitions"
onto.add_object(indivs)

top = sc.ViewingHint(NS['sc'].topHint)
top.comment = "The topmost range in a nested hierarchy, such as a table of contents"
onto.add_object(top)

facing = sc.ViewingHint(NS['sc'].facingPagesHint)
facing.comment = "Canvases with this hint depict both parts of an opening."
onto.add_object(facing)

mpart = sc.ViewingHint(NS['sc'].multiPartHint)
mpart.comment = "Collections with this hint consist of multiple manifests that each form part of a logical whole."
onto.add_object(mpart)

srlz = onto.serialize('pretty-xml')
print srlz.data
