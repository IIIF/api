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
  - name: Dawn Childress
    ORCID: https://orcid.org/0000-0003-2602-2788
    institution: UCLA
  - name: Tom Crane
    ORCID: https://orcid.org/0000-0003-1881-243X
    institution: Digirati
  - name: Jeff Mixter
    ORCID: https://orcid.org/0000-0002-8411-2952
    institution: OCLC
  - name: Robert Sanderson
    ORCID: https://orcid.org/0000-0003-4441-6852
    institution: Yale University
  - name: Julie Winchester
    ORCID: https://orcid.org/0000-0001-6578-764X
    institution: Duke University
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

a > code::after {
  content: "↗";
  font-size: 0.65em;
  opacity: 0.6;
  margin-left: 0.2em;
  vertical-align: super;
  text-decoration: none;
}

a > code {
 /* text-decoration: underline;*/
  color: var(--link-color);
  cursor: pointer;
}

a:hover > code {
  background-color: rgba(0,0,0,0.05);
  text-decoration: underline;
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

The Manifest's [`items`][prezi-40-model-items] property is an ordered list of _Containers_ of _Content Resources_ (images, 3D models, audio, etc). Client software loads the Manifest and presents each Container's Content Resources. The client software also presents user interface controls to navigate the list of Content Containers.

Manifests have descriptive, technical and linking properties. The required properties of Manifests are [`id`][prezi-40-model-id], [`type`][prezi-40-model-type], [`items`][prezi-40-model-items] and [`label`][prezi-40-model-label]. Other commonly used properties include [`summary`][prezi-40-model-summary], [`metadata`][prezi-40-model-metadata], [`rights`][prezi-40-model-rights], [`thumbnail`][prezi-40-model-thumbnail], [`homepage`][prezi-40-model-homepage] and [`provider`][prezi-40-model-provider].

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

The required properties of all Containers are [`id`][prezi-40-model-id], and [`type`][prezi-40-model-type]. Most Containers also have the [`items`][prezi-40-model-items] and [`label`][prezi-40-model-label] properties. Further properties are required for the different types of Container.

The defined Container types are:

### Timeline

A Container that represents a bounded temporal range, without any spatial coordinates. It is typically used for audio-only content.

Timelines have an additional required property of [`duration`][prezi-40-model-duration], which gives the extent of the Timeline as a floating point number of seconds.

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

Canvases have two additional required properties: [`height`][prezi-40-model-height] and [`width`][prezi-40-model-width], which give the spatial extent as integers. Canvases may also have the [`duration`][prezi-40-model-duration] property in the same manner as Timelines.

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

Scenes may also have the [`duration`][prezi-40-model-duration] property in the same manner as Timelines.

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

In each of the three Containers above, an **Annotation** links the Container to a Content Resource. The Content Resource in the [`body`][prezi-40-model-body] property is _painted_ into the Container by an Annotation whose [`target`][prezi-40-model-target] property is the [`id`][prezi-40-model-id] of the Container. In all three simple cases here the [`target`][prezi-40-model-target] property is the [`id`][prezi-40-model-id] of the Container with no further qualification.

Different uses of Annotation are distinguished through their [`motivation`][prezi-40-model-motivation] property. This specification defines a value for [`motivation`][prezi-40-model-motivation] called `painting` for associating Content Resources with Containers, which this specification calls a Painting Annotation. The verb "paint" is also used to refer to the associating of a Content Resource with a Container by a Painting Annotation. This is from the notion of painting onto a canvas, a metaphor borrowed from art and used for image-based digital applications, and expanded by IIIF into "painting" any Content Resource into a Container of any number of dimensions.

The same linking mechanism is also used in IIIF with other motivations for transcriptions, commentary, tags and other content. This provides a single, unified method for aligning content, and provides a standards-based framework for referencing parts of resources. As Annotations can be added later, it promotes a distributed system in which further content such as commentary can be aligned with the objects published on the web.

Annotations are grouped within the [`items`][prezi-40-model-items] property of an Annotation Page, and the [`items`][prezi-40-model-items] property of the Container is a list of Annotation Pages. This allows consistent grouping of Annotations when required.

(👀) [Model Documentation](model/#Annotations)


## Content Resources

Content Resources are external web resources, including images, video, audio, 3D models, data, web pages or any other format. Typically these are the resources that will be painted into a Container using a Painting Annotation.

In addition to the required properties [`id`][prezi-40-model-id] and [`type`][prezi-40-model-type], other commonly used properties include [`format`][prezi-40-model-format], and [`width`][prezi-40-model-width], [`height`][prezi-40-model-height] and [`duration`][prezi-40-model-duration] as appropriate to the Content Resource format. The values of these properties are often the source of the equivalent Container properties.

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

Here the Canvas [`id`][prezi-40-model-id] from the earlier example is still the [`target`][prezi-40-model-target] of an Annotation, but it has been qualified to a specific region of that Canvas by a URI fragment `#xywh=6050,3220,925,1250`. Note that the x, y, w, and h are in the Canvas coordinate space, not the image pixel dimensions space. This annotation has no knowledge of or dependency on the particular image we painted onto the Canvas; we could replace that image with one of a different, higher resolution without affecting this annotation or the region of the Canvas it targets.


### Specific Resource

URIs with fragments are insufficient for complex referencing, like circular regions or arbitrary text spans, and do not support other useful features such as describing styling or transformation. The Web Annotation Data Model introduces a class called [`SpecificResource`][prezi-40-model-SpecificResource] that represents the resource in a specific context or role, which IIIF uses to describe these more complex requirements.

Several different classes of Selector are used in IIIF, including an alternative implementation of the fragment pattern called [`FragmentSelector`][prezi-40-model-FragmentSelector]. The fragment is given in the `value` property of the [`FragmentSelector`][prezi-40-model-FragmentSelector], and the resource it should be applied to is given in [`source`][prezi-40-model-source].

The required properties of Specific Resources are [`id`][prezi-40-model-id], [`type`][prezi-40-model-type], and [`source`][prezi-40-model-source]. Other commonly used properties include `selector`, [`transform`][prezi-40-model-transform], and `scope`.

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

Navigational resources provide structure for IIIF resources that allow viewing clients to guide users through IIIF content and collections. They define how resources are organized for discovery and interaction across multiple resources, like Collections, or within a resource, like Ranges, that help clients construct meaningful navigational interfaces, such as hierarchies, groupings, lists, or tables of contents.

### Collection

IIIF Collections are ordered lists of Manifests and Collections. Collections allow these resources to be grouped in a hierarchical structure for navigation and other purposes.

Collections may include both other Collections and Manifests, forming a tree-structured hierarchy that expresses relationships among IIIF resources. This organization can represent archival or curatorial structures, logical groupings such as volumes or series, or dynamically generated sets of related items. As such, they enable clients to load predefined sets of resources at initialization, render dynamically generated sets such as search results, visualize lists or hierarchies of related content, and facilitate navigation through structured aggregations of Manifests and Collections.

```json
{
  "id": "https://iiif.example.org/collection/top",
  "type": "Collection",
  "label": { "en": ["Top-level Collection"] },
  "items": [
    {
      "id": "https://iiif.example.org/collection/sub1",
      "type": "Collection",
      "label": { "en": ["Sub-Collection 1"] }
    },
    {
      "id": "https://iiif.example.org/manifest/1",
      "type": "Manifest",
      "label": { "en": ["Manifest 1"] }
    },
    {
      "id": "https://iiif.example.org/manifest/2",
      "type": "Manifest",
      "label": { "en": ["Manifest 2"] }
    }
  ]
}
```

:eyes:

### Range

IIIF Ranges are used to represent structure _WITHIN_ a Manifest beyond the default order of the Containers in the [`items`][prezi-40-model-items] property. Ranges define meaningful divisions or sequences---such as chapters in a book, sections of a newspaper, or movements of a musical work---that allow clients to present hierarchical or linear navigation interfaces that enable the user to quickly move through the object's content.

Ranges may include Containers, parts of Containers via Specific Resources or fragment URIs, or other Ranges, creating tree-like structures that reflect the logical or intellectual organization of the resource, such as a table of contents or an alternative ordering of items.

```json
{
  "id": "https://iiif.example.org/manifest/1/range/toc",
  "type": "Range",
  "label": { "en": ["Table of Contents"] },
  "items": [
    {
      "id": "https://iiif.example.org/manifest/1/canvas/1",
      "type": "Canvas",
      "label": { "en": ["Page 1"] }
    },
    {
      "id": "https://iiif.example.org/manifest/1/canvas/2",
      "type": "Canvas",
      "label": { "en": ["Page 2"] }
    },
    {
      "id": "https://iiif.example.org/manifest/1/range/chapter2",
      "type": "Range",
      "label": { "en": ["Chapter 2"] },
      "items": [
        {
          "id": "https://iiif.example.org/manifest/1/canvas/3",
          "type": "Canvas",
          "label": { "en": ["Page 3"] }
        }
      ]
    }
  ]
}
```

:eyes:



# Image Content

## Use Case 1: Artwork with deep zoom

This example is a Manifest with one Canvas, representing an artwork. The content resource, a JPEG image of the artwork, is associated with the Canvas via a Painting Annotation.

The unit integer coordinates of the Canvas (12000 x 9000) are not the same as the pixel dimensions of the JPEG image (4000 x 3000), but they are proportional---the Canvas has a 4:3 landscape aspect ratio, and so does the JPEG image.The [`target`][prezi-40-model-target] property of the Annotation is the Canvas [`id`][prezi-40-model-id], unqualified by any particular region; this is taken to mean the content (the image) should fill the Canvas completely. As the Canvas and the image are the same aspect ratio, no distortion will occur. This approach allows the current image to be replaced by a higher resolution image in future, on the same Canvas. The Canvas dimensions establish a coordinate system for _painting annotations_ and other kinds of annotation that link content with the Canvas; they are not pixels of images.

The example demonstrates the use of the common descriptive properties [`label`][prezi-40-model-label] for the title of the artwork, [`metadata`][prezi-40-model-metadata] for additional information to display to the user, [`summary`][prezi-40-model-summary] for a brief description of the artwork, [`rights`][prezi-40-model-rights] to assert a rights statement or license from a controlled vocabulary, [`homepage`][prezi-40-model-homepage] to link to the artwork's specific web page, [`thumbnail`][prezi-40-model-thumbnail] to provide a small image to stand for the Manifest, [`provider`][prezi-40-model-provider] to give information about the publisher of the Manifest, and finally, [`service`][prezi-40-model-service] to specify a IIIF Image API service that provides features such as deep zooming, derivative generation, image fragment referencing, rotation, and more.

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
* Every JSON object that has a [`type`][prezi-40-model-type] property also has an [`id`][prezi-40-model-id] property and vice versa.
* Text elements intended for display to the user are conveyed by _Language Maps_, JSON objects in which the keys are language codes and the values are lists of one or more strings in that language.  [👀 Model Documentation](model/#language-of-property-values)
* The Painting Annotation is a member of the [`items`][prezi-40-model-items] property of an Annotation Page. While in this case there is only one Annotation Page and one Annotation, the mechanism is needed for consistency when there are multiple Annotation Pages, and it allows for Annotation Pages in general to be separate resources on the web.
* The [`metadata`][prezi-40-model-metadata] label and value pairs are for display to the user rather than for machines to interpret.
* The [`rights`][prezi-40-model-rights] property is always a single string value which is a URI.
* Any resource can have a [`provider`][prezi-40-model-provider] property which a client can display to the user. This typically tells the user who the publisher is and how they might be contacted. The value of this property is an [Agent](model/#agent).
* The [`service`][prezi-40-model-service] property specifies a software application that a client might interact with to gain additional information or functionality, in this case, the IIIF Image API. Images in IIIF do not require an Image Service---we have included one here as an example, but do not include a service in the following image examples for brevity.
{: .note}

!!! warning TODO: The above should be a green class rgb(244,252,239) to distinguish from properties

__Definitions__<br/>
Classes: [Manifest][prezi-40-model-Manifest], [Canvas][prezi-40-model-Canvas], [AnnotationPage][prezi-40-model-AnnotationPage], [Annotation][prezi-40-model-Annotation], [Agent][prezi-40-model-Agent]<br/><br/>
Properties: [id][prezi-40-model-id], [type][prezi-40-model-type], [label][prezi-40-model-label], [metadata][prezi-40-model-metadata], [summary][prezi-40-model-summary], [rights][prezi-40-model-rights], [homepage][prezi-40-model-homepage], [thumbnail][prezi-40-model-thumbnail], [provider][prezi-40-model-provider], and [service][prezi-40-model-Service]
{: .note}


## Use Case 2: Book

This example is a Manifest with multiple Canvases, each of which represents a page of a book. It demonstrates the use of the [`behavior`][prezi-40-model-behavior] property to indicate to a client that the object is _paged_---this helps a client generate the correct user experience. The [`viewingDirection`][prezi-40-model-viewingDirection] property indicates that the book is read left-to-right. In this case, the property is redundant as `left-to-right` is the default value. The Manifest has a [`rendering`][prezi-40-model-rendering] property linking to a PDF representation; typically a client would offer this as a download or "view as" option. The [`start`][prezi-40-model-start] property is used to tell a client to initialize the view on a particular Canvas, useful if the digitized work contains a large amount of irrelevant front matter or blank pages. The [`requiredStatement`][prezi-40-model-requiredStatement] is a message that a client MUST show to the user when presenting the Manifest.

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
Classes: [Manifest][prezi-40-model-Manifest], [Canvas][prezi-40-model-Canvas]<br/><br/>
Properties: [behavior][prezi-40-model-behavior], [viewingDirection][prezi-40-model-viewingDirection], [start][prezi-40-model-start], [rendering][prezi-40-model-rendering], [requiredStatement][prezi-40-model-requiredStatement]
{: .note}



## Use Case 3: Periodical

This example demonstrates the use of IIIF Collections to group Manifests into a hierarchy. In this case, there is a Collection for a run of the _The Tombstone Epitaph_, published from 1880 to 1920. This contains 41 child Collections each representing a year's worth of issues. The parent Collection and each of its child Collections use the [`behavior`][prezi-40-model-behavior] "multi-part" to signal that the Collections and their Manifests are part of a logical set. Each of the year Collections has one Manifest for each issue of the newspaper.

The top-level Collection has a [`navPlace`][prezi-40-model-navPlace] property that could be used on a "Newspapers of America" map to allow users to view newspapers by location. Each Manifest has a [`navDate`][prezi-40-model-navDate] property that could be used to plot the issues on a timeline or calendar-style user interface. Within each Manifest, the [`structures`][prezi-40-model-structures] property provides Ranges which are used to identify individual sections of the Newspaper, and individual stories within those sections, which may be spread across multiple columns and pages. Each story's Range includes the [`supplementary`][prezi-40-model-supplementary] property to link to an Annotation Collection that provides the text of the story.

IIIF Collection with [`behavior`][prezi-40-model-behavior] "multi-part" that contains the individual "multi-part" Collections for each year/volume:

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
IIIF Collection with [`behavior`][prezi-40-model-behavior] "multi-part" for the second volume (1881), with individual Manifests for each issue:

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
Classes: [Collection][prezi-40-model-Collection], [Range][prezi-40-model-Range], [AnnotationCollection][prezi-40-model-AnnotationCollection]<br/><br/>
Properties: [behavior][prezi-40-model-behavior], [navPlace][prezi-40-model-navPlace], [navDate][prezi-40-model-navDate], [structure][prezi-40-model-structures], [supplementary][prezi-40-model-supplementary]
{: .note}

thumbnail-nav
sequence



# Audio and Video

## Use Case 4: A 45 single with 2 tracks

This example is a Manifest with two Timelines, each of which represent a temporal extent during which a song is played. As in most cases, the Timeline [`duration`][prezi-40-model-duration] is the same length as that of Content Resource painted into it. This example is a recording digitized from a 45 RPM 7 inch single. It demonstrates the use of [`format`][prezi-40-model-format] for the audio files' content type, [`language`][prezi-40-model-language] (One song is in English and one is in German), [`behavior`][prezi-40-model-behavior] with value "auto-advance" that tells a client to automatically advance to the second Timeline after playing the first, [`annotations`][prezi-40-model-annotations] that link to Annotation Pages of annotations with the motivation `supplementing` that provide the lyrics (one example is given afterwards) - and an [`accompanyingContainer`][prezi-40-model-accompanyingContainer] that carries a picture of the single's cover that is shown while the songs are playing.


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
              "motivation": [ "painting" ],
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
      "motivation": [ "supplementing" ],
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
Classes: [Manifest][prezi-40-model-Manifest], [Timeline][prezi-40-model-Timeline],[TextualBody][prezi-40-model-TextualBody]<br/><br/>
Properties: [duration][prezi-40-model-duration], [format][prezi-40-model-format], [language][prezi-40-model-language], [behavior][prezi-40-model-behavior], [annotations][prezi-40-model-annotations], [accompanyingContainer][prezi-40-model-accompanyingContainer]
{: .note}


## Use Case 5: Movie with subtitles

This example is a Manifest with one Canvas that represents the temporal extent of the movie (the Canvas [`duration`][prezi-40-model-duration]) and its aspect ratio (given by the [`width`][prezi-40-model-width] and [`height`][prezi-40-model-height] of the Canvas). The example demonstrates the use of a [`Choice`][prezi-40-model-Choice] annotation body to give two alternative versions of the movie, indicated by their [`label`][prezi-40-model-label] and `fileSize` properties as well as [`height`][prezi-40-model-height] and [`width`][prezi-40-model-width]. Subtitles are provided by an annotation that links to a VTT file. The motivation of this annotation is `supplementing` and the [`provides`][prezi-40-model-provides] property of this annotation indicates what accessibility feature it provides, in this case the term `subtitles`. The [`timeMode`][prezi-40-model-timeMode] property in this case is redundant as `trim` is the default value. The Canvas has a [`placeholderContainer`][prezi-40-model-placeholderContainer] that provides a poster image to show in place of the video file before the user initiates playback.

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
* The decision about which item in the [`Choice`][prezi-40-model-Choice] to play by default is client dependent. In the absence of any other decision process the client should play the first item. In this specific example, the user might make the decision after reading the [`label`][prezi-40-model-label], or the client might make the decision based on the `fileSize` property and an assessment of the user's available bandwidth. However, the client may have no way of determining why the publisher has offered the choices, and should not prevent the user from making the choice. The cookbook demonstrates several uses of [`Choice`][prezi-40-model-Choice] for common image and AV use cases.
* Slop - impl note - don't interpret **very** minor discrepancies between [`duration`][prezi-40-model-duration] on the different Choices and the Container [`duration`][prezi-40-model-duration] as an instruction to stretch or compress the audio/video stream to match the Container duration. No real way to quantify this, just _be sensible_.
{: .note}


!!! warning TODO: The above should be a green class rgb(244,252,239) to distinguish from properties

__Definitions__<br/>
Classes: [Manifest][prezi-40-model-Manifest], [Canvas][prezi-40-model-Canvas], [Choice][prezi-40-model-Choice]<br/><br/>
Properties: [fileSize](#model/fileSize), [format][prezi-40-model-format], [provides][prezi-40-model-provides], [timeMode][prezi-40-model-timeMode], [behavior][prezi-40-model-behavior], [placeholderContainer][prezi-40-model-placeholderContainer]
{: .note}

# 3D

Scenes describe a 3D boundless space with infinite height (y axis), width (x axis) and depth (z axis), where 0 on each axis (the origin of the coordinate system) is treated as the center of the scene's space.

The positive y axis points upwards, the positive x axis points to the right, and the positive z axis points forwards (a [right-handed cartesian coordinate system](https://en.wikipedia.org/wiki/Right-hand_rule)).

<img src="https://raw.githubusercontent.com/IIIF/3d/eds/assets/images/right-handed-cartesian.png" title="Right handed cartesian coordinate system" alt="diagram of Right handed cartesian coordinate system" width=200 />

(Image: Wikipedia)

3D Content Resources are painted into Scenes. This can include 3D models, which can be painted into Scenes as Annotations with [`motivation`][prezi-40-model-motivation] "painting". Due to particular considerations of 3D space and rendering content within that space, such as scaling or textures with forward and backward faces, non-3D Content Resources must first be wrapped within an appropriate Container or Resource before being painted into a Scene. Image and video resources should be painted on to a Canvas, where the Canvas can in turn be painted into a Scene. Audio resources or Timelines should be referenced by an AudioEmitter and the AudioEmitter can be painted into a Scene. For further detail about painting Containers within other Containers, see [Nesting](#nesting).

## 3D Supporting Resources

Constructs from the domain of 3D graphics are expressed in IIIF as Resources. They are associated with Scenes via Painting Annotations in the same manner as Content Resources. They aid in or enhance the rendering of Content Resources, especially in Scenes.

### Cameras

A Camera provides a view of a region of the Scene's space from a particular position within the Scene; the client constructs a viewport into the Scene and uses the view of one or more Cameras to render that region. The size and aspect ratio of the viewport is client and device dependent.

There are two types of Camera, [`PerspectiveCamera`][prezi-40-model-PerspectiveCamera] and [`OrthographicCamera`][prezi-40-model-OrthographicCamera]. The first Camera defined and not [hidden](model#hidden-value) in a Scene is the default Camera used to display Scene contents. If the Scene does not have any Cameras defined within it, then the client provides a default Camera. The type, properties and position of this default camera are client-dependent.


### Lights

There are four types of Light: AmbientLight, DirectionalLight, PointLight and SpotLight. They have a [`color`][prezi-40-model-color] and an [`intensity`][prezi-40-model-intensity]. SpotLight has an additional property of [`angle`][prezi-40-model-angle] that determines the spread of its light cone.

If the Scene has no Lights, then the client provides its own lighting as it sees fit.


### Audio Emitters

There are three types of Audio emitter: AmbientAudio, PointAudio and SpotAudio. They have a [`source`][prezi-40-model-source] (an audio Content Resource) and a [`volume`][prezi-40-model-volume].

### Transforms

When painting resources into Scenes, it is often necessary to resize, rotate or move them relative to the coordinate space of the Scene. These operations are specified using three Transforms: ScaleTransform, RotateTransform and TranslateTransform. Each Transform has three properties, [`x`][prezi-40-model-x], [`y`][prezi-40-model-y] and [`z`][prezi-40-model-z] which determine how the Transform affects that axis in the local coordinate space.

Transforms are added to a SpecificResource using the [`transform`][prezi-40-model-transform] property, and there may be more than one applied when adding a model to a Scene. Different orders of the same set of transforms can have different results, so attention must be paid when creating the array and when processing it.


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
* In this simplest use case, the Painting Annotation targets the whole Scene rather than a specific point. The client places the model's origin at the Scene's origin. This is in contrast to the _bounded_ Containers [`Canvas`][prezi-40-model-Canvas] and [`Timeline`][prezi-40-model-Timeline], where the painted resource fills the Container completely.
{: .note}


## Use Case 5a: Simple 3D Model in Configured Scene

This example adds a Light and a Camera to the previous example, and places the model at a specific point rather than at the default origin position.

Annotations may use a type of Selector called a [`PointSelector`][prezi-40-model-PointSelector] to align the Annotation to a point within the Scene that is not the Scene's origin. PointSelectors have three spatial properties, [`x`][prezi-40-model-x], [`y`][prezi-40-model-y] and [`z`][prezi-40-model-z] which give the value on that axis. They also have a temporal property [`instant`][prezi-40-model-instant] which can be used if the Scene has a duration, which gives the temporal point in seconds from the start of the duration, the use of which is defined in the [section on Scenes with Durations]().

The Light is green and has a position, but has its default orientation of looking along the negative-y axis as no rotation has been specified. The Camera has a position and is pointing at the model's origin via the [`lookAt`][prezi-40-model-lookAt] property. The Camera has a [`fieldOfView`][prezi-40-model-fieldOfView] of 50. The [`near`][prezi-40-model-near] and [`far`][prezi-40-model-far] properties are included to ensure the model falls within the camera's range (although unnecessary in a simple Scene like this). The Scene has a background color.

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
                "source":
                {
                  "id": "https://example.org/iiif/scene1/page/p1/1",
                  "type": "Scene"
                },
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
              "body": [
                {
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
                }
              ],
              "target": [
                {
                  "type": "SpecificResource",
                  "source":
                  {
                    "id": "https://example.org/iiif/scene1/page/p1/1",
                    "type": "Scene"
                  },
                  "selector": [
                    {
                      "type": "PointSelector",
                      "x": 0.0,
                      "y": 6.0,
                      "z": 10.0
                    }
                  ]
                }
              ]
            },
            {
              "id": "https://example.org/iiif/3d/anno2",
              "type": "Annotation",
              "motivation": ["painting"],
              "body": [{
                  "id": "https://example.org/iiif/3d/lights/1",
                  "type": "SpotLight",
                  "label": {"en": ["Spot Light 1"]},
                  "angle": 90.0,
                  "color": "#A0FFA0"
              }],
              "target": [{
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
              }]
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
* A Point Selector explicitly places the model in the Scene via the Painting Annotation's [`target`][prezi-40-model-target] property. In the previous example, there was an implicit Point Selector placing the model at (0,0,0) because no explicit Point Selector was provided.
* The provided Light should replace any default lighting the client might have.
{: .note}

__Definitions__<br/>
Classes: [Manifest][prezi-40-model-Manifest], [Scene][prezi-40-model-Scene], [Model](#model/Model), [SpecificResource][prezi-40-model-SpecificResource], [PointSelector][prezi-40-model-PointSelector], [PerspectiveCamera][prezi-40-model-PerspectiveCamera], [SpotLight][prezi-40-model-SpotLight] <br/><br/>
Properties: [backgroundColor][prezi-40-model-backgroundColor], [lookAt][prezi-40-model-lookAt], [near][prezi-40-model-near], [far][prezi-40-model-far], [feildOfView][prezi-40-model-fieldOfView], [angle][prezi-40-model-angle], [color][prezi-40-model-color]
{: .note}

## Use Case 6: Complex Scene

This example is a Manifest with a single Scene with multiple models painted into the Scene at specific positions with transforms applied. It represents a collection of chess game pieces with multiple pawns and a single queen. The example demonstrates painting multiple models into a Scene, including one Content Resource being painted into a Scene multiple times. Transforms and Point Selectors are used to establish position and scale for Annotations. Some external web resources referenced as Content Resources may include elements such as lights or audio that are undesirable within a Manifest, and the [`exclude`][prezi-40-model-exclude] property is used to prevent these from being rendered. The property [`interactionMode`][prezi-40-model-interactionMode] is used to guide clients in how to best guide or limit user interaction with rendered content.

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
              "body": [{
                "id": "https://raw.githubusercontent.com/IIIF/3d/main/assets/chess/pawn.glb",
                "label": {"en": ["Pawn 1"]},
                "type": "Model",
                "format": "model/gltf-binary"
              }],
              "target": [{
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
              }]
            },
            {
              "id": "https://example.org/iiif/3d/anno1",
              "type": "Annotation",
              "motivation": ["painting"],
              "body": [{
                "type": "SpecificResource",
                "source":
                  {
                    "id": "https://raw.githubusercontent.com/IIIF/3d/main/assets/chess/pawn.glb",
                    "label": {"en": ["Pawn 2 tipped over"]},
                    "type": "Model",
                    "format": "model/gltf-binary"
                  },
                "transform": [
                  {
                    "type": "RotateTransform",
                    "x": 0.0,
                    "y": 0.0,
                    "z": -90.0
                  },
                  {
                    "type": "TranslateTransform",
                    "x": 0.0,
                    "y": 1.0,
                    "z": 0.0
                  }
                ]
              }],
              "target": [{
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
              }]
            },
            {
              "id": "https://example.org/iiif/3d/anno1",
              "type": "Annotation",
              "motivation": ["painting"],
              "exclude": ["Audio", "Lights"],
              "body": [{
                "type": "SpecificResource",
                "source":
                  {
                    "id": "https://raw.githubusercontent.com/IIIF/3d/main/assets/chess/queen.glb",
                    "label": {"en": ["Queen"]},
                    "type": "Model",
                    "format": "model/gltf-binary"
                  },
                "transform": [
                  {
                    "type": "ScaleTransform",
                    "x": 1.5,
                    "y": 1.5,
                    "z": 1.5
                  },
                ]
              }],
              "target": [{
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
              ]
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
* The [`exclude`][prezi-40-model-exclude] property instructs clients not to import or render any external audio or light content present in the Content Resource for the queen game piece.
* The [`interactionMode`][prezi-40-model-interactionMode] property instructs clients that, if possible, user interactions relating to orbiting the scene should be restricted to a hemisphere.
{: .note}

__Definitions__<br/>
Classes: [Manifest][prezi-40-model-Manifest], [Scene][prezi-40-model-Scene], [Model](#model/Model), [SpecificResource][prezi-40-model-SpecificResource], [PointSelector][prezi-40-model-PointSelector], [RotateTransform][prezi-40-model-RotateTransform], [TranslateTransform][prezi-40-model-TranslateTransform], [ScaleTransform][prezi-40-model-ScaleTransform]<br/><br/>
Properties: [exclude][prezi-40-model-exclude], [interactionMode][prezi-40-model-interactionMode]
{: .note}

<!--

Is this still needed or wanted here?

### Chessboard is a Canvas with image (not a 3D chessboard)

A Scene or a Canvas may be treated as a content resource, referenced or described within the [`body`][prezi-40-model-body] of an Annotation. As with models and other resources, the Annotation is associated with a Scene into which the Scene or Canvas is to be nested through an Annotation [`target`][prezi-40-model-target]. The content resource Scene will be placed within the [`target`][prezi-40-model-target] Scene by aligning the coordinate origins of the two scenes. Alternately, Scene Annotations may use [`PointSelector`][prezi-40-model-PointSelector] to place the origin of the resource Scene at a specified coordinate within the [`target`][prezi-40-model-target] Scene.

-->

## Use Case 7: Scene with Audio

This example is a Manifest with a single Scene with a duration. Multiple Audio Emitter Annotations are painted into the Scene, with positional emitters used to create a 3D audio experience. Some of the Audio Emitter Annotations are only painted into the Scene for a limited period of time, producing dynamic change in the sounds heard within the Scene. A commenting Annotation is also provided to highlight the instant in time when a change in sound occurs.

A content resource may be annotated into a Scene for a period of time by use of a PointSelector that is temporally scoped by a [FragmentSelector](https://www.w3.org/TR/annotation-model/#fragment-selector). The FragmentSelector has a `value` property, the value of which follows the [media fragment syntax](https://www.w3.org/TR/media-frags/#naming-time) of `t=`.  This annotation pattern uses the [`refinedBy`][prezi-40-model-refinedBy] property [defined by the W3C Web Annotation Data Model](https://www.w3.org/TR/annotation-model/#refinement-of-selection). When using a URL fragment in place of a SpecificResource, the parameter `t` can be used to select the temporal region. Both patterns are used in this example.

An Annotation may target a specific point in time using a PointSelector's [`instant`][prezi-40-model-instant] property.  The property's value must be a positive floating point number indicating a value in seconds that falls within the Scene's duration. In this example this is used for a comment Annotation.

In this example, the audio content resources have durations that do not match the Scene's duration. The Annotation property [`timeMode` property](https://iiif.io/api/presentation/3.0/#timemode) is used to indicate the desired behavior when the duration of the content resource that is not equal to the temporal region targeted by the annotation.

```jsonc
{
  "@context": "http://iiif.io/api/presentation/4/context.json",
  "id": "https://example.org/iiif/3d/model_origin.json",
  "type": "Manifest",
  "label": { "en": ["Use Case 7: Scene with Audio"] },
  "items": [
    {
      "id": "https://example.org/iiif/scene1/page/p1/1",
      "type": "Scene",
      "label": { "en": ["Positional Audio Symphony Hall Experience"] },
      "duration": 60,
      "items": [
        {
          "id": "https://example.org/iiif/3d/anno1",
          "type": "Annotation",
          "motivation": ["painting"],
          "body": [{
            "id": "https://example.org/iiif/audio/1",
            "type": "AmbientAudio",
            "source": {
              "id": "https://example.org/iiif/assets/symphony_hall_ambience.mp3",
              "type": "Audio",
              "format": "audio/mp3"
            },
            "volume": {
              "id": "https://example.org/iiif/quantity/1",
              "type": "Quantity",
              "unit": "relative",
              "quantityValue": 0.1
            }
          }],
          "target": [
            {
              "id": "https://example.org/iiif/scene1",
              "type": "Scene"
            }
           ]
        },
        {
          "id": "https://example.org/iiif/3d/anno2",
          "type": "Annotation",
          "motivation": ["painting"],
          "timeMode": "trim",
          "body": [{
            "id": "https://example.org/iiif/audio/2",
            "type": "PointAudio",
            "source": {
              "id": "https://example.org/iiif/assets/orchestra_percussion_120s.mp3",
              "type": "Audio",
              "format": "audio/mp3",
              "duration": 120.0
            },
            "volume": {
              "id": "https://example.org/iiif/quantity/2",
              "type": "Quantity",
              "unit": "relative",
              "quantityValue": 0.2
            }
          }],
          "target": [{
            "id": "https://example.org/iiif/selectors/anno2",
            "type": "SpecificResource",
            "source":
              {
                "id": "https://example.org/iiif/scene1",
                "type": "Scene"
              },
            "selector": [
              {
                "id": "https://example.org/uuid/9fbd580b-895b-41b9-974a-1553329037f2",
                "type": "PointSelector",
                "x": -3.0,
                "y": 0.0,
                "z": -2.0,
                "refinedBy": {
                    "id": "https://example.org/uuid/3d0d097b-2b37-4a15-b6a5-506e417d5115",
                    "type": "FragmentSelector",
                    "value": "t=0,30"
                }
              }
            ]
          }]
        },
        {
          "id": "https://example.org/iiif/3d/anno3",
          "type": "Annotation",
          "motivation": ["painting"],
          "timeMode": "loop",
          "body": [{
            "id": "https://example.org/iiif/audio/3",
            "type": "SpotAudio",
            "source": {
              "id": "https://example.org/iiif/assets/orchestra_tuba_10s.mp3",
              "type": "Audio",
              "format": "audio/mp3",
              "duration": 10.0
            },
            "angle": 45.0,
            "volume": {
              "id": "https://example.org/iiif/quantity/3",
              "type": "Quantity",
              "unit": "relative",
              "quantityValue": 0.3
            },
            "lookAt": "https://example.org/iiif/scene1"
          }],
          "target": [
            {
              "id": "https://example.org/iiif/scene1#xyz=3,0,-2&t=30,60",
              "type": "Scene"
            }
          ]
        }
      ],
      "annotations": [
        {
          "id": "https://example.org/iiif/3d/commenting",
          "type": "Annotation",
          "motivation": ["commenting"],
          "body": [
            {
              "type": "TextualBody",
              "value": "This is the point when the percussion stops playing and the tuba begins playing."
            }
          ],
          "target": [{
            "type": "SpecificResource",
            "source":
              {
                "id": "https://example.org/iiif/scene1",
                "type": "Scene"
              }
            ,
            "selector": [
                {
                    "type": "PointSelector",
                    "instant": 30.0
                }
            ]
          }]
        }
      ]
    }
  ]
}
```

>
**Key Points**
* The Scene has a duration of 60 seconds.
* The Scene has three different Audio Emitter Annotations painted into the Scene---AmbientAudio, PointAudio, and SpotAudio. Each Audio Emitter uses the [`volume`][prezi-40-model-volume] property to specify audio volume.
* AmbientAudio targets the Scene via a reference to the Scene URI, which implicitly targets the Scene's entire duration.
* PointAudio targets the Scene with a PointSelector to paint the Audio Emitter at a specific point in 3D space, and that PointSelector is temporally scoped by a FragmentSelector to target the first 30 seconds of the Scene duration.
* SpotAudio targets the Scene via a URL fragment to demonstrate an alternate approach to target a point and range of time in the Scene. It uses the [`lookAt`][prezi-40-model-lookAt] property to point the Audio Emitter cone toward the Scene origin.
* The content resources for PointAudio and SpotAudio use the property [`timeMode`][prezi-40-model-timeMode] to specify different ways of handling mismatches between content resource audio length and Scene duration.
* A commenting Annotation targets the Scene at the instant corresponding to 30 seconds of the Scene duration to highlight the point at which PointAudio stops playing and SpotAudio begins playing.
* It is an error to select a temporal region of a Scene that does not have a [`duration`][prezi-40-model-duration], or to select a temporal region that is not within the Scene's temporal extent.  A Canvas or Scene with a [`duration`][prezi-40-model-duration] may not be annotated as a content resource into a Scene that does not itself have a [`duration`][prezi-40-model-duration].
{: .note}

__Definitions__<br/>
Classes: [Manifest][prezi-40-model-Manifest], [Scene][prezi-40-model-Scene], [SpecificResource][prezi-40-model-SpecificResource], [PointSelector][prezi-40-model-PointSelector], [FragmentSelector][prezi-40-model-FragmentSelector], [AmbientAudio][prezi-40-model-AmbientAudio], [PointAudio][prezi-40-model-PointAudio], [SpotAudio][prezi-40-model-SpotAudio]<br/><br/>
Properties: [duration][prezi-40-model-duration], [volume][prezi-40-model-volume], [angle][prezi-40-model-angle], [lookAt][prezi-40-model-lookAt], [timeMode][prezi-40-model-timeMode]
{: .note}


# Nesting

> How does this relate to model doc? What's normative and needs to be in model.md because it defines a Scene?

A Container can be painted into another Container as an Annotation with [`motivation`][prezi-40-model-motivation] "painting". For example, a Timeline may be painted into a Canvas, a Canvas may be painted into another Canvas, a Canvas may be painted into a Scene, and a Scene may be painted into another Scene. Multiple Containers may be hierarchically nested within each other, and so the list of examples above could be implemented as a single nesting sequence of five Containers.

A Timeline, Canvas, or Scene with [`duration`][prezi-40-model-duration] can only be painted into a Container that also has [`duration`][prezi-40-model-duration]. It is possible to associate a Container with [`duration`][prezi-40-model-duration] with a Container that does not have [`duration`][prezi-40-model-duration] as the content of a `commenting` annotation rather than painting it into the Container. If a Container with [`duration`][prezi-40-model-duration] has a shorter or longer [`duration`][prezi-40-model-duration] than the Container into which it is to be painted, the [`timeMode`][prezi-40-model-timeMode] property can be used to instruct clients how to resolve the mismatch.

```jsonc
{
  "id": "https://example.org/iiif/presentation/examples/nesting/anno1",
  "type": "Annotation",
  "motivation": ["painting"],
  "timeMode": "loop",
  "body": [
    {
      "id": "https://example.org/iiif/presentation/examples/nesting/timeline/t1",
      "type": "Timeline",
      "label": { "en": [ "Side A: 99 Luftballons" ] },
      "duration": 231
    }
  ],
  "target": "https://example.org/iiif/presentation/examples/nesting/canvas-10minute-duration"
}
```


## Painting a Canvas or Timeline into a Scene

Painting nested content into a Scene has some special requirements that must be observed due to important distinctions relating to the infinite boundless 3D space described by a Scene. 2D image or video content resources can be painted into a Scene by first painting the image or video content resource on a Canvas and then painting the Canvas into the Scene. In the case of painting a Timeline into a Scene, an Audio Emitter can be painted into the scene where Timeline is the [`body`][prezi-40-model-body] of the Audio Emitter. This provides greater control over the intended presentation of the Timeline's audio content within the 3D space of the Scene.

A Canvas can be painted into a Scene as an Annotation, though differences between the 2D space described by a Canvas and the 3D space described by a Scene must be considered. A Canvas describes a bounded 2D space with finite [`height`][prezi-40-model-height] and [`width`][prezi-40-model-width] measured in 2D integer coordinates with a coordinate origin at the top-left corner of the Canvas, while Scenes describe a boundless 3D space with x, y, and z axes of 3D continuous coordinates and a coordinate origin at the center of the space. Further, although 2D images or videos with pixel height and width can be painted into a Canvas, Canvas 2D coordinates are not equivalent to pixels. An image of any height and width in pixels can be painted into a Canvas with different height and weight in coordinate units, and this has important consequences for painting Canvases into Scenes.

When a Canvas is painted as an Annotation targeting a Scene, the top-left corner of the Canvas (the 2D coordinate origin) is aligned with the 3D coordinate origin of the Scene. The top edge of the Canvas is aligned with (e.g., is colinear to) the positive x axis extending from the coordinate origin. The left edge of the Canvas is aligned with (e.g., is colinear to) the negative y axis extending from the coordinate origin. The direction terms "top", "bottom", "right", and "left" used in this section refer to the frame of reference of the Canvas itself, not the Scene into which the Canvas is painted.

The Canvas is scaled to the Scene such that the 2D coordinate dimensions correspond to 3D coordinate units - a Canvas 16 units wide and 9 units high will extend 16 coordinate units across the x axis and 9 coordinate units across the y axis. Because Canvas coordinate units and image content resource pixels are not equivalent, any image with a 16:9 aspect ratio painted on this Canvas would extend 16 coordinate units by 9 coordinate units in the 3D space of the Scene, whether it was 160 pixels wide and 90 pixels high or 16,000 pixels wide and 9,000 pixels high. This provides one way to control the size of a Canvas painted into a Scene.

A Canvas in a Scene has a specific forward face and a backward face. By default, the forward face of a Canvas should point in the direction of the positive z axis. If the property [`backgroundColor`][prezi-40-model-backgroundColor] is used, this color should be used for the backward face of the Canvas. Otherwise, a reverse view of the forward face of the Canvas should be visible on the backward face.

<div style="background: #A0F0A0; padding: 10px; padding-left: 30px; margin-bottom: 10px">
  To Do: Add an image demonstrating default Canvas placement in Scene
</div>

A [`PointSelector`][prezi-40-model-PointSelector] can be used to modify the point at which the Canvas will be painted, by establishing a new point to align with the top-left corner of the Canvas instead of the Scene coordinate origin. [Transforms](#transforms) can be used to modify Canvas rotation, scale, or translation, allowing in particular for an alternate method to control the size of a Canvas to be scaled appropriately to other contents within a Scene. The forward face and backward face of a Canvas can be interchanged with a Scale Transform scaling the z axis by -1.0, though this reflection will also produce mirroring.

```jsonc
{
  "id": "https://example.org/iiif/presentation/examples/nesting/anno2",
  "type": "Annotation",
  "motivation": ["painting"],
  "body": [{
    "type": "SpecificResource",
    "source":
      {
        "id": "https://example.org/iiif/presentation/examples/nesting/canvas/c1",
        "type": "Canvas",
        "width": 2,
        "height": 2,
        "items": [ { ... } ]
      },
    "transform": [
      {
        "type": "ScaleTransform",
        "x": 2.0,
        "y": 2.0,
        "z": -1.0
      }
    ]
  }],
  "target": [{
    "type": "SpecificResource",
    "source": {
      "id": "https://example.org/iiif/presentation/examples/nesting/scene/s1",
      "type": "Scene"
    },
    "selector": [
      {
        "type": "PointSelector",
        "x": 4.0,
        "y": 4.0,
        "z": 0.0
      }
    ]
  }]
}
```

>
**Key Points**
* The 2D Canvas painted into the Scene has an initial height and width of 2 units by 2 units. Absent any transform or the use of a PointSelector, this Canvas would by default face toward the Scene's positive z axis, would stretch 2 units across the x axis and 2 units across the y axis, and its top-left corner would align with the coordinate origin of the Scene. Instead, transforms and a PointSelector will modify this placement significantly.
* A ScaleTransform is used to double the Canvas height and width, so that after transformation the Canvas will extend 4 coordinate units across the Scene x axis and 4 coordinate units across the Scene y axis.
* The same ScaleTransform also reflects the z axis by scaling it by -1.0, meaning the Canvas is mirrored (flipped) and now faces toward the negative z axis.
* A PointSelector is used to align the top-left corner of the transformed Canvas with Scene coordinate (4,4,0). In combination with the ScaleTransform, the bottom-right corner of the Canvas is now aligned with the coordinate origin of the Scene.
{: .note}


## Painting a Scene into a Scene

Like Timelines or Canvases, Scenes can be painted into Scenes. As with other resources, it may be appropriate to modify the initial scale, rotation, or translation of a content resource Scene prior to painting it within another Scene. Scenes associated with SpecificResources may be manipulated through [Transforms](#transforms).

When a Scene is nested into another Scene, the [`backgroundColor`][prezi-40-model-backgroundColor] of the Scene to be nested should be ignored as it is non-sensible to import. All Annotations painted into the Scene to be nested will be painted into the Scene into which content is being nested, including Light or Camera resources. If the Scene to be nested has one or more Camera Annotations while the Scene into which content is being nested does not, the first Camera Annotation from the nested Scene will become the default Camera for the overall Scene.

```jsonc
{
    "id": "https://example.org/iiif/presentation/examples/nesting/anno3",
    "type": "Annotation",
    "motivation": ["painting"],
    "body": {
        "id": "https://example.org/iiif/presentation/examples/nesting/scene/s1",
        "type": "Scene"
    },
    "target": "https://example.org/iiif/presentation/examples/nesting/scene/s2"
}
```


# Annotations

In the examples so far, Annotations have been used to associate the images, audio and other Content Resources with their Containers for presentation. IIIF uses the same W3C standard for the perhaps more familiar _annotation_ concepts of commenting, tagging, describing and so on. Annotations can carry textual transcriptions or translations of the content, discussion about the content and any other linking between resources.

Whereas annotations that associate content resources with Containers are included in the [`items`][prezi-40-model-items] property of the Container, all other types of Annotation are referenced from the [`annotations`][prezi-40-model-annotations] property. Containers, Manifests, Collections and Ranges can all have this property, linking to relevant annotations. As with the [`items`][prezi-40-model-items] property, annotations are grouped into one or more AnnotationPage resources. These are usually external references.

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

Each Annotation Page can be embedded or externally referenced. Clients should process the Annotation Pages and their items in the order given in the Container.  Publishers may choose to expedite the processing of embedded Annotation Pages by ordering them before external pages, which will need to be dereferenced by the client.  Order can be significant, however. Annotations are assigned an ascending [z-index](https://developer.mozilla.org/en-US/docs/Web/CSS/z-index) from the first annotation encountered. Annotations with a higher z-index will render in front of those with a lower z-index when displayed on a Canvas.

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
      "motivation": [ "commenting" ],
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

A comment on a Canvas can target a non-rectangular area.  This example uses a [`SvgSelector`][prezi-40-model-SvgSelector] to comment on a painting.

```json
{
      "id": "https://example.org/iiif/presentation/examples/commenting/anno/2",
      "type": "Annotation",
      "motivation": [ "commenting" ],
      "body": [{
        "id": "https://example.org/iiif/presentation/examples/commenting/anno/2/person2",
        "type": "TextualBody",
        "language": "en",
        "format": "text/plain",
        "value": "Note the expressive eyes of the subject of this painting."
      }],
      "target": [{
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
    }]
}
```

Annotations may alternately use a different type of Selector, called a [`WktSelector`][prezi-40-model-WktSelector], to align the Annotation to a target region within a Canvas or Scene.

### A comment about 3D sculpture

A commenting annotation can also reference a Content Resource, such as a Model, within a Scene.  This is accomplished by targeting the annotation that paints the resource into the Scene.  In this example, the commenting annotation targets an annotation that paints a model of a portrait bust into a scene.

In some cases it is desirable to influence the client's positioning of the commenting annotation when rendered.  This may be done to ensure that the annotation does not hide key visual elements or to ensure that the annotation itself is not obscured by resources painted in the Container, such as 3D models. In these cases, the [`position`][prezi-40-model-position] property may be used to define the position where a TextualBody should be rendered.  The example shows a [`position`][prezi-40-model-position] that places the annotation at a specific coordinate within the Scene.  The position is a [`SpecificResource`][prezi-40-model-SpecificResource] that requires a [`source`][prezi-40-model-source] and `selector`.

```jsonc
{
    "@context": "http://iiif.io/api/presentation/4/context.json",
    "id": "https://example.org/iiif/manifest/commenting/manifest/3",
    "type": "Manifest",
    "label": { "en": [ "1st Centry Roman portrait bust with comment" ] },
    "items": [
      {
        "id": "https://example.org/iiif/scene/commenting/scene3",
        "type": "Scene",
        "items": [
          {
            "id": "https://example.org/iiif/scene/commenting/scene3/painting-annotation-pages/1",
            "type": "AnnotationPage",
            "items": [
                {
                    "id": "https://example.org/iiif/scene/commenting/scene3/sculpture",
                    "type": "Annotation",
                    "motivation": [ "painting"] ,
                    "label": {
                        "en": [ "A 1st century Roman portait bust." ]
                    },
                    "body": {
                        "id": "https://example.org/iiif/scene/commenting/models/portait.gltf",
                        "type": "Model"
                    },
                    "target": "https://example.org/iiif/scene/commenting/scene3"
                }
            ]
          }
        ]
      }
    ],
    "annotations": [
      {
        "id": "https://example.org/iiif/scene/commenting/scene3/commenting-annotation-pages/1",
        "type": "AnnotationPage",
        "items": [
          {
            "id": "https://example.org/iiif/presentation/examples/commenting/anno/3",
            "type": "Annotation",
            "motivation": [ "commenting" ],
            "body": {
              "id": "https://example.org/iiif/presentation/examples/commenting/anno/3/comment1",
              "type": "TextualBody",
              "language": "en",
              "format": "text/plain",
              "value": "This marble portrait exemplifies the veristic tradition that dominated Roman Republican portraiture and persisted into the early Imperial period.",
              "position": {
                "type": "SpecificResource",
                "source": [
                  {
                    "id": "https://example.org/iiif/scene/commenting/scene3",
                    "type": "Scene"
                  }
                ],
                "selector": [
                  {
                    "type": "PointSelector",
                    "x": 0.75,
                    "y": 1.5,
                    "z": 0.1
                  }
                ]
              }
            },
            "target": "https://example.org/iiif/scene/commenting/scene3/sculpture"
          }
        ]
      }
    ]
}
```

<!--
TODO: This is mostly copy-pasted from properties, is it needed here? Use in above example.

It is important to be able to position the textual body of an annotation within the Container's space that the annotation also targets. For example, a description of part of an image in a Canvas should be positioned such that it does not obscure the image region itself and labels to be displayed as part of a Scene should not be rendered such that the text is hidden by the three dimensional geometry of the model. The positioning of the textual body in a container is accomplished through the [`position`][prezi-40-model-position] property, which has as a value a Specific Resource identifying the targeted container as the source and a selector defining how the textual body should be positioned in the targeted container. If this property is not supplied, then the client should do its best to ensure the content is visible to the user.
 -->


## Linking Annotations

An Annotation with the motivation `linking` is used to create links between resources, both within the Manifest or to external content on the web, including other IIIF resources. Examples include linking to the continuation of an article in a digitized newspaper in a different Canvas, or to an external web page that describes the diagram in the Canvas. A client typically renders the links as clickable "Hotspots" - but can offer whatever accessible affordance as appropriate. The user experience of whether the linked resource is opened in a new tab, new window or by replacing the current view is up to the implementation.

The resource the user should be taken to is the [`body`][prezi-40-model-body] of the annotation, and the region of the Container that the user clicks or otherwise activates to follow the link is the [`target`][prezi-40-model-target]:

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

Sometimes it is necessary to modify the state of resources. Annotations with the motivation `activating` are referred to as _activating_ annotations, and are used to change resources from their initial state defined in the Manifest or from their current state. They allow IIIF to be used for interactive exhibitions, storytelling, digital dioramas and other interactive applications beyond simply conveying a set of static resources in a Container.

The [`target`][prezi-40-model-target] of the activating annotation is the resource that triggers an action. This could be a commenting annotation, for which a user might click a corresponding UI element. In other scenarios the [`target`][prezi-40-model-target] could be the painting annotation of a 3D model, or an annotation that targets part of a model, or a region of a Canvas, or a point or segment of a Timeline, or any other annotation that a user could interact with (in whatever manner) to trigger an event. Even a volume of space in a Scene or an extent of time in a Container with [`duration`][prezi-40-model-duration] could be the [`target`][prezi-40-model-target]. When that volume or time extent is triggered - which might be the user entering that volume or the playhead reaching the extent independently of user interaction - something happens.

This specification does not define how a client indicates to a user that a resource is able to be interacted with.

The body of the activating annotation is always an ordered list of Specific Resources, each with [`source`][prezi-40-model-source] and [`action`][prezi-40-model-action] properties. The [`source`][prezi-40-model-source] is the resource to be acted upon in some way, and the [`action`][prezi-40-model-action] property is an ordered list of named actions to perform on that resource. Valid values include "show", "hide", "enable", "disable", "start", "stop", "reset" and "select".

Activating annotations are provided in a Container's [`annotations`][prezi-40-model-annotations] property. They can be mixed in with the commenting (or other interactive annotations) they target, or they can be in a separate Annotation Page. The client should evaluate all of the enabled activating annotations it can find.


### Hiding and disabling resources

A resource with the [`behavior`][prezi-40-model-behavior] value "hidden" is not rendered by the client. A resource with the [`behavior`][prezi-40-model-behavior] value "disabled" is not available for user interaction and does not trigger any actions. The following example is a light switch that can be toggled on and off using activating annotations that result in these behaviors being applied or removed. It demonstrates a painted resource - a light - being shown and hidden, and activating annotations being enabled and disabled. Both of these are done by the client processing the action properties of the activating annotation bodies: the actions "show" and "hide" remove or add the behavior value "hidden", and the actions "enable" and "disable" modify the behavior value "disabled".

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
                            "body": [
                              {
                                "type": "SpecificResource",
                                "source": "https://example.org/iiif/scene/switch/scene-1/annos/1/activating-on-2",
                                "action": ["disable"]
                              },
                              {
                                "type": "SpecificResource",
                                "source": "https://example.org/iiif/scene/switch/scene-1/annos/1/activating-off-3",
                                "action": ["enable"]
                              },
                              {
                                "type": "SpecificResource",
                                "source": "https://example.org/iiif/scene/switch/scene-1/lights/point-light-4",
                                "action": ["show"]
                              }
                            ]
                        },
                        {
                            "id": "https://example.org/iiif/scene/switch/scene-1/annos/1/activating-off-3",
                            "type": "Annotation",
                            "motivation": [
                                "activating"
                            ],
                            "target": "https://example.org/iiif/painting-annotation/lightswitch-1",
                            "body": [
                              {
                                "type": "SpecificResource",
                                "source": "https://example.org/iiif/scene/switch/scene-1/annos/1/activating-off-3",
                                "action": ["disable"]
                              },
                              {
                                "type": "SpecificResource",
                                "source": "https://example.org/iiif/scene/switch/scene-1/lights/point-light-4",
                                "action": ["hide"]
                              },
                              {
                                "type": "SpecificResource",
                                "source": "https://example.org/iiif/scene/switch/scene-1/annos/1/activating-on-2",
                                "action": ["enable"]
                              }
                            ],
                            "behavior": ["disabled"]
                        }
                    ]
                }
            ]
        }
    ]
}
```

* Initially, a model of a light switch is painted into the Scene. A PointLight is also painted, but with the [`behavior`][prezi-40-model-behavior] "hidden", which means it is inactive (i.e., off). A commenting annotation with the text "Click the switch to turn the light on or off" targets the light switch. An activating annotation targets the painting annotation that paints the switch, so that user interaction with the light switch will trigger the activating annotation. This activating annotation has a [`body`][prezi-40-model-body] property with three Specific Resources. The first enables the "off" activating annotation, the second shows the PointLight, and the last disables the activating annotation _itself_ - this activating annotation can no longer be activated by a user interaction with the light switch model (its [`target`][prezi-40-model-target]).
* A further activating annotation has the opposite effect. Initially this has the [`behavior`][prezi-40-model-behavior] "disabled" - which means it is inactive. It also targets the painting annotation, but has no effect while disabled.
* When the user interacts with the light switch model, the client processes any activating annotations that target it and are enabled. In this case, the first activating annotation is triggered because while both target the switch, only the first is enabled. This activation shows the light (i.e., removes its "hidden" [`behavior`][prezi-40-model-behavior] and therefore turning it on) and enables the other activating annotation, and disables itself.
* If the user clicks the light again, the client again processes any activating annotations that target it and are not disabled. This time the second activating annotation is the enabled one - and it hides the light (turning it off) and disables itself, and enables the first activating annotation again.
* Subsequent clicks simply alternate between these two states, indefinitely.


### Triggering a named animation in a model

Sometimes a model file has inbuilt animations. While a description of these is outside the scope of IIIF, because it is 3D-implementation-specific, as long as there is a way to refer to a model's animation(s) by name, we can connect the animation to IIIF resources.

This pattern is also achieved with activating annotations, except that the body of the activating annotation references a _named animation_ in the model. The [`body`][prezi-40-model-body] is a Specific Resource, where the [`source`][prezi-40-model-source] is the Painting Annotation that paints the model, and the `selector` is of type [`AnimationSelector`][prezi-40-model-AnimationSelector] with the `value` being a string that corresponds to the name of the animation in the model.

The format of the `value` string is implementation-specific, and will depend on how different 3D formats support addressing of animations within models. The same model can be painted multiple times into the scene, and you might want to activate only one painted instance of the model's animation, thus we need to refer to the annotation that paints the model, not the model directly.


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
                      "value": "Click me to open the lid"
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
                      ],
                      "action": ["start"]
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

It is possible to associate a particular camera with a particular commenting annotation. In many complex 3D Scenes, it may not be clear from where to look at a particular point of interest. The view may be occluded by parts of the model, or other models in the Scene. In the following example, the user can explore the Scene freely, but when they select a particular comment, a specific Camera that was previously hidden (unavailable to the user) is activated, moving the user (i.e., setting the viewport) to a chosen position suitable for looking at the point of interest:


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
              "body":  [
                {
                  "id": "https://example.org/iiif/3d/cameras/1",
                  "type": "PerspectiveCamera",
                  "label": {"en": ["Perspective Camera Pointed At Front of Cranium and Mandible"]},
                  "fieldOfView": 50.0,
                  "near": 0.10,
                  "far": 2000.0
                }
              ],
              "target": [
                {
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
              ]
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
          "body": [
            {
            "type": "TextualBody",
            "value": "Mandibular tooth"
            }
          ],
          "target": {
            // SpecificResource with PointSelector
          }
        },
        {
          "id": "https://example.org/iiif/3d/commenting-anno-for-right-pterygoid-hamulus",
          "type": "Annotation",
          "motivation": ["commenting"],
          "body": [
            {
            "type": "TextualBody",
            "value": "Right pterygoid hamulus"
            }
          ],
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
              "type": "SpecificResource",
              "source": "https://example.org/iiif/3d/anno-that-paints-desired-camera-to-view-tooth",
              "action": ["show", "enable", "select"]
            }
          ]
        }
      ]
    }
  ]
}
```

The client will render a UI that presents the two commenting annotations in some form and allows the user to navigate between them. An active Camera is not provided (while there is a Camera in the Scene it has [`behavior`][prezi-40-model-behavior] "hidden", i.e., it is inactive: not usable). The commenting annotations are ordered; while the user might explore them freely in the Scene they might also go "forward" from the first to the second commenting annotation and "back" to the first from the second. In either case the above example instructs the client to activate the Camera when the user interacts with the comment. The user is free to move away but any interaction with that comment will bring them back to the specific viewpoint. (forward ref to chains of activation example)

Default camera:

<img src="{{ site.api_url | absolute_url }}/assets/images/p4/whale-default-camera.png" alt="Camera for annotation" >

Camera when annotation selected:

<img src="{{ site.api_url | absolute_url }}/assets/images/p4/whale-anno-camera.png" alt="Camera for annotation" >


#### Using scope to select a Camera

The previous example can also be expressed in a more concise form by providing a reference to the Camera in the `scope` property of the commenting annotation.

The commenting annotation now looks like this:

```json
{
  "id": "https://example.org/iiif/3d/commenting-anno-for-mandibular-tooth",
  "type": "Annotation",
  "motivation": ["commenting"],
  "bodyValue": "Mandibular tooth",
  "scope": [
    {
      "id": "https://example.org/iiif/3d/anno-that-paints-desired-camera-to-view-tooth",
      "type": "Annotation"
    }
  ],
  "target": {
    // SpecificResource with PointSelector
  }
},
```

... and the activating annotation is no longer required.

This only works for cameras.

Repeat full example? no, link to external.


### Interactivity, Guided Viewing and Storytelling

Activating annotations add explicit mechanisms for interactive user experiences such as guided viewing and storytelling. A narrative might comprise an Annotation Page of `commenting` annotations that target different parts of the Container, for example a guided tour of a painting or a map. For a Canvas or Timeline it is usually sufficient to leave the interactivity to the client; the fact that comments target different extents implies the client must offer some affordance for those comments (typically the user can click each one), and in response the client will move the current play point of the Timeline to the commenting annotation target, or pan and zoom the viewport to show the relevant part of an image. For 3D this may not be enough; a particular comment may only make sense from a certain viewpoint (i.e., Camera), or different steps of the story require different Lights to be active.

In a storytelling or exhibition scenario, the non-painting [`annotations`][prezi-40-model-annotations] might be carrying informative text, or even rich HTML bodies. They can be considered to be _steps_ in the story. The use of activating annotations allows a precise storytelling experience to be specified, including:

 - providing a specific viewpoint for each step of the narrative (or even a choice of viewpoints)
 - modifying the lighting of the Scene for each step, for example shining a spotlight on a point of interest
 - hiding models in the Scene at a particular step
 - showing additional models at a particular step

All the annotations referred to by the activating annotations' [`target`][prezi-40-model-target] and [`body`][prezi-40-model-body] properties are already present in the Scene from the beginning. Initially, many of them may have the behavior `hidden`, invisible until activated.

Interactive examples are provided as recipes in the [IIIF Cookbook](link).


#### The `sequence` behavior

While all Annotation Page [`items`][prezi-40-model-items] are inherently ordered, an Annotation Page with the [`behavior`][prezi-40-model-behavior] "sequence" is explicitly a narrative, and clients should prevent (dissuade) users from jumping about - the annotations, and the effects of them _activating_ other contents of the Container, are intended to be experienced in order and individually. Normally, a client might display all the comments in an Annotation Page in a sidebar so they are all visible in the UI, but for an Annotation Page with [`behavior`][prezi-40-model-behavior] "sequence" only show the currently active annotation text, and next and previous UI.



# Conveying Physical Dimensions

In many cases, the dimensions of a Canvas, or the pixel density of a photograph, are not necessarily related to a real-world size of the object they show. A large wall painting and a tiny miniature may both be conveyed by 20 megapixel source images on a 4000 by 3000 unit Canvas. But it can be important to know how big something is or if there is a relationship between pixel density and physical length, especially when comparing objects together. Each pixel in an image may correspond precisely to a physical area, allowing measurement of real world distances from the image. A scanned 3D model may be constructed such that each 3D coordinate unit corresponds to one meter of physical distance.

The [`spatialScale`][prezi-40-model-spatialScale] property of a Canvas or Scene provides a corresponding real-world scale for a unit of the Canvas or Scene coordinate system, allowing clients to provide scale information to users, for example by an on-screen virtual ruler. In a 2-up viewer, a client could scale two views to convey the true relative sizes of two objects.

The value of [`spatialScale`][prezi-40-model-spatialScale] is a `UnitValue` (ref) that has as a value a length unit. This specification defines only one length unit, "m", i.e., meters, though others may be defined externally as an [extension][prezi30-ldce]. If source size metadata is machine readable (or parse-able) in other measurement systems (e.g., feet and inches) then it should be converted to meters for use in [`spatialScale`][prezi-40-model-spatialScale]. Publishers may wish to present the original given measure (e.g., from catalogue metadata) in a [`metadata`][prezi-40-model-metadata] field for context.

The Presentation API also offers a corresponding [`temporalScale`][prezi-40-model-temporalScale] property for the [`duration`][prezi-40-model-duration] dimension of a Container, when 1 second in the Container does not correspond to 1 second of real time. This is useful for speeded-up or slowed-down audio or video.

An extreme example of both physical dimension properties together is a Canvas showing an animation of continental drift over the course of Earth history, where the spatialScale could convey that each Canvas unit is several thousand meters, and each second of the Canvas [`duration`][prezi-40-model-duration] is several million years.



# Integration

seeAlso, service(s), extensions
mention search, image api, auth

profile for seeAlso

partOf -

Talk about Content State and use the phrase "Content State Annotations" - how you transmit IIIF from software to software.

## Authentication

It is possible to include Image API service descriptions within the Manifest, and within those it is also possible to include links to the Authentication API's services that are needed to interact with the image content. The first time an Authentication API service is included within a Manifest, it _MUST_ be the complete description. Subsequent references _SHOULD_ be just the URI of the service, and clients are expected to look up the details from the full description by matching the URI. Clients _MUST_ anticipate situations where the Authentication service description in the Manifest is out of date: the source of truth is the Image Information document, or other system that references the Authentication API services.




# Other stuff

## Style

### Rotation

An image might not be correctly aligned with the Canvas, and require rotation as it is painted. In the following example, the image is painted with a 90-degree rotation. This example uses the ImageApiSelector to convey the number of degrees of the rotation. As this particular image has an image service, the client can use the Image API to request an image that has already been rotated on the server, or it can use the information in the ImageApiSelector to rotate the image itself.

```json
{
  "id": "http://example.org/iiif/book1/annotation/anno1",
  "type": "Annotation",
  "motivation": ["painting"],
  "body": [
    {
      "type": "SpecificResource",
      "source": {
        "id": "http://example.org/iiif/book1-page1/my-image.jpg",
        "type": "Image",
        "service": {
          "id": "http://example.org/iiif/book1-page1",
          "type": "ImageService3",
          "profile": "level2"
        }
      },
      "selector": {
        "type": "ImageApiSelector",
        "rotation": "90"
      }
  }
  ],
  "target": [
    {
      "id": "http://example.org/iiif/book1/canvas/p1#xywh=50,50,320,240",
      "type": "Canvas"
    }
  ]
}

```






# Protocol

This section outlines recommendations and requirements related to URIs, HTTP requests, and authentication for IIIF resources.

## URI Recommendations

While any HTTP(S) URI is technically acceptable for any of the resources in the API, there are several best practices for designing the URIs for the resources.

* The URI _SHOULD_ use the HTTPS scheme, not HTTP.
* The URI _SHOULD NOT_ include query parameters or fragments.
* Once published, they _SHOULD_ be as persistent and unchanging as possible.
* Special characters _MUST_ be encoded.

## HTTP Requests and Responses

This section describes the _RECOMMENDED_ request and response interactions for the API. The REST and simple HATEOAS approach is followed where an interaction will retrieve a description of the resource, and additional calls may be made by following links obtained from within the description. All of the requests use the HTTP GET method; creation and update of resources is not covered by this specification. It is _RECOMMENDED_ that implementations also support HTTP HEAD requests.

### Requests

Clients are only expected to follow links to Presentation API resources. Unlike [IIIF Image API][image-api] requests, or other parameterized services, the URIs for Presentation API resources cannot be assumed to follow any particular pattern.

### Responses

The format for all responses is JSON, as described above. It is good practice for all resources with an HTTP(S) URI to provide their description when the URI is dereferenced. If a resource is [referenced][prezi30-terminology] within a response, rather than being [embedded][prezi30-terminology], then it _MUST_ be able to be dereferenced.

If the server receives a request with an `Accept` header, it _SHOULD_ respond following the rules of [content negotiation][org-rfc-7231-conneg]. Note that content types provided in the `Accept` header of the request _MAY_ include parameters, for example [`profile`][prezi-40-model-profile] or `charset`.

If the request does not include an `Accept` header, the HTTP `Content-Type` header of the response _SHOULD_ have the value `application/ld+json` (JSON-LD) with the [`profile`][prezi-40-model-profile] parameter given as the context document: `http://iiif.io/api/presentation/4/context.json`.

{% include api/code_header.html %}
```
Content-Type: application/ld+json;profile="http://iiif.io/api/presentation/4/context.json"
```
{: .urltemplate}

If the `Content-Type` header `application/ld+json` cannot be generated due to server configuration details, then the `Content-Type` header _SHOULD_ instead be `application/json` (regular JSON), without a [`profile`][prezi-40-model-profile] parameter.

{% include api/code_header.html %}
```
Content-Type: application/json
```
{: .urltemplate}

The HTTP server _MUST_ follow the [CORS requirements][org-w3c-cors] to enable browser-based clients to retrieve the descriptions. If the server receives a request with one of the content types above in the Accept header, it _SHOULD_ respond with that content type following the rules of [content negotiation][org-rfc-7231-conneg]. Recipes for enabling CORS and conditional Content-Type headers are provided in the [Apache HTTP Server Implementation Notes][notes-apache].

Responses _SHOULD_ be compressed by the server as there are significant performance gains to be made for very repetitive data structures.



# Accessibility

(new section)

[`provides`][prezi-40-model-provides]
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

{% include links.md %}
