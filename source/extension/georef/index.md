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

This document will supply vocabulary and a linked data 1.1 context allowing for a JSON-LD pattern by which to extend Web Annotation and the IIIF Presentation API to support georeferencing.

We will adopt the [existing GeoJSON specification](https://datatracker.ietf.org/doc/html/rfc7946) for its linked data vocabulary and context for geographic coordinates. This means coordinates are expressed through the [WGS84](http://www.w3.org/2003/01/geo/wgs84_pos) coordinate reference system. As such, expressing the location of extraterrestrial entities is not supported by this technique.

### 1.2 Motivating Use Cases

A georeferencing extension for IIIF resources will enable the following use cases:

- Overlay IIIF image resources on a geographic map by rotating and stretching it. This transforming an image to make it fit on a map is also called _warping_.
- Stitching multiple images of map sheets together to form a single map.
- Georeference data can also be used to compute the exact geospatial area depicted on an image. This will enable geospatial indexing of IIIF resources and enabling them to be found by geospatial search engines.
- A georeferenced IIIF resource can be converted to a variety of GIS formats, like GeoTIFF, GeoJSON and XYZ map tiles.

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

### 2.1 Georeferencing
[Georeferencing](https://en.wikipedia.org/wiki/Georeferencing) is the process of mapping internal coordinates of a resource to geographic coordinates. For the purposes of this extension, references to "resource" equates to a IIIF [Canvas](https://iiif.io/api/presentation/3.0/#53-canvas) or [Image Service](https://iiif.io/api/presentation/3.0/#service) that contains one or more cartographic projections such as plans, maps and aerial photographs.

`[@BERT, @JULES, @BRYAN]` is "cartographic projection" a good word? Maybe confusing, projection also is used in "WGS84 projection" for example. Calling it "map" may also be confusing, because you overlay the "image" on the "map". We are trying to separate the "image of the earth" from the "cartographic system" giving it the ability to use coordinates.

`[@BRYAN] suggests` "...that contains one or more representations of cartographic information relative to modern Geographic Information Systems such as..."

### 2.2 Georeferencing Process

The process of georeferencing consists of the following steps:

`[@BRYAN]` should we rename pixel mask to resource mask? Or something similar?

`[@BRYAN] suggests` -- We renamed the property itself, but for the narrative maybe defining early on that it is a "selected area of a resource, referred to as a 'mask'" then we can just call it 'the mask' 

1. A pointer to a IIIF Canvas or Image Service, or a part of it. When a resource depicts multiple cartographic projections (such as inset maps) or when the resource contains non-cartographic parts (such as legends or borders), a pixel mask can be used to select the portion of the resource that belongs to a single cartographic projection. The shape of such a pixel mask can vary from a simple rectangle to a more complex polygon.
2. A mapping between the pixel coordinates of the IIIF resource and geographic WGS84 coordinates. This mapping consists of pairs of pixel coordinates and geographic coordinates. Each pair of coordinates is called a Ground Control Point (GCP). At least three GCPs are needed to enable clients to overlay a georeferenced IIIF resource on a map.
3. Optionally, a transformation algorithm can be defined that tells clients what algorithm should be used to turn the discrete set of GCPs into a function that can transform any of the IIIF resource pixel coordinates to geographic coordinates, and vice versa.

### 2.3 Required Data for Georeferencing

The following encoding is used to store the data needed by the steps above:

| Required data            | Encoding                                                       |
|--------------------------|---------------------------------------------------------------------|
| Resource and pixel mask  | IIIF Presentation API Canvas or Image API Image Service with an optional [SVG Selector](https://www.w3.org/TR/annotation-model/#svg-selector) or [Image API Selector](https://iiif.io/api/annex/openannotation/#iiif-image-api-selector) to specify a pixel mask |
| GCPs                     | A GeoJSON Feature Collection where each GCP is stored as a GeoJSON Feature with a Point geometry and a `resourceCoords` property in the Feature's `properties` object |
| Transformation algorithm | A `transformation` property defined on the GeoJSON Feature Collection that holds the GCPs |
{: .api-table #table-required-data}

## 3. Web Annotations for Georeferencing

Web Annotations can contain all of the required information mentioned in Section 2 and when they do we will refer to them as a "Georeferencing Annotation". We will describe how each piece of the Georeferencing Annotation is used and what its job is, followed by a full example.

### 3.1 Embedded vs. Referenced Targets and Resources

To supply a resource with georeferecing information, implementers _MUST_ add at least one Annotation Page to the `annotations` property. Implementers have the option to reference or embed those Annotation Pages. For the purposes of this extension, implementers _SHOULD_ embed the Annotation Pages in the `annotations` property as opposed to referencing them.

Georeferencing Annotations can exist independent of the resource they target and in such cases the resource is often only referenced via its URI in the Georeferencing Annotation's `target` property. For the purposes of this extension, implementers _SHOULD_ embed the Canvas or Image Service within the Georeferencing Annotation instead of referencing it.

Embedding resources reduces the need to make HTTP calls and increases the reliability of the included resources. Sometimes URIs do not resolve and in those cases it will not be possible to display or use those resources in georeferencing scenarios. Embedding the resources ensures each resource is available for georeferencing algorithms and viewers and ensures the metadata about the resource, such as height and width, remains consistent.

### 3.2 Georeferencing Annotation `motivation`

The `motivation` property is used by Georeferencing Annotations to understand the reason why the Annotation was created. The `motivation` property _SHOULD_ be included on all Georeferencing Annotations and when included its value _MUST_ be `georeferencing`.

Note that the linked data context provided with this document includes the formal linked data 1.1 motivation extension, and the vocabulary provided with this document contains the formal vocabulary for the "georeferencing" motivation discussed above.

### 3.3 Georeferencing Annotation `target`

The Georeferencing Annotation `target` is the resource to supply the `body` information to. Here the `target` _MUST_ either be an entire IIIF Canvas or Image Service, or an area of interest within a IIIF Canvas or Image Service represented as a [Specific Resource](https://www.w3.org/TR/annotation-model/#specific-resources). Viewers processing the georeferencing information require the original height and width of the resources in order to have the proper aspect ratios. Implementers _SHOULD_ supply this information with their embedded resources.

`[@BERT]` finish this section!
`[@BRYAN]` do you think including examples of different possible IIIF and SVG selectors is a good idea?
`[@BRYAN] suggests` I do not think having all the examples in here is a good idea.  We can say "there's too much variance to give examples of everything here.  For more examples, see 'The IIIF Georeferencing Guide'.  For more examples, see Implementation notes below for links.  See these from our /examples space. Something like that, but then we need to have a thing that lists examples."

Example of a Georeference Annotation with an ImageService `target`:

{% include api/code_header.html %}
```json-doc
"target": {
  "type": "SpecificResource",
  "source": {
    "@id": "https://cdm21033.contentdm.oclc.org/digital/iiif/krt/2891",
    "type": "ImageService2",
    "height": 2514,
    "width": 5965
  }
}
```

Example of a Georeference Annotation with a Canvas `target`:
`[@BRYAN]` should a Canvas be in a SpecificResource as well?

{% include api/code_header.html %}
```json-doc
"target": {
  "type": "Canvas",
  "height": 2514,
  "width": 5965,
  "items": [
    // single AnnotationPage with single painting annotation
    ...
  ]
},
```

It is important to maintain a link back to the Manifest for a given Canvas so clients consuming the Canvases have the opportunity to provide contextual information about the Manifest. To do this, implementers _SHOULD_ use the `partOf` property on the Canvas with as much information about the Manifest as is useful. For example,


{% include api/code_header.html %}
```json-doc
"target": {
  "type": "Canvas",
  ...
  "partOf": [{
    "id": "http://example.org/manifest/1",
    "type": "Manifest",
    "label": {
      "en": ["Useful Label"]
    }
  }]
}
```

`[@BRYAN]` can a ImageService target also have a `partOf` property?
`[@BRYAN] says` Yes, _ANY_ resource type can have a `partOf` property.

In cases where the `target` is not the entire Canvas or Image Service and is instead an area of interest, the selected area _MUST_ be supplied as part of the `target`. This is accomplished using a [Specific Resource](https://www.w3.org/TR/annotation-model/#specific-resources) where the `source` and `selector` can be supplied. You can use a IIIF Image Selector when the area of interest is a rectangle, or an SVG Polygon that... [@BERT what Polygons can and cannot be used?].  See the Specific Resource Example from the examples directory provided with this document.




[@BERT] tell about svg selector, and the shape of SVG. polygon, rect, no transforms, no <g>.
or iiif image selector
EXAMPLE!!

{% include api/code_header.html %}
```json-doc
"target": {
  "type": "SpecificResource",
  "source": {
    "id": "https://cdm21033.contentdm.oclc.org/digital/iiif/krt/2891",
    "type": "ImageService2",
    "profile": "http://iiif.io/api/image/2/level2.json"
  },
  "selector": {
    "type": "ImageApiSelector",
    "region": "810,900,260,370",
    "size": "5965,2514"
  }
}
```


SVgSelector link to



{% include api/code_header.html %}
```json-doc
"target": {
  "type": "SpecificResource",
  "source": {
    "@id": "https://cdm21033.contentdm.oclc.org/digital/iiif/krt/2891",
    "type": "ImageService2",
    "height": 2514,
    "width": 5965
  },
  "selector": {
    "type": "SvgSelector",
    "value": "<svg width=\"5965\" height=\"2514\"><rect x=\"59\" y=\"84\" width=\"5921\" height=\"2343\" /></svg>"
  }
}
```

{% include api/code_header.html %}
```json-doc
"target": {
  "type": "SpecificResource",
  "source": {
    "@id": "https://cdm21033.contentdm.oclc.org/digital/iiif/krt/2891",
    "type": "ImageService2",
    "height": 2514,
    "width": 5965
  },
  "selector": {
    "type": "SvgSelector",
    "value": "<svg width=\"5965\" height=\"2514\"><polygon points=\"59,84 44,2329 5932,2353 5920,103 \" /></svg>"
  }
}
```


`[@BERT @JULES @BRYAN]` The paragraph below will require some real focus.  If we really have these limits, we may have to say it in the section in pertains to and should/must language.


This specification expects that a single Image is painted on the Canvas and that the Images contain only a single cartographic depiction/representation. When the resource is a Canvas, it expects that the Image within the Canvas and the Canvas itself have the same `height` and `width` values. Further, it expects the Canvas or Image Service has only a single Annotation Page in the `annotations` property which supplies the georeferencing information.






However, it is possible for multiple Annotations within a single Annotation Page to target different, more specific areas of a single Image or Canvas. It is also possible for a Canvas to contain multiple unique Images. It is also possible that a single Canvas or Image Service have more than one Annotation Page in `annotations` whose Georeferencing Annotations target different areas of the resource. These situations can occur when a single Canvas or Image Service depicts multiple cartographic projections such as inset maps. Below is an image that exemplifies these scenarios.

<table border="0">
  <tr>
    <td>
      <figure>
        <img src="images/loc-acadia-np-original.jpg"
          alt="Original image (National Park Service map of Acadia National Park, from the Library of Congress)">
        <figcaption>Original image (National Park Service map of Acadia National Park, from the <a href="https://www.loc.gov/resource/g3732a.np000049/">Library of Congress</a>)</figcaption>
      </figure>
    </td>
    <td>
      <figure>
        <img src="images/loc-acadia-np-maps.jpg"
          alt="The same image with four pixel masks that capture the cartographic projections contained by the image">
        <figcaption>The same image with four pixel masks that capture the cartographic projections contained by the image</figcaption>
      </figure>
    </td>
  </tr>
</table>

### 3.4 Georeferencing Annotation `body`

The `body` of a Georeferencing Annotation contains geospatial information to apply to the resource noted in the `target` property.  For the purposes of this extension the `body` contains the GCPs.  The value for `body` _MUST_ be a GeoJSON Feature Collection.  The Feature Collection _MUST_ only contain Features with [Point](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.2) geometries, `[@BERT] is it _SHOULD_ or _MUST_` contain at least three Point Features as prescribed by [Section 2.2](#22-georeferencing-process). 


### 3.5 The `resourceCoords` Property

The `resourceCoords` property is defined by this document in order to supply the resource coordinates from the IIIF Canvas or Image Service with the WGS84 `coordinates` in a Feature to form a single GCP. Each Feature in the Feature Collection _MUST_ have the `resourceCoords` property in the `properties` property. The value is an array representing a resource coordinate at (x, y) and _MUST_ be exactly in that order. Here is an example of a Feature with the `resourceCoords` property:

{% include api/code_header.html %}
```json-doc
{
  "type": "Feature",
  "properties": {
    "resourceCoords": [5085, 782]
  },
  "geometry": {
    "type": "Point",
    "coordinates": [4.4885839, 51.9101828]
  }
}
```

### 3.6 The `transformation` Property

The `transformation` property is defined by this document in order to supply the preferred transformation algorithm that is used to create a complete mapping from pixel coordinates to geographic coordinates (and vice versa) based on a list of GCPs. The value for `transformation` is a JSON object which includes the properties `type` and `options`. The property _MAY_ be added to the Feature Collection used in the Georeferencing Annotation `body` and clients _MAY_ use the information in the object.

If a transformation algorithm is not provided, clients _SHOULD_ use their default algorithm if they are using a Georeferencing Annotation to transform between pixel coordinates and geographic coordinates. Similarly, if the supplied transformation algorithm is not implemented by a client, the default algorithm _SHOULD_ be used as well.

For more details about different transformation algorithms, see the [Implementation Notes](#6-implementation-notes) section.

The name of the preferred transformation algorithm is stored in the `type` property inside the `transformation` JSON object. Typical values include but are not limited to:

| Transformation type          | Description                                                       | Options  |
|------------------------------|-------------------------------------------------------------------|----------|
| `polynomial`                 | 1st, 2nd or 3rd order polynomial transformation                   | `order`  |
| `thinPlateSpline`            | Thin plate spline transformation, also known as _rubber sheeting_ | N/A      |
{: .api-table #table-transformation-types}

The `options` property is used to supply additional parameters related to the selected transformation type. If a transformation type does not have or need options, implementers _SHOULD NOT_ include the `options` property.

The table below describes all the different possible `order` values for the `polynomial` transformation type.

| Value | Description                                     |
|-------|-------------------------------------------------|
| `1`   | 1st order (linear) polynomial transformation    |
| `2`   | 2nd order (quadratic) polynomial transformation |
| `3`   | 3nd order (cubic) polynomial transformation     |

Other properties within `options`, including other transformation types not defined in this document, _SHOULD_ be described either by [registered IIIF API extensions](https://iiif.io/api/extension/) or [local linked data contexts](https://www.w3.org/TR/json-ld11/#dfn-local-context). If a client discovers properties that it does not understand, then it _MUST_ ignore them.

Example of a `transformation` JSON object:

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
              "options": {
                "order": 1
              }
            },
            "features": [
              {
                "type": "Feature",
                "properties": {
                  "resourceCoords": [5085, 782]
                },
                "geometry": {
                  "type": "Point",
                  "coordinates": [4.4885839, 51.9101828]
                }
              },
              {
                "type": "Feature",
                "properties": {
                  "resourceCoords": [5467, 1338]
                },
                "geometry": {
                  "type": "Point",
                  "coordinates": [4.5011785, 51.901595]
                }
              },
              {
                "type": "Feature",
                "properties": {
                  "resourceCoords": [2006, 374]
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
  "partOf": [{
    "id": "http://example.org/manifest/1",
    "type": "Manifest"
  }]
}
```

### 4.2 Full Georeferencing Annotation Example

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
    "partOf": [{
      "id": "http://example.org/manifest/1",
      "type": "Manifest"
    }]
  },
  "body": {
    "id": "http://iiif.io/api/extension/georef/examples/3/feature-collection.json",
    "type": "FeatureCollection",
    "transformation": {
      "type": "polynomial",
      "options": {
        "order": 1
      }
    },
    "features": [
      {
        "type": "Feature",
        "properties": {
          "resourceCoords": [5085, 782]
        },
        "geometry": {
          "type": "Point",
          "coordinates": [4.4885839, 51.9101828]
        }
      },
      {
        "type": "Feature",
        "properties": {
          "resourceCoords": [5467, 1338]
        },
        "geometry": {
          "type": "Point",
          "coordinates": [4.5011785, 51.901595]
        }
      },
      {
        "type": "Feature",
        "properties": {
          "resourceCoords": [2006, 374]
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
- The URI of the IIIF Presentation API linked data context is
`http://iiif.io/api/presentation/3/context.json`

The linked data context of this extension _MUST_ be included before the IIIF Presentation API linked data context on the top-level object. The extension linked data context file includes the [GeoJSON-LD context](https://geojson.org/geojson-ld/geojson-context.jsonld) through [context scoping](https://www.w3.org/TR/json-ld11/#dfn-scoped-context). This means the GeoJSON-LD context URI does not have to be explicitly included on the top level object. Note that since the IIIF Presentation API linked data context has the JSON-LD `@version` set to 1.1, all linked data contexts are processed as JSON-LD 1.1. It is also worth noting the linked data context for this extension also has `@version` set to 1.1. If this context is used in another setting, it will have the same behavior. JSON-LD 1.0 processors will throw a version error.

Consult the [Linked Data Context and Extensions section of IIIF Presentation API](https://iiif.io/api/presentation/3.0/#46-linked-data-context-and-extensions) for further guidance on use of the `@context` property.

## 6. Implementation Notes

`[@BERT @JULES @BRYAN]`
This section will likely link back to specific implementation notes as they relate to how the Allmaps viewer is processing this information to display it within a web map.

Briefly explain `transformation` algorithms, why you need 3 or more control points, perhaps examples to show different implementations. Mention IIIF Presentation API 2 and the presi 2 examples?? Mention GeoJSON sections on FeatureCollection, Feature, or position??

## Appendices

## Open source implementations

GCP-based image georeferencing is a common task that's available in many GIS applications. For example, the following open source applications provide this functionality:

- [GDAL](https://gdal.org/programs/gdaltransform.html)
- [QGIS](https://docs.qgis.org/3.22/en/docs/user_manual/working_with_raster/georeferencer.html)
- [Map Warper](https://github.com/timwaters/mapwarper)

Note that none of the tools listed above currently support georeferencing IIIF resources using Georeferencing Annotations.

### A. Acknowledgements

### B. Change Log