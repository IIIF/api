---
title: "Image API Compliance, Version 2.0.0"
id: image-api-compliance
layout: spec
tags: [compliance, image-api]
major: 2
minor: 0
patch: 0
pre: draft1
---

## Status of this Document
{:.no_toc}

__This version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest stable version:__ {{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }}.{{ site.image_api.latest.patch }}

## Introduction
{:.no_toc}

This document is a companion to the [IIIF Image API Specification][image-api]. It defines the set of supported parameters that correspond to different levels of compliance to the API.

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}


## Compliance

Three levels of compliance are defined. Level 0 is defined as the minimum set of supported parameters and features that _MUST_ be implemented to qualify the service as compliant to the IIIF standard. Level 1 is defined as the _RECOMMENDED_ set of parameters and features to be implemented.

In the tables below "![required][icon-req]" indicates that support is _REQUIRED_, "![optional][icon-opt]" indicates that support is _OPTIONAL_.

## Image Parameters

### Region

| Syntax      | Feature Name    | Level 0 | Level 1 | Level 2  |
|:------------|:--------------- |:-------:|:-------:|:--------:|
| `full`      |                 | ![required][icon-req] | ![required][icon-req]       | ![required][icon-req]        |
| x,y,w,h     | `region_by_px`  | ![optional][icon-opt] | ![required][icon-req]       | ![required][icon-req]        |
| pct:x,y,w,h | `region_by_pct` | ![optional][icon-opt] | ![optional][icon-opt]       | ![required][icon-req]        |
{: .image-api-table}

### Size

| Syntax      | Feature Name        | Level 0 | Level 1 | Level 2  |
|:------------|:--------------------|:-------:|:-------:|:--------:|
| `full`      |                     | ![required][icon-req]      | ![required][icon-req]      | ![required][icon-req]       |
| w,          | `size_by_w`         | ![optional][icon-opt]      | ![required][icon-req]      | ![required][icon-req]       |
| ,h          | `size_by_h`         | ![optional][icon-opt]      | ![required][icon-req]      | ![required][icon-req]       |
| pct:x       | `size_by_pct`       | ![optional][icon-opt]      | ![required][icon-req]      | ![required][icon-req]       |
| w,h         | `size_by_forced_wh` | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req]       |
| !w,h        | `size_by_wh`        | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req]       |
|             | `size_above_full`   | ![optional][icon-opt]      | ![optional][icon-opt]      | ![optional][icon-opt]       |
{: .image-api-table}

### Rotation

| Syntax | Feature Name | Level 0 | Level 1 | Level 2  |
|:-------|:-------------|:-------:|:-------:|:--------:|
| `0`    |              | ![required][icon-req] | ![required][icon-req] | ![required][icon-req] |
| `90`,`180`,`270` | `rotation_by_90s` | ![optional][icon-opt] | ![optional][icon-opt] | ![required][icon-req]       |
| _arbitrary_ | `rotation_arbitrary` | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
| !_n_ | `mirroring` | ![optional][icon-opt] | ![optional][icon-opt] | ![optional][icon-opt] |
{: .image-api-table}

### Quality

| Syntax        | Level 0 | Level 1 | Level 2  |
|:--------------|:-------:|:-------:|:--------:|
| `default`     | ![required][icon-req]      | ![required][icon-req]      | ![required][icon-req]       |
| `color`       | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req] (if applicable) |
| `gray`        | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req] (if applicable) |
| `bitonal`     | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req]       |
{: .image-api-table}

### Format

| Syntax      | Level 0 | Level 1 | Level 2  |
|:------------|:-------:|:-------:|:--------:|
| `jpg`       | ![required][icon-req]      | ![required][icon-req]      | ![required][icon-req]       |
| `png`       | ![optional][icon-opt]      | ![optional][icon-opt]      | ![required][icon-req]       |
| `tif`       | ![optional][icon-opt]      | ![optional][icon-opt]      | ![optional][icon-opt]       |
| `gif`       | ![optional][icon-opt]      | ![optional][icon-opt]      | ![optional][icon-opt]       |
| `pdf`       | ![optional][icon-opt]      | ![optional][icon-opt]      | ![optional][icon-opt]       |
| `jp2`       | ![optional][icon-opt]      | ![optional][icon-opt]      | ![optional][icon-opt]       |
{: .image-api-table}

## HTTP Features

| HTTP Feature          | Feature Name            | Level 0 | Level 1 | Level 2  |
|:----------------------|:------------------------|:-------:|:-------:|:--------:|
| base URI redirects    | `base_uri_redirect`     | ![optional][icon-opt]      | ![required][icon-req]      | ![required][icon-req]       |
| CORS                  | `cors`                  | ![optional][icon-opt]      | ![required][icon-req]      | ![required][icon-req]       |
| json-ld media type    | `jsonld_media_type`     | ![optional][icon-opt]      | ![required][icon-req]      | ![required][icon-req]       |
| profile link header   | `profile_link_header`   | ![optional][icon-opt]      | ![required][icon-req]      | ![required][icon-req]       |
| canonical link header | `canonical_link_header` | ![optional][icon-opt]      | ![optional][icon-opt]      | ![optional][icon-opt]       |
{: .image-api-table}

## Indicating Compliance

Servers indicate compliance with level 0 by including the following header in IIIF responses:

```
Link: <http://iiif.io/api/image/{{ page.major }}/level0.json>;rel="profile"
```
{: .urltemplate}

A level 0 compliant image server _MAY_ specify `scale_factors` and/or `tile_width` and `tile_height` values in the Image Information response. At Level 0 compliance, a service is only required to deliver images of sizes computed using the scaling factors declared in the Image Information response. If specified they should be interpreted with the following special meanings:

 * `scale_factors` - only the specified scaling factors are supported
 * `tile_width`, `tile_height` - clients should request only regions that correspond to output tiles of the specified dimensions

If a client requests a size or region outside these parameters then the image server _MAY_ reject the request with an error.

Servers indicate compliance with level 1 by including the following header in IIIF responses:

```
Link: <http://iiif.io/api/image/{{ page.major }}/level1.json>;rel="profile"
```
{: .urltemplate}

Servers indicate compliance with level 2 by including the following header in IIIF responses:

```
Link: <http://iiif.io/api/image/{{ page.major }}/level2.json>;rel="profile"
```
{: .urltemplate}

[image-api]: /api/image/2.0/ "Image API 2.0"
[icon-req]: /img/metadata-api/required.png "Required"
[icon-recc]: /img/metadata-api/recommended.png "Recommended"
[icon-opt]: /img/metadata-api/optional.png "Optional"
[icon-na]: /img/metadata-api/not_allowed.png "Not allowed"

{% include acronyms.md %}
