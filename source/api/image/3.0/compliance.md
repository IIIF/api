---
title: "Image API Compliance, Version 3.0.0"
id: image-api-compliance
layout: spec
tags: [compliance, image-api]
major: 3
minor: 0
patch: 0
pre: ALPHA
cssversion: 3
redirect_from:
  - /api/image/compliance.html
  - /api/image/3/compliance.html
---

## Status of this Document
{:.no_toc}

__This version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest stable version:__ [{{ site.image_api.stable.major }}.{{ site.image_api.stable.minor }}.{{ site.image_api.stable.patch }}][image-compliance-stable-version]

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## 1. Introduction

This document is a companion to the [IIIF Image API 3.0 Specification][image30]. It defines the set of supported parameters that correspond to different levels of compliance to the API.

## 2. Compliance

Three levels of compliance are defined. Level 0 is the minimum set of parameters and features that _MUST_ be implemented to qualify the service as compliant with the IIIF Image API Specification. Level 1 is the _RECOMMENDED_ set of parameters and features to be implemented. Note that servers may not support all combinations of all supported parameters and features, as noted in the appropriate sections below.

In the tables below ![required][icon-req] indicates that support is _REQUIRED_, and ![optional][icon-opt] indicates that support is _OPTIONAL_.

## 3. Image Parameters

### 3.1 Region

| Syntax          | Feature Name   | Level 0 | Level 1 | Level 2  |
|:----------------|:-------------- |:-------:|:-------:|:--------:|
| `full`          |                | ![required][icon-req] | ![required][icon-req] | ![required][icon-req] |
| _`x,y,w,h`_     | `regionByPx`   | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| _`pct:x,y,w,h`_ | `regionByPct`  | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req] |
| `square`        | `regionSquare` | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
{: .api-table}

See also the note under [Size][image30-size] about combinations of Size and Region that may not be supported.

### 3.2 Size

| Syntax    | Feature Name        | Level 0 | Level 1 | Level 2  |
|:----------|:--------------------|:-------:|:-------:|:--------:|
| `max`     |                     | ![required][icon-req] | ![required][icon-req] | ![required][icon-req] |
| _`w,`_    | `sizeByW`           | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| _`,h`_    | `sizeByH`           | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| _`pct:n`_ | `sizeByPct`         | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req] |
| _`!w,h`_  | `sizeByConfinedWh`  | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req] |
| _`w,h`_   | `sizeByWh`          | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req] |
{: .api-table}

At any level of compliance, an image service whose Image Information response includes the `sizes` property must support requests for the sizes listed, and a service whose Image Information response includes the `tiles` property must support requests for the sizes implicit in the `width`, `height` and `scaleFactors` values given for tiles.

Note that servers may express limits on the sizes available for an image with the optional `maxWidth`, `maxHeight` and/or `maxArea` [Profile Description properties][image30-profile-description]. Servers are compliant provided they support the forms of the Size parameter shown above for image sizes up to the limits specified. Clients should not assume that the full image at the `width` and `height` specified in the Image Information response will be available. The full image will be available at the `max` size, which might be less than the `width` and `height`.

### 3.3 Rotation

| Syntax           | Feature Name        | Level 0 | Level 1 | Level 2  |
|:-----------------|:--------------------|:-------:|:-------:|:--------:|
| `0`              |                     | ![required][icon-req] | ![required][icon-req] | ![required][icon-req] |
| `90`,`180`,`270` | `rotationBy90s`     | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req] |
| _arbitrary_      | `rotationArbitrary` | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
| _`!n`_           | `mirroring`         | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
{: .api-table}

### 3.4 Quality

| Syntax        | Level 0 | Level 1 | Level 2  |
|:--------------|:-------:|:-------:|:--------:|
| `default`     | ![required][icon-req] | ![required][icon-req] | ![required][icon-req] |
| `color`       | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req] (if applicable) |
| `gray`        | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req] (if applicable) |
| `bitonal`     | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req] |
{: .api-table}

### 3.5 Format

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

| HTTP Feature          | Feature Name          | Level 0 | Level 1 | Level 2  |
|:----------------------|:----------------------|:-------:|:-------:|:--------:|
| base URI redirects    | `baseUriRedirect`     | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| CORS                  | `cors`                | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| json-ld media type    | `jsonldMediaType`     | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| profile link header   | `profileLinkHeader`   | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
| canonical link header | `canonicalLinkHeader` | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
{: .api-table}

## 5. Level 0 Compliance

A level 0 compliant image server _MAY_ specify `scaleFactors` and/or `width` and `height` values for `tiles` in the Image Information response. At level 0 compliance, a service is only required to deliver images of sizes computed using the scaling factors declared in the Image Information response. If specified they should be interpreted with the following special meanings:

 * `scaleFactors` - only the specified scaling factors are supported
 * `width`, `height` within `tiles` - clients should request only regions that correspond to output tiles of the specified dimensions

A level 0 compliant image server _MAY_ specify `sizes` to indicate specific `width` and `height` values for sizes available for the `full` region.

If a client requests a combination of size and region outside these parameters then the image server _MAY_ reject the request with an error.

{% include links.md %}
{% include acronyms.md %}
