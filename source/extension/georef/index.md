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

The [IIIF Presentation API](https://iiif.io/api/presentation/3.0/) has the capability to support complex Web Annotations which can provide detailed and specific information regarding IIIF resources. You can see various use cases which implement such Web Annotations in the [IIIF Cookbook](https://iiif.io/api/cookbook/). Through the work of the [IIIF Maps](https://iiif.io/community/groups/maps/) and [IIIF Maps TSG](https://iiif.io/community/groups/maps-tsg/) groups, a commonality of techniques to georeference IIIF Canvases and Images in the context of a global map became evident, and a desire to have standards and best practices for georeferencing became known.

### 1.1 Objectives and Scope

This document will supply a Linked Data 1.1 context and JSON-LD pattern by which to extend Web Annotation and the IIIF Presentation API to support georeferening.

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

## 2. Georeferencing IIIF Resources

[Georeferening](https://editor.allmaps.org/#/) is the process of mapping internal coordinates of a resource to geographic coordinates. For the purposes of this extension, the resource is a IIIF [Canvas](https://iiif.io/api/presentation/3.0/#53-canvas) or [Image Service](https://iiif.io/api/presentation/3.0/#service) that contains one or more carthographic projections such as plans, maps and aerial photographs.

The process of georeferencing consists of the following steps:

1. The cartographic part of the resource is selected by means of a pixel mask. This accounts for the fact that resources often contain non-cartographic parts and may contain multiple cartographic projections that should be focused on individually. The shape of the mask varies from a simple rectangle to a complex polygon.
2. Three or more pixel coordinates of the resource are mapped on to geographic coordinates, in this case WGS84. Each pair of pixel coordinates and geographic coordinates is called a Ground Control Point (GCP).
3. Optionally, a preferred transformation algoritm is defined for interpolating other values, based on the GCPs. This may be used by clients to calculate the geographic coordinates of other pixel coordinates and vice versa.

To store the resulting data in a Web Annotation, the following encoding is used:

| Required Data                |  Data Encoding                                                      |
|------------------------------|---------------------------------------------------------------------|
| Resource                     |  IIIF Presentation API Canvas or Image API Service                  |
| Pixel Mask                   |  `selector` on the resource                                         |
| Pixel Coordinates            |  A new property called `pixelCoords`                                |
| Geographic coordinates       |  GeoJSON Feature Collection containing Point Features               |
| Transformation algorithm     |  `transformation` property within the Feature's `properties` object.|
{: .api-table #table-required-data}

The sections below will introduce the two new properties `pixelCoords` and `transformation`.

## 3. Web Annotations for Georeferencing

Web Annotations can contain all of the required information mentioned in Section 2. We will describe how each piece of the Web Annotation is used and what its job is, followed by a full example.

### 3.1 Embedded vs. Referenced Targets and Resources

To supply a resource with georeferecing information, implmenters _MUST_ add at least one Annotation Page to the `annotations` property.  Implementers have the option to reference or embed those Annotation Pages.  For the purposes of this extension, implementers _SHOULD_ embed the Annotation Pages in the `annotations` property as opposed to referencing them. This reduces the need to make HTTP calls to resolve the resource.

Web Annotations can exist independent of the resource they target and in such cases the resource is often only referenced via its URI in the Web Annotation's `target` property.  For the purposes of this extension, implmenters _SHOULD_ embed the Canvas or Image Service within the Web Annotation instead of referecing it. `[@BERT and @JULES]` a sentence about why? This reduces the need to make HTTP calls to resolve the resource, which is especially important for Canvases.

### 3.2 Web Annotation `motivation`

The `motivation` property is used by Web Annotations to understand the reason why the Annotation was created.  This document offers two defined Web Annotation Motivation Extensions, seen below.

`[@BERT and @JULES]` see https://www.w3.org/TR/annotation-model/#motivation-and-purpose

|Motivation Name               |  Description                                                           |
|------------------------------|------------------------------------------------------------------------|
| `georeferencing`             |  `[@BERT and @JULES]` The motivation for when the user intends to...   |
| `gcp-georeferecing`          |  `[@BERT and @JULES]` The motivation for when the user intends to...   |
{: .api-table #table-motivation-extension}

- The `motivation` property _SHOULD_ be included on all Web Annotations and when included its value _MUST_ be one of the strings listed above.

Note that the linked data context provided with this document includes the formal Linked Data 1.1 Motivation Extension, and the vocabulary provided with this document contains the formal vocabulary for the "Motvation Names" listed in the table above.

### 3.3 Web Annotation `target`

The Web Annotation `target` is the resource to supply the `body` information to.  In our case, the `target` _SHOULD_ be an IIIF Canvas or Image Service. It is important that viewers processing this information know the original height and width of the resources in order to have the proper aspect ratios. Implementers _SHOULD_ supply this information with their embedded resources.

It is important to maintain a link back to the Manifest for a given Canvas so clients consuming the Canvases have the opportunity to provide contextual information about the Manifest.  To do this, implementers _SHOULD_ use the `partOf` property on the Canvas with as much information about the Manifest as is useful.  For example,

{% include api/code_header.html %}
```json-doc
{
  "partOf": {
    "id": "http://example.org/manifest/1",
    "type": "Manifest",
    "label": {
      "en": ["Useful Label"]
    }
  }
}
```

In cases where the `target` is not the entire Canvas or Image Service and is instead an area of interest, the selected area _MUST_ be supplied as part of the `target`.  This is accomplished using a [Specific Resource](https://www.w3.org/TR/annotation-model/#specific-resources) where the `source` and `selector` can be supplied. `[@BERT and @JULES]` link to an example?

Note that it is possible for multiple Annotations within a single Annotation Page to target different, more specific areas of a single Image or Canvas.  It is also possible for a Canvas to contain multiple unique images.  It is also possible that a single Canvas or Image Service have more than one Annotation Page in `annotations`.    This usually occurs when the Image or Canvas contains multiple maps, or displays a single map with inset maps built in. Below is an image that exemplifies this scenario.

<table border="0">
  <tr>
    <td><img alt="Multi Map Example" src="images/loc-acadia-np-original.jpg"></td>
    <td><img alt="Multi Map Example" src="images/loc-acadia-np-maps.jpg"></td>
   </tr>
</table>

### 3.4 Web Annotation `body`

The `body` of a Web Annotation contains the data you would like to relate to some Canvas or IIIF Image Service. In our case, the `body` contains the GCPs and geocoordinates.  Since geocoordinates are encoded as GeoJSON-LD, the value for `body` _MUST_ be a GeoJSON Feature Collection.  The Feature Collection _MUST_ only contain Features with [Point](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.2) geometry, and each `geometry` property must contain the `coordinates` property.  The Feature Collection _SHOULD_ contain at least three point Features.

### 3.5 The `pixelCoords` Property

The `pixelCoords` property is defined by this document in order to supply the pixel coordinates from the IIIF Canvas or Image Service along with the WGS84 `coordinates` in the Features.  Each Point Feature in the Feature Collection _MUST_ have the `pixelCoords` property in the `properties` property.  The value is an array representing a pixel point at [x,y] and _MUST_ be precisely in that order. Here is an example of a Feature with the `pixelCoords` property:

{% include api/code_header.html %}
```json-doc
{
  "type": "Feature",
  "properties": {
    "pixelCoords": [5085, 782]
  },
  "geometry": {
    "type": "Point",
    "coordinates": [4.4885839, 51.9101828]
  }
}
```

### 3.6 The `transformation` Property

The `transformation` property is defined by this document in order to supply the preferred transformation algoritm. The value for `transformation` is a JSON Object which includes the properties `type` and `options`. The property _MAY_ be added to the Feature Collection used in the Web Annotation `body` and clients _MAY_ use the information in the object.

The value for `type` is a string, and typical values include but are not limited to:

`[@BERT and @JULES]`

|Transformation Types          |  Description                      |  Options                      |
|------------------------------|-----------------------------------|--------------------------------
| `polynomial`                 |  Lorem Ipusm and some other stuff | `order`
| `thinPlateSpline`            |  Lorem Ipusm and some other stuff | N/A
{: .api-table #table-transformation-types}

If an implementer chooses to use other transformation types, they _SHOULD_ supply the Linked Data Context terms and vocabulary for those types.  `[@Bryan]` See xyz for examples of more types.

The `options` property is used to supply additional parameters related to the selected transformation type. If a Transformation Type does not have or need options, implementers _SHOULD NOT_ include the `options` property.  Typically `options` will include an `order` property with one of the following values.

|Order Value                      |  Description                      |
|---------------------------------|-----------------------------------|
| 1                               |  Linear                           |
| 2                               |  Quadratic                        |
| 3                               |  Cubic                            |

Using other properties within `options` is permissable so long as a Linked Data context has been provided that properly defines the vocabulary of those properties.

Example of a `transformation` JSON Object:

{% include api/code_header.html %}
```json-doc
{
  "transformation": {
    "type": "polynomial",
    "options": {
      "order": 1
    }
  }
}
```

## 4. Full Examples

### 4.1 Full Canvas Example

{% include api/code_header.html %}
```json-doc
{
  "@context": [
    "http://iiif.io/api/extension/georef/1/context.json",
    "http://iiif.io/api/presentation/3/context.json"
  ],
  "id": "http://iiif.io/api/extension/georef/examples/3/georeferenced-canvas.json",
  "type": "Canvas",
  "label": {
    "nl": ["River Nieuwe Maas and Rotterdam's Havens"],
    "en": ["Guide to the New-Waterway"]
  },
  "height": 2514,
  "width": 5965,
  "items": [
    {
      "id": "http://iiif.io/api/extension/georef/examples/3/contentPage.json",
      "type": "AnnotationPage",
      "items": [
        {
          "id": "http://iiif.io/api/extension/georef/examples/3/content.json",
          "type": "Annotation",
          "motivation": "painting",
          "body": {
            "id": "https://cdm21033.contentdm.oclc.org/digital/iiif/krt/2891/full/full/0/default.jpg",
            "type": "Image",
            "format": "image/jpeg",
            "height": 2514,
            "width": 5965,
            "service": [
              {
                "@id": "https://cdm21033.contentdm.oclc.org/digital/iiif/krt/2891",
                "type": "ImageService2"
              }
            ]
          },
          "target": "http://iiif.io/api/extension/georef/examples/3/georeferenced-canvas.json"
        }
      ]
    }
  ],
  "annotations": [
    {
      "id": "http://iiif.io/api/extension/georef/examples/3/annotationPage.json",
      "type": "AnnotationPage",
      "items": [
        {
          "id": "http://iiif.io/api/extension/georef/examples/3/canvas-annotation.json",
          "type": "Annotation",
          "motivation": "georeferencing",
          "target": "http://iiif.io/api/extension/georef/examples/3/georeferenced-canvas.json",
          "body": {
            "id": "http://iiif.io/api/extension/georef/examples/3/feature-collection.json",
            "type": "FeatureCollection",
            "transformation": {
              "type": "polynomial",
              "order": 0
            },
            "features": [
              {
                "type": "Feature",
                "properties": {
                  "pixelCoords": [5085, 782]
                },
                "geometry": {
                  "type": "Point",
                  "coordinates": [4.4885839, 51.9101828]
                }
              },
              {
                "type": "Feature",
                "properties": {
                  "pixelCoords": [5467, 1338]
                },
                "geometry": {
                  "type": "Point",
                  "coordinates": [4.5011785, 51.901595]
                }
              },
              {
                "type": "Feature",
                "properties": {
                  "pixelCoords": [2006, 374]
                },
                "geometry": {
                  "type": "Point",
                  "coordinates": [4.405981, 51.9091596]
                }
              }
            ]
          }
        }
      ]
    }
  ],
  "partOf": {
    "id": "http://example.org/manifest/1",
    "type": "Manifest"
  }
}
```

### 4.2 Full Web Annotation Example

{% include api/code_header.html %}
```json-doc
{
  "@context": [
    "http://iiif.io/api/extension/georef/1/context.json",
    "http://iiif.io/api/presentation/3/context.json"
  ],
  "id": "http://iiif.io/api/extension/georef/examples/3/canvas-annotation.json",
  "type": "Annotation",
  "motivation": "georeferencing",
  "target": {
    "id": "http://iiif.io/api/extension/georef/examples/3/canvas.json",
    "type": "Canvas",
    "label": {
      "nl": ["River Nieuwe Maas and Rotterdam's Havens"],
      "en": ["Guide to the New-Waterway"]
    },
    "height": 2514,
    "width": 5965,
    "items": [
      {
        "id": "http://iiif.io/api/extension/georef/examples/3/contentPage.json",
        "type": "AnnotationPage",
        "items": [
          {
            "id": "http://iiif.io/api/extension/georef/examples/3/content.json",
            "type": "Annotation",
            "motivation": "painting",
            "body": {
              "id": "https://cdm21033.contentdm.oclc.org/digital/iiif/krt/2891/full/full/0/default.jpg",
              "type": "Image",
              "format": "image/jpeg",
              "height": 2514,
              "width": 5965,
              "service": [
                {
                  "@id": "https://cdm21033.contentdm.oclc.org/digital/iiif/krt/2891",
                  "type": "ImageService2"
                }
              ]
            },
            "target": "http://iiif.io/api/extension/georef/examples/3/canvas.json"
          }
        ]
      }
    ],
    "partOf": {
      "id": "http://example.org/manifest/1",
      "type": "Manifest"
    }
  },
  "body": {
    "id": "http://iiif.io/api/extension/georef/examples/3/feature-collection.json",
    "type": "FeatureCollection",

    "transformation": {
      "type": "polynomial",
      "order": 0
    },
    "features": [
      {
        "type": "Feature",
        "properties": {
          "pixelCoords": [5085, 782]
        },
        "geometry": {
          "type": "Point",
          "coordinates": [4.4885839, 51.9101828]
        }
      },
      {
        "type": "Feature",
        "properties": {
          "pixelCoords": [5467, 1338]
        },
        "geometry": {
          "type": "Point",
          "coordinates": [4.5011785, 51.901595]
        }
      },
      {
        "type": "Feature",
        "properties": {
          "pixelCoords": [2006, 374]
        },
        "geometry": {
          "type": "Point",
          "coordinates": [4.405981, 51.9091596]
        }
      }
    ]
  }
}
```

## 5. Linked Data Context

- The URI of this extension's linked data context is
`http://iiif.io/api/extension/georef/1/context.json`
- The URI of the IIIF Presentation API 3 linked data context is
`http://iiif.io/api/presentation/3/context.json`

The linked data context of this extension must be included before the IIIF Presentation API 3 linked data context on the top-level object. The extension linked data context file includes the [GeoJSON-LD context](https://geojson.org/geojson-ld/geojson-context.jsonld) through [context scoping](https://www.w3.org/TR/json-ld11/#dfn-scoped-context). This means the GeoJSON-LD context URI does not have to be explicitly included on the top level object. It is important to note that since the IIIF Presentation API 3 linked data context has the JSON-LD `@version` set to 1.1, all linked data contexts are processed as JSON-LD 1.1.  It is also worth noting the linked data context for this extension also has `@version` set to 1.1.  If this context is used in another setting, it will have the same behavior.  JSON-LD 1.0 processors will throw a version error.

Consult the [Linked Data Context and Extensions section of IIIF Presentation API 3](https://iiif.io/api/presentation/3.0/#46-linked-data-context-and-extensions) for further guidance on use of the `@context` property.

## 6. Implementation Notes

`[@BERT and @JULES]`
This section will likely link back to specific implementation notes as they relate to how the Allmaps viewer is processing this information to display it within a web map.

Briefly explain `transformation` algorithms, why you need 3 or more control points, perhaps examples to show different implementations.  Mention IIIF Presentation API 2 and the presi 2 examples??  Mention GeoJSON sections on FeatureCollection, Feature, or position??

## Appendices

`[@BERT]`

Examples/references:
- GDAL - https://gdal.org/programs/gdaltransform.html
- QGIS - https://docs.qgis.org/3.22/en/docs/user_manual/working_with_raster/georeferencer.html
- Map Warper - https://github.com/timwaters/mapwarper

### A. Acknowledgements

### B. Change Log