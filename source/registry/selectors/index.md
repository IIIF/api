---
title: "Registry of Selectors"
tags: [registry, selectors, specifications]
layout: spec
cssversion: 2
editors:
- name: Michael Appleby
  ORCID: https://orcid.org/0000-0002-1266-298X
  institution: Yale University
- name: Tom Crane
  ORCID: https://orcid.org/0000-0003-1881-243X
  institution: Digirati
- name: Robert Sanderson
  ORCID: https://orcid.org/0000-0003-4441-6852
  institution: J. Paul Getty Trust
- name: Simeon Warner
  ORCID: https://orcid.org/0000-0002-7970-7855
  institution: Cornell University
- name: Dawn Childress
  ORCID: https://orcid.org/0000-0003-2602-2788
  institution: UCLA
- name: Jeff Mixter
  ORCID: https://orcid.org/0000-0002-8411-2952
  institution: OCLC Research
---

## Status of this Document
{:.no_toc}

This document is not subject to [semantic versioning][notes-versioning].
Changes will be tracked within the document.

**Editors:**

{% include api/editors.md editors=page.editors %}

{% include copyright.md %}


## 1. Introduction
{: #introduction}

Selectors in Annotations are used to describe how to retrieve a given part of a resource. They are then associated with an instance of `SpecificResource` that also references the resource of which the Specific Resource is part.

The Selectors described here extend the use of the [Web Annotation][org-w3c-webanno] model within the IIIF APIs, and were previously applied to the predecessor of the Web Annotation model, Open Annotation. These Selectors can be used with either annotation model.

## 2. Selector Classes

### 2.1 IIIF Image API Selector
{: #iiif-image-api-selector}

The [Image API Selector][registry-selectors] is used to describe the operations available via the Image API in order to retrieve a particular image representation. In this case the resource is the abstract image as identified by the [IIIF Image API][image-api] base URI plus identifier, and the retrieval process involves adding the correct parameters after that base URI. For example, the top left hand quadrant of an image has the region parameter of `pct:0,0,50,50` which must be put into the requested URI to obtain the appropriate representation.

In order to make this as easy as possible for the situations when a IIIF Image API endpoint exists, we introduce a new Selector class called `ImageApiSelector`. It has properties that give the parameter values needed to fill out the URL structure in the request. If the property is not given, then a default should be used.

One use of this is within the [IIIF Presentation API][prezi-api], when a Canvas is being painted by part of an image, or an image that requires rotation before display.  

| Property | Default   | Description                                     |
| -------- | --------  |-----------------------------------------------  |
| type     |           | Required. Must be the value `ImageApiSelector`. |
| region   | `full`    | The string to put in the region parameter of the URI. |
| size     | `max`     | The string to put in the size parameter of the URI. |
| rotation | `0`       | The string to put in the rotation parameter of the URI. Note that this must be a string in order to allow mirroring, for example "!90". |
| quality  | `default` | The string to put in the quality parameter of the URI. |
| format   | `jpg`     | The string to put in the format parameter of the URI. Note that the '.' character is not part of the format, just the URI syntax. |
{: .api-table}

For example, to rotate the top left hand 10% of the image clockwise by 90 degrees would use this configuration of the Selector:

{% include api/code_header.html %}
``` json-doc
{
  "type" : "ImageApiSelector",
  "region" : "pct:0,0,10,10",
  "rotation" : "90"
}
```

And would result in this SpecificResource, when applied to an image service at `https://example.org/iiif/image1`:

{% include api/code_header.html %}
``` json-doc
{
  "type": "SpecificResource",
  "source": "https://example.org/iiif/image1",
  "selector": {
    "type": "ImageApiSelector",
    "region": "pct:0,0,10,10",
    "rotation": "90"
  }
}
```

It can be used in the Presentation API as demonstrated in the section on [Rotation (Presentation 2.1)][prezi21-rot]. For more information on using Selectors in IIIF, see the current [Presentation API 3 specification][prezi-api]. 

*Note: The default values in the table above follow the IIIF Image API 3. For default values in previous Image API versions, you will need to consult the corresponding documentation.*

### 2.2 Point Selectors
{: #point-selector}

There are common use cases in which a point, rather than a range or area, is the target of the Annotation. For example, putting a pin in a map should result in an exact point, not a very small rectangle. Points in time are not very short durations, and user interfaces should also treat these differently. This is particularly important when zooming in (either spatially or temporally) beyond the scale of the frame of reference. Even if the point takes up a 10 by 10 pixel square at the user's current resolution, it is not a rectangle bounding an area.

It is not possible to select a point using URI Fragments with the Media Fragment specification, as zero-sized fragments are not allowed. In order to fulfill the use cases, this specification defines a new Selector class called `PointSelector`.  

| Property | Description                                            |
| -------- | -----------------------------------------------------  |
| type     | Required.  Must be the value `PointSelector`.          |
| x        | Optional. An integer giving the x coordinate of the point, relative to the dimensions of the target resource.  |
| y        | Optional. An integer giving the y coordinate of the point, relative to the dimensions of the target resource.    |
| t        | Optional. A floating point number giving the time of the point in seconds, relative to the duration of the target resource. |
{: .api-table}

For example, to select a point in a video that is 10 pixels in from the top left hand corner of the visual content, and 14.5 seconds into the duration:

{% include api/code_header.html %}
``` json-doc
{
  "type": "PointSelector",
  "x": 10,
  "y": 10,
  "t": 14.5
}
```

### 2.3 Content Selectors
{: #content-selectors}

Video content resources consist of both visual and audio content within the same bit-level representation. There are situations when it is useful to refer to only one aspect of the content -- either the visual or the audio, but not both. For example, an Annotation might associate only the visual content of a video that has spoken English in the audio, and an audio file that has the translation of that content in Spanish.

This specification defines two Selectors, `AudioContentSelector` that selects the audio content and a second `VisualContentSelector` for the visual content. Neither selector has any additional properties.

{% include api/code_header.html %}
``` json-doc
{ "type": "AudioContentSelector" }
```

{% include api/code_header.html %}
``` json-doc
{ "type": "VisualContentSelector" }
```

## Appendices

### A. Acknowledgements

The production of this document was generously supported by a grant from the [Andrew W. Mellon Foundation][org-mellon].

Thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### B. Change Log

| Date       | Description                                        |
| ---------- | -------------------------------------------------- |
| 2023-04-27 | Version 1.2 (Change document to Registry of Selectors from Open/Web Annotation Extensions)
| 2018-03-14 | Version 1.1 (Update ImageApi, add Point Selectors) |
| 2014-07-01 | Version 1.0 (RFC)                                  |
{:.api-table}

{% include acronyms.md %}
{% include links.md %}

