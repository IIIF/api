---
title: "IIIF Open Annotation Extensions"
title_override: "IIIF Open Annotation Extensions"
id: index
layout: spec
tags: [specifications, annex]
cssversion: 2
---

## Status of this Document
{:.no_toc}

This document is not subject to [semantic versioning][semver].
Changes will be tracked within the document.

**Editors**

  * **[Michael Appleby](https://orcid.org/0000-0002-1266-298X)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0002-1266-298X), [_Yale University_](http://www.yale.edu/)
  * **[Robert Sanderson](https://orcid.org/0000-0003-4441-6852)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0003-4441-6852), [_Stanford University_](http://www.stanford.edu/)
  * **[Jon Stroop](https://orcid.org/0000-0002-0367-1243)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0002-0367-1243), [_Princeton University Library_](https://library.princeton.edu/)
  * **[Simeon Warner](https://orcid.org/0000-0002-7970-7855)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0002-7970-7855), [_Cornell University_](https://www.cornell.edu/)
  {: .names}

{% include copyright.md %}

## Abstract
{:.no_toc}
This document describes any extensions to the [Open Annotation][openanno] data model required within the IIIF context.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Introduction

As with the detailed use of any general framework within another, there are some extensions necessary to make the best use of the [Open Annotation][openanno] model within the IIIF APIs.  This document covers those extension points.


## 2.  IIIF Image API Selector

Selectors in Open Annotation are used to describe how to retrieve a given part of a resource.  In this case, the resource is the abstract image as identified by the [IIIF Image API][image-api] base URI plus identifier, and the retrieval process involves adding the correct parameters after that base URI.  For example, the top left hand quadrant of an image has the region parameter of `pct:0,0,50,50` which must be put into the requested URI to obtain the appropriate representation.

In order to make this as easy as possible for the situations when a IIIF Image API endpoint exists, we introduce a new Selector class called `iiif:ImageApiSelector`.  It has properties that give the parameter values needed to fill out the URL structure in the request.  If the property is not given, then a default should be used.

One use of this is within the [IIIF Presentation API][prezi-api], when a Canvas is being painted by part of an image, or an image that requires rotation before display.  

| Property | Default   | Description                                           |
| -------- | --------- | ----------------------------------------------------- |
| @context |           | Required.  Must be the value "http://iiif.io/api/openannotation/context.json". This context is separate from other APIs in order to facilitate and promote reuse of the Selector in other contexts.      |
| @type    |           | Required.  Must be the value "iiif:ImageApiSelector". |
| region   | "full"    | The string to put in the region parameter of the URI.  |
| size     | "full"    | The string to put in the size parameter of the URI.    |
| rotation | "0"       | The string to put in the rotation parameter of the URI. Note that this must be a string in order to allow mirroring, for example "!90". |
| quality  | "default" | The string to put in the quality parameter of the URI. |
| format   | "jpg"     | The string to put in the format parameter of the URI.  Note that the '.' character is not part of the format, just the URI syntax.  |
{: .api-table}

For example, the following object describes the parameters needed to rotate the top left hand 10% of the image clockwise by 90 degrees.

{% highlight json %}
{
  "@context" : "http://iiif.io/api/openannotation/context.json",
  "@type" : "iiif:ImageApiSelector",
  "region" : "pct:0,0,10,10",
  "rotation" : "90"
}
{% endhighlight %}

It can be used in the Presentation API as demonstrated in the section on [Rotation][prezi-rot].


## Appendices

### A. Acknowledgements

The production of this document was generously supported by a grant from the [Andrew W. Mellon Foundation][mellon].

Thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### B. Change Log

| Date       | Description                                        |
| ---------- | -------------------------------------------------- |
| 2014-07-01 | Version 1.0 RFC                                    |


   [semver]: /api/annex/notes/semver/ "Versioning of APIs"
   [iiif-discuss]: mailto:iiif-discuss@googlegroups.com "Email Discussion List"
   [json-ld]: http://www.w3.org/TR/json-ld/ "JSON-LD"
   [iiif-community]: /community/ "IIIF Community"
   [mellon]: http://www.mellon.org/ "The Andrew W. Mellon Foundation"
   [image-api]: /api/image/{{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }}/ "Image API"
   [prezi-api]: /api/presentation/{{ site.presentation_api.latest.major }}.{{ site.presentation_api.latest.minor }}/ "Presentation API"
   [openanno]: http://www.openannotation.org/spec/core/ "Open Annotation"
   [prezi-rot]: /api/presentation/2.0/#rotation "Rotation in Presentation API"
