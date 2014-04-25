---
title: "Image API Compliance, Version 2.0.0-draft1"
id: image-api-compliance
layout: sub-page
permalink: compliance.html
date: 2014-02-18
categories: [compliance, image-api]
major: 2
minor: 0
patch: 0
pre: draft1
---
This version: {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

Latest stable version: {{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }}.{{ site.image_api.latest.patch }}

This document is a companion to the [International Image Interoperability Framework Image API Specification][1]. It defines the set of supported parameters that correspond to different levels of compliance to the IIIF Image API.

Three levels of compliance are defined. Level 0 is defined as the minimum set of supported parameters and features to qualify an implementation of the service as compliant to the IIIF standard. Level 1 is defined as the RECOMMENDED set of parameters and features to be implemented.

In the tables below "x" indicates that support is required, "o" indicates that support is optional.

## Image Parameters

### Region
|             | Level 0 | Level 1 | Level 2  |
| ----------- |:-------:|:-------:|:--------:|
| full        | x       | x       | x        | 
| x,y,w,h     | o       | x       | x        | 
| pct:x,y,w,h | o       | o       | x        | 

### Size
|             | Level 0 | Level 1 | Level 2  |
| ----------- |:-------:|:-------:|:--------:|
| full        | x       | x       | x        |
| w,          | o       | x       | x        |
| ,h          | o       | x       | x        |
| pct:x       | o       | x       | x        |
| w,h         | o       | o       | x        |
| !w,h        | o       | o       | x        |

### Rotation
|             | Level 0 | Level 1 | Level 2  |
| ----------- |:-------:|:-------:|:--------:|
| 0           | x       | x       | x        |
| 90,180,270  | o       | o       | x        |
| arbitrary   | o       | o       | o        |

### Quality
|             | Level 0 | Level 1 | Level 2  |
| ----------- |:-------:|:-------:|:--------:|
| native      | x       | x       | x        |
| color       | o       | o       | x        |
| grey        | o       | o       | x        |
| bitonal     | o       | o       | x        |

### Format
|             | Level 0 | Level 1 | Level 2  |
| ----------- |:-------:|:-------:|:--------:|
| jpg         | x       | x       | x        |
| png         | o       | o       | x        |
| tif         | o       | o       | o        |
| gif         | o       | o       | o        |
| pdf         | o       | o       | o        |
| jp2         | o       | o       | o        |


## HTTP Features

|                       | Level 0 | Level 1 | Level 2  |
| --------------------- |:-------:|:-------:|:--------:|
| CORS                  | o       | x       | x        |
| json-ld media type    | o       | x       | x        |
| profile link header   | o       | x       | x        |
| canonical link header | o       | o       | o        |

## Document Properties

### Image Information Document Properties

The Image Information Document MUST be provided at all levels, and include properties as indicated in the table below:

| Property                  | Level 0 | Level 1 | Level 2  |
| ------------------------- |:-------:|:-------:|:--------:|
| @context                  | x       | x       | x        |
| @id                       | x       | x       | x        |
| height                    | x       | x       | x        |
| width                     | x       | x       | x        |
| protocol                  | x       | x       | x        |
| profile                   | x       | x       | x        |
| capabilities              | o       | o       | o        |
| formats                   | o       | o       | o        |
| scale_factors             | o       | o       | o        |
| sizes                     | o       | o       | o        |
| tile_width                | o       | o       | o        |
| tile_height               | o       | o       | o        |
| qualities                 | o       | o       | o        |

All properties marked as optional SHOULD be included if applicable.

### Server Capabilities Document Properties

The Server Capabilities Document MAY be provided at any levels, and include properties as indicated in the table below:

| Property                  | Level 0 | Level 1 | Level 2  |
| ------------------------- |:-------:|:-------:|:--------:|
| @context                  | x       | x       | x        |
| @id                       | x       | x       | x        |
| documentation             | o       | o       | o        |
| cors                      | o       | o       | o        |
| region_by_pct             | o       | o       | o        |
| region_by_px              | o       | o       | o        |
| rotation_arbitrary        | o       | o       | o        |
| rotation_by_90s           | o       | o       | o        |
| size_by_forced_wh         | o       | o       | o        |
| size_by_h                 | o       | o       | o        |
| size_by_pct               | o       | o       | o        |
| size_by_w                 | o       | o       | o        |
| size_by_wh                | o       | o       | o        |


## Indicating Compliance

Servers indicate compliance with level 0 by including the following header in IIIF responses:

```
Link: <http://iiif.io/api/image/{{ page.major }}/level0.json>;rel="profile"
```

A level 0 compliant image server MAY specify scaling_factors and/or tile_width and tile_height values in the Image information response. At Level 0 compliance, a server is only required to deliver images of sizes computed using the scaling factors declared in the Image Information response. If specified they should be interpreted with the following special meanings:

 * scaling_factors - only the specified scaling factors are supported
 * tile_width, tile_height - clients should request only regions that correspond to output tiles of the specified dimensions

If a client requests an scaling or region outside these parameters then the image server MAY reject the request with a 400 Bad Request error.

Servers indicate compliance with level 1 by including the following header in IIIF responses:

```
Link: <http://iiif.io/api/image/{{ page.major }}/level1.json>;rel="profile"
```

Servers indicate compliance with level 2 by including the following header in IIIF responses:

```
Link: <http://iiif.io/api/image/{{ page.major }}/level2.json>;rel="profile"
```

   [1]: http://iiif.io/api/image/2.0
