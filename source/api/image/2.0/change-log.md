---
title: "Image API 2.0 Change Log"
title_override: "Changes for IIIF Image API Version 2.0"
id: image-api-20-change-log
layout: spec
tags: [specifications, image-api, change-log]
major: 2
minor: 0
# no patch
pre: final
sitemap: false
redirect_from:
  - /api/image/2.0/change-log.html
---

This document is a companion to the [IIIF Image API Specification, Version 2.0][api]. It describes the significant changes to the API since [Version 1.1][api-11]. The changes are broken into three groups: [Breaking Changes][breaking-changes], i.e. those that are not backwards compatible from either a client or server perspective (or both) and mostly consists of new features; [Other Changes][other-changes], i.e. those that are backwards compatible; and [Deferred Changes][deferred-changes], i.e. those that will be made in a future iteration of the Image API.

In addition to changes in the API, the specification documents have been changed as follows:

  * The ordering of the major sections in the specification document has been adjusted for better flow.
  * The use of [RFC 2119 keywords][rfc-2119] has been made more consistent.
  * Language has been adjusted to make the document less developer-centric.

With the [2.0 Release of the IIIF Image API][api], [Semantic Versioning][semver] is used to enumerate releases. As the API relies on predictable URI patterns in several areas, careful choices have been made about which details of the version will be expressed and where. This is explained in [Appendix B][versioning].

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## Breaking Changes

### Renamed Qualities

Previous versions of the specification used "grey" (not "gray") but "color" (not "colour"). While this does reflect the international nature of IIIF, it is not terribly consistent. From this release `grey` is now `gray`.

There was also confusion among users as to the meaning of `native`. The API does not recognize the notion of a source image, and the label `native` was tied too closely to such an idea. In 2.0 `native` has been replaced with `default`, with the implication that the server should return the image in a default quality. The API does not specify how this decision is made (in the future, for example, authorization may determine the default quality).

### Added `profile` property to Image Information document

This is a response to several requests for the ability to describe the capabilities of a server or a particular image with finer granularity than that of the compliance levels. For example, a server may be completely compliant with level 1, but also support the `!w,h` syntax for specifying the size, which is a level 2 feature. This capability can be exposed using the `supports` property with the `profile` property.

The `qualities` and `formats` properties have been moved into the object referenced in `profile`.

### Added `tiles` property to Image Information document

