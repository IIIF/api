---
title: "Image API 2.1.1 Change Log"
title_override: "Changes for IIIF Image API Version 2.1.1"
id: image-api-211-change-log
layout: spec
tags: [specifications, image-api, change-log]
major: 2
minor: 1
patch: 1
pre: final
redirect_from:
  - /api/image/2.1/change-log-211.html
---

This document is a companion to the [IIIF Image API Specification, Version 2.1.1][image-api]. It describes the editorial changes to the API made in this patch release. The changes are all clarifications, typo corrections or to related documents that are not [semantically versioned][semver] such as inline examples and resources to manage transformation to and from the JSON-LD serialization.

For the significant changes between 2.0 and 2.1, please see the [2.1 Change Log][changelog-21].

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## 1. Editorial Changes

### 1.1. Clarify availability of `width` and `height`

The `width` and `height` properties do not necessarily imply that an image of that size is available. Other constraints may be declared that limit the maximum size that can be requested. The `width` and `height` are still required to construct tile requests and to know the aspect ratio of the image.
See issue [#477](https://github.com/IIIF/iiif.io/issues/477)

### 1.2. Clarify the canonical form of `max`

The size keyword `max` will replace `full` in version 3.0 of the Image API, at which time it can be used in the canonical form of requests. Until then, the canonical form of requests equivalent to `max` must continue to use the `w,` syntax, or the `full` syntax if they are equivalent.
See issue [#883](https://github.com/IIIF/iiif.io/issues/883)

### 1.3. Typo in `@context` for Complete Response example

The URI for the `@context` of the physical dimensions service used in the example Complete Response was incorrect and has been fixed.
See issue [#935](https://github.com/IIIF/iiif.io/issues/935)

### 1.4 Update `@context` for GeoJSON example

The URI of the `@context` for GeoJSON services has changed and the example use from the Image API has been updated. 
See issue [#1001](https://github.com/IIIF/iiif.io/issues/1001)

### 1.5 Use better URIs for example rights/licenses

The URIs were not helpful in giving realistic examples. The examples were updated to use Creative Commons and Rights Statements URIs to promote the use of shared agreements.
See issue [#1094](https://github.com/IIIF/iiif.io/issues/1094)




## 2. Changes to Non-Semantically-Versioned Documents

These changes were scheduled to coincide with the release of 2.1.1 to benefit from a shared deadline, but are not managed in the same way as the main specification documents with respect to versioning.

### 2.1. Annexes

#### 2.1.1 Change in location of `@context` for GeoJSON example

The URI of the `@context` to be used for GeoJSON services has changed and the [Services Annex Document][service-profiles] has been updated. 
See issue [#1001](https://github.com/IIIF/iiif.io/issues/1001)

 
[image-api]: {{ site.url }}{{ site.baseurl }}/api/image/2.1/ "Image API 2.1"
[changelog-21]: {{ site.url }}{{ site.baseurl }}/api/image/2.1/change-log.html "Image API 2.1 Change Log"
[semver]: {{ site.url }}{{ site.baseurl }}/api/annex/notes/semver/ "Note on Semantic Versioning"
[service-profiles]: {{ site.url }}{{ site.baseurl }}/api/annex/services/ "Services Annex Document"


{% include acronyms.md %}
