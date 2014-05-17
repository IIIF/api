---
title: "Image API Compliance, Version 2.0.0-draft1"
id: image-api-compliance
layout: sub-page
permalink: compliance.html
date: 2014-02-18
categories: [compliance, image-api, spec-doc]
major: 2
minor: 0
patch: 0
pre: draft1
---

## Status of this Document

This version: {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

Latest stable version: {{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }}.{{ site.image_api.latest.patch }}

## Introduction

This document is a companion to the [International Image Interoperability Framework Image API Specification][1]. It defines the set of supported parameters that correspond to different levels of compliance to the IIIF Image API.

## Compliance

Three levels of compliance are defined. Level 0 is defined as the minimum set of supported parameters and features to qualify an implementation of the service as compliant to the IIIF standard. Level 1 is defined as the RECOMMENDED set of parameters and features to be implemented.

In the tables below "x" indicates that support is required, "o" indicates that support is optional.

## Image Parameters

### Region

| Syntax      | Feature Name    | Level 0 | Level 1 | Level 2  |
|:------------|:--------------- |:-------:|:-------:|:--------:|
| `full`      |                 | x       | x       | x        | 
| x,y,w,h     | `region_by_px`  | o       | x       | x        | 
| pct:x,y,w,h | `region_by_pct` | o       | o       | x        | 
{: .image-api-table}

### Size

| Syntax      | Feature Name        | Level 0 | Level 1 | Level 2  |
|:------------|:--------------------|:-------:|:-------:|:--------:|
| `full`      |                     | x       | x       | x        |
| w,          | `size_by_w`         | o       | x       | x        |
| ,h          | `size_by_h`         | o       | x       | x        |
| pct:x       | `size_by_pct`       | o       | x       | x        |
| w,h         | `size_by_forced_wh` | o       | o       | x        |
| !w,h        | `size_by_wh`        | o       | o       | x        |
|             | `size_above_full`   | o       | o       | o        |
{: .image-api-table}

### Rotation

| Syntax           | Feature Name         | Level 0 | Level 1 | Level 2  |
|:-----------------|:---------------------|:-------:|:-------:|:--------:|
| `0`              |                      | x       | x       | x        |
| `90`,`180`,`270` | `rotation_by_90s`    | o       | o       | x        |
| _arbitrary_      | `rotation_arbitrary` | o       | o       | o        |
{: .image-api-table}

### Quality

| Syntax        | Level 0 | Level 1 | Level 2  |
|:--------------|:-------:|:-------:|:--------:|
| `default`     | x       | x       | x        |
| `color`       | o       | o       | x (if applicable) |
| `gray`        | o       | o       | x (if applicable) |
| `bitonal`     | o       | o       | x        |
{: .image-api-table}

### Format

| Syntax      | Level 0 | Level 1 | Level 2  |
|:------------|:-------:|:-------:|:--------:|
| `jpg`       | x       | x       | x        |
| `png`       | o       | o       | x        |
| `tif`       | o       | o       | o        |
| `gif`       | o       | o       | o        |
| `pdf`       | o       | o       | o        |
| `jp2`       | o       | o       | o        |
{: .image-api-table}

## HTTP Features

| HTTP Feature          | Feature Name                  | Level 0 | Level 1 | Level 2  |
|:----------------------|:----------------------|:-------:|:-------:|:--------:|
| CORS                  | `cors`                  | o       | x       | x        |
| json-ld media type    | `jsonld_media_type`     | o       | x       | x        |
| profile link header   | `profile_link_header`   | o       | x       | x        |
| canonical link header | `canonical_link_header` | o       | o       | o        |
{: .image-api-table}



## Indicating Compliance

Servers indicate compliance with level 0 by including the following header in IIIF responses:

```
Link: <http://iiif.io/api/image/{{ page.major }}/level0.json>;rel="profile"
```
{: .urltemplate}

A level 0 compliant image server MAY specify scaling_factors and/or tile_width and tile_height values in the Image information response. At Level 0 compliance, a server is only required to deliver images of sizes computed using the scaling factors declared in the Image Information response. If specified they should be interpreted with the following special meanings:

 * scaling_factors - only the specified scaling factors are supported
 * tile_width, tile_height - clients should request only regions that correspond to output tiles of the specified dimensions

If a client requests an scaling or region outside these parameters then the image server MAY reject the request with a 400 Bad Request error.

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

  [1]: http://iiif.io/api/image/{{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }} "IIIF Image API"
