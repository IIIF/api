---
title: "Presentation API 2.1 Change Log"
title_override: "Changes for IIIF Presentation API Version 2.1"
id: presentation-api-21-change-log
layout: spec
tags: [specifications, presentation-api, change-log]
major: 2
minor: 1
# no patch
pre: final
redirect_from:
  - /api/presentation/2.1/change-log.html
---

This document is a companion to the [IIIF Presentation API Specification, Version 2.1][prezi-api]. It describes the significant changes to the API since [Version 2.0][prezi-api-20] as well as editorial changes. The changes are all backwards compatible. A third section, [Deferred Proposals][deferred-proposals], lists proposals that have been discussed but did not make it into this version of the specification.


## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## 1. Non-Breaking Changes

### 1.1. Specify language selection algorithm

It was unclear what a client was required to do when it encountered multiple values associated with a single property, when some values had a language associated with them and some did not. This is particularly problematic for `label` and `attribution` as the client is required to render them. The Presentation API now specifies an [algorithm][langs] for how to handle this. See issues [#759](https://github.com/IIIF/iiif.io/issues/759), [#777](https://github.com/IIIF/iiif.io/issues/777)

### 1.2. Specify property cardinalities

It was unclear as to which properties could be repeated, under which circumstances. The property [descriptions and definitions][properties] now specify for each resource type the number of times that they must or may appear. See issue [#468](https://github.com/IIIF/iiif.io/issues/468)

### 1.3. Add paging capabilities for Collection and AnnotationList

With the introduction of the [Search API][search], and the creation of very large collections and annotation lists, it became necessary to introduce [paging][paging] of the resource descriptions.  The solution adopted is from the [ActivityStreams][as2] work of the W3C, mapped into the IIIF use cases and context. See issue [#598](https://github.com/IIIF/iiif.io/issues/598)

### 1.4. Allow single ordered list for Collection and Range

There are situations in which it is important to have a single order for Collections and Manifests within a Collection, such as Manifests representing single volume works and Collections with the new "multi-part" viewingHint that represent multi-volume works in the same series.  The same can occur for Canvases and Ranges within a single Canvas.  The previous solution was to create a Collection or Range with a single Manifest or Canvas within it, respectively, however this is inefficient.  The addition of a new [members][members] list allows for the resources to be included in a single order. See issues [#716](https://github.com/IIIF/iiif.io/issues/716), [#697](https://github.com/IIIF/iiif.io/issues/697), [#646](https://github.com/IIIF/iiif.io/issues/646)

### 1.5. Link to alternate representations of Resources

A commonly requested link from resources in the IIIF Presentation API to other web resources was to link to alternate representations, such as a PDF of the object that the manifest describes.  This was enabled by adding the [rendering][rendering] property, on any type of resource in the model. See issue [#458](https://github.com/IIIF/iiif.io/issues/458)

### 1.6. Allow date-based user interfaces for navigation

For newspaper or other date based series, it is a common interface requirement to allow navigation by date, for example in a calendar or timeline.  The [navDate][navdate] property was added to hold a typed date intended for this purpose. See issue [#442](https://github.com/IIIF/iiif.io/issues/442)

### 1.7. Link from Range to Layer that contains the content

Also inspired by digital newspaper requirements, where an article might span multiple non-contiguous pages and have full text supplied by annotations, Ranges, such as those that identify the area of the article in the canvases, may now link to the Layer that contains the annotations representing the article's text.  The [contentLayer][contentlayer] relationship enables this use case.  See issue [#645](https://github.com/IIIF/iiif.io/issues/645)

### 1.8. Annotations of non-Canvas Resources

In order to allow comments on Ranges (such as a comment about a newspaper article), Manifests (such as a comment about the work as a whole) and other resource types, AnnotationLists may be [referenced][comments] from any resource, when the annotations in the list are comments.  This issue was deferred from version 2.0. See issue [#80](https://github.com/IIIF/iiif.io/issues/80)

### 1.9. Hotspot Annotations

The ability to link from spatial areas of Canvases to either other resources within the manifest (such as a "jump to" link) or to external resources (such as a remote description of the content) was requested.  This feature was enabled through the use of the [linking motivation][hotspots] from the [Open Annotation][openanno] specification. See issue [#611](https://github.com/IIIF/iiif.io/issues/611)

### 1.10. Facing Pages Viewing Hint

A ["facing-pages" `viewingHint`][hints] value was added to indicate that a single canvas represents both sides of an open spread.  This is common in older digitization projects, books containing plates, and many contemporary Eastern digitization projects.  Without the addition of the hint, page turning viewer applications would try to "turn" the entire spread, and get out of sequence with left and right pages. See issue [#419](https://github.com/IIIF/iiif.io/issues/419)

### 1.11. Multi-Part Collections Viewing Hint

A ["multi-part" `viewingHint`][hints] value was added to distinguish when a collection contains manifests that are part of a logical whole, such as a multi-volume book set. See issue [#466](https://github.com/IIIF/iiif.io/issues/466)

### 1.12. Usage of "continuous" Viewing Hint

The intended usage of the ["continuous" `viewingHint`][hints] was clarified; technically this is a breaking change, but it was not possible to implement the original specification because the semantics were identical to those of the "individuals" `viewingHint`. See issue [#451](https://github.com/IIIF/iiif.io/issues/451)

### 1.13. Reference Authentication API

The section on [authentication][auth] was rewritten to refer to the [Authentication API specification][auth-spec] which is nearly complete.

### 1.14. Modifications to JSON-LD Context and RDF Ontology

The above changes and several others were made to the JSON-LD Context mapping of keys to RDF predicates, and the RDF ontology was updated in step. See issues [#636](https://github.com/IIIF/iiif.io/issues/636), [#666](https://github.com/IIIF/iiif.io/issues/666)

### 1.15. Identity management

Requirements and recommendations around the use of URIs were added to promote best practices of linking and dereferencing resources. See issues: [#591](https://github.com/IIIF/iiif.io/issues/591), [#439](https://github.com/IIIF/iiif.io/issues/439)


## 2. Significant Editorial Changes


### 2.1. Restructure of the document

The document was thoroughly restructured, including moving the descriptions of the resource types into a single coherent section.  Further changes, including the removal of the annotation patterns to a separate document, are likely in the future.

### 2.2. Edits for clarity

Many of the descriptions or definitions of the resource types and properties were edited for clarity, based on feedback and questions from the IIIF Community.


## 3. Deferred Proposals
{: #deferred-proposals}

### 3.1. Zones

[Zones][zones] continue to be deferred, however it is anticipated that they will be added to cover audio/visual requirements in a future release. See issue [#42](https://github.com/IIIF/iiif.io/issues/42)

### 3.2. Specification Alignment

Several issues have been deferred until the publication of the W3C's technical recommendation based on Open Annotation.  See issues: [#368](https://github.com/IIIF/iiif.io/issues/368), [456](https://github.com/IIIF/iiif.io/issues/456), [#496](https://github.com/IIIF/iiif.io/issues/496), [#590](https://github.com/IIIF/iiif.io/issues/590), [#644](https://github.com/IIIF/iiif.io/issues/644), [#755](https://github.com/IIIF/iiif.io/issues/755)

### 3.3 AnnotationList hints

Until there is more experience with the Search API, several additions for Annotation Lists have also been deferred. See [#758](https://github.com/IIIF/iiif.io/issues/758), [#754](https://github.com/IIIF/iiif.io/issues/754)  


[deferred-proposals]: #deferred-proposals "Presentation API 2.1 Deferred Proposals"
[other-changes]: #other-changes "Presentation API 2.1 Non-Breaking Changes"
[prezi-api]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/ "Presentation API 2.1"
[prezi-api-20]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.0/ "Presentation API 2.0"
[prezi-api-10]: {{ site.url }}{{ site.baseurl }}/api/metadata/1.0/ "Metadata API 1.0"

[langs]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/#language-of-property-values
[properties]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/#resource-properties
[search]: {{ site.url }}{{ site.baseurl }}/api/search/1.0/
[as2]: https://www.w3.org/TR/activitystreams-core/#collections
[paging]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/#paging
[members]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/#range
[rendering]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/#rendering
[navdate]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/#navdate
[contentlayer]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/#contentlayer
[comments]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/#comment-annotations
[hotspots]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/#hotspot-linking
[openanno]: http://openannotation.org/spec/core/core.html#Motivations
[hints]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/#viewinghint
[auth]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/#authentication
[auth-spec]: {{ site.url }}{{ site.baseurl }}/api/auth/
[zones]: {{ site.url }}{{ site.baseurl }}/model/shared-canvas/1.0/#Zone

{% include acronyms.md %}
