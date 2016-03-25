---
title: "Image API 2.1 Change Log"
title_override: "Changes for IIIF Image API Version 2.1"
id: image-api-21-change-log
layout: spec
tags: [specifications, image-api, change-log]
major: 2
minor: 1
# no patch
pre: final
redirect_from:
  - /api/image/2.1/change-log.html
---

This document is a companion to the [IIIF Image API Specification, Version 2.1][api-21]. It describes the significant changes to the API since [Version 2.0][api-20]. The changes are broken into three groups: [Non-breaking Changes][non-breaking-changes], i.e. those that are backwards compatible from client or server perspectives; [Deprecations][deprecations] and [Deferred Changes][deferred-changes], i.e. those that will be made in a future iteration of the Image API.

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## Non-breaking Changes

### Add `square` region

[Issue 425](https://github.com/IIIF/iiif.io/issues/425), [Issue 560](https://github.com/IIIF/iiif.io/issues/560).

### Add Rights, Logo and Attribution Information

[Issue 227](https://github.com/IIIF/iiif.io/issues/227).

### JSON-LD Link Header to Content is not required

[Issue 556](https://github.com/IIIF/iiif.io/issues/556).

This was an error in 2.0. The context link header should only be included if there is not a context AND if content-type is not `application/ld+json`

### Clarified "forced" in Features

[Issue 720](https://github.com/IIIF/iiif.io/issues/720). Additional Discussion on [Pull Request 727](https://github.com/IIIF/iiif.io/pull/727).

`sizeByForcedWh` was inconsistently defined in version 2.0, and `sizeByWhListed` is implied by listing the sizes in the image information document and is therefore not required as a named feature. `sizeByConfinedWh` and `sizeByDistortedWh` were added to clarify the distinction.

### Added `maxArea`, `maxWidth`, `maxHeight`

[Issue 620](https://github.com/IIIF/iiif.io/issues/620).

### Added `max` Size Keyword

[Issue 663](https://github.com/IIIF/iiif.io/issues/663).

See also [`full` size keyword deprecation][full-size-keyword]

## Deprecations

### `full` size keyword

[Issue 678](https://github.com/IIIF/iiif.io/issues/678).

### Canonical Syntax

The 2.1 canonical syntax will change in the next major release due to two issues:

 * [Issue 554](https://github.com/IIIF/iiif.io/issues/544) changes the canonical size syntax to be consistent with the `sizes` array.
 * [Issue 678](https://github.com/IIIF/iiif.io/issues/678) changes `full` to `max` in

### Feature names `sizeByWhListed` and `sizeByForcedWh`

See [Clarified "forced" in Feature Names][clarified-forced-in-feature-names]

## Deferred Changes

### Add Compression

[Issue nnn]().

A recommendation was made to allow compression to be specified in the image URL in order to obtain a compressed representation of the image.  The motivation was bandwidth management, such as for mobile or rural areas where access is limited.  The change was deferred until a future version of the API to allow extra time to gather use cases and requirements, as no consensus was reached as to how this could be accomplished. No proposal introduced a backwards incompatibility, and hence this feature can be introduced without a new major version.

[api-21]: /api/image/2.1/ "Image API 2.1"
[api-compliance]: /api/image/2.0/#compliance-levels "Image API 6. Compliance Levels"
[api-20]: /api/image/2.0/ "Image API 2.0"
[non-breaking-changes]: #non-breaking-changes "Image API 2.0 Non-reaking Changes"
[deferred-changes]: #deferred-changes "Deferred Changes"
[deprecations]: #deprecations "Deprecations"
[clarified-forced-in-feature-names]: #clarified-forced-in-feature-names "Clarified 'forced' in Feature Names"
[full-size-keyword]: #full-size-keyword "`full` Size Keyword Deprecation"

{% include acronyms.md %}
