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


### 1.1. Objectives and Scope

IIIF provides the information necessary to allow a rich, online viewing environment for compound digital objects to be presented to a human user.  The types of resources and their specific needs continue to enhance the IIIF specifications to greater resource coverage.  The ability to assert ancillary information is a universal need in this expanse.  This is achieved using Annotation, or Web Annotation, and extensions across the IIIF specification versions.  

The ideas of Time and Place are a foundation of human communication and understanding.  In IIIF Presentation API 3 the property `navDate` allows for a calendar date to be associated with a resource in a client friendly format.  However, places are extents in space, independent of time or what may or may not be present in that space. Time and place are first class descriptors and the ability to capture both independently is often required to properly describe a resource.  

This extension describes a property called `navPlace` which contains geographic coordinates in the form of GeoJSON-LD.  GeoJSON-LD uses the WGS84 coordinate system, and so coordinates follow the rules of that geodetic system. Note the importance of the order of coordinates within Feature `coordinates` objects. Clients may use this property to leverage the navigational functionality of web maps such as Google Earth, Leaflet, OpenLayers, etc. giving them the opportunity to enrich data presentation through common web map platforms.  


### 1.2. Motivating Use Cases

The reason for applying geographic coordinates to a resource varies greatly.  This extension does not intend to meet the data requirements for all geospatial practices.  Use cases within the scope include



*   Link a IIIF resource to a single or multiple geographic areas on a map
*   Supply a single geographic bounding box for an image of a map
*   Track locations listed in an itinerary or travel journal

Use cases outside the scope include



*   Spatiotemporal alignment as in a timeline
*   Georeferencing to overlay maps or warp maps into coordinate space.
*   3D spatial representation
*   Geospatial data for resource fragments


## 2. GeoJSON-LD and the `navPlace` Property


### 2.1 GeoJSON

