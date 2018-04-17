---
title: "JSON-LD Implementation Notes"
layout: spec
tags: [annex, presentation-api, image-api]
cssversion: 2
redirect_from:
  - /api/annex/notes/jsonld.html
---

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## Introduction

The IIIF specifications are implemented using JSON-LD, a JSON serialization pattern for RDF.  JSON-LD has the advantage of being, at the same time, both developer readable and tractable, as well as being Linked Data. This allows for easy extensions without fear of term collisions as everything is mapped to a globally unique URI, and to be able to link into other systems as part of the global information graph.  The costs of doing this are minimal, mostly the definition and reference to a context document in each JSON document.

There are, however, some side effects of working with JSON-LD, that implementers should be aware of.  Some of the issues are due to the RDF model, and others are specific to JSON-LD.

## Term Expansion/Compaction Issues

### Unintended Expansion of URI Schemes

The JSON-LD 1.0 term expansion algorithm, as implemented by most JSON-LD libraries, cannot distinguish between a term with a namespace defined in the context and a real URI scheme.  For example, if a context document defined a mapping from `http` to `http://www.tracker.com/`, most JSON-LD libraries will expand `http://iiif.io/` to `http://www.tracker.com///iiif.io/` by simply replacing `http:` in the value.  This issue only occurs if the URI scheme name is defined in the context.

All IIIF APIs are subject to this issue for `service` entries, which conflicts with the [Service URI scheme][service-uri] used [mostly by printers][service-wiki].  The Presentation and Search APIs are also subject to this issue for `resource` entries in Annotations, which conflict with the provisional [Resource URI scheme][resource-uri].  The recommendation for implementers is to not use URIs with these schemes when describing IIIF resources.

This [python code][context-checker] will check for conflicts in a context document.

### Greedy Compaction of Terms

Term compaction in JSON-LD is the process of taking a full URI and a context, and trying to create the appropriate compact form for the serialization.  For example, if the URI is `http://example.com/ns/term`, and the context has a mapping from `eg` to `http://example.com/ns/`, then the URI will be compacted to `eg:term`.  Most JSON-LD libraries use an algorithm that tries to create the shortest term in the JSON serialization, however this has unintended side effects when there are terms which happen to be truncated forms of other terms, as the algorithm cannot distinguish between mappings added for the purposes of creating namespaces and those added for defining the keys of the JSON format.

The IIIF Image API was subject to this issue for the size features until version 2.1 was released.  In particular, there was a definition of `sizes` to `iiif:size`, and the size related features were named according to the pattern: `iiif:sizeByX`, and thus `sizes:ByX` was the shortest legal, if unintended, compaction. For version 2.1, `iiif:size` was renamed to `iiif:hasSize` to avoid this issue.  See also the note on [Semantic Versioning and JSON-LD][int-semver] below.

## Formats and Languages

It is possible to associate a language with a literal in JSON-LD using an object with two keys, `@language` and `@value`, described in the [Presentation API][prezi-language]. It is also possible to describe the format of a literal using `@type`.  However, due to restrictions in RDF 1.1, it is not possible to use both of these features together to have a literal with both format and language declared.

During the design of the Presentation API, it was determined that the correct solution was to be explicit about language as it cannot be determined heuristicly, and provide requirements to make the detection of HTML as easy as possible.  In the future, if RDF provides a method to have both format and language associated with the same literal, these restrictions will be lifted.  Other options were evaluated, including having a resource with `value`, `language` and `format` keys which was determined to be too intrusive compared to what regular JSON would look like, and using HTML with an `xml:lang` attribute and the `rdf:HTML` datatype, however this makes the choice of language much more complex as the values need to be parsed with an HTML parser, rather than using the JSON structure.  As internationalization of the values is a primary use case, the current method was the solution chosen.


## Semantic Versioning

The IIIF editors do not consider the mappings from the JSON to the selected RDF ontology terms to be governed by semantic versioning.  They are provided as a convenience for Linked Data implementers, rather than being a requirement for all adopters of IIIF.  The JSON structure and the names of the keys are governed by semantic versioning, as changing them would break compatibility with the typical JSON based client.

This decision may change in the future, if there are significant Linked Data based clients built around IIIF.  Any such development should be announced on [iiif-discuss][iiif-discuss] so that the community becomes aware of it.

The JSON-LD frames described in the next section are also not considered as governed by semantic versioning, and are provided as a convenience for implementers.

## Frames

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

``` python

from pyld.jsonld import compact, frame
import urllib, json, pprint

manifest = json.load(urllib.urlopen("http://iiif.io/api/presentation/{{ site.presentation_api.stable.major }}.{{ site.presentation_api.stable.minor }}/example/fixtures/1/manifest.json"))
pprint.pprint(
  compact(
    frame(manifest, "http://iiif.io/api/presentation/{{ site.presentation_api.stable.major }}/manifest_frame.json"),
    "http://iiif.io/api/presentation/{{ site.presentation_api.stable.major }}/context.json")
)

```

<br/>

[prezi-api]: {{ site.url }}{{ site.baseurl }}/api/presentation/{{ site.presentation_api.stable.major }}.{{ site.presentation_api.stable.minor }}/
[jsonld-framing]: http://json-ld.org/spec/latest/json-ld-framing/
[pyld]: https://pypi.python.org/pypi/PyLD

[image-api-frame]: {{ site.url }}{{ site.baseurl }}/api/image/{{ site.image_api.stable.major }}/info_frame.json
[manifest-frame]: {{ site.url }}{{ site.baseurl }}/api/presentation/{{ site.presentation_api.stable.major }}/manifest_frame.json
[annolist-frame]: {{ site.url }}{{ site.baseurl }}/api/presentation/{{ site.presentation_api.stable.major }}/annotationList_frame.json
[collection-frame]: {{ site.url }}{{ site.baseurl }}/api/presentation/{{ site.presentation_api.stable.major }}/collection_frame.json
[sequence-frame]: {{ site.url }}{{ site.baseurl }}/api/presentation/{{ site.presentation_api.stable.major }}/sequence_frame.json
[canvas-frame]: {{ site.url }}{{ site.baseurl }}/api/presentation/{{ site.presentation_api.stable.major }}/canvas_frame.json
[anno-frame]: {{ site.url }}{{ site.baseurl }}/api/presentation/{{ site.presentation_api.stable.major }}/annotation_frame.json
[range-frame]: {{ site.url }}{{ site.baseurl }}/api/presentation/{{ site.presentation_api.stable.major }}/range_frame.json

[service-uri]: http://tools.ietf.org/html/rfc2609
[service-wiki]: https://en.wikipedia.org/wiki/Service_Location_Protocol#Adoption
[resource-uri]: http://www.iana.org/assignments/uri-schemes/prov/resource
[context-checker]: {{ site.url }}{{ site.baseurl }}/api/annex/notes/check_context.py
[int-semver]: #semantic-versioning
[prezi-language]: {{ site.url }}{{ site.baseurl }}/api/presentation/{{ site.presentation_api.stable.major }}.{{ site.presentation_api.stable.minor }}/#language-of-property-values
[iiif-discuss]: mailto:iiif-discuss@googlegroups.com

{% include acronyms.md %}
