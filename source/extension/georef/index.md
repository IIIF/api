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

This IIIF Presentation API 3 extension defines a new property, `navPlace`, which is defined by earthbound geographic coordinates in the form of [GeoJSON-LD](https://geojson.org/geojson-ld/). Clients may use this property to leverage the functionality of web-based map platforms such as Google Earth, Leaflet, and OpenLayers to provide a means to enrich data presentation through map-based interfaces.

Spatial coordinates for resources on other celestial bodies or contrived worlds can be expressed using the semantic pattern of GeoJSON. However, `navPlace` adopts the [existing GeoJSON specification](https://datatracker.ietf.org/doc/html/rfc7946) to promote interoperability with industry standard mapping libraries and methods using [WGS84](http://www.w3.org/2003/01/geo/wgs84_pos) as the coordinate reference system for projections of the surface of Earth. As such, expressing the location of extraterrestrial entities is not supported by the `navPlace` property. This extension does not preclude the development of future extensions to address this use case.

### 1.2 Motivating Use Cases

## 2. Full Manifest Example

{% include api/code_header.html %}
```json-doc
{
   "@context":[
      "http://iiif.io/api/extension/navplace/context.json",
      "http://iiif.io/api/presentation/3/context.json"
   ],
   "id":"https://example.org/iiif/manifest/1",
   "type":"Manifest",
   "label":{
      "en":[
         "Georeferencing Extension Example Manifest"
      ]
   },
   "items":[]
}
```

## 3. Implementation Notes


## Appendices

### A. Acknowledgements


### B. Change Log