This extension implements the GeoJSON-LD specification and so its values follow the [GeoJSON](https://tools.ietf.org/html/rfc7946) conventions for Feature Collections. The possible geometric shapes are those defined by GeoJSON Feature `geometry` values.  All coordinates are WGS84 compliant, and no other coordinate system can be used.


#### 2.1.1 GeoJSON as Linked Data

The GeoJSON terms, the navPlace term and the IIIF Presentation API 3 terms are all required for `navPlace` to be linked data compatible.  Any IIIF resource using the navPlace property _MUST_ have the navPlace extension context and the IIIF Presentation API 3 context as part of the top level object.  This is elaborated upon in section 3.


```json-doc
{
    "@context":[ 
       "http://iiif.io/api/extension/navPlace-context.jsonld",
       "https://iiif.io/api/presentation/3/context.json"
    ]

}
```



#### 2.1.2 Feature

A Feature object represents a spatially bounded thing.  Every Feature object is a GeoJSON object.



*   A Feature object has a "type" member with the value "Feature".
*   A Feature object has a member with the name "geometry".  The value of the geometry member SHALL be either a Geometry object as defined above or, in the case that the Feature is unlocated, a JSON null value.
*   A Feature object has a member with the name "properties".  The value of the properties member is an object (any JSON object or a JSON null value).
*   If a Feature has a commonly used identifier, that identifier _SHOULD_ be included as a member of the Feature object with the name "id", and the value of this member is either a JSON string or number.


#### 2.1.3 Feature Collection

A FeatureCollection object has a member with the name `features`.  The value of `features` is a JSON array. Each element of the array is a Feature object as defined above.  It is possible for this array to be empty, but when used in the context of this extension _SHOULD NOT_ be empty.  It is also possible for this array to be extremely complex.  `navPlace` is intended to connect resources with geographic areas.  These areas should be bounded discrete regions of the map akin to extents.  navPlace is not meant for geographic layouts at the township, city, country or continental level.  Such descriptive datasets are meant for processing algorithms to determine complicated geospatial outcomes or overlays.  This goes beyond what navPlace and software consuming navPlace intend to support.  


#### 2.1.4 Position

A position is the fundamental geometry construct and contains a `coordinates` member.  A position is an array of numbers.  There MUST be two or more elements.  The first two elements are longitude and latitude, or easting and northing, precisely in that order and using decimal numbers.  Altitude or elevation MAY be included as an optional third element.


#### 2.1.5 Table of Geometric Shapes

| Geometry Object  |    Description| 
|----|----|
| Point  |  The " coordinates" member is a single position| 
| MultiPoint |  The "coordinates" member is an array of positions| 
| LineString |  The "coordinates" member is an array of two or more positions| 
| MultiLineString   |   The "coordinates" member is an array of LineString coordinate arrays| 
| Polygon   |   The "coordinates" member MUST be an array of linear ring coordinate arrays. For Polygons with more than one of these rings, the first MUST be the exterior ring, and any others MUST be interior rings. The exterior ring bounds the surface, and the interior rings (if present) bound holes within the surface.| 
| MultiPolygon  |   The "coordinates" member is an array of Polygon coordinate arrays| 
| GeometryCollection  | Has a member with the name "geometries". The value of "geometries" is an array. Each element of this array is a GeoJSON Geometry object. It is possible for this array to be empty. | 
{: .api-table}

For examples of these shapes, see the “Examples” section of the GeoJSON specification at [https://datatracker.ietf.org/doc/html/rfc7946#appendix-A](https://datatracker.ietf.org/doc/html/rfc7946#appendix-A)


### 2.2 navPlace Property

The `navPlace` property identifies a single or multiple geographic areas pertinent to a Collection, Manifest, Range or Canvas.  The JSON value of navPlace _MUST_ be a supported GeoJSON Feature Collection and _SHOULD_ contain at least one Feature.  The Feature represents a shape using geographic coordinates for the geometry and described terms for metadata from the resource such as a label.



*   The value _MUST_ be a single GeoJSON-LD FeatureCollection and _MUST_ contain at least one Feature.  
*   The Feature Collection that is the value of `navPlace` _MAY_ have an id.  
*   The Features within the Feature Collection _MAY_ have an id, and the id _MAY_  be the URI of the Feature Collection with a unique fragment on the end.  
*   A Feature or Feature Collection that has the id property _MAY_ be accessible by the URI. 
*   Feature Collections and Feature objects inside of Feature Collections _MUST NOT_ be NULL. 
*   The `navPlace` property _MUST NOT_ be used on other IIIF resource types
*   The value for navPlace _SHOULD_ be an embedded GeoJSON Feature Collection object.  However, the value _MAY_ be referenced and in these cases _MUST_ be dereferencable.  See the [terminology section](https://iiif.io/api/presentation/3.0/#12-terminology) of the IIIF Presentation API 3 for an explanation of “referenced”.


```json-doc
"navPlace":
{
   "id": "http://example.com/featurecollection/1",
   "type": "FeatureCollection",
   "features":[
      {
       "id": "http://example.com/feature/1",
         "type": "Feature",
         "properties":{
            "label":{
               "en":[
                  "IIIF compatible label"
               ]
            }
         },
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
```


Clients may use this property for navigational purposes on open web map systems.  These resources will ultimately be represented as geometric shapes on the interfaces of these systems.


## 3. Linked Data


### 3.1 Linked Data Context

The GeoJSON-LD context and navPlace extension context  _MUST_ be included before the IIIF Presentation API 3 context on the top-level object.



*   The URI of the GeoJSON-LD linked data context is <code>[http://geojson.org/geojson-ld/geojson-context.jsonld](http://geojson.org/geojson-ld/geojson-context.jsonld)</code>
*   The URI of the navPlace linked data context extension is

    ```
    http://iiif.io/api/extension/navPlace-context/context.json
    ```


*   The URI of the IIIF Presentation API 3 linked data context extension is

    ```
    http://iiif.io/api/extension/navPlace-context/context.json
    ```


Consult the Linked Data Context and Extensions section of IIIF Presentation API 3 for further guidance on use of the `@context` property.  It is important to note that since the IIIF Presentation API 3 context has the JSON-LD `@version` set to 1.1, all contexts are processed as JSON-LD 1.1.  It is also worth noting that the navPlace extension context includes GeoJSON-LD context through context scoping.


### 3.2  Full Manifest Example

Here you can see an example of a IIIF Manifest with the navPlace property.  It is made JSON-LD 1.1 compatible by including multiple contexts.  Review the Manifest below in the Linked Data 1.1 playground for an example of Linked Data processing. 


```json-doc
{
   "@context":[
      "http://iiif.io/api/extension/navPlace-context/context.json",
      "http://iiif.io/api/presentation/3/context.json"
   ],
   "id":"https://example.org/iiif/manifest/1",
   "type":"Manifest",
   "label":{
      "en":[
         "Picture of Göttingen taken during the 2019 IIIF Conference"
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
      "type":"FeatureCollection",
      "features":[
         {
            "id":"https://example.org/iiif/geo.json",
            "type":"Feature",
            "properties":{
               "label":{
                  "en":[
                     "Photograph from Göttingen, Germany"
                  ]
               }
            },
            "geometry":{
               "type":"Point",
               "coordinates":[
                  -77.036871,
                  38.907226
               ]
            }
         }
      ]
   }
}
```



### **3.4** **Context Considerations for GeoJSON-LD <code>properties</code></strong>

The GeoJSON `properties` object is generic and can be nearly anything. It is used to pass metadata along with the geographic coordinates.  Web maps know to look to `properties` for metadata to render along with the shape made by the geographic coordinates.  IIIF encourages interoperability, which is made possible in large part due to Linked Data.  Any metadata used in `properties` _SHOULD_ be described by a Linked Data context.  Note that common metadata terms like `label` and `summary` are already described by the IIIF Presentation API 3 context.  The use of IIIF formatted metadata in `properties` is encouraged since it is well described by the IIIF Presentation API 3 context already.  Note that if a client discovers properties that it does not understand, then it _MUST_ ignore them.  You can see this functionality by including your own metadata in the `properties` member of the example Manifest and taking it to the LD 1.1 playground.


## 4. Implementation Notes


### 4.1 GeoJSON-LD on the Web

The choice to use GeoJSON-LD is not arbitrary.  It is the primary geocoordinate data format supported by web maps.  Too often, poorly formatted datasets are programmatically transformed into GeoJSON as a shim into web maps in order to preserve the original data format.  This specification drives implementers to have geocoordinate data saved as GeoJSON-LD when it is intended for use on the web. This practice removes barriers for interoperable geocoordinate data and standardized web map software as well as promotes the robust functionality of prior, current, and upcoming web map developments.


### 4.2 IIIF Cookbook

The IIIF Cookbook serves as a place to exemplify complex digital objects under IIIF Presentation API 3.  You can see an implementation of the `navPlace` property there at [https://preview.iiif.io/cookbook/0154-geo-extension/recipe/0154-geo-extension/](https://preview.iiif.io/cookbook/0154-geo-extension/recipe/0154-geo-extension/).


## 5. Acknowledgements

An enormous amount of gratitude is owed to the IIIF community for their continuous engagement, innovative ideas, and feedback.  Thanks to Sean Gilles and MapBox for the GeoJSON Linked Data context and its promotion of standardized geospatial web data. We would also like to recognize IETF for the semantics produced through the GeoJSON specification. An extra special thank you goes out to the IIIF Maps and IIIF Cookbook communities as implementers of this developing technology. The initial version of this document was the work of the IIIF Maps Technical Specification Group.




## Appendices

### A. Acknowledgements
{: #acknowledgements}


### B. Change Log
{: #change-log}

| Date       | Description           |
| ---------- | --------------------- |
| 2021-06-01 | Initial commit        |
{: .api-table #table-changelog}

{% include acronyms.md %}

{% include links.md %}
