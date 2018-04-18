---
title: Registry of Services
layout: spec
tags: [annex, service, services, specifications]
cssversion: 2
---

## Status of this Document
{:.no_toc}

This document is not subject to [semantic versioning][notes-versioning].
Changes will be tracked within the document.

**Editors**

  * **[Michael Appleby](https://orcid.org/0000-0002-1266-298X)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-1266-298X), [_Yale University_](http://www.yale.edu/)
  * **[Tom Crane](https://orcid.org/0000-0003-1881-243X)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0003-1881-243X), [_Digirati_](http://digirati.com/)
  * **[Robert Sanderson](https://orcid.org/0000-0003-4441-6852)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0003-4441-6852), [_J. Paul Getty Trust_](http://www.getty.edu/)
  * **[Jon Stroop](https://orcid.org/0000-0002-0367-1243)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-0367-1243), [_Princeton University Library_](https://library.princeton.edu/)
  * **[Simeon Warner](https://orcid.org/0000-0002-7970-7855)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-7970-7855), [_Cornell University_](https://www.cornell.edu/)
  {: .names}

{% include copyright.md %}

## Abstract
{:.no_toc}
This is one of a number of [IIIF registries][annex-registry]. It lists a set of services that have been identified as useful for implementations, across the APIs.  They may be defined by the IIIF community, or outside of it.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Introduction

This is one of a number of [IIIF registries][annex-registry]. It lists a set of services that have been identified as useful for implementations, across the APIs.  They may be defined by the IIIF community, or outside of it.

### 1.1. Disclaimer

The inclusion of entries in this document that are outside of the IIIF domain _MUST NOT_ be interpreted as endorsement, support, or approval from the editors, the IIIF community or any individual. This annex is provided as a registry to advertise the existence of these extensions and attempt to ensure some consistency between implementations for common but not universal requirements.

### 1.2. Inclusion Process 

The process for having a new entry added to this registry is [described here][registry-process].

## 2. Requirements for Inclusion

## 3. Registry

This table summarizes the services available and which APIs they may be used in.  The '![not allowed][icon-na]' icon means that the service is not to be used in the API. The '![recommended][icon-rec]' icon means that the service can be used in the API.

| Service                        | Image API                 | Presentation API          |
| ------------------------------ |:-------------------------:|:-------------------------:|
| [Image Information][image-api] | ![optional][icon-opt]     | ![recommended][icon-rec] |  
{: .api-table}


### 3.1 Image Information
_Added: 2014-05-20_

The Image Information service allows the [Presentation API][prezi3], and potentially other APIs, to reference content to be displayed via the [Image API][image-api].  The JSON-LD content to be referenced or embedded is the Image Information document, also known as `info.json`.  The service _MUST_ have the `@context`, `@id` and `profile` keys, pointing to the context document, service base URI and compliance level profile respectively.

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

## Appendices

### A. Acknowledgements

The production of this document was generously supported by a grant from the [Andrew W. Mellon Foundation][org-mellon].

Thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### B. Change Log

| Date       | Description                                        |
| ---------- | -------------------------------------------------- |
| 2018-XX-YY | New Version 3 Registries                           |

{% include acronyms.md %}
{% include links.md %}
