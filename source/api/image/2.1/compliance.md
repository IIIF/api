---
title: "Image API Compliance, Version 2.1.0"
id: image-api-compliance
layout: spec
tags: [compliance, image-api]
major: 2
minor: 1
patch: 0
pre: final
redirect_from:
  - /api/image/compliance.html
  - /api/image/2/compliance.html
---

## Status of this Document
{:.no_toc}

__This version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest stable version:__ [{{ site.image_api.stable.major }}.{{ site.image_api.stable.minor }}.{{ site.image_api.stable.patch }}][stable-version]

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## 1. Introduction
{: #introduction}

This document is a companion to the [IIIF Image API Specification][image-api]. It defines the set of supported parameters that correspond to different levels of compliance to the API.

## 2. Compliance
{: #compliance}

Three levels of compliance are defined. Level 0 is the minimum set of parameters and features that _MUST_ be implemented to qualify the service as compliant with the IIIF Image API Specification. Level 1 is the _RECOMMENDED_ set of parameters and features to be implemented. Note that servers may not support all combinations of all supported parameters and features, as noted in the appropriate sections below.

In the tables below "![required][icon-req]" indicates that support is _REQUIRED_, and "![optional][icon-opt]" indicates that support is _OPTIONAL_.

## 3. Image Parameters
{: #image-parameters}

### 3.1 Region
{: #region}

| Syntax      | Feature Name    | Level 0 | Level 1 | Level 2  |
|:------------|:--------------- |:-------:|:-------:|:--------:|
| `full`      |                 | ![required][icon-req] | ![required][icon-req]       | ![required][icon-req]        |
| x,y,w,h     | `regionByPx`  | ![optional][icon-opt] | ![required][icon-req]       | ![required][icon-req]        |
| pct:x,y,w,h | `regionByPct` | ![optional][icon-opt] | ![optional][icon-opt]       | ![required][icon-req]        |
| `square`    | `regionSquare` | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
{: .api-table}

See also the note under [Size][size] about combinations of Size and Region that may not be supported.

### 3.2 Size
{: #size}

| Syntax | Feature Name        | Level 0 | Level 1 | Level 2  |
|:-------|:--------------------|:-------:|:-------:|:--------:|
| `full` |                     | ![required][icon-req] | ![required][icon-req] | ![required][icon-req] |
| `max`  |                     | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
| w,     | `sizeByW`           | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| ,h     | `sizeByH`           | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| pct:n  | `sizeByPct`         | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| !w,h   | `sizeByConfinedWh`  | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req] |
| w,h    | `sizeByDistortedWh` | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req] |
| w,h    | `sizeByWh`          | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req] |
|        | `sizeAboveFull`     | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
{: .api-table}

At any level of compliance, an image service whose Image Information response includes the `sizes` property must support requests for the sizes listed, and a service whose Image Information response includes the `tiles` property must support requests for the sizes implicit in the `width`, `height` and `scaleFactors` values given for tiles.

Note that servers may express limits on the sizes available for an image with the optional `maxWidth`, `maxHeight` and/or `maxArea` [Profile Description properties][profile]. Servers are compliant provided they support the forms of the Size parameter shown above for image sizes up to the limits specified. Clients should not assume that Region and Size parameter combinations such as `/full/full/` will be supported.

See also the [deprecation warning about `full`][full-dep].

### 3.3 Rotation
{: #rotation}

| Syntax | Feature Name | Level 0 | Level 1 | Level 2  |
|:-------|:-------------|:-------:|:-------:|:--------:|
| `0`    |              | ![required][icon-req] | ![required][icon-req] | ![required][icon-req] |
| `90`,`180`,`270` | `rotationBy90s` | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req]       |
| _arbitrary_ | `rotationArbitrary` | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
| !_n_ | `mirroring` | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
{: .api-table}

### 3.4 Quality
{: #quality}

| Syntax        | Level 0 | Level 1 | Level 2  |
|:--------------|:-------:|:-------:|:--------:|
| `default`     | ![required][icon-req]      | ![required][icon-req]      | ![required][icon-req]       |
| `color`       | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req] (if applicable) |
| `gray`        | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req] (if applicable) |
| `bitonal`     | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req]       |
{: .api-table}

