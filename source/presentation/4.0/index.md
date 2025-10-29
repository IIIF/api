---
title: "Presentation API 4.0"
title_override: "IIIF Presentation API 4.0"
id: presentation-api
layout: spec
cssversion: 3
tags: [specifications, presentation-api]
major: 4
minor: 0
patch: 0
pre:
redirect_from:
  - /presentation/index.html
  - /presentation/4/index.html
editors:
  - name: Michael Appleby
    ORCID: https://orcid.org/0000-0002-1266-298X
    institution: Yale University
  - name: Tom Crane
    ORCID: https://orcid.org/0000-0003-1881-243X
    institution: Digirati
  - name: Robert Sanderson
    ORCID: https://orcid.org/0000-0003-4441-6852
    institution: J. Paul Getty Trust
  - name: Dawn Childress
    ORCID: https://orcid.org/0000-0003-2602-2788
    institution: UCLA
  - name: Julie Winchester
    ORCID: https://orcid.org/0000-0001-6578-764X
    institution: Duke University
  - name: Jeff Mixter
    ORCID: https://orcid.org/0000-0002-8411-2952
    institution: OCLC
hero:
  image: ''
---

<style>
.content, .api-content .highlight, .api-content .code-header {
  max-width:100%;
}

pre.highlight code {
  font-size:0.9rem;
  line-height:1.0;
}

.content h3 {
  font-size:1.4rem
}

.highlight .s2 {
  color: #a0f0f0
}
</style>

# Status of this Document
{:.no_toc}
__This Version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest Stable Version:__ [{{ site.data.apis.presentation.latest.major }}.{{ site.data.apis.presentation.latest.minor }}.{{ site.data.apis.presentation.latest.patch }}][prezi-stable-version]

__Previous Version:__ [3.0][prezi30]

**Editors:**

{% include api/editors.md editors=page.editors %}

{% include copyright.md %}

----

# Introduction

The purpose of the IIIF Presentation API specification is to provide a [model](model) and JSON serialization format of that model.

It provides a document format---the IIIF Manifest---for cultural heritage organizations (and anyone else) to present objects in a standardized, interoperable way. This allows compatible software such as viewers and annotation tools to load and present complex digital objects on the web from thousands of different providers.

**If you have existing images, audio, video and models on the web, you can easily provide IIIF Manifests for them by publishing the appropriate JSON documents.**

The IIIF Presentation API is concerned with enabling user experiences---providing enough information to present objects in compatible software, and leaving the meaning of the objects to external descriptive metadata standards.

This document acts as an introduction to the specification through a set of typical (but non-exhaustive) use cases. The [Presentation API 4.0 Properties](model) document provides the formal specification of the model and terms used in this introduction.

## IIIF Use cases

1. **Artwork** - a Manifest that represents a painting, comprising a single image and accompanying display information.
2. **Book** - a Manifest that represents a digitized bound volume made up many separate images in order. The IIIF model provides structural elements to indicate the chapters. The text of the book is made available in machine-readable form as Web Annotations.
3. **Periodical** - a IIIF Collection that provides multiple child Collections and Manifests, representing the publication run of a newspaper over many years. The IIIF model provides structural elements to indicate individual articles and other elements.
4. **45 Single** - a Manifest that represents the digitized audio from the two sides of a vinyl 7 inch record.
5. **Movie** - a Manifest that represents the digitized video of a film. A transcript of the audio is provided as Web Annotations, and additional machine-readable files provide subtitles and captions.
6. **Simple 3D Model** - a Manifest that publishes a single 3D model.
7. **Complex Scene** - a Manifest that publishes a complex 3D scene comprising multiple models, lights and cameras.
8. **Storytelling in 3D** - a Manifest that defines a sequence of states in a complex scene for the purposes of guiding a user through a particular experience.

These use case were chosen as a broad sample to introduce IIIF concepts. Many more use cases are provided as recipes in the [IIIF Cookbook](link).


> TODO Consider diagrams


# Foundations

This section is what you need to know to make sense of the examples that follow it.

<p style="float: right">
  <img src="{{ site.api_url | absolute_url }}/assets/images/data-model.png" alt="Data Model" width="400"><br/>
</p>


## Manifests

A Manifest is the primary unit of distribution of IIIF. Each Manifest usually describes how to present an object, such as a book, statue, music album or 3 dimensional scene. It is a JSON document that carries information needed for the client to present content to the user, such as a title and other descriptive information. The scope of what constitutes an object, and thus its Manifest, is up to the publisher of that Manifest. The Manifest contains sufficient information for the client to initialize itself and begin to display something quickly to the user.

The Manifest's `items` property is an ordered list of _Containers_ of _Content Resources_ (images, 3D models, audio, etc). Client software loads the Manifest and presents each Container's Content Resources. The client software also presents user interface controls to navigate the list of Content Containers.

Manifests have descriptive, technical and linking properties. The required properties of Manifests are `id`, `type`, `items` and `label`. Other commonly used properties include `summary`, `metadata`, `rights`, `thumbnail`, `homepage` and `provider`.

