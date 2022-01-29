---
title: Registry of Services
layout: spec
tags: [annex, service, services, specifications]
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
  - name: Jon Stroop
    ORCID: https://orcid.org/0000-0002-0367-1243
    institution: Princeton University Library
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

## Abstract
{:.no_toc}
This is one of a number of [IIIF registries][registry]. It lists a set of services that have been identified as useful for implementations, across the APIs.  They may be defined by the IIIF community, or outside of it.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]


## 1. Introduction

This is one of a number of [IIIF registries][registry]. It lists a set of services that have been identified as useful for implementations, across the APIs.  They may be defined by the IIIF community, or outside of it.

### 1.1. Disclaimer

The inclusion of entries in this document that are outside of the IIIF domain _MUST NOT_ be interpreted as endorsement, support, or approval from the editors, the IIIF community or any individual. This annex is provided as a registry to advertise the existence of these extensions and attempt to ensure some consistency between implementations for common but not universal requirements.

### 1.2. Inclusion Process

The process for having a new entry added to this registry is [described here][registry-process].

## 2. Requirements for Inclusion

## 3. Registry

This table summarizes the services available and which APIs they may be used in.  The '![not allowed][icon-na]' icon means that the service is not to be used in the API. The '![recommended][icon-rec]' icon means that the service can be used in the API.

| Service                        | Image API                 | Presentation 2 API        | Presentation 3 API   |
| ------------------------------ |:-------------------------:|:-------------------------:|:-------------------------:|
| [Image Information][image-api] | ![optional][icon-opt]     | ![recommended][icon-rec]  | ![recommended][icon-rec] |
| [GeoJSON][lgeojson]            | ![not allowed][icon3-na]  | ![recommended][icon3-rec] | ![not allowed][icon3-na] |
| [Physical Dimensions][physdim] | ![recommended][icon3-rec] | ![recommended][icon3-rec] | ![recommended][icon3-rec] |
{: .api-table}


### 3.1 Image Information
_Added: 2014-05-20_

The Image Information service allows the [Presentation API][prezi3], and potentially other APIs, to reference content to be displayed via the [Image API][image-api].  The JSON-LD content to be referenced or embedded is the Image Information document, also known as `info.json`.  The service _MUST_ have the `@context`, `@id` and `profile` keys, pointing to the context document, service base URI and compliance level profile respectively.

{% include api/code_header.html %}
``` json-doc
{
  "service": {
    "@context" : "http://iiif.io/api/image/2/context.json",
    "@id" : "http://www.example.org/image-service/abcd1234",
    "profile": "http://iiif.io/api/image/2/level2.json"
  }
}
```

The service _MAY_ have additional information embedded from the Image Information document to avoid the need to retrieve and parse it separately.  In this case, the profile _MAY_ also point to the profile of what functionality is supported, as described in the Image API.

{% include api/code_header.html %}
``` json-doc
{
  "service": {
    "@context" : "http://iiif.io/api/image/2/context.json",
    "@id" : "http://www.example.org/image-service/abcd1234",
    "protocol": "http://iiif.io/api/image",
    "width" : 6000,
    "height" : 4000,
    "sizes" : [
      {"width" : 150, "height" : 100},
      {"width" : 600, "height" : 400},
      {"width" : 3000, "height": 2000}
    ],
    "tiles": [
      {"width" : 512, "scaleFactors" : [1,2,4,8,16]}
    ],
    "profile" : [
      "http://iiif.io/api/image/2/level2.json",
      {
        "formats" : [ "gif", "pdf" ],
        "qualities" : [ "color", "gray" ],
        "supports" : [
            "canonicalLinkHeader", "rotationArbitrary", "http://example.com/feature"
        ]
      }
    ]
  }
}
```

With the `logo` property added to the Image Information description in version 2.1 of the Image API, it is possible and reasonable for one `info.json` response to embed another using this pattern.  In this case, the second service is related to the icon that should be displayed when a client renders the image described by the main response.

{% include api/code_header.html %}
``` json-doc
{
  "@context" : "http://iiif.io/api/image/2/context.json",
  "@id" : "http://www.example.org/image-service/baseImage",
  "protocol" : "http://iiif.io/api/image",

  "attribution" : "Provided by Example Organization",
  "logo" : {
    "@id": "http://example.org/image-service/logo/full/full/0/default.png",
    "service": {
      "@id": "http://example.org/image-service/logo",
      "protocol": "http://iiif.io/api/image",
      "profile": "http://iiif.io/api/image/2/level2.json"
    }
  }
}
```

