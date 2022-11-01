---
title: Georeferencing Extension
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

The [IIIF Presentation API 3](https://iiif.io/api/presentation/3.0/) has the capability to support complex Web Annotations which can provide detailed and specific information regarding IIIF resources. You can see various use cases which implement such Web Annotations in the IIIF Cookbook. Through the work of IIIF Maps, a commonality of techniques to georeference IIIF Canvases and Images in the context of a global map became evident, and a desire to have standards and best practices for georeferencing became known.

### 1.1 Objectives and Scope

This document will supply a Linked Data 1.1 context and JSON-LD pattern by which to extend Web Annotation and the IIIF Presentation API in support of georeferenced resources.

We will adopt the [existing GeoJSON specification](https://datatracker.ietf.org/doc/html/rfc7946) for its Linked Data vocabulary and context for geographic coordinates. This means coordinates are expressed through the [WGS84](http://www.w3.org/2003/01/geo/wgs84_pos) coordinate reference system. As such, expressing the location of extraterrestrial entities is not supported by this technique.  

### 1.2 Motivating Use Cases

- overlay iiif images on a map, which may include warping the image
- stitching multiple maps together
- geospatial area, enabling them to be found by search engines with geospatial coordinates
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
The main process for georeferencing a IIIF resources involves connecting image coordinates in pixels to WGS84 geographic coordinates over a projection of the surface of the Earth. The main pieces of data required to do this are 

- Image -- A IIIF Image API service, or raw IIIF Image
- Ground Control Points (GCP) -- WGS82 geographic coordinate points represented as GeoJSON Features
- Pixel Mask -- The specific pixel region of the Image to display as they relate to the WGS84 GCPs represented by a `selector` on the Image
- Transformation -- The specific transformation type and order to apply to the coordinate conversion
  
A new property, `transformation` is described by this document in order to supply the Transformation mentioned here. The value for `transformation` is a JSON Object which includes the properties `type` and `order`. The property _MUST_ be added to the Feature Collection used in the Annotation `body`.

- `type` is the type of transformation, which can be "linear", "polynomial", or ??
- `order` is the ?? of transformation, which can be ??

All of the other information can already be supplied through the Web Annotation.

## 3. [Web Annotations for Georeferencing](https://www.w3.org/TR/annotation-model/)

Web Annotations can contain all of the required information mentioned in Section 2. We will describe how each piece of the Web Annotation is used and what its job is, followed by a full example.

### Embedded vs. Referenced Targets and Resources
Web Annotations can exist independent of the resource they target. The resource they target is often only referenced in the Web Annotation.  For the purposes of this extension, implmenters _SHOULD_ embed the target within the Web Annotation instead of referecing it. This reduces the need to make HTTP calls to resolve the resource, which is especially important for Canvas resources.  Likewise, resources that record the Web Annotations pertinent to the resource via the `annotations` property have the option to be referenced or embedded.  For the purposes of this extension, implementers _SHOULD_ embed the Annotation Lists in the `annotations` property as opposed to referencing them.

### Annotation `motivation` and `purpose`
The `motivation` and `purpose` properties are used by Web Annotations to understand the reasons why the Annotation was created, or why the `body` was included in the Annotation.  These properties _SHOULD_ be included, and when they are included they _MUST_ be "georeferencing" or "gcp-georeferecing".

### Annotation `body`
The `body` of an Annotation contains the data you would like to relate to some web resource. In our case, the `body` must contain the transformation information, the GCPs, and the Pixel Mask. We do this through a GeoJSON-LD Feature Collection where each Feature contains the pixel coordinate information and the GCP those pixels relate to. The transformation information is supplied as its own property on the Feature Collection. As such, the transformation _MUST_ be the same for each feature. See the `body` in the example at the end of this section.

### Annotation `target`
The Annotation `target` is the resource to supply the `body` information to.  In our case, the `target` _SHOULD_ be an IIIF Canvas or Image Service. It is important that viewers processing this information know the original height and width of the resources in order to have the proper aspect ratios. Implementers _SHOULD_ supply this information via an embedded resource as opposed to a referenced resource.

In cases where the `target` is not the entire resource and is instead an area of interest, the selected area must be supplied as part of the target.  This is accomplished using a [Specific Resource]() where the `source` and `selector` can be supplied. See the `target` in the example at the end of this section

### 4. Full Examples

#### 4.1 Full Web Annotation Example
{% include api/code_header.html %}
```json-doc
{
   "@context":[
      "http://iiif.io/api/extension/georef/1/context.json",
      "http://iiif.io/api/presentation/3/context.json"
   ],
   "id":"http://iiif.io/api/extension/georef/examples/specific-image-service-2-svg-annotation.json",
   "type":"Annotation",
   "motivation":"georeferencing",
   "target":{
      "id":"http://iiif.io/api/extension/georef/examples/specific-image-service.json",
      "type":"SpecificResource",
      "source":{
         "@id":"https://cdm21033.contentdm.oclc.org/digital/iiif/krt/2891",
         "type":"ImageService2",
         "height":2514,
         "width":5965
      },
      "selector":{
         "type":"SvgSelector",
         "value":"<svg width=\"5965\" height=\"2514\"><polygon points=\"59,84 44,2329 5932,2353 5920,103 \" /></svg>"
      }
   },
   "body":{
      "id":"http://iiif.io/api/extension/georef/examples/feature-collection.json",
      "type":"FeatureCollection",
      "purpose":"gcp-georeferencing",
      "transformation":{
         "type":"polynomial",
         "order":0
      },
      "features":[
         {
            "type":"Feature",
            "properties":{
               "pixelCoords":[
                  5085,
                  782
               ]
            },
            "geometry":{
               "type":"Point",
               "coordinates":[
                  4.4885839,
                  51.9101828
               ]
            }
         },
         {
            "type":"Feature",
            "properties":{
               "pixelCoords":[
                  5467,
                  1338
               ]
            },
            "geometry":{
               "type":"Point",
               "coordinates":[
                  4.5011785,
                  51.901595
               ]
            }
         },
         {
            "type":"Feature",
            "properties":{
               "pixelCoords":[
                  2006,
                  374
               ]
            },
            "geometry":{
               "type":"Point",
               "coordinates":[
                  4.405981,
                  51.9091596
               ]
            }
         }
      ]
   }
}
```

#### 4.2 Full Canvas Example
{% include api/code_header.html %}
```json-doc
{
   "@context":[
      "http://iiif.io/api/extension/georef/1/context.json",
      "http://iiif.io/api/presentation/3/context.json"
   ],
   "id":"http://iiif.io/api/extension/georef/examples/georeferenced-canvas.json",
   "type":"Canvas",
   "label":{
      "nl":[
         "River Nieuwe Maas and Rotterdam's Havens"
      ],
      "en":[
         "Guide to the New-Waterway"
      ]
   },
   "height":2514,
   "width":5965,
   "items":[
      {
         "id":"http://iiif.io/api/extension/georef/examples/contentPage.json",
         "type":"AnnotationPage",
         "items":[
            {
               "id":"http://iiif.io/api/extension/georef/examples/content.json",
               "type":"Annotation",
               "motivation":"painting",
               "body":{
                  "id":"https://cdm21033.contentdm.oclc.org/digital/iiif/krt/2891/full/full/0/default.jpg",
                  "type":"Image",
                  "format":"image/jpeg",
                  "height":2514,
                  "width":5965,
                  "service":[
                     {
                        "@id":"https://cdm21033.contentdm.oclc.org/digital/iiif/krt/2891",
                        "type":"ImageService2"
                     }
                  ]
               },
               "target":"http://iiif.io/api/extension/georef/examples/georeferenced-canvas.json"
            }
         ]
      }
   ],
   "annotations":[
      {
         "id":"http://iiif.io/api/extension/georef/examples/annotationPage.json",
         "type":"AnnotationPage",
         "items":[
            {
               "id":"http://iiif.io/api/extension/georef/examples/canvas-annotation.json",
               "type":"Annotation",
               "motivation":"georeferencing",
               "target":"http://iiif.io/api/extension/georef/examples/georeferenced-canvas.json",
               "body":{
                  "id":"http://iiif.io/api/extension/georef/examples/feature-collection.json",
                  "type":"FeatureCollection",
                  "purpose":"gcp-georeferencing",
                  "transformation":{
                     "type":"polynomial",
                     "order":0
                  },
                  "features":[
                     {
                        "type":"Feature",
                        "properties":{
                           "pixelCoords":[
                              5085,
                              782
                           ]
                        },
                        "geometry":{
                           "type":"Point",
                           "coordinates":[
                              4.4885839,
                              51.9101828
                           ]
                        }
                     },
                     {
                        "type":"Feature",
                        "properties":{
                           "pixelCoords":[
                              5467,
                              1338
                           ]
                        },
                        "geometry":{
                           "type":"Point",
                           "coordinates":[
                              4.5011785,
                              51.901595
                           ]
                        }
                     },
                     {
                        "type":"Feature",
                        "properties":{
                           "pixelCoords":[
                              2006,
                              374
                           ]
                        },
                        "geometry":{
                           "type":"Point",
                           "coordinates":[
                              4.405981,
                              51.9091596
                           ]
                        }
                     }
                  ]
               }
            }
         ]
      }
   ],
   "partOf":{
      "id":"http://example.org/manifest/1",
      "type":"Manifest"
   }
}
```

## 5. Linked Data Context
- The URI of this extension's linked data context is 
`http://iiif.io/api/extension/georef/1/context.json`
- The URI of the IIIF Presentation API 3 linked data context is 
`http://iiif.io/api/presentation/3/context.json`

The linked data context of this extension must be included before the IIIF Presentation API 3 linked data context on the top-level object. The extension linked data context file includes the [GeoJSON-LD context]() through [context scoping](). This means the GeoJSON-LD context URI does not have to be explicitly included on the top level object. It is important to note that since the IIIF Presentation API 3 linked data context has the JSON-LD @version set to 1.1, all linked data contexts are processed as JSON-LD 1.1.

Consult the [Linked Data Context and Extensions section of IIIF Presentation API 3]() for further guidance on use of the `@context` property.

## 6. Implementation Notes
Not sure we need this.  The way this is designed, we will have said everything that would belong here I think.

## Appendices
Examples/references:
- GDAL
- QGIS
- Map Warper

### A. Acknowledgements

### B. Change Log