A `tiles` property was added to the top level of the JSON in the Image Information document response.  The rationale was to promote consistency between information about tiles (regions of an image at different sizes) and the different sizes available (see `sizes` below), to clarify that the `scale_factors` are related to tiles rather than the complete image, and to allow different tile sizes at different scale factors.  The property is a list of JSON objects, with `height`, `width` and `scaleFactors` properties.  This change therefore renames `tile_height` to `height`, `tile_width` to `width`, `scale_factors` to `scaleFactors` (to follow the Presentation API's camelCase) and moves them into the new structure.  The `height` property is now optional, defaulting to the same as `width`.  This makes the default of square tiles easier to record.

### Required <abbr title="Cross-Origin Resource Sharing">CORS</abbr> for level 1 Compliance

One of the core purposes--if not _the_ core purpose--of IIIF is to share images between institutions. This is is impossible without the ability to exchange images and metadata across different HTTP domains. CORS is the standard way to do this.

A few other HTTP features have been enumerated in the [HTTP Features][http-features] section of the [compliance document][compliance-doc].

### Changed URIs for compliance levels

The compliance URIs have been moved into the `http://iiif.io/` domain. They now resolve to JSON-LD documents that enumerate the features that are supported by a server that implements this level of compliance. See [Section 6. Compliance Levels][api-compliance] for detailed explanation.

### Dropped Support for Content Negotiation and Default Image Format

As of this version, a client must specify the format of the image as a file-extension like suffix on the URI (e.g. `.jpg`). There are several reasons for this change:

 * This a typical convention employed by image processing utilities, (cf. [ImageMagick][imagemagick-output], [Pillow][pillow], [Kakadu][kdu-usage], and most others).
 * The formats in which the image is available are explicitly enumerated by the `info.json` document for an image and/or the server compliance level document. A client should never need to guess or let the server decide.
 * The `jpg` format must be supported at all compliance levels and thus applications requiring it can rely upon its availability.
 * Static image files on the web typically have file extensions that indicate the format, and there was never a clear use case for when a client would prefer content negotiation over expressing the format in the URI.

Servers should now return a 400 (Bad Request) if possible, or else a 404 (Not Found) when an image request does not include a format suffix.

### Limited Error Response Code Requirements for Level 0

Servers compliant at level 0 may always return a 404 (Not Found) error for any bad requests. While this is not brought out explicitly in the document, the RFC keyword describing when to return a 400 (Bad Request) response has been reduced to "should".

## Other Changes

### Added Canonical URI Form

There are potentially several ways to request the same image, and two cases arose in which it makes sense to have a canonical form of image request URI:

  * A server compliant at level 0 based on pre-made images on a file system needs to know which URI form to use in order to avoid either failing to support applications or having to generate multiple files for the same image. For example, are the region and size best specified by percent or pixel dimensions or `full`?
  * A more capable server may redirect to the canonical syntax for better cache performance.

The canonical URI for an image may be specified in an HTTP Link Header with the attribute `rel=canonical`. See [Section 4.7 Canonical URI Syntax][canonical-uris] for details.

### Added `protocol` property to Image Information document

The value of this property is always the URI `http://iiif.io/api/image` which purposefully does not reflect the version of the API the server implements or its level of compliance. This will enable clients that can consume other JSON-based image information syntaxes and/or multiple versions of the IIIF Image API to easily identify the image service as a IIIF image server.

The `protocol` property is required at all levels of compliance.

### Drop Rotation from Level 1 Compliance

Rotation in multiples of 90 was previously a level 1 requirement. As this can be--and frequently is--handled in the browser via the HTML 5 `<canvas>` element or CSS instructions, the editors felt this was an unnecessary barrier to level 1 compliance.

### Drop Profile Link Header to Optional

After much discussion, the profile link header for indicating the basic profile of an image resource was dropped to optional.  This was because clients typically cannot intercept link headers on resources without using AJAX, and if you were going to test for the profile by doing a HEAD or GET on an image you could more easily construct the Image Information document's URI and GET everything needed.

### Add mirroring to rotation parameter

The rotation value may now be preceded by an exclamation mark to specify mirroring about the vertical axis before rotation. The motivating use cases are display of negatives, reflection to support a carousel display, and support for reading bleed through text.

### Added `services` property to Image Information document

In order to provide the same extension point as is in the [Presentation API][prezi-api], the `services` property was added to info.json.  The predominant use case is recording pixels per inch, via the same mechanism as providing the size of the physical object in the Presentation API.  The [Services Annex][services] specifies which services can be used with which APIs.

### Added `sizes` property to Image Information document

Servers that do not support arbitrary size parameters for image requests may still wish make multiple sizes of an image available. The sizes that are available may be listed using an array of JSON objects in the `sizes` property of the top level of the Image Information response.  The object has `height` and `width` properties.
Even when a server does support arbitrary resizing, it may be useful to report pre-cached or otherwise recommended sizes of an image.

### Published JSON-LD Context

The [context document][context] for the `info.json` document was not published for version 1.1. It is now available.

### Support JSON-LD Content-Type/Accept header

As transition to JSON-LD (since it is not fully supported by browsers), clients that favor the "application/ld+json" media type in the accept header of their request may receive this as the Content-Type of the response. Also note that it is recommended that the server include the context URI in a Link header of the response if the request was for for "application/json". See [Section 5][info-request] and the documents to which it links for further details.

### Background Color for non-90 degree Rotations

Clarified that clients should request image formats capable of transparent backgrounds when rotation is not a multiple of 90 degrees, and that servers should return transparent backgrounds for such images.  For formats that do not support transparent backgrounds, no requirements are specified.

### Added WebP to Formats

Added Google's [webp][goog-webp] to the list of supported image formats as optional.

## Deferred Changes

### Add Rights Information

A proposal was made to add rights level information from the [Presentation API][prezi-api] to the Image Information response for images to avoid requiring support for both APIs just to give a license or attribution statement for the image.  This change was deferred until the next version of the API to coincide with the introduction of Authentication and Authorization information, and to allow extra time to gather use cases and requirements.

### Add Compression

A recommendation was made to allow compression to be specified in the image URL in order to obtain a compressed representation of the image.  The motivation was bandwidth management, such as for mobile or rural areas where access is limited.  The change was deferred until the next version of the API to allow extra time to gather use cases and requirements, as no consensus was reached as to how this could be accomplished.  No proposal introduced a backwards incompatibility, and hence this feature can be introduced without a new major version.



[api-11]: {{ site.url }}{{ site.baseurl }}/api/image/1.1/ "Image API 1.1"
[api-compliance]: {{ site.url }}{{ site.baseurl }}/api/image/2.0/#compliance-levels "Image API 6. Compliance Levels"
[api]: {{ site.url }}{{ site.baseurl }}/api/image/2.0/ "Image API 2.0"
[breaking-changes]: #breaking-changes "Image API 2.0 Breaking Changes"
[canonical-uris]: {{ site.url }}{{ site.baseurl }}/api/image/2.0/#canonical-uri-syntax "Image API 4.7. Canonical URI Syntax"
[info-request]: {{ site.url }}{{ site.baseurl }}/api/image/2.0/#information-request "Image API Section 5. Information Request"
[compliance-doc]: {{ site.url }}{{ site.baseurl }}/api/image/2.0/compliance/ "Image API 2.0 Compliance Document"
[context]: {{ site.url }}{{ site.baseurl }}/api/image/2/context.json  "Image API 2.0 JSON-LD Context"
[http-features]: {{ site.url }}{{ site.baseurl }}/api/image/2.0/compliance/#http-features "Image API Compliance: HTTP Features"
[imagemagick-output]: http://www.imagemagick.org/script/command-line-processing.php#output "ImageMagick: Command-line Processing: Output Filename"
[kdu-usage]: http://kakadusoftware.com/wp-content/uploads/2014/06/Usage_Examples.txt "Usage Examples for the Demonstration Applications Supplied with Kakadu V7.4"
[pillow]: http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html#image-file-formats "Pillow: Image file formats"
[other-changes]: #other-changes "Image API 2.0 Other Changes"
[rfc-2119]: http://tools.ietf.org/html/rfc2119 "Key words for use in RFCs to Indicate Requirement Levels"
[semver]: http://semver.org/ "Semantic Versioning Specification"
[versioning]: {{ site.url }}{{ site.baseurl }}/api/image/2.0/#b-versioning "Image API Appendix B: Versioning"
[prezi-api]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.0/
[services]: {{ site.url }}{{ site.baseurl }}/api/annex/services/
[goog-webp]: https://developers.google.com/speed/webp/
[deferred-changes]: #deferred-changes "Deferred Changes"

{% include acronyms.md %}
