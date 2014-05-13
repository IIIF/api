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

<style>
.usage { margin: 0px; padding-top: 0px; padding-bottom: 2px; font-style: italic; }
dd ul li { margin: 0px; padding: 0px; }
dd ul { margin: 0px; padding-top: 0px; padding-bottom: 0px }
dt {font-weight: bold;}

.examplelist li {
  margin-bottom: 8px;
}

.examplelist li code {
  background: #eee;
  border: 1px dashed #bbb;
  padding: 3px;  
}

.CodeRay {background: #eee; border: 1px dashed #bbb; padding-left: 5px ; margin-left: 30px;}
.string {color: #209020;}
.comment {font-style: italic; color: #909090;}
.key {color: #202090;}
.integer {color: #902020;}
.error {color: red; font-weight: bold; font-size: +1;}

pre {
  margin-top: 8px; 
  margin-bottom: 8px;
}

.urltemplate { 
  background: #eee; 
  border: 1px dashed #bbb; 
  padding-left: 5px ; 
  margin-left: 30px;
  margin-right: 30px; 
  padding-top: 5px; 
  padding-bottom: 5px; 
}


body { line-height: 1.1;}

.specbody { 
  margin-left: 10px;
  margin-right: 10px;
}

.names { margin-top: 2px;}
.names li { padding-top: 0px; line-height: 1.1; list-style: none;}

p { margin-top: 8px; margin-bottom: 8px;}

.sub-pages-container .presentation-api .names li {
  line-height: 1.1;
  padding-left: 0;
}

.specbody h2 {
  color: #2f353e;
  font-family: 'Raleway', Arial, sans-serif;
  font-weight: 300;
  letter-spacing: 1px;
  margin-top: 10px;
}

.specbody h3 {
  margin-top: 10px;
}

.specbody h4 {
  margin-top: 10px;
}

.mytoc ol {
  margin: 0px;
  margin-top: 2px;
}

dt {
  margin-top: 8px;
}

.rfc {
  color: #d55;
  font-variant: small-caps;
  font-style: normal;
  font-size: 1.2em;
}

.legend { 
  width: 50%;
}

table {
  border: 1px solid black;
}

tr {
  border: 1px solid #666;
}

td, th {
  border: 1px solid #666;
  padding: 3px;
}

#markdown-toc li {
  list-style-type: none;
  padding-top: 0px; 
  padding-bottom: 0px; 
  line-height: 1.1;

  margin-top: 8px;
  margin-bottom: 8px;
}
#markdown-toc ul {
  margin-top: 8px;
  margin-bottom: 8px;
}

</style>

<div class="specbody">

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
| default     | x       | x       | x        |
| color       | o       | o       | x (if applicable) |
| gray        | o       | o       | x (if applicable) |
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
| formats                   | o       | o       | o        |
| scale_factors             | o       | o       | o        |
| sizes                     | o       | o       | o        |
| tile_width                | o       | o       | o        |
| tile_height               | o       | o       | o        |
| qualities                 | o       | o       | o        |

All properties marked as optional SHOULD be included if applicable.

### Profile Properties

The Server Capabilities Document MAY be provided at any levels, and include properties as indicated in the table below:

| Property                  | Level 0 | Level 1 | Level 2  |
| ------------------------- |:-------:|:-------:|:--------:|
| @context                  | x       | x       | x        |
| @id                       | x       | x       | x        |
| canonical_link_header     | o       | o       | o        |
| cors                      | o       | o       | o        |
| jsonld_media_type         | o       | x       | x        |
| profile_link_header       | o       | x       | x        |
| region_by_pct             | o       | o       | o        |
| region_by_px              | o       | o       | o        |
| rotation_arbitrary        | o       | o       | o        |
| rotation_by_90s           | o       | o       | o        |
| size_above_full           | o       | o       | o        |
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

</div>

   [1]: http://iiif.io/api/image/2.0