### 3.5 Format
{: #format}

| Syntax      | Level 0 | Level 1 | Level 2  |
|:------------|:-------:|:-------:|:--------:|
| `jpg`       | ![required][icon-req] | ![required][icon-req] | ![required][icon-req] |
| `png`       | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req] |
| `tif`       | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
| `gif`       | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
| `pdf`       | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
| `jp2`       | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
| `webp`      | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
{: .api-table}

## 4. HTTP Features
{: #http-features}

| HTTP Feature          | Feature Name          | Level 0 | Level 1 | Level 2  |
|:----------------------|:----------------------|:-------:|:-------:|:--------:|
| base URI redirects    | `baseUriRedirect`     | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| CORS                  | `cors`                | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| json-ld media type    | `jsonldMediaType`     | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| profile link header   | `profileLinkHeader`   | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
| canonical link header | `canonicalLinkHeader` | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
{: .api-table}

## 5. Indicating Compliance
{: #indicating-compliance}

Servers _MAY_ indicate compliance with by including a header in IIIF responses for images:

```
Link: <http://iiif.io/api/image/{{ page.major }}/level1.json>;rel="profile"
```
{: .urltemplate}

The URIs for the the compliance levels are as follows:

| Level | URI                                                   |
|:-----:|:------------------------------------------------------|
| 0     | http://iiif.io/api/image/{{ page.major }}/level0.json |
| 1     | http://iiif.io/api/image/{{ page.major }}/level1.json |
| 2     | http://iiif.io/api/image/{{ page.major }}/level2.json |
{: .urltemplate .api-table}

### 5.1 Level 0 Compliance
{: #level-0-compliance}

A level 0 compliant image server _MAY_ specify `scaleFactors` and/or `width` and `height` values for `tiles` in the Image Information response. At Level 0 compliance, a service is only required to deliver images of sizes computed using the scaling factors declared in the Image Information response. If specified they should be interpreted with the following special meanings:

 * `scaleFactors` - only the specified scaling factors are supported
 * `width`, `height` within `tiles` - clients should request only regions that correspond to output tiles of the specified dimensions

A level 0 compliant image server _MAY_ also specify `sizes` to indicate specific `width` and `height` values for sizes available for the `full` region.

If a client requests a combination of size and region outside these parameters then the image server _MAY_ reject the request with an error.

[iiif-discuss]: mailto:iiif-discuss@googlegroups.com "Email Discussion List"
[image-api]: {{ site.url }}{{ site.baseurl }}/api/image/{{ page.major }}.{{ page.minor }}/ "Image API {{ page.major }}.{{ page.minor }}"
[icon-req]: {{ site.url }}{{ site.baseurl }}/img/metadata-api/required.png "Required"
[icon-rec]: {{ site.url }}{{ site.baseurl }}/img/metadata-api/recommended.png "Recommended"
[icon-opt]: {{ site.url }}{{ site.baseurl }}/img/metadata-api/optional.png "Optional"
[icon-na]: {{ site.url }}{{ site.baseurl }}/img/metadata-api/not_allowed.png "Not allowed"
[size]: #size "3.2 Size"
[profile]: {{ site.url }}{{ site.baseurl }}/api/image/{{ page.major }}.{{ page.minor }}/#profile-description "5.3 Profile Description"
[stable-version]: {{ site.url }}{{ site.baseurl }}/api/image/{{ site.image_api.stable.major }}.{{ site.image_api.stable.minor }}/compliance/ "Stable Version"
[full-dep]: {{ site.url }}{{ site.baseurl }}/api/image/2.{{ page.minor }}/#full-dep "Full Size Keyword Deprecation Warning"

{% include acronyms.md %}
