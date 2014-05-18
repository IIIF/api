---
title: "Image API 2.0 Changelog"
title_override: "Changes for IIIF Image API Version 2.0"
id: image-api-20-changelog
layout: sub-page
categories: [specifications, image-api, spec-doc, changelog]
major: 2
minor: 0
# no patch
pre: draft
---

**Author:** Jon Stroop

This document is a companion to the [<abbr title="International Image Interoperability Framework">IIIF</abbr> Image API Specification, Version 2.0][api]. It describes the significant changes to the API since [Version 1.1][api-11]. The changes broken into two groups: [Breaking Changes][breaking-changes], i.e. those that are not backwards compatible; and [Other Changes][other-changes] i.e. those that are backwards compatible. The latter group mostly describes new features.

In addition to the changes described above:

  * the ordering of the major sections in specification document has been adjusted for better flow
  * the use of [RFC 2119 keywords][rfc-2119] has been made more consistent
  * language adjustments have been made to make the document less developer-centric.

These changes will not be described further in this document.

With the [2.0 Release of the IIIF Image API][api], the editors will begin using [Semantic Versioning][semver] to enumerate releases. As the API relies on predictable URI patterns in serveral areas, careful choices have been made about which details of the version will be expressed and where. This is explained in [Appendix B][versioning].

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## Breaking Changes

### Added `profile` property to Image Information document

This is a response to several requests for the ability to describe the capabilites of a server or a particular image with finer granularity than that of the compliance levels. For example, a server may be completely compliant with level 1, but also support the `!w,h` syntax for specifying the size, which is a level 2 feature. This capability can be exposed using the `supports` property with the `profile` property.

The `supports` property may be used to describe extension features. See [5.2 Extensions][extensions] for details.

`qualities` and `formats` have been moved into the `profile` attribute as well.

### Added `protocol` property to Image Information document

The value of this property is always the URI `http://iiif.io/api/image` which purposefully does not reflect the version of the API it implements or its level of compliance. This will enable clients that can consume other image information syntaxes in JSON, and/or multiple versions of the IIIF Image API to easily identify the image service as a IIIF image server.

The `protocol` property is required at all levels of compliance.

### Required <abbr title="Cross-Origin Resource Sharing">CORS</abbr> for level 1 Compliance

The one of the core purposes--if not _the_ core purpose-- of IIIF is to share images across domains. This is is impossible

A few other HTTP features have been enumerated in the [HTTP Features][http-features] section of the [compliance document][20-compliance].

### Renamed Qualities

Previously the specification used "grey" (not "gray") but "color" (not "colour"). While this does reflect the international nature if IIIF, it is not terribly consistent. From this release `grey` is now `gray`.

There was also confusion among users as to the meaning of `native`. The API does not recognize the notion of a source image, and the label `native` was tied too closely to such an idea. `native` has been replaced with `default`, with the implication that the server should return the image in a default quality, however this decision is made.

### Changed URIs for compliance levels

__TODO__

### Dropped Support for Content Negotiation and Default Image Format

__TODO__

### Limited Error Response Code Requirements for Level 0

Level-0-compliant servers may always return a 404 (Not Found) error for any bad requests. While this is not brought out expliclty in the document, the RFC keyword describing when to return a 400 (Bad Request) response has been reduced to "should".

## Other Changes

### Added Canonical URI Form

There are potentially several ways to request the same image, and two cases arose in which it makes sense to have a canonical form of image request URI:

  * A level-0-compliant server based on pre-made images on a file system needs to know whether to use percent or pixels and the directory names, specify width only, width and height, etc.
  * A level-2-compliant server may want to server may want to redirect to the canonical syntax for better cache performance.

The canonical URI for an image may be specfied in an HTTP Link Header with the attribute `rel=canonical`. See [Section 4.7 Canonical URI Syntax][canonical-uris] for details.

### Drop Rotation to Level 2 Compliance

Rotation in multiples of 90 was previously a level 1 requirement. As this can be--and frequently is--handled in the browser via the HTML 5 `<canvas>` element, the editors felt this was an unnecessary barrier to level 1 compliance.

### Added `size` property to Image Information document

Servers that do not support arbitrary size parameters for image requests may still wish make multiple sizes of an image available. The sizes that are available may be listed using the `w,h`syntax in the `size` property. Even when a server does support arbitrary resizing, it may be useful to report pre-cached, recommended sizes of an image, e.g. thumbnails.

### Published JSON-LD Context

__TODO__

### Support JSON-LD ContentType/Accept

__TODO__

[20-compliance]: /api/image/2.0/compliance.html "Image API 2.0 Compliance "
[breaking-changes]: #breaking-changes "Image API 2.0 Breaking Changes"
[api]: /api/image/2.0/ "IIIF Image API 2.0"
[api-11]: /api/image/1.1/ "IIIF Image API 1.1"
[canonical-uris]: /api/image/2.0/#canonical-uri-syntax "Image API 4.7 Canonical URI Syntax"
[http-features]: /api/image/2.0/compliance.html#http-features "Image API Compliance: HTTP Features"
[extensions]: /api/image/2.0/#extensions "Image API 4.7 Canonical URI Syntax"
[versioning]: /api/image/2.0/#b-versioning "Image API Appendix B: Versioning"
[other-changes]: #other-changes "Image API 2.0 Other Changes"
[rfc-2119]: http://tools.ietf.org/html/rfc2119 "Key words for use in RFCs to Indicate Requirement Levels"
[semver]: http://semver.org/ "Semantic Versioning Specification"
