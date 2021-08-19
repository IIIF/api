---
title: navPlace Extension
layout: spec
tags: [extension, navPlace]
cssversion: 2
---

## Status of this Document
{:.no_toc}

This document is not subject to [semantic versioning][notes-versioning].
Changes will be tracked within the document.

{% include copyright.md %}

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Introduction

The ideas of Time and Place are a foundation of human communication and understanding. These concepts are first class descriptors for resources. The ability to capture both concepts independently is often required for data presentation and preservation. In IIIF Presentation API 3 the property `navDate` allows for a calendar date to be associated with a resource in a client friendly format but there is no property designed for a geographic location. Locations are extents in space, independent of time and what may or may not be present in that space, and so need a unique property.


### 1.1 Objectives and Scope

IIIF provides the information necessary to allow a rich, online viewing environment for compound digital objects to be presented to a human user. The types of resources and their specific needs continue to enhance the IIIF specifications to greater resource coverage. The ability to assert ancillary information is a universal need in this expanse. This is achieved using Annotation, or Web Annotation, and extensions across the IIIF specification versions.

This extension describes a property called `navPlace` which contains earthbound geographic coordinates in the form of [GeoJSON-LD](https://geojson.org/geojson-ld/). Clients may use this property to leverage the navigational functionality of web maps such as Google Earth, Leaflet, OpenLayers, etc. giving them the opportunity to enrich data presentation through common web map platforms.

Spatial coordinates for resources on other celestial bodies or contrived worlds can be expressed using the semantic pattern of GeoJSON. However, `navPlace` makes use of the existing GeoJSON specification to promote interoperability with industry standard mapping libraries and methods using [WGS84](http://www.w3.org/2003/01/geo/wgs84_pos) as the coordinate reference system for projections of the surface of Earth. As such, expressing the location of extraterrestrial entities is not supported by the `navPlace` property. This extension does not preclude the development of future extensions to address this use case.


### 1.2 Motivating Use Cases

The reasons for associating geographic coordinates with web resources vary greatly. This extension does not intend to meet the data requirements for all geospatial practices. Use cases within the scope include



*   Link a IIIF resource to a single or multiple geographic areas on a web map
*   Supply a single geographic bounding box for an image of a map
*   Track locations listed in an itinerary or travel journal

Situations which are not in scope include


*   Spatiotemporal alignment with the place, as in a timeline or specific placement because of time
*   Georeferencing to overlay maps or warp maps into coordinate space
*   3D spatial representation
*   [Application of geospatial information to resource fragments](https://iiif.io/api/cookbook/recipe/0139-geolocate-canvas-fragment/)


### 1.3 Terminology

This specification uses the following terms:

* __embedded__: When a resource (A) is embedded within an embedding resource (B), the complete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will not result in additional information. Example: Canvas A is embedded in Manifest B.
* __referenced__: When a resource (A) is referenced from a referencing resource (B), an incomplete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will result in additional information. Example: Manifest A is referenced from Collection B.
* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

The terms _array_, _JSON object_, _number_, _string_, and _boolean_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].


## 2. GeoJSON-LD and the `navPlace` Property


### 2.1 GeoJSON

This extension implements the [GeoJSON-LD specification](https://geojson.org/geojson-ld/) and so its values follow the [GeoJSON](https://tools.ietf.org/html/rfc7946) conventions for Feature Collections. The possible geometric shapes are those defined by GeoJSON Feature `geometry` values.


#### 2.1.1 GeoJSON as Linked Data

The GeoJSON terms, the IIIF Presentation API 3 terms, and the `navPlace` term are all required linked data contexts for `navPlace` to be linked data compatible. This is elaborated upon in [section 3](#3-linked-data).



```json-doc
{
    "@context":[ 
       "http://iiif.io/api/extension/navplace/context.json",
       "http://iiif.io/api/presentation/3/context.json"
    ]
}
```


#### 2.1.2 Feature

A Feature object represents a spatial bounding. Every Feature object is a GeoJSON object.



*   A Feature object has a `type` property with the value "Feature".
*   A Feature object has a property with the name `geometry`. The value of the `geometry` property _SHALL_ be either a Geometry object as defined above or, in the case that the Feature is unlocated, a JSON null value.
*   A Feature object has a property with the name `properties`. The value of the `properties` property is an object (any JSON object or a JSON null value).
*   If a Feature has a commonly used identifier, that identifier _SHOULD_ be included as a property of the Feature object with the name `id`. The value _MUST_ be a string, and the value _MUST_ be an HTTP(S) URI [as defined by the IIIF Presentation API 3](https://iiif.io/api/presentation/3.0/#61-uri-recommendations). The `id` _MAY_ be the URI of a Feature Collection that contains the Feature with a unique fragment on the end.


#### 2.1.3 Feature Collection

A Feature Collection object represents an aggregation of spatial boundings.



*   A Feature Collection object has a `type` property with the value "FeatureCollection".
*   A Feature Collection object has a property with the name `features`. The value of `features` is a JSON array. Each element of the array is a Feature object as defined above. It is possible for this array to be empty, but when used in the context of this extension it _SHOULD NOT_ be empty.
*   If a Feature Collection has a commonly used identifier, that identifier _SHOULD_ be included as a property of the Feature Collection object with the name `id`. The value _MUST_ be a string, and the value _MUST_ be an HTTP(S) URI [as defined by the IIIF Presentation API 3](https://iiif.io/api/presentation/3.0/#61-uri-recommendations).

#### 2.1.4 Position

A position is the fundamental geometry construct and contains a `coordinates` property. A position is an array of numbers. There _MUST_ be two or more elements. The first two elements are longitude and latitude, or easting and northing, precisely in that order and using decimal numbers. Altitude or elevation _MAY_ be included as an optional third element.


#### 2.1.5 Table of Geometric Shapes

| Geometry Object  |    Description| 
|----|----|
| Point  |  The "coordinates" property is a single position| 
| MultiPoint |  The "coordinates" property is an array of positions| 
| LineString |  The "coordinates" property is an array of two or more positions| 
| MultiLineString   |   The "coordinates" property is an array of LineString coordinate arrays| 
| Polygon   |   The "coordinates" property _MUST_ be an array of linear ring coordinate arrays. For Polygons with more than one of these rings, the first _MUST_ be the exterior ring, and any others _MUST_ be interior rings. The exterior ring bounds the surface, and the interior rings (if present) bound holes within the surface.| 
| MultiPolygon  |   The "coordinates" property is an array of Polygon coordinate arrays| 
| GeometryCollection  | Has a property with the name "geometries". The value of "geometries" is an array. Each element of this array is a GeoJSON Geometry object. It is possible for this array to be empty. | 
{: .api-table}

For examples of these shapes, see the “Examples” section of the GeoJSON specification at [https://datatracker.ietf.org/doc/html/rfc7946#appendix-A](https://datatracker.ietf.org/doc/html/rfc7946#appendix-A)


### 2.2 `navPlace` Property

The `navPlace` property identifies a single or multiple geographic areas pertinent to a resource using a GeoJSON Feature Collection containing one or more Features. A Feature represents a shape by using the geographic coordinates supplied in the `geometry` property. The shape does not imply any level of precision, fuzziness, temporality or state of existence. 

The `navPlace` property can be used with the [IIIF Presentation 3 API Defined Types](https://iiif.io/api/presentation/3.0/#21-defined-types)



*   A Collection _MAY_ have the `navPlace` property.<br/>
   Clients _MAY_ render `navPlace` on a Collection.
*   A Manifest _MAY_ have the `navPlace` property.<br/>
   Clients _MAY_ render `navPlace` on a Manifest.
*   A Range _MAY_ have the `navPlace` property.<br/>
   Clients _MAY_ render `navPlace` on a Range.
*   A Canvas _MAY_ have the `navPlace` property.<br/>
   Clients _MAY_ render `navPlace` on a Canvas.
*   Other types of resource _MUST NOT_ have the `navPlace` property.<br/>
   Clients _SHOULD_ ignore `navPlace` on other types of resource.

The `navPlace` property's value follows a specific pattern.



*   The value _MUST_ be a single GeoJSON-LD Feature Collection and _SHOULD_ contain at least one Feature.
*   A Feature or Feature Collection that has the `id` property _MAY_ be accessible by the URI. 
*   Feature Collections and Feature objects inside of Feature Collections _MUST NOT_ be NULL. 
*   The value for `navPlace` _SHOULD_ be an embedded GeoJSON Feature Collection object. However, the value _MAY_ be a referenced GeoJSON Feature Collection. 
*   Feature Collections referenced in the `navPlace` property _MUST_ have the `id` and `type` properties.
*   The reference object _MUST NOT_ have the `features` property, such that clients are able to recognize that it should be retrieved in order to be processed.</br> 
`{"navPlace":{"id": "https://example.org/iiif/1/feature-collection", "type": "FeatureCollection"}}`


`navPlace` is intended to connect IIIF web resources with geographic areas. These areas _SHOULD_ be bounded discrete regions of the map akin to extents. For information on using the GeoJSON `properties` property to provide information associated with the geographic coordinates, see [Section 3.3](#33-context-considerations-for-geojson-ld-properties).

```json-doc
{
   "navPlace":{
      "id": "http://example.com/feature-collection/1",
      "type": "FeatureCollection",
      "features":[
         {
            "id": "http://example.com/feature/1",
            "type": "Feature",
            "properties":{},
            "geometry":{
               "type": "Point",
               "coordinates":[
                  9.94,
                  51.53
               ]
            }
         }
      ]
   }
}
```


## 3. Linked Data


### 3.1 Linked Data Context


*   The URI of the `navPlace` linked data context is [`http://iiif.io/api/extension/navplace/context.json`](http://iiif.io/api/extension/navplace/context.json)
*   The URI of the IIIF Presentation API 3 linked data context is [`http://iiif.io/api/presentation/3/context.json`](http://iiif.io/api/presentation/3/context.json)

The navPlace extension linked data context _MUST_ be included before the IIIF Presentation API 3 linked data context on the top-level object. The navPlace extension context file includes the [GeoJSON-LD context](https://geojson.org/geojson-ld/geojson-context.jsonld) through context scoping. This means the GeoJSON-LD context URI does not have to be explicitly included on the top level object, unless GeoJSON is used in other properties besides `navPlace`. It is important to note that since the IIIF Presentation API 3 context has the JSON-LD `@version` set to 1.1, all contexts are processed as JSON-LD 1.1.  

Consult the [Linked Data Context and Extensions section of IIIF Presentation API 3](https://iiif.io/api/presentation/3.0/#46-linked-data-context-and-extensions) for further guidance on use of the `@context` property.

### 3.2 Full Manifest Example

Here you can see an example of a IIIF Manifest with the `navPlace` property. It is made JSON-LD 1.1 compatible by including multiple contexts. Review the Manifest below in the [JSON-LD playground](https://json-ld.org/playground/) for an example of Linked Data processing. 



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
         "navPlace Extension Specification Example Manifest"
      ]
   },
   "items":[
      {
         "id":"https://example.org/iiif/canvas/p1",
         "type":"Canvas",
         "label":{
            "en":[
               "Picture of Göttingen taken during the 2019 IIIF Conference"
            ]
         },
         "type":"Canvas",
         "height":3024,
         "width":4032,
         "items":[
            {
               "id":"https://example.org/iiif/page/p1/1",
               "type":"AnnotationPage",
               "items":[
                  {
                     "id":"https://example.org/iiif/annotation/p0001-image",
                     "type":"Annotation",
                     "motivation":"painting",
                     "label":{
                        "en":[
                           "Picture of Göttingen"
                        ]
                     },
                     "body":{
              "id":"https://iiif.io/api/image/3.0/example/reference/918ecd18c2592080851777620de9bcb5-gottingen/full/max/0/default.jpg",
                        "type":"Image",
                        "format":"image/jpeg",
                        "height":3024,
                        "width":4032,
                        "service":[
                           {
                              "id":"https://iiif.io/api/image/3.0/example/reference/918ecd18c2592080851777620de9bcb5-gottingen",
                              "profile":"level1",
                              "type":"ImageService3"
                           }
                        ]
                     },
                     "target":"https://example.org/iiif/canvas/p1"
                  }
               ]
            }
         ]
      }
   ],
   "navPlace":{
      "id" : "https://example.org/iiif/feature-collection/2",
      "type":"FeatureCollection",
      "features":[
         {
            "id":"https://example.org/iiif/feature/2",
            "type":"Feature",
            "properties":{
               "label":{
                  "en":[
                     "navPlace Extension Specification Example Manifest"
                  ]
               }
            },
            "geometry":{
               "type":"Point",
               "coordinates":[
                  9.94,
                  51.53
               ]
            }
         }
      ]
   }
}
```


### 3.3 Context Considerations for GeoJSON-LD `properties`

The value of `properties` can be any JSON object and is used to supply additional information associated with the geographic coordinates. Terms used in `properties` _SHOULD_ be described either by [local linked data contexts](https://www.w3.org/TR/json-ld11/#dfn-local-context) or public [contexts endorsed by the IIIF community](https://iiif.io/api/extension/#abstract). Clients _SHOULD NOT_ assume synchronized contexts or vocabulary for terms found here. If a client discovers properties that it does not understand, then it _MUST_ ignore them.

## 4. Implementation Notes


### 4.1 GeoJSON-LD on the Web

The choice to use GeoJSON-LD is not arbitrary. It is the primary geocoordinate data format supported by web maps. Too often, poorly formatted datasets are programmatically transformed into GeoJSON as a shim into web maps in order to preserve the original data format. This specification drives implementers to have geocoordinate data saved as GeoJSON-LD when it is intended for use on the web. This practice removes barriers for interoperable geocoordinate data and standardized web map software as well as promotes the robust functionality of prior, current, and upcoming web map developments.


### 4.2 IIIF Cookbook

The [IIIF Cookbook](https://iiif.io/api/cookbook/) serves as a place to exemplify implementations of digital objects under IIIF Presentation API 3. At the release of this specification, recipes were already underway. You can see an implementation of the `navPlace` property as a "for demonstration only" preview at [https://preview.iiif.io/cookbook/0154-geo-extension/recipe/0154-geo-extension/](https://preview.iiif.io/cookbook/0154-geo-extension/recipe/0154-geo-extension/). This specification will update with links to recipes as they are published.

## Appendices

### A. Acknowledgements

An enormous amount of gratitude is owed to the IIIF community for their continuous engagement, innovative ideas, and feedback. Thanks to Sean Gilles and MapBox for the GeoJSON linked data context and its promotion of standardized geospatial web data. We would also like to recognize IETF for the semantics produced through the GeoJSON specification. An extra special thank you goes out to the IIIF Maps and IIIF Cookbook communities as implementers of this developing technology. The initial version of this document was the work of the IIIF Maps Technical Specification Group.
{: #acknowledgements}


### B. Change Log
{: #change-log}

| Date       | Description           |
| ---------- | --------------------- |
| 2021-06-01 | Initial commit        |
| 2021-06-28 | Updated copy over from Google Doc draft|
{: .api-table #table-changelog}

{% include acronyms.md %}

{% include links.md %}
