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

## 2. Full Georef Annotation Example

{% include api/code_header.html %}
```json-doc
{

}
```

- Georef annotations target IIIF Images, not Canvases.
    - Images are georeferenced using the original image. Images on a canvas can be scaled or rotated
- Waarom alleen IIIF-afbeeldingen? Manifests with non-IIIF images, like Europeana is sometimes using in their manifests, are not supported. Zie motivating use cases: anders niet mogelijk om in te zoomen, XYZ-tiles te maken, aan elkaar te plakken.
- IIIF Image API 2 and 3 are supported.
- Annotations can be separate, or [embedded in manifest](https://iiif.io/api/cookbook/recipe/0269-embedded-or-referenced-annotations/).


## 3. Implementation Notes


## Appendices

### A. Acknowledgements

### B. Change Log

