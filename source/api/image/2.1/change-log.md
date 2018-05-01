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

## 1. Non-breaking Changes
{: #non-breaking-changes}

### 1.1. Added `square` Region
{: #added-square-region}

The `square` [region keyword][region] selects a region where the width and height are both equal to the length of the shorter dimension of the complete image. The region may be positioned anywhere in the longer dimension of the image content at the server’s discretion, and centered is often a reasonable default. The corresponding feature name `regionSquare` has also been added to the [profile description][profile-description]. It is an open question whether support for `square` will become mandatory at levels 1 and 2 in the next major version of the Image API. See [issue 425](https://github.com/IIIF/iiif.io/issues/425), [issue 560](https://github.com/IIIF/iiif.io/issues/560), and [issue 501](https://github.com/IIIF/iiif.io/issues/501).

### 1.2. Added Rights and Licensing Properties

[Rights and Licensing Properties][rights] `attribution`, `license` and `logo` properties have been added to the Image Information. They have the same semantics and requirements as the properties of the same names in the Presentation API. See [issue 227](https://github.com/IIIF/iiif.io/issues/227) and note also deferred change of the JSON-LD tag name from `license` to `rights`.

### 1.3. Removed Recommendation to include HTTP Link Header to JSON-LD Context

Version 2.0 incorrectly recommended the inclusion of a HTTP link header for the JSON-LD context, which was unnecessary as the `@context` key in the JSON document would override it. Therefore, the description of the [Image Information Request][image-information-request] no longer includes this. See [issue 556](https://github.com/IIIF/iiif.io/issues/556).

### 1.4. Added `sizeByConfinedWh` and `sizeByDistortedWh` Feature Names
{: #added-sizebyconfinedwh-and-sizebydistortedwh-feature-names}

New feature names `sizeByConfinedWh` and `sizeByDistortedWh` in the [profile description][profile-description] provide clear indications of support for `!w,h` and distorting `w,h` size requests respectively. As a result the related feature names `sizeByWhListed` and `sizeByForcedWh` have been [deprecated][deprecated-sizebywhlisted-and-sizebyforcedwh]. See [issue 720](https://github.com/IIIF/iiif.io/issues/720) and additional discussion on [pull pequest 727](https://github.com/IIIF/iiif.io/pull/727).

### 1.5. Added `maxWidth`, `maxHeight` and `maxArea` Properties

The `maxWidth`, `maxHeight` and `maxArea` properties in the [profile description][profile-description] provide a way for image servers to express the limits on its supported sizes for image requests. See [issue 620](https://github.com/IIIF/iiif.io/issues/620).

### 1.6. Added `max` Size Keyword

The [size keyword][size] `max` may be used to request that the image or region is returned at the maximum size available, as indicated by `maxWidth`, `maxHeight` and `maxArea` properties. See [issue 663](https://github.com/IIIF/iiif.io/issues/663) and the related [deprecation of the size keyword `full`][deprecated-size-full].

## 2. Deprecations
{: #deprecations}

### 2.1. Deprecated Size Keyword `full`
{: #deprecated-size-keyword-full}

The [size keyword][size] `full` will be replaced by `max` in version 3.0. It is impractical to deliver the full size of very large images, and thus the keyword is not helpful when the Image Information has not been read. When the Image Information has been read, clients can request the explicit `w,h` size. See [issue 678](https://github.com/IIIF/iiif.io/issues/678).

### 2.2. Deprecated `sizeByWhListed` and `sizeByForcedWh` Feature Names
{: #deprecated-sizebywhlisted-and-sizebyforcedwh-feature-names}

The feature names `sizeByWhListed` and `sizeByForcedWh` will be removed from the [profile description][profile-description] in version 3.0. The feature `sizeByForcedWh` was inconsistently defined in version 2.0. The feature `sizeByWhListed` is implied by including `sizes` in the image information document and is therefore not required as a named feature. See [issue 720](https://github.com/IIIF/iiif.io/issues/720) and related [addition of `sizeByConfinedWh` and `sizeByDistortedWh`][added-sizebyconfinedwh-and-sizebydistortedwh].

## 3. Deferred Changes
{: #deferred-changes}

### 3.1. Change Canonical Syntax

The [canonical URI syntax][canonical-uri-syntax] will change in the next major release to use the `w,h` size syntax in a manner compatible with the `sizes` array, and to use `max` instead of `full` as the size keyword. See [issue 554](https://github.com/IIIF/iiif.io/issues/544) and [issue 678](https://github.com/IIIF/iiif.io/issues/678).

### 3.2. Change `license` property name to `rights`

The mapping of the [`license` property][rights] has already been changed to `dcterms:rights` in the [JSON-LD context][context] to more accurately represent its use for both rights and licensing information. However, the change of the property name will be a breaking change and thus must wait for the next major version release. See [issue 644](https://github.com/IIIF/iiif.io/issues/644).


[added-sizebyconfinedwh-and-sizebydistortedwh]: #added-sizebyconfinedwh-and-sizebydistortedwh-feature-names "Added `sizeByConfinedWh` and `sizeByDistortedWh` Feature Names"
[api-21]: {{ site.url }}{{ site.baseurl }}/api/image/2.1/ "Image API 2.1"
[api-compliance]: {{ site.url }}{{ site.baseurl }}/api/image/2.0/#compliance-levels "Image API 6. Compliance Levels"
[api-20]: {{ site.url }}{{ site.baseurl }}/api/image/2.0/ "Image API 2.0"
[canonical-uri-syntax]: {{ site.url }}{{ site.baseurl }}/api/image/2.1/#canonical-uri-syntax "Canonical URI syntax"
[context]: {{ site.url }}{{ site.baseurl }}/api/image/2/context.json "JSON-LD context"
[deprecated-sizebywhlisted-and-sizebyforcedwh]: #deprecated-sizebywhlisted-and-sizebyforcedwh-feature-names "Deprecated `sizeByWhListed` and `sizeByForcedWh` Feature Names"
[deprecated-size-full]: #deprecated-size-keyword-full "Deprecated Size Keyword `full`"
[deferred-changes]: #deferred-changes "Deferred Changes"
[deprecations]: #deprecations "Deprecations"
[image-information-request]: {{ site.url }}{{ site.baseurl }}/api/image/2.1/#image-information-request "Image Information Request"
[non-breaking-changes]: #non-breaking-changes "Image API 2.0 Non-reaking Changes"
[profile-description]: {{ site.url }}{{ site.baseurl }}/api/image/2.1/#profile-description "Profile Description"
[region]: {{ site.url }}{{ site.baseurl }}/api/image/2.1/#region "Region"
[rights]: {{ site.url }}{{ site.baseurl }}/api/image/2.1/#rights-and-licensing-properties "Rights and Licensing Properties"
[size]: {{ site.url }}{{ site.baseurl }}/api/image/2.1/#size "Size"

{% include acronyms.md %}