(👀) [Model Documentation](model/#manifest)


```jsonc
{
  "@context": "http://iiif.io/api/presentation/4/context.json",
  "id": "https://iiif.io/api/cookbook/recipe/0001-mvm-image/manifest.json",
  "type": "Manifest",
  "label": {
    "en": [ "Single Image Example" ]
  },
  "items": [
    // A list of Containers
  ]
}
```



## Containers

A Container is a frame of reference that allows the relative positioning of Content Resources, a concept borrowed from standards like PDF and HTML, or applications like Photoshop and PowerPoint, where an initially blank display surface has images, video, text and other content "painted" on to it. The frame is defined by a set of dimensions, with different types of Container having different dimensions. This specification defines three sub-classes of Container: Timeline (which only has a duration), Canvas (which has bounded height and width, and may have a duration), and Scene (which has infinite height, width and depth, and may have a duration).

The required properties of all Containers are `id`, and `type`. Most Containers also have the `items` and `label` properties. Further properties are required for the different types of Container.

The defined Container types are:

### Timeline

A Container that represents a bounded temporal range, without any spatial coordinates. It is typically used for audio-only content.

Timelines have an additional required property of `duration`, which gives the extent of the Timeline as a floating point number of seconds.

```json
{
  "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/timeline",
  "type": "Timeline",
  "duration": 32.76,
  "items": [
    {
      "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/page/p1",
      "type": "AnnotationPage",
      "items": [
        {
          "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/annotation/t1",
          "type": "Annotation",
          "motivation": [ "painting" ],
          "body": {
            "id": "https://iiif.io/api/presentation/example-content-resources/audio/clip.mp3",
            "type": "Audio",
            "format": "audio/mp3",
            "duration": 32.76
          },
          "target": "https://example.org/iiif/presentation/examples/manifest-with-containers/timeline"
        }
      ]
    }
  ]
}
```

### Canvas

A Container that represents a bounded, two-dimensional space, optionally with a bounded temporal range. Canvases are typically used for Image and Video content.

Canvases have two additional required properties: `height` and `width`, which give the spatial extent as integers. Canvases may also have the `duration` property in the same manner as Timelines.

```json
{
  "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/canvas",
  "type": "Canvas",
  "width": 12000,
  "height": 9000,
  "items": [
    {
      "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/page/p2",
      "type": "AnnotationPage",
      "items": [
        {
          "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/annotation/c1",
          "type": "Annotation",
          "motivation": [ "painting" ],
          "body": {
            "id": "https://iiif.io/api/presentation/example-content-resources/image/painting.jpg",
            "type": "Image",
            "format": "image/jpeg",
            "width": 4000,
            "height": 3000
          },
          "target": "https://example.org/iiif/presentation/examples/manifest-with-containers/canvas"
        }
      ]
    }
  ]
}
```

### Scene

A Container that represents a boundless three-dimensional space, optionally with a bounded temporal range. Scenes are typically used for rendering 3D models, and can additionally have Cameras and Lights.

Scenes may also have the `duration` property in the same manner as Timelines.

```json
{
  "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/scene",
  "type": "Scene",
  "items": [
    {
      "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/page/p3",
      "type": "AnnotationPage",
      "items": [
        {
          "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/annotation/s1",
          "type": "Annotation",
          "motivation": [ "painting" ],
          "body": {
            "id": "https://iiif.io/api/presentation/example-content-resources/models/astronaut.glb",
            "type": "Model",
            "format": "model/gltf-binary"
          },
          "target": "https://example.org/iiif/presentation/examples/manifest-with-containers/scene"
        }
      ]
    }
  ]
}
```

Scenes can have time-based and image content in them as well as 3D content. See model for how to do this.

[👀 Model Documentation](model/#containers)


## Annotations


IIIF uses the concept of _Annotation_ to link resources together from around the web. This specification uses a World Wide Web Consortium (W3C) standard for this called the [Web Annotation Data Model][org-web-anno]. This is a structured linking mechanism useful for making comments about Content Resources, but IIIF's primary use of it is to associate the images, audio and other Content Resources with their Containers for presentation.

In each of the three Containers above, an **Annotation** links the Container to a Content Resource. The Content Resource in the `body` property is _painted_ into the Container by an Annotation whose `target` property is the `id` of the Container. In all three simple cases here the `target` property is the `id` of the Container with no further qualification.

Different uses of Annotation are distinguished through their `motivation` property. This specification defines a value for `motivation` called `painting` for associating Content Resources with Containers, which this specification calls a Painting Annotation. The verb "paint" is also used to refer to the associating of a Content Resource with a Container by a Painting Annotation. This is from the notion of painting onto a canvas, a metaphor borrowed from art and used for image-based digital applications, and expanded by IIIF into "painting" any Content Resource into a Container of any number of dimensions.

The same linking mechanism is also used in IIIF with other motivations for transcriptions, commentary, tags and other content. This provides a single, unified method for aligning content, and provides a standards-based framework for referencing parts of resources. As Annotations can be added later, it promotes a distributed system in which further content such as commentary can be aligned with the objects published on the web.

Annotations are grouped within the `items` property of an Annotation Page, and the `items` property of the Container is a list of Annotation Pages. This allows consistent grouping of Annotations when required.

(👀) [Model Documentation](model/#Annotations)


## Content Resources

Content Resources are external web resources, including images, video, audio, 3D models, data, web pages or any other format. Typically these are the resources that will be painted into a Container using a Painting Annotation.

In addition to the required properties `id` and `type`, other commonly used properties include `format`, and `width`, `height` and `duration` as appropriate to the Content Resource format. The values of these properties are often the source of the equivalent Container properties.

(👀) [Model Documentation](model/#ContentResources)

### Containers as Content Resources

Containers may also be treated as Content Resources and painted into other Containers. This allows composition of content, such as painting a Canvas bearing a Video into a Scene, or painting a 3D model along with its associated Lights into an encompassing Scene. This capability is described further in [nesting](#nesting).

### Referencing Parts of Resources

A common scenario is to refer to only part of a resource, either a Container or a Content Resource. There are two primary methods for achieving this: adding a fragment to the end of the URI for the resource, or creating a Specific Resource that describes the method for selecting the desired part.

Parts of resources on the Web can be identified using URIs with a fragment component that both describes how to select the part from the resource, and, as a URI, also identifies it. In HTML this is frequently used to refer to part of the web page, called an anchor. The URI with the fragment can be used in place of the URI without the fragment in order to refer to this part.

There are different types of fragment based on the format of the resource. The most commonly used type in IIIF is the W3C's Media Fragments specification, as it can define a temporal and 2D spatial region.

```json
{
  "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/comments/c1",
  "type": "Annotation",
  "motivation": [ "commenting" ],
  "body": {
    "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/bodies/koto-body",
    "type": "TextualBody",
    "value": "Koto with a cover being carried",
    "language": "en",
    "format": "text/plain"
  },
  "target": "https://example.org/iiif/presentation/examples/manifest-with-containers/canvas#xywh=6050,3220,925,1250"
}
```

Here the Canvas `id` from the earlier example is still the `target` of an Annotation, but it has been qualified to a specific region of that Canvas by a URI fragment `#xywh=6050,3220,925,1250`. Note that the x, y, w, and h are in the Canvas coordinate space, not the image pixel dimensions space. This annotation has no knowledge of or dependency on the particular image we painted onto the Canvas; we could replace that image with one of a different, higher resolution without affecting this annotation or the region of the Canvas it targets.


### Specific Resource

URIs with fragments are insufficient for complex referencing, like circular regions or arbitrary text spans, and do not support other useful features such as describing styling or transformation. The Web Annotation Data Model introduces a class called `SpecificResource` that represents the resource in a specific context or role, which IIIF uses to describe these more complex requirements.

Several different classes of Selector are used in IIIF, including an alternative implementation of the fragment pattern called `FragmentSelector`. The fragment is given in the `value` property of the `FragmentSelector`, and the resource it should be applied to is given in `source`.

The required properties of Specific Resources are `id`, `type`, and `source`. Other commonly used properties include `selector`, `transform`, and `scope`.

The fragment example above can be expressed using a Specific Resource:

```json
{
  "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/comments/c1",
  "type": "Annotation",
  "motivation": [ "commenting" ],
  "body": {
    "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/bodies/koto-body",
    "type": "TextualBody",
    "value": "Koto with a cover being carried",
    "language": "en",
    "format": "text/plain"
  },
  "target": {
    "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/resources/koto-sr",
    "type": "SpecificResource",
    "source":  {
      "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/canvas",
      "type": "Canvas"
    },
    "selector": {
      "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/selectors/koto-selector",
      "type": "FragmentSelector",
      "value": "xywh=6050,3220,925,1250"
    }
  }
}
```

## Navigational Resources

### Collection

IIIF Collections are ordered lists of Manifests, Collections, and/or Specific Resources. Collections allow these resources to be grouped in a hierarchical structure for navigation and other purposes.

:eyes:

### Range

IIIF Ranges are used to represent structure _WITHIN_ a Manifest beyond the default order of the Containers in the `items` property. Example uses include newspaper sections or articles, chapters within a book for a table of contents, or movements within a piece of music. Ranges can include Containers, parts of Containers via Specific Resources or fragment URIs, or other Ranges, creating a tree structure like a table of contents. The typical intent of adding a Range to the Manifest is to allow the client to display a linear or hierarchical navigation interface to enable the user to quickly move through the object's content.

:eyes:



# Image Content

## Use Case 1: Artwork with deep zoom

This example is a Manifest with one Canvas, representing an artwork. The content resource, a JPEG image of the artwork, is associated with the Canvas via a Painting Annotation.

The unit integer coordinates of the Canvas (12000 x 9000) are not the same as the pixel dimensions of the JPEG image (4000 x 3000), but they are proportional - the Canvas has a 4:3 landscape aspect ratio, and so does the JPEG image.The `target` property of the Annotation is the Canvas `id`, unqualified by any particular region; this is taken to mean the content (the image) should fill the Canvas completely. As the Canvas and the image are the same aspect ratio, no distortion will occur. This approach allows the current image to be replaced by a higher resolution image in future, on the same Canvas. The Canvas dimensions establish a coordinate system for _painting annotations_ and other kinds of annotation that link content with the Canvas; they are not pixels of images.

The example demonstrates the use of the common descriptive properties `label` for the title of the artwork, `metadata` for additional information to display to the user, `summary` for a brief description of the artwork, `rights` to assert a rights statement or license from a controlled vocabulary, `homepage` to link to the artwork's specific web page, `thumbnail` to provide a small image to stand for the Manifest, `provider` to give information about the publisher of the Manifest, and finally, `service` to specify a IIIF Image API service that provides features such as deep zooming, derivative generation, image fragment referencing, rotation, and more.

```jsonc
{
  "@context": "http://iiif.io/api/presentation/4/context.json",
  "id": "https://iiif.io/api/cookbook/recipe/0001-mvm-image/manifest.json",
  "type": "Manifest",
  "label": {
    "en": [ "Use case 1: Artwork" ]
  },
  "metadata": [
    {
      "label": { "en": [ "Artist" ] },
      "value": { "en": [ "Anne Artist" ] }
    },
    {
      "label": { "en": [ "Date" ] },
      "value": { "en": [ "c. 1800" ] }
    }
  ],
  "summary":  { "en": [ "A longer piece of text to be shown when the metadata is not." ] },
  "rights": "http://rightsstatements.org/vocab/NoC-NC/1.0/",
  "homepage": [
    {
      "id": "https://example.org/works/artwork37",
      "type": "Text",
      "format": "text/html",
      "label": { "en": [ "Homepage for artwork37" ] }
    }
  ],
  "thumbnail": [
    {
      "id": "https://example.org/works/artwork37/thumbnail.jpg",
      "type": "Image",
      "format": "image/jpeg",
      "width": 100,
      "height": 150
    }
  ],
  "provider":
    [
      {
        "id": "https://example.org/about",
        "type": "Agent",
        "label": { "en": [ "Example Organization" ] },
        "homepage": [
          {
            "id": "https://example.org/",
            "type": "Text",
            "label": { "en": [ "Example Organization Homepage" ] },
            "format": "text/html"
          }
        ],
        "logo": [
          {
            "id": "https://example.org/images/logo.png",
            "type": "Image",
            "format": "image/png",
            "height": 100,
            "width": 120
          }
        ]
      }
    ],
  "items": [
    {
      "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/canvas",
      "type": "Canvas",
      "width": 12000,
      "height": 9000,
      "items": [
        {
          "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/page/p2",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/presentation/examples/manifest-with-containers/annotation/c1",
              "type": "Annotation",
              "motivation": [ "painting" ],
              "body": {
                "id": "https://iiif.io/api/presentation/example/image/painting/full/max/0/default.jpg",
                "type": "Image",
                "format": "image/jpeg",
                "width": 4000,
                "height": 3000,
                "service": [
                  {
                    "id": "https://iiif.io/api/presentation/example/image/painting",
                    "profile": "level1",
                    "type": "ImageService3",
                    // etc
                  }
                ]
              },
              "target": "https://example.org/iiif/presentation/examples/manifest-with-containers/canvas"
            }
          ]
        }
      ]
    }
  ]
}
```


>
**Key Points**
* All IIIF documents begin with the `@context` key, which maps the JSON structure into a linked data representation. The value identifies the version of the specification in use. [👀 Model Documentation](model/#json-ld-contexts-and-extensions)
* Every JSON object that has a `type` property also has an `id` property and vice versa.
* Text elements intended for display to the user are conveyed by _Language Maps_, JSON objects in which the keys are language codes and the values are lists of one or more strings in that language.  [👀 Model Documentation](model/#language-of-property-values)
* The Painting Annotation is a member of the `items` property of an Annotation Page. While in this case there is only one Annotation Page and one Annotation, the mechanism is needed for consistency when there are multiple Annotation Pages, and it allows for Annotation Pages in general to be separate resources on the web.
* The `metadata` label and value pairs are for display to the user rather than for machines to interpret.
* The `rights` property is always a single string value which is a URI.
* Any resource can have a `provider` property which a client can display to the user. This typically tells the user who the publisher is and how they might be contacted. The value of this property is an [Agent](model/#agent).
* The `service` property specifies a software application that a client might interact with to gain additional information or functionality, in this case, the IIIF Image API. Images in IIIF do not require an Image Service---we have included one here as an example, but do not include a service in the following image examples for brevity.
{: .note}

!!! warning TODO: The above should be a green class rgb(244,252,239) to distinguish from properties

__Definitions__<br/>
Classes: [Manifest](#model/Manifest), [Canvas](#model/Canvas), [AnnotationPage](#model/AnnotationPage), [Annotation](#model/Annotation), [Agent](#model/Agent)<br/><br/>
Properties: [id](#model/id), [type](#model/type), [label](#model/label), [metadata](#modle/metadata), [summary](#modle/summary), [rights](#model/rights), [homepage](#model/homepage), [thumbnail](#model/thumbnail), [provider](#model/provider), and [service](#model/Service)
{: .note}


## Use Case 2: Book

This example is a Manifest with multiple Canvases, each of which represents a page of a book. It demonstrates the use of the `behavior` property to indicate to a client that the object is _paged_---this helps a client generate the correct user experience. The `viewingDirection` property indicates that the book is read left-to-right. In this case, the property is redundant as `left-to-right` is the default value. The Manifest has a `rendering` property linking to a PDF representation; typically a client would offer this as a download or "view as" option. The `start` property is used to tell a client to initialize the view on a particular Canvas, useful if the digitized work contains a large amount of irrelevant front matter or blank pages. The `requiredStatement` is a message that a client MUST show to the user when presenting the Manifest.

```json
{
  "@context": "http://iiif.io/api/presentation/4/context.json",
  "id": "https://example.org/iiif/presentation/examples/manifest-with-book.json",
  "type": "Manifest",
  "label": { "en": [ "Use case 2: Book" ] },
  "behavior": [ "paged" ],
  "viewingDirection": "left-to-right",
  "rendering": [
    {
      "id": "https://example.org/pdfs/book.pdf",
      "type": "Text",
      "label": { "en": [ "PDF version" ] },
      "format": "application/pdf"
    }
  ],
  "start": {
    "id": "https://example.org/iiif/presentation/examples/manifest-with-book/canvas/c2",
    "type": "Canvas"
  },
  "requiredStatement": {
    "label": { "en": [ "Attribution" ] },
    "value": { "en": [ "Provided courtesy of Example Institution" ] }
  },
  "items": [
    {
      "id": "https://example.org/iiif/presentation/examples/manifest-with-book/canvas/c1",
      "type": "Canvas",
      "label": { "en": [ "Blank page" ] },
      "height": 4613,
      "width": 3204,
      "items": [
        {
          "id": "https://example.org/iiif/presentation/examples/manifest-with-book/page/p1",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/presentation/examples/manifest-with-book/annotation/a1",
              "type": "Annotation",
              "motivation": [ "painting" ],
              "body": {
                "id": "https://iiif.io/api/presentation/example-content-resources/image/page1.jpg",
                "type": "Image",
                "format": "image/jpeg",
                "height": 4613,
                "width": 3204,
                },
              "target": "https://example.org/iiif/presentation/examples/manifest-with-book/canvas/c1"
            }
          ]
        }
      ]
    },
    {
      "id": "https://example.org/iiif/presentation/examples/manifest-with-book/canvas/c2",
      "type": "Canvas",
      "label": { "en": [ "Frontispiece" ] },
      "height": 4613,
      "width": 3204,
      "items": [
        {
          "id": "https://example.org/iiif/presentation/examples/manifest-with-book/page/p2",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/presentation/examples/manifest-with-book/annotation/a2",
              "type": "Annotation",
              "motivation": [ "painting" ],
              "body": {
                "id": "https://iiif.io/api/presentation/example-content-resources/image/page2.jpg",
                "type": "Image",
                "format": "image/jpeg",
                "height": 4613,
                "width": 3204,
              },
              "target": "https://example.org/iiif/presentation/examples/manifest-with-book/canvas/c2"
            }
          ]
        }
      ]
    },
    {
      "id": "https://example.org/iiif/presentation/examples/manifest-with-book/canvas/c3",
      "type": "Canvas",
      "label": { "en": [ "Title Page" ] },
      "height": 4613,
      "width": 3204,
      "items": [
        {
          "id": "https://example.org/iiif/presentation/examples/manifest-with-book/page/p3",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/presentation/examples/manifest-with-book/annotation/a3",
              "type": "Annotation",
              "motivation": [ "painting" ],
              "body": {
                "id": "https://iiif.io/api/presentation/example-content-resources/image/page3.jpg",
                "type": "Image",
                "format": "image/jpeg",
                "height": 4613,
                "width": 3204,
              },
              "target": "https://example.org/iiif/presentation/examples/manifest-with-book/canvas/c3"
            }
          ]
        }
      ]
    },
    // Additional Canvases
  ]
}
```

>
**Key Points**
* Canvas labels are not required, but are recommended when a Manifest has more than one Canvas in order to provide visual labels for each Canvas for navigation within the IIIF client UI.
{: .note}

!!! warning TODO: The above should be a green class rgb(244,252,239) to distinguish from properties

__Definitions__<br/>
Classes: [Manifest](#model/Manifest), [Canvas](#model/Canvas)<br/><br/>
Properties: [behavior](#model/behavior), [viewingDirection](#model/viewingDirection), [start](#model/start), [rendering](#model/rendering), [requiredStatement](#model/requiredStatement)
{: .note}



## Use Case 3: Periodical

This example demonstrates the use of IIIF Collections to group Manifests into a hierarchy. In this case, there is a Collection for a run of the _The Tombstone Epitaph_, published from 1880 to 1920. This contains 41 child Collections each representing a year's worth of issues. The parent Collection and each of its child Collections use the `behavior` "multi-part" to signal that the Collections and their Manifests are part of a logical set. Each of the year Collections has one Manifest for each issue of the newspaper.

The top-level Collection has a `navPlace` property that could be used on a "Newspapers of America" map to allow users to view newspapers by location. Each Manifest has a `navDate` property that could be used to plot the issues on a timeline or calendar-style user interface. Within each Manifest, the `structures` property provides Ranges which are used to identify individual sections of the Newspaper, and individual stories within those sections, which may be spread across multiple columns and pages. Each story's Range includes the `supplementary` property to link to an Annotation Collection that provides the text of the story.

IIIF Collection with `behavior` "multi-part" that contains the individual "multi-part" Collections for each year/volume:

```json
{
  "@context": "http://iiif.io/api/presentation/4/context.json",
  "id": "https://example.org/iiif/periodical/collection.json",
  "type": "Collection",
  "label": { "en": [ "The Tombstone Epitaph (1880-1920)" ] },
  "behavior": [ "multi-part" ],
  "navPlace": {
    "id": "https://example.org/iiif/periodical/collection/place/1",
    "type": "FeatureCollection",
    "features": [
      {
        "id": "https://example.org/iiif/periodical/collection/feature/1",
        "type": "Feature",
        "properties": {
          "label": { "en": ["Tombstone, Cochise County, Arizona"] }
        },
        "geometry": {
          "type": "Point",
          "coordinates": [31.715940, −110.064827]
        }
      }
    ]
  },
  "items": [
    {
      "id": "https://example.org/iiif/periodical/multi-part-collection/v1.json",
      "type": "Collection",
      "label": { "en": [ "The Tombstone Epitaph, 1880" ] }
    },
    {
      "id": "https://example.org/iiif/periodical/multi-part-collection/v2.json",
      "type": "Collection",
      "label": { "en": [ "The Tombstone Epitaph, 1881" ] }
    },
    // Additional multi-part collections for each year/volume
  ]
}
```
IIIF Collection with `behavior` "multi-part" for the second volume (1881), with individual Manifests for each issue:

```json
{
  "@context": "http://iiif.io/api/presentation/4/context.json",
  "id": "https://example.org/iiif/periodical/multi-part-collection/v1.json",
  "type": "Collection",
  "label": { "en": [ "The Tombstone Epitaph, 1881" ] },
  "behavior": [ "multi-part" ],
  "items": [
    // Previous issues
    {
      "id": "https://example.org/iiif/periodical/multi-part-collection/issue1.json",
      "type": "Manifest",
      "label": { "en": [ "October 27, 1881" ] }
    },
    // Subsequent issues
  ]
}
```

Manifest for the October 27, 1881 issue, with Ranges for table of contents:

```json
{
  "@context": "http://iiif.io/api/presentation/4/context.json",
  "id": "https://example.org/iiif/periodical/multi-part-collection/issue1.json",
  "type": "Manifest",
  "label": { "en": [ "The Tombstone Epitaph, October 27, 1881" ] },
  "behavior": [ "paged" ],
  "navDate": "1881-10-27T00:00:00+00:00",
  "items": [
    {
      "id": "https://example.org/iiif/periodical/multi-part-collection/canvas/c1",
      "type": "Canvas",
      "label": { "en": [ "Page 1" ] },
      "height": 4613,
      "width": 3204,
      "items": [
        {
          "id": "https://example.org/iiif/periodical/multi-part-collection/page/p1",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/periodical/multi-part-collection/annotation/a1",
              "type": "Annotation",
              "motivation": [ "painting" ],
              "body": {
                "id": "https://example.org/image/page1.jpg",
                "type": "Image",
                "format": "image/jpeg",
                "height": 4613,
                "width": 3204,
                },
              "target": "https://example.org/iiif/periodical/multi-part-collection/canvas/c1"
            }
          ]
        }
      ]
    },
    {
      "id": "https://example.org/iiif/periodical/multi-part-collection/canvas/c2",
      "type": "Canvas",
      "label": { "en": [ "Page 2" ] },
      "height": 4613,
      "width": 3204,
      "items": [
        {
          "id": "https://example.org/iiif/periodical/multi-part-collection/page/p2",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/periodical/multi-part-collection/annotation/a2",
              "type": "Annotation",
              "motivation": [ "painting" ],
              "body": {
                "id": "https://example.org/image/page2.jpg",
                "type": "Image",
                "format": "image/jpeg",
                "height": 4613,
                "width": 3204,
                },
              "target": "https://example.org/iiif/periodical/multi-part-collection/canvas/c2"
            }
          ]
        }
      ]
    },
    // Additional Canvases
  ],
  "structures": [
    {
      "id": "https://example.org/iiif/periodical/multi-part-collection/range/r0",
      "type": "Range",
      "label": { "en": [ "October 27, 1881" ] },
      "items": [
        {
          "id": "https://example.org/iiif/periodical/multi-part-collection/range/r1",
          "type": "Range",
          "label": { "en": [ "Yesterday's Tragedy: Three Men Hurled Into Eternity In the Duration of a Moment" ] },
          "supplementary": { "id": "https://example.org/iiif/full-text-anno-collection", "type": "AnnotationCollection" },
          "items": [
            {
              "id": "https://example.org/iiif/periodical/multi-part-collection/canvas/c1",
              "type": "Canvas"
            },
            // Additional contents
          ]
        }
      ]
    }
  ]
}
```

>
**Key Points**
*
{: .note}

__Definitions__<br/>
Classes: [Collection](#model/Collection), [Range](#model/Range), [AnnotationCollection](#model/AnnotationCollection)<br/><br/>
Properties: [behavior](#model/behavior), [navPlace](#model/navPlace), [navDate](#model/navDate), [structure](#model/structures), [supplementary](#model/supplementary)
{: .note}

thumbnail-nav
sequence



# Audio and Video

## Use Case 4: A 45 single with 2 tracks

This example is a Manifest with two Timelines, each of which represent a temporal extent during which a song is played. As in most cases, the Timeline `duration` is the same length as that of Content Resource painted into it. This example is a recording digitized from a 45 RPM 7 inch single. It demonstrates the use of `format` for the audio files' content type, `language` (One song is in English and one is in German), `behavior` with value "auto-advance" that tells a client to automatically advance to the second Timeline after playing the first, `annotations` that link to Annotation Pages of annotations with the motivation `supplementing` that provide the lyrics (one example is given afterwards) - and an `accompanyingContainer` that carries a picture of the single's cover that is shown while the songs are playing.


```json
{
  "@context": "http://iiif.io/api/presentation/4/context.json",
  "id": "https://example.org/iiif/presentation/examples/manifest-with-audio.json",
  "type": "Manifest",
  "label": { "en": [ "Use case 3: 45 single with 2 tracks" ] },
  "behavior": [ "auto-advance" ],
  "accompanyingContainer": {
    "id": "https://example.org/iiif/presentation/examples/manifest-with-audio/accompany/c1",
    "type": "Canvas",
    "label": { "en": [ "Photo of cover sleeve" ] },
    "height": 900,
    "width": 900,
    "items": [
      {
        "id": "https://example.org/iiif/presentation/examples/manifest-with-audio/accompany/c1/page",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/presentation/examples/manifest-with-audio/accompany/c1/image",
              "type": "Annotation",
              "motivation": "painting",
              "body": {
                "id": "https://example.org/presentation/example-content-resources/image/cover.jpg",
                "type": "Image",
                "format": "image/jpeg",
                "height": 900,
                "width": 900
              },
              "target": "https://example.org/iiif/presentation/examples/manifest-with-audio/accompany/ac1"
            }
          ]
      }
    ]
  },
  "items": [
    {
      "id": "https://example.org/iiif/presentation/examples/manifest-with-audio/timeline/t1",
      "type": "Timeline",
      "label": { "en": [ "Side A: 99 Luftballons" ] },
      "duration": 231,
      "items": [
        {
          "id": "https://example.org/iiif/presentation/examples/manifest-with-audio/track/tr1",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/presentation/examples/manifest-with-audio/annotation/a1",
              "type": "Annotation",
              "motivation": [ "painting" ],
              "body": {
                "id": "https://example.org/presentation/example-content-resources/audio/track1.mp4",
                "type": "Sound",
                "format": "audio/mp4",
                "duration": 231,
                "language": [ "de" ],
                },
              "target": "https://example.org/iiif/presentation/examples/manifest-with-audio/timeline/t1"
            }
          ]
        }
      ]
    },
    {
      "id": "https://example.org/iiif/presentation/examples/manifest-with-audio/timeline/t2",
      "type": "Timeline",
      "label": { "en": [ "Side B: 99 Red Balloons" ] },
      "duration": 230.5,
      "items": [
        {
          "id": "https://example.org/iiif/presentation/examples/manifest-with-audio/track/tr2",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/presentation/examples/manifest-with-audio/annotation/a2",
              "type": "Annotation",
              "motivation": [ "painting" ],
              "body": {
                "id": "https://example.org/presentation/example-content-resources/audio/track2.mp4",
                "type": "Sound",
                "format": "audio/mp4",
                "duration": 230.5,
                "language": [ "en" ],
                },
              "target": "https://example.org/iiif/presentation/examples/manifest-with-audio/timeline/t2"
            }
          ]
        }
      ]
    }
  ],
  "annotations": [
    {
      "id": "https://example.org/iiif/presentation/examples/external-anno.json",
      "type": "AnnotationPage",
    }
  ]
}
```


```json
{
  "@context": "http://iiif.io/api/presentation/3/context.json",
  "id": "https://example.org/iiif/presentation/examples/external-anno.json",
  "type": "AnnotationPage",
  "items": [
    {
      "id": "https://example.org/iiif/presentation/examples/external-anno/a1",
      "type": "Annotation",
      "motivation": "supplementing",
      "body": {
        "id": "https://example.org/presentation/example-content-resources/lyrics1.txt",
        "type": "TextualBody",
        "language": "de",
        "format": "text/plain",
        "value": "Hast du etwas Zeit für mich?"
      },
      "target": "https://example.org/iiif/presentation/examples/manifest-with-audio/timeline/t1#t=3.5,6.8"
    }
  ],
  // (annotations for the rest of the song lines)
}
```

>
**Key Points**
* t vs. instant / verbose vs. append to URI???
{: .note}

!!! warning TODO: The above should be a green class rgb(244,252,239) to distinguish from properties

__Definitions__<br/>
Classes: [Manifest](#model/Manifest), [Timeline](#model/Timeline),[TextualBody](#model/TextualBody)<br/><br/>
Properties: [duration](#model/duration), [format](#model/format), [language](#model/language), [behavior](#model/behavior), [annotations](#model/annotations), [accompanyingContainer](#model/accompanyingContainer)
{: .note}


## Use Case 5: Movie with subtitles

This example is a Manifest with one Canvas that represents the temporal extent of the movie (the Canvas `duration`) and its aspect ratio (given by the `width` and `height` of the Canvas). The example demonstrates the use of a `Choice` annotation body to give two alternative versions of the movie, indicated by their `label` and `fileSize` properties as well as `height` and `width`. Subtitles are provided by an annotation that links to a VTT file. The motivation of this annotation is `supplementing` and the `provides` property of this annotation indicates what accessibility feature it provides, in this case the term `subtitles`. The `timeMode` property in this case is redundant as `trim` is the default value. The Canvas has a `placeholderContainer` that provides a poster image to show in place of the video file before the user initiates playback.

```json
{
  "@context": "http://iiif.io/api/presentation/4/context.json",
  "id": "https://example.org/iiif/presentation/examples/manifest-with-movie.json",
  "type": "Manifest",
  "label": { "en": [ "Use Case 4: Movie with Subtitles" ] },
  "items": [
    {
      "id": "https://example.org/iiif/presentation/examples/manifest-with-movie/canvas",
      "type": "Canvas",
      "height": 1080,
      "width": 1440,
      "duration": 3600,
      "timeMode": "trim",
      "placeholderContainer": {
        "id": "https://example.org/iiif/presentation/examples/manifest-with-movie/placeholder",
        "type": "Canvas",
        "height": 320,
        "width": 400,
        "items": [
          {
            "id": "https://example.org/image/placeholder/annopage",
            "type": "AnnotationPage",
            "items": [
              {
                "id": "https://example.org/iiif/presentation/examples/manifest-with-movie/placeholder/image",
                "type": "Annotation",
                "motivation": "painting",
                "body": {
                  "id": "https://example.org/image/placeholder.png",
                  "type": "Image",
                  "format": "image/png",
                  "height": 320,
                  "width": 400,
                },
                "target": "https://iiif.io/api/cookbook/recipe/0013-placeholderCanvas/canvas/donizetti/placeholder"
              }
            ]
          }
        ]
      },
      "items": [
        {
          "id": "https://example.org/iiif/presentation/examples/manifest-with-movie/annopage1",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/presentation/examples/manifest-with-movie/anno1",
              "type": "Annotation",
              "motivation": "painting",
              "body": {
                "type": "Choice",
                "items": [
                  {
                    "id": "https://example.org/video/movie-low.mp4",
                    "type": "Video",
                    "label": { "en": ["Low resolution (360 MB)" ]},
                    "height": 360,
                    "width": 480,
                    "duration": 3600,
                    "format": "video/mp4",
                    "fileSize": 360553219
                  },
                  {
                    "id": "https://example.org/video/movie-hi.mp4",
                    "type": "Video",
                    "label": { "en": ["High resolution (1.3 GB)" ]},
                    "height": 1080,
                    "width": 1440,
                    "duration": 3600,
                    "format": "video/mp4",
                    "fileSize": 1345876231
                  }
                ]
              },
              "target": "https://example.org/iiif/presentation/examples/manifest-with-movie/canvas"
            }
          ]
        }
      ],
      "annotations": [
        {
          "id": "https://example.org/iiif/presentation/examples/manifest-with-movie/subtitles",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/presentation/examples/manifest-with-movie/subtitles/anno",
              "type": "Annotation",
              "motivation": "supplementing",
              "body": {
                "id": "https://example.org/text/subtitles.vtt",
                "type": "Text",
                "format": "text/vtt",
                "provides": [ "subtitles" ],
                "label": {
                  "en": [
                    "Subtitles in WebVTT format"
                  ]
                },
                "language": "en"
              },
              "target": "https://example.org/iiif/presentation/examples/manifest-with-movie/canvas"
            }
          ]
        }
      ]
    }
  ]
}
```

>
**Key Points**
* The decision about which item in the `Choice` to play by default is client dependent. In the absence of any other decision process the client should play the first item. In this specific example, the user might make the decision after reading the `label`, or the client might make the decision based on the `fileSize` property and an assessment of the user's available bandwidth. However, the client may have no way of determining why the publisher has offered the choices, and should not prevent the user from making the choice. The cookbook demonstrates several uses of `Choice` for common image and AV use cases.
* Slop - impl note - don't interpret **very** minor discrepancies between `duration` on the different Choices and the Container `duration` as an instruction to stretch or compress the audio/video stream to match the Container duration. No real way to quantify this, just _be sensible_.
{: .note}


!!! warning TODO: The above should be a green class rgb(244,252,239) to distinguish from properties

__Definitions__<br/>
Classes: [Manifest](#model/Manifest), [Canvas](#model/Canvas), [Choice](#model/Choice)<br/><br/>
Properties: [fileSize](#model/fileSize), [format](#model/format), [provides](#model/provides), [timeMode](#model/timeMode), [behavior](#model/behavior), [placeholderContainer](#model/placeholderContainer)
{: .note}

# 3D

3D Content Resources are painted into Scenes.

Scenes have infinite height (y axis), width (x axis) and depth (z axis), where 0 on each axis (the origin of the coordinate system) is treated as the center of the scene's space.

The positive y axis points upwards, the positive x axis points to the right, and the positive z axis points forwards (a [right-handed cartesian coordinate system](https://en.wikipedia.org/wiki/Right-hand_rule)).

(image of coordinate system here)

## 3D Supporting Resources


Constructs from the domain of 3D graphics are expressed in IIIF as Resources. They are associated with Scenes via Painting Annotations in the same manner as Content Resources. They aid in or enhance the rendering of Content Resources, especially in Scenes.

### Cameras

A Camera provides a view of a region of the Scene's space from a particular position within the Scene; the client constructs a viewport into the Scene and uses the view of one or more Cameras to render that region. The size and aspect ratio of the viewport is client and device dependent.

There are two types of Camera, `PerspectiveCamera` and `OrthographicCamera`. The first Camera defined and not hidden in a Scene is the default Camera used to display Scene contents. If the Scene does not have any Cameras defined within it, then the client provides a default Camera. The type, properties and position of this default camera are client-dependent.


### Lights

There are four types of Light: AmbientLight, DirectionalLight, PointLight and SpotLight. They have a `color` and an `intensity`. SpotLight has an additional property of `angle` that determines the spread of its light cone.

If the Scene has no Lights, then the client provides its own lighting as it sees fit.


### Audio Emitters

There are three types of Audio emitter: AmbientAudio, PointAudio and SpotAudio. They have a `source` (an audio Content Resource) and a `volume`.

### Transforms

When painting resources into Scenes, it is often necessary to resize, rotate or move them relative to the coordinate space of the Scene. These operations are specified using three Transforms: ScaleTransform, RotateTransform and TranslateTransform. Each Transform has three properties, `x`, `y` and `z` which determine how the Transform affects that axis in the local coordinate space.

Transforms are added to a SpecificResource using the `transform` property, and there may be more than one applied when adding a model to a Scene. Different orders of the same set of transforms can have different results, so attention must be paid when creating the array and when processing it.


## Use Case 5: Simple 3D Model

This example is a Manifest with a single Scene, with a single model of a space suit painted at the Scene's origin.

> PNG of Scene

```jsonc
{
  "@context": "http://iiif.io/api/presentation/4/context.json",
  "id": "https://example.org/iiif/3d/model_origin.json",
  "type": "Manifest",
  "label": { "en": ["Single Model"] },
  "summary": { "en": ["Viewer should render the model at the scene origin, and then viewer should add default lighting and camera"] },
  "items": [
    {
      "id": "https://example.org/iiif/scene1/page/p1/1",
      "type": "Scene",
      "label": { "en": ["A Scene"] },
      "items": [
        {
          "id": "https://example.org/iiif/scene1/page/p1/1",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/3d/anno1",
              "type": "Annotation",
              "motivation": ["painting"],
              "body": {
                "id": "https://raw.githubusercontent.com/IIIF/3d/main/assets/astronaut/astronaut.glb",
                "type": "Model",
                "format": "model/gltf-binary"
              },
              "target": "https://example.org/iiif/scene1/page/p1/1"
            }
          ]
        }
      ]
    }
  ]
}
```

>
**Key Points**
* As this Scene only has one resource in it (the model), the client must provide lighting and a default camera.
* In this simplest use case, the Painting Annotation targets the whole Scene rather than a specific point. The client places the model's origin at the Scene's origin. This is in contrast to the _bounded_ Containers `Canvas` and `Timeline`, where the painted resource fills the Container completely.
{: .note}


## Use Case 5a: Simple 3D Model in Configured Scene

This example adds a Light and a Camera to the previous example, and places the model at a specific point rather than at the default origin position.

Annotations may use a type of Selector called a `PointSelector` to align the Annotation to a point within the Scene that is not the Scene's origin. PointSelectors have three spatial properties, `x`, `y` and `z` which give the value on that axis. They also have a temporal property `instant` which can be used if the Scene has a duration, which gives the temporal point in seconds from the start of the duration, the use of which is defined in the [section on Scenes with Durations]().

The Light is green and has a position, but has its default orientation of looking along the negative-y axis as no rotation has been specified. The Camera has a position and is pointing at the model's origin via the `lookAt` property. The Camera has a `fieldOfView` of 50. The `near` and `far` properties are included to ensure the model falls within the camera's range (although unnecessary in a simple Scene like this). The Scene has a background color.

<img src="{{ site.api_url | absolute_url }}/assets/images/p4/use-case-5a.png" alt="Use case 5a" >


```jsonc
 {
  "@context": "http://iiif.io/api/presentation/4/context.json",
  "id": "https://example.org/iiif/3d/model_origin.json",
  "type": "Manifest",
  "label": { "en": ["Single Model with light and Camera"] },
  "summary": { "en": ["Viewer should render the model at (-1,0,1), add the light, and base the viewport on the provided camera"] },
  "items": [
    {
      "id": "https://example.org/iiif/scene1/page/p1/1",
      "type": "Scene",
      "label": { "en": ["A Scene"] },
      "backgroundColor": "#FF00FE",
      "items": [
        {
          "id": "https://example.org/iiif/scene1/page/p1/1",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/3d/anno1",
              "type": "Annotation",
              "motivation": ["painting"],
              "body": {
                "id": "https://raw.githubusercontent.com/IIIF/3d/main/assets/astronaut/astronaut.glb",
                "type": "Model",
                "format": "model/gltf-binary"
              },
              "target": {
                "type": "SpecificResource",
                "source": [
                  {
                    "id": "https://example.org/iiif/scene1/page/p1/1",
                    "type": "Scene"
                  }
                ],
                "selector": [
                  {
                    "type": "PointSelector",
                    "x": -1.0,
                    "y": 1.0,
                    "z": 1.0
                  }
                ]
              }
            },
            {
              "id": "https://example.org/iiif/3d/anno2",
              "type": "Annotation",
              "motivation": ["painting"],
              "body": {
                "id": "https://example.org/iiif/3d/cameras/1",
                "type": "PerspectiveCamera",
                "label": {"en": ["Perspective Camera 1"]},
                "lookAt": {
                  "id": "https://example.org/iiif/3d/anno1",
                  "type": "Annotation"
                },
                "near": 1,
                "far": 100,
                "fieldOfView": 50
              },
              "target": {
                "type": "SpecificResource",
                "source": [
                  {
                    "id": "https://example.org/iiif/scene1/page/p1/1",
                    "type": "Scene"
                  }
                ],
                "selector": [
                  {
                    "type": "PointSelector",
                    "x": 0.0,
                    "y": 6.0,
                    "z": 10.0
                  }
                ]
              }
            },
            {
              "id": "https://example.org/iiif/3d/anno2",
              "type": "Annotation",
              "motivation": ["painting"],
              "body": {
                  "id": "https://example.org/iiif/3d/lights/1",
                  "type": "SpotLight",
                  "label": {"en": ["Spot Light 1"]},
                  "angle": 90.0,
                  "color": "#A0FFA0"
              },
              "target": {
                "type": "SpecificResource",
                "source": {
                  "id": "https://example.org/iiif/scene1/page/p1/1",
                  "type": "Scene"
                },
                "selector": [
                  {
                    "type": "PointSelector",
                    "x": 0.0,
                    "y": 3.0,
                    "z": 1.0
                  }
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}
```

>
**Key Points**
* This example uses some of the Scene-Specific resources introduced in the next section.
* A Point Selector explicitly places the model in the Scene via the Painting Annotation's `target` property. In the previous example, there was an implicit Point Selector placing the model at (0,0,0) because no explicit Point Selector was provided.
* The provided Light should replace any default lighting the client might have.
{: .note}

__Definitions__<br/>
Classes: [Manifest](#model/Manifest), [Scene](#model/Scene), [Model](#model/Model), [SpecificResource](#model/SpecificResource), [PointSelector](#model/PointSelector), [PerspectiveCamera](#model/PerspectiveCamera), [SpotLight](#model/SpotLight) <br/><br/>
Properties: [backgroundColor](#model/backgroundColor), [lookAt](#model/lookAt), [near](#model/near), [far](#model/far), [feildOfView](#model/fieldOfView), [angle](#model/angle), [color](#model/color)
{: .note}

## Use Case 6: Complex Scene

This example is a Manifest with a single Scene with multiple models painted into the Scene at specific positions with transforms applied. It represents a collection of chess game pieces with multiple pawns and a single queen. The example demonstrates painting multiple models into a Scene, including one Content Resource being painted into a Scene multiple times. Transforms and Point Selectors are used to establish position and scale for Annotations. Some external web resources referenced as Content Resources may include elements such as lights or audio that are undesirable within a Manifest, and the `exclude` property is used to prevent these from being rendered. The property `interactionMode` is used to guide clients in how to best guide or limit user interaction with rendered content.

```jsonc
{
  "@context": "http://iiif.io/api/presentation/4/context.json",
  "id": "https://example.org/iiif/3d/model_origin.json",
  "type": "Manifest",
  "label": { "en": ["Use Case 6: Complex Scene"] },
  "items": [
    {
      "id": "https://example.org/iiif/scene1/page/p1/1",
      "type": "Scene",
      "label": { "en": ["Chess Game Pieces"] },
      "interactionMode": ["hemisphere-orbit"],
      "items": [
        {
          "id": "https://example.org/iiif/scene1/page/p1/1",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/3d/anno1",
              "type": "Annotation",
              "motivation": ["painting"],
              "body": {
                "id": "https://raw.githubusercontent.com/IIIF/3d/main/assets/chess/pawn.glb",
                "label": {"en": ["Pawn 1"]},
                "type": "Model",
                "format": "model/gltf-binary"
              },
              "target": {
                "type": "SpecificResource",
                "source": {
                  "id": "https://example.org/iiif/scene1/page/p1/1",
                  "type": "Scene"
                },
                "selector": [
                  {
                    "type": "PointSelector",
                    "x": 1.0,
                    "y": 0.0,
                    "z": 0.0
                  }
                ]
              }
            },
            {
              "id": "https://example.org/iiif/3d/anno1",
              "type": "Annotation",
              "motivation": ["painting"],
              "body": {
                "type": "SpecificResource",
                "source": [
                  {
                    "id": "https://raw.githubusercontent.com/IIIF/3d/main/assets/chess/pawn.glb",
                    "label": {"en": ["Pawn 2 tipped over"]},
                    "type": "Model",
                    "format": "model/gltf-binary"
                  }
                ],
                "transform": [
                  {
                    "type": "RotateTransform",
                    "x": 0.0,
                    "y": 0.0,
                    "z": -90.0
                  },
                  {
                    "type": "Translate Transform",
                    "x": 0.0,
                    "y": 1.0,
                    "z": 0.0
                  }
                ]
              },
              "target": {
                "type": "SpecificResource",
                "source": {
                  "id": "https://example.org/iiif/scene1/page/p1/1",
                  "type": "Scene"
                },
                "selector": [
                  {
                    "type": "PointSelector",
                    "x": 2.0,
                    "y": 0.0,
                    "z": 3.0
                  }
                ]
              }
            },
            {
              "id": "https://example.org/iiif/3d/anno1",
              "type": "Annotation",
              "motivation": ["painting"],
              "exclude": ["Audio", "Lights"],
              "body": {
                "type": "SpecificResource",
                "source": [
                  {
                    "id": "https://raw.githubusercontent.com/IIIF/3d/main/assets/chess/queen.glb",
                    "label": {"en": ["Queen"]},
                    "type": "Model",
                    "format": "model/gltf-binary"
                  }
                ],
                "transform": [
                  {
                    "type": "ScaleTransform",
                    "x": 1.5,
                    "y": 1.5,
                    "z": 1.5
                  },
                ]
              },
              "target": {
                "type": "SpecificResource",
                "source": {
                  "id": "https://example.org/iiif/scene1/page/p1/1",
                  "type": "Scene"
                },
                "selector": [
                  {
                    "type": "PointSelector",
                    "x": 1.0,
                    "y": 0.0,
                    "z": 2.0
                  }
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}
```

>
**Key Points**
* Each Annotation is painted into the Scene at a different point via Point Selectors.
* The second Annotation represents a pawn game piece that is tipped over, and Transforms are used to achieve this. RotateTransform is used to tip the pawn over and TranslateTransform is used to align the bottom of the pawn with the coordinate origin's XY plane.
* The third Annotation represents a queen game piece that is scaled to be larger than the pawns using ScaleTransform.
* The `exclude` property instructs clients not to import or render any external audio or light content present in the Content Resource for the queen game piece.
* The `interactionMode` property instructs clients that, if possible, user interactions relating to orbiting the scene should be restricted to a hemisphere.
{: .note}

__Definitions__<br/>
Classes: [Manifest](#model/Manifest), [Scene](#model/Scene), [Model](#model/Model), [SpecificResource](#model/SpecificResource), [PointSelector](#model/PointSelector), [RotateTransform](#model/RotateTransform), [TranslateTransform](#model/TranslateTransform), [ScaleTransform](#model/ScaleTransform)<br/><br/>
Properties: [exclude](#model/exclude), [interactionMode](#model/interactionMode)
{: .note}

<!--

Is this still needed or wanted here?

### Chessboard is a Canvas with image (not a 3D chessboard)

A Scene or a Canvas may be treated as a content resource, referenced or described within the `body` of an Annotation. As with models and other resources, the Annotation is associated with a Scene into which the Scene or Canvas is to be nested through an Annotation `target`. The content resource Scene will be placed within the `target` Scene by aligning the coordinate origins of the two scenes. Alternately, Scene Annotations may use `PointSelector` to place the origin of the resource Scene at a specified coordinate within the `target` Scene.

-->

## Use Case 7: Another Complex Scene

What is it

### More on Point and Fragment Selectors

A content resource may be annotated into a Scene for a period of time by use of a PointSelector that is temporally scoped by a [FragmentSelector](https://www.w3.org/TR/annotation-model/#fragment-selector).  The FragmentSelector has a `value` property, the value of which follows the [media fragment syntax](https://www.w3.org/TR/media-frags/#naming-time) of `t=`.  This annotation pattern uses the `refinedBy` property [defined by the W3C Web Annotation Data Model](https://www.w3.org/TR/annotation-model/#refinement-of-selection).

```json
{
  "id": "https://example.org/iiif/3d/anno1",
  "type": "Annotation",
  "motivation": ["painting"],
  "body": {
      "id": "https://example.org/iiif/assets/model1.glb",
      "type": "Model"
  },
  "target": {
    "id": "https://example.org/iiif/selectors/model1-glb-sr",
    "type": "SpecificResource",
    "source": [
      {
        "id": "https://example.org/iiif/scene1",
        "type": "Scene"
      }
    ],
    "selector": [
      {
        "id": "https://example.org/uuid/9fbd580b-895b-41b9-974a-1553329037f2",
        "type": "PointSelector",
        "x": -1.0,
        "y": -1.0,
        "z": 3.0,
        "refinedBy": {
            "id": "https://example.org/uuid/3d0d097b-2b37-4a15-b6a5-506e417d5115",
            "type": "FragmentSelector",
            "value": "t=45,95"
        }
      }
    ]
  }
}
```

When using a URL fragment in place of a SpecificResource, the parameter `t` can be used to select the temporal region:

```json
{
    "id": "https://example.org/iiif/3d/anno1",
    "type": "Annotation",
    "motivation": ["painting"],
    "body": {
        "id": "https://example.org/iiif/assets/model1.glb",
        "type": "Model"
    },
    "target": "https://example.org/iiif/scene1#xyz=-1,-1,3&t=45,95"
}
```

An Annotation may target a specific point in time using a PointSelector's `instant` property.  The property's value must be a positive floating point number indicating a value in seconds that falls within the Scene's duration.

```json
{
    "id": "https://example.org/iiif/3d/anno1",
    "type": "Annotation",
    "motivation": ["painting"],
    "body": {
        "id": "https://example.org/iiif/assets/model1.glb",
        "type": "Model"
    },
    "target": {
        "type": "SpecificResource",
        "source": [
          {
            "id": "https://example.org/iiif/scene1",
            "type": "Scene"
          }
        ],
        "selector": [
            {
                "type": "PointSelector",
                "x": -1.0,
                "y": -1.0,
                "z": 3.0,
                "instant": 45.0
            }
        ]
    }
}
```

### Time mode

The Annotation's [`timeMode` property](https://iiif.io/api/presentation/3.0/#timemode) can be used to indicate the desired behavior when the duration of the content resource that is not equal to the temporal region targeted by the annotation.

It is an error to select a temporal region of a Scene that does not have a `duration`, or to select a temporal region that is not within the Scene's temporal extent.  A Canvas or Scene with a `duration` may not be annotated as a content resource into a Scene that does not itself have a `duration`.


An annotation that targets a Scene using a PointSelector without any temporal refinement implicitly targets the Scene's entire duration.


### Audio and 3D


AmbientAudio (everywhere)
PointAudio (sphere)
SpotAudio (cone)

   source: Audio (id, type, format, profile, duration, label)
   volume: UnitValue (value: 0.3, unit: relative)
   angle: degrees of the cone, per SpotLight

Ambient and Point can be painted on to Canvas
hidden on audio = inaudible


All resources that can be added to a Scene have an implicit (e.g. Lights, Cameras) or explicit (e.g. Models, Scenes), local coordinate space. If a resource does not have an explicit coordinate space, then it is positioned at the origin of its coordinate space. In order to add a resource with its local coordinate space into a Scene with its own coordinate space, these spaces must be aligned. This done by aligning the origins of the two coordinate spaces.

"Exclude Audio"














# Nesting (more about Containers as Content Resources)

> How does this relate to model doc? What's normative and needs to be in model.md because it defines a Scene?

A Canvas can be painted into a Scene as an Annotation, but the 2D nature of Canvases requires special consideration due to important differences between Canvases and Scenes. A Canvas describes a bounded 2D space with finite `height` and `width` measured in pixels with a pixel origin at the top-left corner of the Canvas, while Scenes describe a boundless 3D space with x, y, and z axes of arbitrary coordinate units and a coordinate origin at the center of the space. It is important to note that in many cases the pixel scale used by a Canvas or a 2D image content resource will not be in proportion to the desired 3D coordinate unit scale in a Scene.

When a Canvas is painted as an Annotation targeting a Scene, the top-left corner of the Canvas (the pixel origin) is aligned with the 3D coordinate origin of the Scene. The top edge of the Canvas is aligned with (e.g., is colinear to) the positive x axis extending from the coordinate origin. The left edge of the Canvas is aligned with (e.g., is colinear to) the negative y axis extending from the coordinate origin. The Canvas is scaled to the Scene such that the pixel dimensions correspond to 3D coordinate units - a Canvas 200 pixels wide and 400 pixels high will extend 200 coordinate units across the x axis and 400 coordinate units across the y axis. Please note: direction terms "top", "bottom", "right", and "left" used in this section refer to the frame of reference of the Canvas itself, not the Scene into which the Canvas is painted.

A Canvas in a Scene has a specific forward face and a backward face. By default, the forward face of a Canvas should point in the direction of the positive z axis. If the property `backgroundColor` is used, this color should be used for the backward face of the Canvas. Otherwise, a reverse view of the forward face of the Canvas should be visible on the backward face.

<div style="background: #A0F0A0; padding: 10px; padding-left: 30px; margin-bottom: 10px">
  To Do: Add an image demonstrating default Canvas placement in Scene
</div>

A `PointSelector` can be used to modify the point at which the Canvas will be painted, by establishing a new point to align with the top-left corner of the Canvas instead of the Scene coordinate origin. Transforms can also be used to modify Canvas rotation, scale, or translation.

<!--
It may be desirable to exercise greater control over how the Canvas is painted into the Scene by selecting the coordinate points in the Scene that should correspond to each corner of the Canvas. This provides fine-grained manipulation of Canvas placement and/or scale, and for optionally introducing Canvas distortion or skew. Annotations may use a WktSelector to select different points in the Scene to align with the top-left, bottom-left, bottom-right, and top-right corners of the Canvas. In this case, the four Scene coordinates should be listed beginning with the coordinate corresponding to the top-left corner of the Canvas, and should proceed in a counter-clockwise winding order around the Canvas, with coordinates corresponding to bottom-left, bottom-right, and top-right corners in order respectively. The use of WktSelector for this purpose overrides any use of Transforms on the Canvas Annotation.

Example placing top-left at (0, 1, 0); bottom-left at (0, 0, 0); bottom-right at (1, 0, 0); and top-right at (1, 1, 0):

```json
"selector": [
  {
    "type": "WktSelector",
    "wktLiteral": "POLYGON Z ((0 1 0, 0 0 0, 1 0 0, 1 1 0))"
  }
]
```
-->

## Scene in Scene

Scenes and other IIIF containers, such as Canvases, may also be embedded within Scenes, as described below in the nesting section [fwd-ref-to-nesting].

```json
{
  "id": "https://example.org/iiif/scenes/1",
  "type": "Scene",
  "label": {"en": ["Chessboard"]},
  "backgroundColor": "#000000",
  "items": [
   "Note: Annotations Live Here"
  ]
}
```
As with other resources, it may be appropriate to modify the initial scale, rotation, or translation of a content resource Scene prior to painting it within another Scene. Scenes associated with SpecificResources may be manipulated through the transforms described in Transforms(transforms_section).

A simple example painting one Scene into another:

```json
{
    "id": "https://example.org/iiif/3d/anno1",
    "type": "Annotation",
    "motivation": ["painting"],
    "body": {
        "id": "https://example.org/iiif/scene1",
        "type": "Scene"
    },
    "target": "https://example.org/iiif/scene2"
}
```

When a Scene is nested into another Scene, the `backgroundColor` of the Scene to be nested should be ignored as it is non-sensible to import. All Annotations painted into the Scene to be nested will be painted into the Scene into which content is being nested, including Light or Camera resources. If the Scene to be nested has one or more Camera Annotations while the Scene into which content is being nested does not, the first Camera Annotation from the nested Scene will become the default Camera for the overall Scene.




# Annotations

In the examples so far, Annotations have been used to associate the images, audio and other Content Resources with their Containers for presentation. IIIF uses the same W3C standard for the perhaps more familiar _annotation_ concepts of commenting, tagging, describing and so on. Annotations can carry textual transcriptions or translations of the content, discussion about the content and any other linking between resources.

Whereas annotations that associate content resources with Containers are included in the `items` property of the Container, all other types of Annotation are referenced from the `annotations` property. Containers, Manifests, Collections and Ranges can all have this property, linking to relevant annotations. As with the `items` property, annotations are grouped into one or more AnnotationPage resources. These are usually external references.

```
Manifest
  items
    Canvas
      annotations
        AnnotationPage
          items
            Annotation
```

## Annotation Page

Annotation Pages are used to group Annotations.  In cases where many annotations are present, such as when transcription, translation, and commentary are associated with a manuscript, it can be useful to separate these annotations into groups that can facilitate improved user interactions in a client.  

Each Annotation Page can be embedded or externally referenced. Clients should process the Annotation Pages and their items in the order given in the Container.  Publishers may choose to expedite the processing of embedded Annotation Pages by ordering them before external pages, which will need to be dereferenced by the client.  Order can be significant, however. Painting annotations are assigned an ascending [z-index](https://developer.mozilla.org/en-US/docs/Web/CSS/z-index) from the first painting annotation encountered. Annotations with a higher z-index will render in front of those with a lower z-index when displayed on a Canvas.
<!-- Any impact of order in a Timeline or Scene? -->
<!-- https://iiif.io/api/cookbook/recipe/0036-composition-from-multiple-images/ -->

## Annotation Collection

Annotation Collections represent groupings of Annotation Pages that should be managed as a single whole, regardless of which Container or resource they target. This allows, for example, all of the Annotations that make up a particular translation of the text of a book to be collected together. A client might then present a user interface that allows all of the Annotations in an Annotation Collection to be displayed or hidden according to the user’s preference.

For Annotation Collections with many Annotations, there will be many pages. The Annotation Collection refers to the first and last page, and then the pages refer to the previous and next pages in the ordered list. Each page is part of the Annotation Collection.

```json
{
  "id": "https://example.org/iiif/book1/annocoll/transcription",
  "type": "AnnotationCollection",
  "label": {"en": ["Diplomatic Transcription"]},
  "total": 112,
  "first": { "id": "https://example.org/iiif/book1/annopage/l1", "type": "AnnotationPage" },
  "last": { "id": "https://example.org/iiif/book1/annopage/l112", "type": "AnnotationPage" }
}
```

```jsonc
{
  "id": "https://example.org/iiif/book1/annopage/l2",
  "type": "AnnotationPage",
  "prev": "https://example.org/iiif/book1/annopage/l1",
  "next": "https://example.org/iiif/book1/annopage/l3",
  "items": [
    {
      "id": "https://example.org/iiif/book1/annopage/l2/a1",
      "type": "Annotation"
      // ...
    },
    {
      "id": "https://example.org/iiif/book1/annopage/l2/a2",
      "type": "Annotation"
      // ...
    }
  ],
  "partOf": [
    {
      "id": "https://example.org/iiif/book1/annocoll/transcription",
      "type": "AnnotationCollection",
    }
  ]
}
```

<!--
use totalItems? https://iiif.io/api/discovery/1.0/#totalitems
https://github.com/IIIF/api/issues/2118
-->

## Comment Annotations

Commentary can be associated with a Timeline, Canvas, or Scene via Annotations with a `commenting` motivation.

### A comment about a segment of music

<!-- This is redundant with Use Case 4 -->

This is an example of a commenting annotation that targets two-minute segment of a muscial performance.

```json
{
      "id": "https://example.org/iiif/presentation/examples/commenting/anno/1",
      "type": "Annotation",
      "motivation": "commenting",
      "body": {
        "id": "https://example.org/iiif/presentation/examples/commenting/anno/1/theme2",
        "type": "TextualBody",
        "language": "en",
        "format": "text/plain",
        "value": "The second theme of the concerto is introduced."
      },
      "target": "https://example.org/iiif/presentation/examples/commenting/timeline/t1#t=38.0,158.0"
    }
```

### A comment about a face in a painting

A comment on a Canvas can target a non-rectangular area.  This example uses a `SvgSelector` to comment on a painting.

```json
{
      "id": "https://example.org/iiif/presentation/examples/commenting/anno/2",
      "type": "Annotation",
      "motivation": "commenting",
      "body": {
        "id": "https://example.org/iiif/presentation/examples/commenting/anno/2/person2",
        "type": "TextualBody",
        "language": "en",
        "format": "text/plain",
        "value": "Note the expressive eyes of the subject of this painting."
      },
      "target": {
        "type": "SpecificResource",
        "source": {
          "id": "https://example.org/iiif/presentation/examples/commenting/canvas/2",
          "type": "Canvas"
        },
        "selector": [
          {
            "id": "https://example.org/iiif/presentation/examples/commenting/anno2/selector2",
            "type": "SvgSelector",
            "value": "<svg:svg> ... </svg:svg>"
          }
        ]
    }
}
```

Annotations may alternately use a different type of Selector, called a `WktSelector`, to align the Annotation to a target region within a Canvas or Scene.

### A comment about something in a Model

(targets Scene)
Look at this scratch in the helmet

> Todo: This is mostly copy-pasted from properties, is it needed here? Use in above example.

It is important to be able to position the textual body of an annotation within the Container's space that the annotation also targets. For example, a description of part of an image in a Canvas should be positioned such that it does not obscure the image region itself and labels to be displayed as part of a Scene should not be rendered such that the text is hidden by the three dimensional geometry of the model. The positioning of the textual body in a container is accomplished through the `position` property, which has as a value a Specific Resource identifying the targeted container as the source and a selector defining how the textual body should be positioned in the targeted container. If this property is not supplied, then the client should do its best to ensure the content is visible to the user.

> Forward ref to 3D comments with Cameras


## Linking Annotations

An Annotation with the motivation `linking` is used to create links between resources, both within the Manifest or to external content on the web, including other IIIF resources. Examples include linking to the continuation of an article in a digitized newspaper in a different Canvas, or to an external web page that describes the diagram in the Canvas. A client typically renders the links as clickable "Hotspots" - but can offer whatever accessible affordance as appropriate. The user experience of whether the linked resource is opened in a new tab, new window or by replacing the current view is up to the implementation.

The resource the user should be taken to is the `body` of the annotation, and the region of the Container that the user clicks or otherwise activates to follow the link is the `target`: 

```jsonc
{
  "id": "https://example.com/annotation/p0002-link",
  "type": "Annotation",
  "motivation": "linking",
  "body": [
    {
    "id": "https://example.com/website1",
    "type": "Text"
    }
  ],
  "target": "https://example.com/canvas/p1#xywh=265,661,1260,1239"
}
```


## Activating Annotations

Sometimes it is necessary to modify the contents of a Container in the contexts of different annotations on that Container. This technique allows IIIF to be used for _storytelling_ (ref) and other narrative applications beyond simply conveying a static Digital Object into a viewer and leaving subsequent interactions entirely in the control of the user.

Annotations with the motivation `activating` are referred to as _activating_ annotations, and are used to link a resource that triggers an action with the resource(s) to change, enable or disable. The `target` of the activating annotation could be a commenting annotation, for which a user might click a corresponding UI element. In other scenarios the `target` could be the painting annotation of a 3D model, or an annotation that targets part of a model, or a region of a Canvas, or a point or segment of a Timeline, or any other annotation that a user could interact with (in whatever manner) to trigger an event. Even a region of space in a Scene or an extent of time in a Container with `duration` could be the `target`, so that when the user "enters" that region or extent, something happens. The `body` of the annotation is the resource that is then activated:

- a Camera: if "hidden" the behavior is removed, and this Camera becomes the viewport.
- AnimationSelector: A named animation within a model is played (fwd ref)
- (anything else yet?)

Activating annotations are provided in a Container's `annotations` property. They can be mixed in with the commenting (or other interactive annotations) they target, or they can be in a separate AnnotationPage. The client should evaluate all the activating annotations it can find.

```jsonc
{
  "id": "https://example.org/iiif/3d/anno9",
  "type": "Annotation",
  "motivation": ["activating"],
  "target": [
    {
      "id": "https://example.org/iiif/3d/commenting-anno-for-mandibular-tooth",
      "type": "Annotation"
    }
  ],
  "body": [
    {
      "id": "https://example.org/iiif/3d/anno-that-paints-desired-camera-to-view-tooth",
      "type": "Annotation"
    }
  ]
}
```


### Showing and hiding resources

An activating annotation has two additional optional properties:

* `enables`: For each annotation in the value, remove the 'hidden' behavior if it has it.
* `disables`: For each annotation in the value, add the 'hidden' behavior if it does not have it.

Hidden resources cannot be active or activated. If the values are the `id` properties of painting resources that paint models, they are hidden or made visible. If Lights, they are turned on. The following example demonstrates a light switch that can be toggled on and off.

```jsonc
{
    "@context": "http://iiif.io/api/presentation/4/context.json",
    "id": "https://example.org/iiif/manifest/switch",
    "type": "Manifest",
    "label": { "en": [ "Light switch" ] },
    "items": [
        {
            "id": "https://example.org/iiif/scene/switch/scene-1",
            "type": "Scene",
            "items": [
                {
                    "id": "https://example.org/iiif/scene/switch/scene-1/painting-annotation-pages/1",
                    "type": "AnnotationPage",
                    "items": [
                        {
                            "id": "https://example.org/iiif/painting-annotation/lightswitch-1",
                            "type": "Annotation",
                            "motivation": ["painting"],
                            "label": {
                                "en": ["A light switch"]
                            },
                            "body": {
                                "id": "https://example.org/iiif/model/models/lightswitch.gltf",
                                "type": "Model"
                            },
                            "target": "https://example.org/iiif/scene/switch/scene-1"
                        },
                        {
                            "id": "https://example.org/iiif/scene/switch/scene-1/lights/point-light-4",
                            "type": "Annotation",
                            "motivation": ["painting"],
                            "body": {
                                "id": "https://example.org/iiif/scene/switch/scene-1/lights/4/body",
                                "type": "PointLight"
                            },
                            "target": {
                                "type": "SpecificResource",
                                "source": "https://example.org/iiif/scene/switch/scene-1",
                                "selector": [
                                    {
                                        "type": "PointSelector",
                                        "x": 5, "y": 5, "z": 5
                                    }
                                ]
                            },
                            "behavior": ["hidden"]
                        }
                    ]
                }
            ],
            "annotations": [
                {
                    "id": "https://example.org/iiif/scene/switch/scene-1/annos/1",
                    "type": "AnnotationPage",
                    "items": [
                        {
                            "id": "https://example.org/iiif/scene/switch/scene-1/annos/1/switch-comment-0",
                            "type": "Annotation",
                            "motivation": [
                                "commenting"
                            ],
                            "body": {
                                "type": "TextualBody",
                                "value": "Click the switch to turn the light on or off"
                            },
                            "target": "https://example.org/iiif/painting-annotation/lightswitch-1"
                        },
                        {
                            "id": "https://example.org/iiif/scene/switch/scene-1/annos/1/activating-on-2",
                            "type": "Annotation",
                            "motivation": [
                                "activating"
                            ],
                            "target": "https://example.org/iiif/painting-annotation/lightswitch-1",
                            "disables": [
                                "https://example.org/iiif/scene/switch/scene-1/annos/1/activating-on-2"
                            ],
                            "enables": [
                                "https://example.org/iiif/scene/switch/scene-1/annos/1/activating-off-3",
                                "https://example.org/iiif/scene/switch/scene-1/lights/point-light-4"
                            ]
                        },
                        {
                            "id": "https://example.org/iiif/scene/switch/scene-1/annos/1/activating-off-3",
                            "type": "Annotation",
                            "motivation": [
                                "activating"
                            ],
                            "target": "https://example.org/iiif/painting-annotation/lightswitch-1",
                            "disables": [
                                "https://example.org/iiif/scene/switch/scene-1/annos/1/activating-off-3",
                                "https://example.org/iiif/scene/switch/scene-1/lights/point-light-4"
                            ],
                            "enables": [
                                "https://example.org/iiif/scene/switch/scene-1/annos/1/activating-on-2"
                            ],
                            "behavior": ["hidden"]
                        }
                    ]
                }
            ]
        }
    ]
}
```

* Initially, a model of a light switch is painted into the Scene. A PointLight is also painted, but with the `behavior` "hidden", which means it is inactive (i.e., off). A commenting annotation with the text "Click the switch to turn the light on or off" targets the light switch. An activating annotation targets the commenting annotation, so that user interaction with the commenting annotation will trigger the activating annotation. This activating annotation has no `body`, but it does have `enables` with values that are the `id` properties of the painting annotation for the light switch model, and the activating annotation that turns the light off. It also has a `disables` with the value of its own `id` - i.e., it disables _itself_. A further activating annotation has the opposite effect. Initially this has the `behavior` "hidden" - which means it is inactive. It also targets the commenting annotation, but has no effect while hidden.
* When the user interacts with the light switch model, the client processes any activating annotations that target it and are not hidden. In this case, the first activating annotation is triggered because while both target the switch, only the first is not hidden. This activation `enables` the light (i.e., removing its "hidden" `behavior` and therefore turning it on) and the other activating annotation, and `disables` itself.
* If the user clicks the light again, the client again processes any activating annotations that target it and are not hidden. This time the second annotation is the active one - and it `disables` the light (turning it off) and itself, and enables the first activating annotation again.
* Subsequent clicks simply alternate between these two states, indefinitely.


### Triggering a named animation in a model

Sometimes a model file has inbuilt animations. While a description of these is outside the scope of IIIF, because it is 3D-implementation-specific, as long as there is a way to refer to a model's animation(s) by name, we can connect the animation to IIIF resources.

This pattern is also achieved with activating annotations, except that the body of the activating annotation references a _named animation_ in the model. The `body` MUST be a SpecificResource, where the `source` is the Painting Annotation that paints the model, and the `selector` is of type `AnimationSelector` with the `value` being a string that corresponds to the animation in the model.

The format of the `value` string is implementation-specific, and will depend on how different 3D formats support addressing of animations within models. The same model can be painted multiple times into the scene, and you might want to activate only one model's animation, thus we need to refer to the annotation that paints the model, not the model directly.


```jsonc
{
  "id": "https://example.org/iiif/3d/activating-animation.json",
  "type": "Manifest",
  "label": { "en": ["Music Box with lid that opens as an internal animation"] },
  "items": [
    {
      "id": "https://example.org/iiif/scene1/scene-with-activation-animation",
      "type": "Scene",
      "label": { "en": ["A Scene Containing a Music Box"] },
      "items": [
        {
          "id": "https://example.org/iiif/scene-with-activation-animation/page/p1/1",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/3d/painting-anno-for-music-box",
              "type": "Annotation",
              "motivation": ["painting"],
              "body": {
                "id": "https://raw.githubusercontent.com/IIIF/3d/main/assets/music-box.glb",
                "type": "Model"
              },
              "target": {
                // SpecificResource with PointSelector
              }
            }
          ],
          "annotations": [
            {
              "id": "https://example.org/iiif/scene1/page/activators",
              "type": "AnnotationPage",
              "items": [
                {
                  "id": "https://example.org/iiif/3d/box-opening-commenting-anno",
                  "type": "Annotation",
                  "motivation": ["commenting"],
                  "body": [
                    {
                      "type": "TextualBody",
                      "value": "Click the box to open the lid"
                    }
                  ],
                  "target": [
                    {
                      "id": "https://example.org/iiif/3d/painting-anno-for-music-box",
                      "type": "Annotation"
                    }
                  ]
                }
                {
                  "id": "https://example.org/iiif/3d/box-opening-activating-anno",
                  "type": "Annotation",
                  "motivation": ["activating"],
                  "target": [
                    {
                      "id": "https://example.org/iiif/3d/box-opening-commenting-anno",
                      "type": "Annotation"
                    }
                  ],
                  "body": [
                    {
                      "type": "SpecificResource",
                      "source": "https://example.org/iiif/3d/painting-anno-for-music-box",
                      "selector": [
                        {
                          "type": "AnimationSelector",
                          "value": "open-the-lid"
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```
### 3D Comments with Cameras

In many complex 3D Scenes, it may not be clear what or how to look at a particular point of interest even when the commenting annotation targets a particular point. The view may be occluded by parts of the model, or other models in the Scene. In the following example, the user can explore the Scene freely, but when they select a particular comment, a specific Camera that was previously hidden (unavailable to the user) is activated, moving the user (i.e., setting the viewport) to a chosen position suitable for looking at the point of interest:

```jsonc
{
  "id": "https://example.org/iiif/3d/whale_comment_scope_content_state.json",
  "type": "Manifest",
  "label": { "en": ["Whale Cranium and Mandible with Dynamic Commenting Annotations and Custom Per-Anno Views"] },
  "items": [
    {
      "id": "https://example.org/iiif/scene1/page/p1/1",
      "type": "Scene",
      "label": { "en": ["A Scene Containing a Whale Cranium and Mandible"] },
      "items": [
        {
          "id": "https://example.org/iiif/scene1/page/p1/1",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/3d/anno1",
              "type": "Annotation",
              "motivation": ["painting"],
              "body": {
                "id": "https://raw.githubusercontent.com/IIIF/3d/main/assets/whale/whale_mandible.glb",
                "type": "Model"
              },
              "target": {
                // SpecificResource with PointSelector
              }
            },
            {
              "id": "https://example.org/iiif/3d/anno-that-paints-desired-camera-to-view-tooth",
              "type": "Annotation",
              "motivation": ["painting"],
              "behavior": ["hidden"],
              "body": {
                "type": "SpecificResource",
                "source": [
                  {
                    "id": "https://example.org/iiif/3d/cameras/1",
                    "type": "PerspectiveCamera",
                    "label": {"en": ["Perspective Camera Pointed At Front of Cranium and Mandible"]},
                    "fieldOfView": 50.0,
                    "near": 0.10,
                    "far": 2000.0
                  }
                ]
              },
              "target": {
                "type": "SpecificResource",
                "source": [
                  {
                    "id": "https://example.org/iiif/scene1",
                    "type": "Scene"
                  }
                ],
                "selector": [
                  {
                    "type": "PointSelector",
                    "x": 0.0, "y": 0.15, "z": 0.75
                  }
                ]
              }
            },
            {
              "id": "https://example.org/iiif/3d/anno2",
              "type": "Annotation",
              "motivation": ["painting"],
              "body": {
                "id": "https://raw.githubusercontent.com/IIIF/3d/main/assets/whale/whale_cranium.glb",
                "type": "Model"
              },
              "target": {
                // SpecificResource with PointSelector
              }
            }
          ]
        }
      ]
    }
  ],
  "annotations": [
    {
      "id": "https://example.org/iiif/scene1/page/p1/annotations/1",
      "type": "AnnotationPage",
      "items": [
        {
          "id": "https://example.org/iiif/3d/commenting-anno-for-mandibular-tooth",
          "type": "Annotation",
          "motivation": ["commenting"],
          "bodyValue": "Mandibular tooth",
          "target": {
            // SpecificResource with PointSelector
          }
        },
        {
          "id": "https://example.org/iiif/3d/commenting-anno-for-right-pterygoid-hamulus",
          "type": "Annotation",
          "motivation": ["commenting"],
          "bodyValue": "Right pterygoid hamulus",
          "target": {
            // SpecificResource with PointSelector
          }
        },
        {
          "id": "https://example.org/iiif/3d/anno9",
          "type": "Annotation",
          "motivation": ["activating"],
          "target": [
            {
              "id": "https://example.org/iiif/3d/commenting-anno-for-mandibular-tooth",
              "type": "Annotation"
            }
          ],
          "body": [
            {
              "id": "https://example.org/iiif/3d/anno-that-paints-desired-camera-to-view-tooth",
              "type": "Annotation"
            }
          ]
        }
      ]
    }
  ]
}
```

The client will render a UI that presents the two commenting annotations in some form and allows the user to navigate between them. An active Camera is not provided (while there is a Camera in the Scene it has `behavior` "hidden", i.e., it is inactive: not usable). The commenting annotations are ordered; while the user might explore them freely in the Scene they might also go "forward" from the first to the second commenting annotation and "back" to the first from the second. In either case the above example instructs the client to activate the Camera when the user interacts with the comment. The user is free to move away but any interaction with that comment will bring them back to the specific viewpoint. (forward ref to chains of activation example)


### Modifying resource properties

Many Scene interaction use cases can be accomplished using the `enables` and `disables` properties to toggle the `"behavior": ["hidden"]`, and/or using activating annotations with bodies that can be _activated_: the examples above show a Camera and then an Animation being activated. Models in the Scene can also be shown and hidden via these properties.

> when to use enables and when to use the `body` of the activating anno - are they equivalent for, say, a hidden model: enable it, activate it - interchangeable?

For some interactions it is necessary to do more than show or hide or "activate" resources, by changing just `"behavior": ["hidden"]`. Other properties can also be changed via the [JSON Patch](link) mechanism.

```jsonc
{
  "type": "JSONPatch",
  "patchTarget":  "https://example.org/iiif/scene1/scene-with-color-change", // the Scene
  "operations": [
    {
        "op": "replace",
        "path": "/backgroundColor", // path to the property being changed.
        "value": "#FF99AA"
    }
  ]
}
```

> **This is a clear distinction like level0, level1 - a client can simply choose not to support arbitrary patching.**

> Be clear that you still need to have all the patchable resources present from the start, you can't pull them in later.

In the following simple example, the background color of the Scene is changed:


```jsonc
{
  "id": "https://example.org/iiif/3d/property-change.json",
  "type": "Manifest",
  "label": { "en": ["Whale Mandible"] },
  "items": [
    {
      "id": "https://example.org/iiif/scene1/scene-with-color-change",
      "type": "Scene",
      "label": { "en": ["A Scene Containing a Whale Mandible"] },
      "items": [
        {
          "id": "https://example.org/iiif/scene1/page/p1/1",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://example.org/iiif/3d/painting-anno-for-mandible",
              "type": "Annotation",
              "motivation": ["painting"],
              "body": {
                "id": "https://raw.githubusercontent.com/IIIF/3d/main/assets/whale/whale_mandible.glb",
                "type": "Model"
              },
              "target": "https://example.org/iiif/scene1/scene-with-color-change"
            }
          ],
          "annotations": [
            {
              "id": "https://example.org/iiif/scene1/page/activators",
              "type": "AnnotationPage",
              "items": [
                {
                  "id": "https://example.org/iiif/3d/color-change-commenting-anno",
                  "type": "Annotation",
                  "motivation": ["commenting"],
                  "body": [
                    {
                      "type": "TextualBody",
                      "value": "Change the background color"
                    }
                  ],
                  "target": [
                    {
                      "id": "https://example.org/iiif/3d/painting-anno-for-mandible", // or the Scene?
                      "type": "Annotation"
                    }
                  ]
                }
                {
                  "id": "https://example.org/iiif/3d/color-change-activating-anno",
                  "type": "Annotation",
                  "motivation": ["activating"],
                  "target": [
                    {
                      "id": "https://example.org/iiif/3d/color-change-commenting-anno",
                      "type": "Annotation"
                    }
                  ],
                  "body": [
                    {
                      "type": "JSONPatch",
                      "patchTarget":  "https://example.org/iiif/scene1/scene-with-color-change",
                      "operations": [
                        {
                            "op": "replace",
                            "path": "/backgroundColor",
                            "value": "#FF99AA"
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

# Integration

seeAlso, service(s), extensions
mention search, image api, auth

profile for seeAlso

partOf -





# Content State

(this + model doc should relieve Content State spec of modelling concerns and leave it entirely about protocol)

A Content State is simply any valid IIIF Presentation Resource, or part of a Presentation resource. The following are all Content States that describe a "fragment" of IIIF:

A "bare" Manifest URI:

```
https://example.org/manifests/1
```

A reference to a Manifest:

```json
{
  "id": "https://example.org/manifests/1",
  "type": "Manifest"
}
```

A region of a Canvas within a Manifest:

```json
{
  "id": "https://example.org/canvases/aabb#xywh=4500,1266,600,600",
  "type": "Canvas",
  "partOf": {
    "id": "https://example.org/manifests/1",
    "type": "Manifest"
  }
}
```

Two versions of a painting from different publishers:

```json
[
  {
    "id": "https://gallery-1.org/iiif/sunflowers/canvas1",
    "type": "Canvas",
    "partOf": [
      {
        "id": "https://gallery-1.org/iiif/sunflowers",
        "type": "Manifest"
      }
    ]
  },
  {
    "id": "https://gallery-2.org/collection/sunflowers/c1",
    "type": "Canvas",
    "partOf": [
      {
        "id": "https://gallery-2.org/collection/sunflowers",
        "type": "Manifest"
      }
    ]
  }
]
```

A Scene with a Camera at a particular point:


```json
{
  "id": "https://example.org/iiif/scene1/page/p1/1",
  "type": "Scene",
  "items": [
    {
      "id": "https://example.org/iiif/3d/anno8",
      "type": "Annotation",
      "motivation": ["painting"],
      "body": {
        "type": "SpecificResource",
        "source": [
          {
            "id": "https://example.org/iiif/3d/cameras/1",
            "type": "PerspectiveCamera",
            "label": {
              "en": [
                "Perspective Camera Pointed At Front of Cranium and Mandible"
              ]
            },
            "fieldOfView": 50.0,
            "near": 0.1,
            "far": 2000.0
          }
        ]
      },
      "target": {
        "type": "SpecificResource",
        "source": [
          {
            "id": "https://example.org/iiif/scene1",
            "type": "Scene"
          }
        ],
        "selector": [
          {
            "type": "PointSelector",
            "x": 0.0, "y": 0.15, "z": 0.75
          }
        ]
      }
    }
  ]
}
```

The term _Content State_ is used for any arbitrary fragments of IIIF such as the above when they are used in the particular ways defined by this specification. A Content State is **usually** carried by the `target` of an annotation with the motivation `contentState`, or `body` of an annotation with the motivation `activating`, but in some scenarios may be transferred between client applications without an enclosing annotation, as a "bare" URI (see Content State 2.0 specification).

Annotations with the motivation `contentState` are referred to as _content state_ annotations.

Content States are used for the following applications:

## Load a particular view of a resource or group of resources

In this usage, an annotation with the motivation `contentState` is passed to a client to initialize it with a particular view of a resource. Almost all IIIF Clients initialize from the very simplest form of Content State - a Manifest URI. A more complex Content State might target a particular region of a particular canvas within a Manifest, as in the second example above. A client initialized from such a Content State would load the Manifest, show the particular Canvas, and perhaps zoom in on the target region.

The mechanisms for passing Content State into a client, and exporting a Content State from a client, are given in the Content State Protocol API 2.0 specification, which describes the scenarios in which a URI, or Content State not carried by an annotation, should be interpreted by a Client as a Content State.


## Load a particular view of some resource and modify it

⚠ what are we doing with this? Do we still allow it? It's a good use case...

In the previous usage, the fragment of IIIF carried by the annotation with the motivation `contentState` provides enough information for a Client to load a resource and show it. This fragment can also carry additional IIIF Presentation API resources not shown in the referred-to resource. For example, in the following example the Content State carries additional annotations not present in the original published Manifest. A client initializing from this Content State would show these additional annotations to the user:

What to do about activating annos in the introduced content?

```json
{
  "id": "https://example.org/import/3",
  "type": "Annotation",
  "motivation": "contentState",
  "target": {
    "id": "https://example.org/canvases/aabb#xywh=4500,1266,600,600",
    "type": "Canvas",
    "partOf": {
      "id": "https://example.org/manifests/nook12",
      "type": "Manifest"
    },
    "annotations": [
      {
        "id": "https://my-annotation-store.org/user4532/notes-on-book12/p1",
        "type": "AnnotationPage"
      }
    ]
  }
}
```


# Interactivity, Guided Viewing and Storytelling


A narrative might comprise an AnnotationPage of `commenting` annotations that target different parts of the Container, for example a guided tour of a painting or a map. For a Canvas or Timeline it is usually sufficient to leave the interactivity to the client; the fact that comments target different extents implies the client must offer some affordance for those comments (typically the user can click each one), and in response the client will move the current play point of the Timeline to the commenting annotation target, or pan and zoom the viewport to show the relevant part of an image. For 3D this may not be enough; a particular comment may only make sense from a certain viewpoint (i.e., Camera), or different steps of the story require different Lights to be active.

In a storytelling or exhibition scenario, the non-painting `annotations` might be carrying informative text, or even rich HTML bodies. They can be considered to be _steps_ in the story. The use of activating annotations (back ref) allows a precise storytelling experience to be specified, including:

 - providing a specific viewpoint for each step of the narrative (or even a choice of viewpoints)
 - modifying the lighting of the Scene for each step, for example shining a spotlight on a point of interest
 - hiding models in the Scene at a particular step
 - showing additional models at a particular step

All the annotations referred to by the activating annotations' `target` and `body` properties are already present in the Scene from the beginning. Initially, many of them may have the behavior `hidden`, invisible until activated.


## The `sequence` behavior

While all AnnotationPage `items` are inherently ordered, an Annotation Page with the `behavior` "sequence" is explicitly a narrative, and clients should prevent (dissuade) users from jumping about - the annotations, and the effects of them _activating_ other contents of the Container, are intended to be experienced in order and individually. Normally, a client might display all the comments in an AnnotationPage in a sidebar so they are all visible in the UI, but for an AnnotationPage with `behavior` "sequence" only show the currently active annotation text, and next and previous UI.


## Chains of activation

Chaining together activating annotations can then allow the implementation of, at least:

* Specific camera position to look at an Annotation
* Multi-step linear stories
* Animations, including as part of stories without disrupting the flow, and looping animations (they activate themselves)
* Interactive components such as light switches (enable/disable a light), jukeboxes (enable/disable Audio Emitter)


## Storytelling example

* Something really cool that brings a lot of things together!
* Use JSONPatch to move a model too.


# Conveying Physical Dimensions

In many cases, the dimensions of a Canvas, or the pixel density of a photograph, are not necessarily related to a real-world size of the object they show. A large wall painting and a tiny miniature may both be conveyed by 20 megapixel source images on a 4000 by 3000 unit Canvas. But it can be important to know how big something is or if there is a relationship between pixel density and physical length, especially when comparing objects together. Each pixel in an image may correspond precisely to a physical area, allowing measurement of real world distances from the image. A scanned 3D model may be constructed such that each 3D coordinate unit corresponds to one meter of physical distance.

The `spatialScale` property of a Canvas or Scene provides a corresponding real-world scale for a unit of the Canvas or Scene coordinate system, allowing clients to provide scale information to users, for example by an on-screen virtual ruler. In a 2-up viewer, a client could scale two views to convey the true relative sizes of two objects.

The value of `spatialScale` is a `UnitValue` (ref) that has as a value a length unit. This specification defines only one length unit, "m", i.e., meters, though others may be defined externally as an [extension][prezi30-ldce]. If source size metadata is machine readable (or parse-able) in other measurement systems (e.g., feet and inches) then it should be converted to meters for use in `spatialScale`. Publishers may wish to present the original given measure (e.g., from catalogue metadata) in a `metadata` field for context.

The Presentation API also offers a corresponding `temporalScale` property for the `duration` dimension of a Container, when 1 second in the Container does not correspond to 1 second of real time. This is useful for speeded-up or slowed-down audio or video.

An extreme example of both physical dimension properties together is a Canvas showing an animation of continental drift over the course of Earth history, where the spatialScale could convey that each Canvas unit is several thousand meters, and each second of the Canvas `duration` is several million years.



# Other stuff

## Embedded Content

e.g., painting TextualBody on Canvas


## Style

### Rotation






# Protocol



## HTTP Requests and Responses

### URI Recommendations

### Requests

### Responses

### Authentication






# Accessibility

(new section)

`provides`
`provides[]`







# Terminology

The principles of [Linked Data][org-linked-data] and the [Architecture of the Web][org-w3c-webarch] are adopted in order to provide a distributed and interoperable framework. The [Shared Canvas data model][shared-canvas] and [JSON-LD][org-w3c-json-ld] are leveraged to create an easy-to-implement, JSON-based format.

This specification uses the following terms:

* __embedded__: When a resource (A) is embedded within an embedding resource (B), the complete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will not result in additional information. Example: Canvas A is embedded in Manifest B.
* __referenced__: When a resource (A) is referenced from a referencing resource (B), an incomplete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will result in additional information. Example:  Manifest A is referenced from Collection B.
* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

The terms _array_, _JSON object_, _number_, _string_, and _boolean_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].



# Appendices

## Versioning

## Acknowledgements

## Change Log