### 3.2 GeoJSON
{: #geojson}
_Added: 2014-05-20_, _Latest Revision: 2022-02-01_

*Note: GeoJSON as a service is supported in the Presentation 2 API. For the Presentation 3 API, use the [navPlace extension][navPlace].*

[GeoJSON][geojson] provides the ability to associate a geographical place with a resource, in order to drive a map-based user interface or visualization tool.  This might be a location associated with the provenance of the object such as where it was created, or where it is currently held.  The location might also be related to the content of the resource, such as a city mentioned in the text or the landmark depicted in a photograph.  It is not appropriate to use this feature for tagging of time, people, events, and other semantic metadata outside of the scope of the Presentation API.

The [JSON-LD representation][geojson-ld] of GeoJSON, with `@context` `http://geojson.org/geojson-ld/geojson-context.jsonld` _SHOULD_ be used. See the GeoJSON documentation for a full description of the functionality available.

An external reference example for tagging a place, where the URI would return a GeoJSON description of the city of Paris, France:

{% include api/code_header.html %}
``` json-doc
{
  "service": {
    "@context" : "http://geojson.org/geojson-ld/geojson-context.jsonld",
    "@id" : "http://www.example.org/geojson/paris.json"
  }
}
```

Or embedding the content:

{% include api/code_header.html %}
``` json-doc
{
  "service": {
    "@context" : "http://geojson.org/geojson-ld/geojson-context.jsonld",
    "@id" : "http://www.example.org/geojson/paris.json",
    "type": "Feature",
    "properties": {"name": "Paris"},
    "geometry": {
      "type": "Point",
      "coordinates" : [48.8567,2.3508]
    }
  }
}
```
### 3.3 Physical Dimensions
{: #physical-dimensions}
_Added: 2014-05-20_, _Latest Revision: 2015-12-04_

For digitized objects, it is often useful to know the physical dimensions of the object.  When available, they allow a client to present a ruler, or other rendition of physical scale, to the user.  However, implementers are warned that while this information may be available, frequently:

  * It is not available at all.
  * It is unreliable when it is recorded.
  * It is different for every view of an object.
  * When used with the Presentation API, the Canvas might not be sized to depict only the physical object, but might also include a ruler, color bar, the scanning bed or other background objects.  In these cases, the Canvas height and width will not be representative of the main object.

As the Presentation API already includes an aspect ratio for the Canvas, and the Image API includes the height and width of the Image, the physical dimensions service need only report two additional pieces of information: the scale factor to multiply the dimensions by to calculate the physical dimensions, and the units for those generated physical dimensions.  It is _RECOMMENDED_ that the information always be embedded rather than requiring the client to retrieve it with an additional HTTP request, however some implementers _MAY WISH TO_ keep the information separate.

When used with the Image API, it allows a client to calculate the pixels per inch (often abbreviated as PPI or DPI) of the image it is associated with.  When used with the Presentation API, it gives the size of the object that the Canvas is a surrogate for.

The physical dimensions description includes the following properties:

| Property         | Required? | Description |
| ---------------- | --------- | ----------- |
| `@context`       | Required  | The string "http://iiif.io/api/registry/services/physdim/1/context.json". |
| `@id`            | Optional  | A URI that will return the information, perhaps generated dynamically from the image. |
| `profile`        | Required  | The string "http://iiif.io/api/registry/services/physdim". |
| `physicalScale` | Required  | The floating point ratio by which the digital resource's height and width are multiplied in order to determine the depicted scene's height and width.  |
| `physicalUnits` | Required  | The physical units for the generated height and width.  Possible values are: "mm", "cm", in". |
{: .api-table}

The following example demonstrates the resulting structure, as embedded within the [Presentation API][prezi-api] response:

{% include api/code_header.html %}
``` json-doc
{
  "service": {
    "@context": "http://iiif.io/api/registry/services/physdim/1/context.json",
    "profile": "http://iiif.io/api/registry/services/physdim",
    "physicalScale": 0.0025,
    "physicalUnits": "in"
  }
}
```

If the above example was associated with a Canvas of width 4000 and height 6000, then the physical object would be 4000 * 0.0025 = 10 inches wide, and 15 inches high.  If it was associated with an image with width 4000 and height 6000, then it would mean the image was 4000 pixels for 10 inches, or 400 pixels per inch.

__Note:__
There is a proposal to add a confidence label or value to this service to allow clients to either determine if they should use the information, or to display an appropriate warning or description when using it.  This proposal is currently deferred until additional experience and use cases have been explored.  Any interest in this feature should be brought up on [iiif-discuss][iiif-discuss].
{: .note}

## Appendices

### A. Acknowledgements

The production of this document was generously supported by a grant from the [Andrew W. Mellon Foundation][org-mellon].

Thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### B. Change Log

| Date       | Description                                        |
| ---------- | -------------------------------------------------- |
| 2022-02-01 | Migrate Physical Dimensions from Annex             |
| 2022-02-01 | Migrate GeoJSON from Annex                         |
| 2018-XX-YY | New Version 3 Registries                           |


{% include acronyms.md %}
{% include links.md %}
