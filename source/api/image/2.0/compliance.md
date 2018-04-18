---
title: "Image API Compliance, Version 2.0.0"
id: image-api-compliance
layout: spec
tags: [compliance, image-api]
major: 2
minor: 0
patch: 0
pre: final
sitemap: false
redirect_from:
  - /api/image/2.0/compliance.html
---

## Status of this Document
{:.no_toc}

__This version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest stable version:__ {{ site.image_api.stable.major }}.{{ site.image_api.stable.minor }}.{{ site.image_api.stable.patch }}

## Introduction
{:.no_toc}

This document is a companion to the [IIIF Image API Specification][image-api]. It defines the set of supported parameters that correspond to different levels of compliance to the API.

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}


## Compliance

Three levels of compliance are defined. Level 0 is defined as the minimum set of supported parameters and features that _MUST_ be implemented to qualify the service as compliant to the IIIF standard. Level 1 is defined as the _RECOMMENDED_ set of parameters and features to be implemented.

In the tables below "![required][icon-req]" indicates that support is _REQUIRED_, and "![optional][icon-opt]" indicates that support is _OPTIONAL_.

## Image Parameters

### Region

| Syntax      | Feature Name    | Level 0 | Level 1 | Level 2  |
|:------------|:--------------- |:-------:|:-------:|:--------:|
| `full`      |                 | ![required][icon-req] | ![required][icon-req]       | ![required][icon-req]        |
| x,y,w,h     | `regionByPx`  | ![optional][icon-opt] | ![required][icon-req]       | ![required][icon-req]        |
| pct:x,y,w,h | `regionByPct` | ![optional][icon-opt] | ![optional][icon-opt]       | ![required][icon-req]        |
{: .api-table}

### Size

| Syntax      | Feature Name        | Level 0 | Level 1 | Level 2  |
|:------------|:--------------------|:-------:|:-------:|:--------:|
| `full`      |                     | ![required][icon-req]      | ![required][icon-req]      | ![required][icon-req]       |
| w,h         | `sizeByWhListed` | ![required][icon-req]      | ![required][icon-req]      | ![required][icon-req]       |
| w,          | `sizeByW`         | ![optional][icon-opt]      | ![required][icon-req]      | ![required][icon-req]       |
| ,h          | `sizeByH`         | ![optional][icon-opt]      | ![required][icon-req]      | ![required][icon-req]       |
| pct:x       | `sizeByPct`       | ![optional][icon-opt]      | ![required][icon-req]      | ![required][icon-req]       |
| w,h         | `sizeByForcedWh` | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req]       |
| !w,h        | `sizeByWh`        | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req]       |
|             | `sizeAboveFull`   | ![optional][icon-opt]      | ![optional][icon-opt]      | ![optional][icon-opt]       |
{: .api-table}

### Rotation

| Syntax | Feature Name | Level 0 | Level 1 | Level 2  |
|:-------|:-------------|:-------:|:-------:|:--------:|
| `0`    |              | ![required][icon-req] | ![required][icon-req] | ![required][icon-req] |
| `90`,`180`,`270` | `rotationBy90s` | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req]       |
| _arbitrary_ | `rotationArbitrary` | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
| !_n_ | `mirroring` | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
{: .api-table}

### Quality

| Syntax        | Level 0 | Level 1 | Level 2  |
|:--------------|:-------:|:-------:|:--------:|
| `default`     | ![required][icon-req]      | ![required][icon-req]      | ![required][icon-req]       |
| `color`       | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req] (if applicable) |
| `gray`        | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req] (if applicable) |
| `bitonal`     | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req]       |
{: .api-table}

### Format

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


## HTTP Features

| HTTP Feature          | Feature Name          | Level 0 | Level 1 | Level 2  |
|:----------------------|:----------------------|:-------:|:-------:|:--------:|
| base URI redirects    | `baseUriRedirect`     | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| CORS                  | `cors`                | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| json-ld media type    | `jsonldMediaType`     | ![optional][icon-opt] | ![required][icon-req] | ![required][icon-req] |
| profile link header   | `profileLinkHeader`   | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
| canonical link header | `canonicalLinkHeader` | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
{: .api-table}

## Indicating Compliance

Servers _MAY_ indicate compliance with by including a header in IIIF responses for images:

``` none
Link: <http://iiif.io/api/image/{{ page.major }}/level1.json>;rel="profile"
```


The URIs for the the compliance levels are as follows:

| Level | URI                                                   |
|:-----:|:------------------------------------------------------|
| 0     | http://iiif.io/api/image/{{ page.major }}/level0.json |
| 1     | http://iiif.io/api/image/{{ page.major }}/level1.json |
| 2     | http://iiif.io/api/image/{{ page.major }}/level2.json |
{: .api-table}

A level 0 compliant image server _MAY_ specify `scaleFactors` and/or `width` and `height` values for `tiles` in the Image Information response. At Level 0 compliance, a service is only required to deliver images of sizes computed using the scaling factors declared in the Image Information response. If specified they should be interpreted with the following special meanings:

 * `scaleFactors` - only the specified scaling factors are supported
 * `width`, `height` within `tiles` - clients should request only regions that correspond to output tiles of the specified dimensions

If a client requests a size or region outside these parameters then the image server _MAY_ reject the request with an error.

[image-api]: {{ site.url }}{{ site.baseurl }}/api/image/2.0/ "Image API 2.0"
[icon-req]: {{ site.url }}{{ site.baseurl }}/img/metadata-api/required.png "Required"
[icon-rec]: {{ site.url }}{{ site.baseurl }}/img/metadata-api/recommended.png "Recommended"
[icon-opt]: {{ site.url }}{{ site.baseurl }}/img/metadata-api/optional.png "Optional"
[icon-na]: {{ site.url }}{{ site.baseurl }}/img/metadata-api/not_allowed.png "Not allowed"

{% include acronyms.md %}
