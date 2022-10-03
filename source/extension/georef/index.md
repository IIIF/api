---
title: Georeferencing Extension Extension
layout: spec
tags: [extension, georef]
cssversion: 2
---

## Status of this Document
{:.no_toc}

This document is not subject to [semantic versioning][notes-versioning].
Changes will be tracked within the document.

{% include copyright.md %}

## 1. Introduction

The [IIIF Presentation API 3](https://iiif.io/api/presentation/3.0/) does not provide a resource property designed specifically for geographic location. However, the concept of location is a first class descriptor for many resources and thus calls for its own property by which it can be expressed.

### 1.1 Objectives and Scope

This IIIF extension defines Web Annotation format which maps parts of IIIF Images to earthbound geographic coordinates.


Spatial coordinates for resources on other celestial bodies or contrived worlds can be expressed using the semantic pattern of GeoJSON. However, `navPlace` adopts the [existing GeoJSON specification](https://datatracker.ietf.org/doc/html/rfc7946) to promote interoperability with industry standard mapping libraries and methods using [WGS84](http://www.w3.org/2003/01/geo/wgs84_pos) as the coordinate reference system for projections of the surface of Earth. As such, expressing the location of extraterrestrial entities is not supported by the `navPlace` property. This extension does not preclude the development of future extensions to address this use case.

### 1.2 Motivating Use Cases

- overlay iiif images on a map, warping.
- stitching multiple maps together.
- geospatial area, enabling them to be found by search engines with geoapatial coordinates
- xyz map tile layer, gis software

Situations which are not in scope include:

- 3D spatial representation
- Photo geotagging

### 1.3 Terminology

This extension uses the following terms:

* __embedded__: When a resource (A) is embedded within an embedding resource (B), the complete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will not result in additional information. Example: Canvas A is embedded in Manifest B.
* __referenced__: When a resource (A) is referenced from a referencing resource (B), an incomplete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will result in additional information. Example: Manifest A is referenced from Collection B.
* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

The terms _array_, _JSON object_, _number_, _string_, and _boolean_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].

## 2. Georeferencing with Ground Control Points

mapping between image coordinates in pixels and geospatial coordinates.

Examples/references:

- GDAL
- QGIS
- Map Warper

What data is needed to georeference and warp a map? (reference use cases)?

- image data
- GCPs
- pixel mask

## 3. Web Annotations

Why web annotation?
Anyone can georeference any IIIF image.


- Annotation target:
    - IIIF image service
    - selector: either complete image, or SvgSelector


- Georef annotations target IIIF Images, not Canvases.
    - Images are georeferenced using the original image. Images on a canvas can be scaled or rotated
- Waarom alleen IIIF-afbeeldingen? Manifests with non-IIIF images, like Europeana is sometimes using in their manifests, are not supported. Zie motivating use cases: anders niet mogelijk om in te zoomen, XYZ-tiles te maken, aan elkaar te plakken.
- IIIF Image API 2 and 3 are supported.
- Annotations can be separate, or [embedded in manifest](https://iiif.io/api/cookbook/recipe/0269-embedded-or-referenced-annotations/).
- multiple georeferenced maps in a single image

- Annotation body: ground control points


## 4. Full Georef Annotation Example

{% include api/code_header.html %}
```json-doc
{
  "type": "Annotation",
  "@context": [
    "http://iiif.io/api/extension/georef/context.json",
    "http://iiif.io/api/presentation/3/context.json"
  ],
  "motivation": "georeferencing",
  "target": {
    "type": "Image",
    "source": "https://cdm21033.contentdm.oclc.org/digital/iiif/krt/2891/full/full/0/default.jpg",
    "service": [
      {
        "@id": "https://cdm21033.contentdm.oclc.org/digital/iiif/krt/2891",
        "type": "ImageService2"
      }
    ],
    "selector": {
      "type": "SvgSelector",
      "value": "<svg width=\"5965\" height=\"2514\"><polygon points=\"59,84 44,2329 5932,2353 5920,103 \" /></svg>"
    }
  },
  "body": {
    "type": "FeatureCollection",
    "purpose": "gcp-georeferencing",
    "transformation": {
      "type": "polynomial",
      "order": 0
    },
    "features": [
      {
        "type": "Feature",
        "properties": {
          "pixelCoords": [
            5085,
            782
          ]
        },
        "geometry": {
          "type": "Point",
          "coordinates": [
            4.4885839,
            51.9101828
          ]
        }
      },
      {
        "type": "Feature",
        "properties": {
          "pixelCoords": [
            5467,
            1338
          ]
        },
        "geometry": {
          "type": "Point",
          "coordinates": [
            4.5011785,
            51.901595
          ]
        }
      },
      {
        "type": "Feature",
        "properties": {
          "pixelCoords": [
            2006,
            374
          ]
        },
        "geometry": {
          "type": "Point",
          "coordinates": [
            4.405981,
            51.9091596
          ]
        }
      }
    ]
  }
}
```

## 5. Specification

- `type` must be `Annotation` or `AnnotationPage`
- `motivation` must be `georeferencing`

...

## 6. Implementation Notes



## Appendices

### A. Acknowledgements

### B. Change Log

