---
title: "Image API Compliance, Version 1.2"
id: image-api-compliance
layout: sub-page
permalink: compliance.html
date: 2014-02-18
categories: [compliance, image-api]
---
# IIIF: Image API Compliance, Version 1.2

This document is a companion to the [International Image Interoperability Framework Image API Specification, version 1.2][1]. It defines the set of supported parameters that correspond to different levels of compliance to the IIIF Image API.


Three levels of compliance are defined. Level 0 is defined as the minimum set of supported parameters and features to qualify an implementation of the service as compliant to the IIIF standard. Level 1 is defined as the RECOMMENDED set of parameters and features to be implemented.


### Region
|             | Level 0 | Level 1 | Level 2  | Optional |
| ----------- |:-------:|:-------:|:--------:|:--------:| 
| full        | x       | x       | x        |          | 
| x,y,w,h     |         | x       | x        |          | 
| pct:x,y,w,h |         |         | x        |          | 

### Size
|             | Level 0 | Level 1 | Level 2  | Optional |
| ----------- |:-------:|:-------:|:--------:|:--------:| 
| full        | x       | x       | x        |          | 
| w,          |         | x       | x        |          | 
| ,h          |         | x       | x        |          | 
| pct:x       |         | x       | x        |          | 
| w,h         |         |         | x        |          | 
| !w,h        |         |         | x        |          | 

### Rotation
|             | Level 0 | Level 1 | Level 2  | Optional |
| ----------- |:-------:|:-------:|:--------:|:--------:| 
| 0           | x       | x       | x        |          | 
| 90,180,270  |         |         | x        |          | 
| arbitrary   |         |         |          | x        | 

### Quality
|             | Level 0 | Level 1 | Level 2  | Optional |
| ----------- |:-------:|:-------:|:--------:|:--------:| 
| native      | x       | x       | x        |          | 
| color       |         |         | x        |          | 
| grey        |         |         | x        |          | 
| bitonal     |         |         | x        |          | 

### Format
|             | Level 0 | Level 1 | Level 2  | Optional |
| ----------- |:-------:|:-------:|:--------:|:--------:| 
| jpg         | x       | x       | x        |          | 
| png         |         |         | x        |          | 
| tif         |         |         |          | x        | 
| gif         |         |         |          | x        | 
| pdf         |         |         |          | x        | 
| jp2         |         |         |          | x        | 

### Image Information Request
| Property                  | Level 0 | Level 1 | Level 2  | Optional |
| ------------------------- |:-------:|:-------:|:--------:|:--------:| 
| @context                  | x       | x       | x        |          |
| @id                       | x       | x       | x        |          |
| height                    | x       | x       | x        |          |
| width                     | x       | x       | x        |          |
| protocol                  | x       | x       | x        |          |
| profile                   | x       | x       | x        |          |
| capabilities              |         |         |          | x        |
| formats                   |         |         |          | x        |
| scale_factors             |         |         |          | x        |
| sizes                     |         |         |          | x        |
| tile_width                |         |         |          | x        |
| tile_height               |         |         |          | x        |
| qualities                 |         |         |          | x        |

All property marked as optional SHOULD be included if applicable. 

## Indicating Compliance

Servers indicate compliance with level 0 by including the following header in IIIF responses:

```
Link: <http://iiif.io/image/1.2/compliance/level0.json>;rel="profile"
```

A level 0 compliant image server MAY specify scaling_factors and/or tile_width and tile_height values in the Image information response. At Level 0 compliance, a server is only required to deliver images of sizes computed using the scaling factors declared in the Image Information response. If specified they should be interpreted with the following special meanings:

 * scaling_factors - only the specified scaling factors are supported
 * tile_width, tile_height - clients should request only regions that correspond to output tiles of the specified dimensions

If a client requests an scaling or region outside these parameters then the image server MAY reject the request with a 400 Bad Request error.

Servers indicate compliance with level 1 by including the following header in IIIF responses:

```
Link: <http://iiif.io/image/1.2/compliance/level1.json>;rel="profile"
```

Servers indicate compliance with level 2 by including the following header in IIIF responses:

```
Link: <http://iiif.io/image/1.2/compliance/level2.json>;rel="profile"
```

> TODO: add a note about the capabilites document here
