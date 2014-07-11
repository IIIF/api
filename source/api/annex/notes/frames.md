---
title: "JSON-LD Frames Implementation Notes"
layout: spec
tags: [annex, presentation-api, image-api]
---

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## JSON-LD Frames

JSON-LD Frames are a method of determining the layout of a JSON-LD serialization, in particular which resource should be at the root of the JSON structure and whether information about the resource should be embedded in a particular location or not.  This has practical applications for IIIF specifications, and especially for the [IIIF Presentation API][prezi-api] such as ensuring that the Manifest resource is at the root of the JSON file and that Canvases are serialized as part of the Sequence rather than within a Range, among others.

More information about JSON-LD frames can be found at the [JSON-LD site][jsonld-framing].

## Image API Frame

A minimal frame for the IIIF Image API information response.

* [Image API Frame][image-api-frame]


## Presentation API Frames

Frames for the main resources defined by the IIIF Presentation API.

* [Manifest Frame][manifest-frame]
* [AnnotationList Frame][annolist-frame]
* [Collection Frame][collection-frame]
* [Sequence Frame][sequence-frame]
* [Canvas Frame][canvas-frame]
* [Annotation Frame][anno-frame]
* [Range Frame][range-frame]


## Sample Usage

The following code uses the Python [PyLD implementation][pyld] of JSON-LD to read in example manifest data, parse it and then re-serialize using the manifest frame.

{% highlight python %}

from pyld.jsonld import compact, frame
import urllib, json, pprint

manifest = json.load(urllib.urlopen("http://iiif.io/api/presentation/2/example/manifest1.json"))
pprint.pprint(
  compact(
    frame(manifest, "http://iiif.io/api/presentation/2/manifest_frame.json"), 
    "http://iiif.io/api/presentation/2/context.json")
)

{% endhighlight %}

<br/>

[prezi-api]: /api/presentation/2.0/index.html
[jsonld-framing]: http://json-ld.org/spec/latest/json-ld-framing/
[pyld]: https://pypi.python.org/pypi/PyLD

[image-api-frame]: /api/image/2/info_frame.json
[manifest-frame]: /api/presentation/2/manifest_frame.json
[annolist-frame]: /api/presentation/2/annotationList_frame.json
[collection-frame]: /api/presentation/2/collection_frame.json
[sequence-frame]: /api/presentation/2/sequence_frame.json
[canvas-frame]: /api/presentation/2/canvas_frame.json
[anno-frame]: /api/presentation/2/annotation_frame.json
[range-frame]: /api/presentation/2/range_frame.json



{% include acronyms.md %}
