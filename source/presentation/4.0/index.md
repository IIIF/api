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
    ORCID:
    institution: UCLA
  - name: Julie Winchester
    ORCID: 
    institution: Duke University
  - name: Jeff Mixter
    ORCID: 
    institution: OCLC
hero:
  image: ''
---

## Status of this Document
{:.no_toc}
__This Version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest Stable Version:__ [{{ site.data.apis.presentation.latest.major }}.{{ site.data.apis.presentation.latest.minor }}.{{ site.data.apis.presentation.latest.patch }}][prezi-stable-version]

__Previous Version:__ [3.0][prezi30]

**Editors:**

{% include api/editors.md editors=page.editors %}

{% include copyright.md %}

----

## Introduction

Presentation, the clue is in the name


(non-exhaustive) List of use cases

1. Digitized books and manuscripts   (images, paged things, transcripts, translations)
2. Artworks and Maps                 (navPlace, maybe commenting annos)
3. Audio and Video recordings        (time-based, transcriptions)
4. 3D scans of objects               (3D)
5. Periodicals                       (Collections, Ranges, navDate)
6. Archival collections              (Collections, Ranges, navDate)
7. Storytelling and exhibitions      (State, annotations)

see Terminology at the end

Mention model.md

Mention cookbook



## Foundations

<p style="float: right">
  <img src="{{ site.api_url | absolute_url }}/assets/images/data-model.png" alt="Data Model" width="400"><br/>
</p>


### Manifests

A Manifest is the primary unit of distribution of IIIF. Each Manifest usually describes how to present an object, such as a book, statue, music album or 3 dimensional scene. It is a JSON document that carries information needed for the client to present content to the user, such as a title and other descriptive information. The scope of what constitutes an object, and thus its Manifest, is up to the publisher of that Manifest. The Manifest contains sufficient information for the client to initialize itself and begin to display something quickly to the user.

The Manifest's `items` property is an ordered list of _Containers_ of _Content Resources_ (images, 3D models, audio, etc). Client software loads the Manifest and presents the Content Resources to the user in that order.

Manifests have descriptive, technical and linking properties. The required properties of Manifests are `id`, `type`, `items` and `label`. Additional descriptive properties include `summary`, `metadata`, `rights`, `thumbnail`, `homepage` and `provider`. 

See the [Model Documentation](model/#manifest) for more information.

```
Manifest JSON
```


### Containers

A Container is a frame of reference that allows the relative positioning of Content Resources, a concept borrowed from standards like PDF and HTML, or applications like Photoshop and PowerPoint, where an initially blank display surface has images, video, text and other content "painted" on to it. The frame is defined by a set of dimensions, with different types of Container having different dimensions. This specification defines three sub-classes of Container: Timeline (which only has a duration), Canvas (which has bounded height and width, and may have a duration), and Scene (which has infinite height, width and depth, and may have a duration). 

And we can also put other things:
"supplementing"



The defined Container types are: 

#### Timeline

A Container that represents a bounded temporal range, without any spatial coordinates.

* has continuous duration in seconds for all or part of its duration.
* Typically used for audio-only content

#### Canvas

A Container that represents a bounded, two-dimensional space and has content resources associated with all or parts of it. It may also have a bounded temporal range in the same manner as a Timeline.

* has integer, unitless width and height
* has optional continuous duration in seconds
* Typically used for Image content, and with duration, for Video content.

#### Scene

A Container that represents a boundless three-dimensional space and has content resources positioned at locations within it. Rendering a Scene requires the use of Cameras and Lights. It may also have a bounded temporal range in the same manner as a Timeline.

* has continuous, unitless x,y,z cartesian coordinate space
* has optional continuous duration in seconds
* Typically used for 3D models, and can include audio, video and image content


### Annotations

IIIF uses the concept of _Annotation_ to link resources together. Why is this a different sense from what I am used to? Because this: W3C go read that then come back.

BUT it can be used for notes in the margin, commentary and all those more usual senses of the word, too. It's just that we borrow that linking mechanism for the Content Resources, too.

Annotations are primarily used to associate content resources with Containers. The same mechanism is used for the visible and/or audible resources as is used for transcriptions, commentary, tags and other content. This provides a single, unified method for aligning information, and provides a standards-based framework for distinguishing parts of resources and parts of Canvases. As Annotations can be added later, it promotes a distributed system in which publishers can align their content with the descriptions created by others.

Now that we have this linking mechanism... PAINTING

Painting Annotations are used to associate models, lights, cameras, and IIIF containers such as Canvases, with Scenes. They have a `type` of "Annotation", a `body` (being the resource to be added to the scene) and a `target` (being the scene or a position within the scene). They must have a `motivation` property with the value of "painting" to assert that the resource is being painted into the Scene, rather than the Annotation being a comment about the Scene.
Everything is an anno but these are special and core

There are other important uses of annotation, they are not all painting annos - see later...

```
JSON of painting anno
```

By the time you get here you are comfortable dropping the phrase "painting annotation" into casual conversation.


### Content Resources


There is stuff that we want to show - images, video, audio, 3D models etc

Image, Sound, Video, Model, Text 
(see model)

And we can nest Containers so they are Content Resources too

SpecificResource



## Presenting Content Resources - what you came here for

### Images

A painting

A paged thing


### Audio and Video

A timeline - audio only

A video on a Canvas with duration


### 3D

A Scene in IIIF is a virtual container that represents a boundless three-dimensional space and has content resources, lights and cameras positioned at locations within it. It may also have a duration to allow the sequencing of events and timed media. Scenes have infinite height (y axis), width (x axis) and depth (z axis), where 0 on each axis (the origin of the coordinate system) is treated as the center of the scene's space. 
The positive y axis points upwards, the positive x axis points to the right, and the positive z axis points forwards (a [right-handed cartesian coordinate system](https://en.wikipedia.org/wiki/Right-hand_rule)).

The axes of the coordinate system are measured in arbitrary units and these units do not necessarily correspond to any physical unit of measurement. This allows arbitrarily scaled models to be used, including very small or very large, without needing to deal with very small or very large values. If there is a correspondence to a physical scale, then this can be asserted using the physical dimensions pattern(fwd-ref-to-phys-dims).

<img src="https://raw.githubusercontent.com/IIIF/3d/eds/assets/images/right-handed-cartesian.png" title="Right handed cartesian coordinate system" alt="diagram of Right handed cartesian coordinate system" width=200 />



As multiple models, lights, cameras, and other resources can be associated with and placed within a Scene container, Scenes provide a straightforward way of grouping content resources together within a space. Scenes, as well as other IIIF containers such as Canvases, can also be embedded within a Scene, allowing for the nesting of content resources. 

A Scene or a Canvas may be treated as a content resource, referenced or described within the `body` of an Annotation. As with models and other resources, the Annotation is associated with a Scene into which the Scene or Canvas is to be nested through an Annotation `target`. The content resource Scene will be placed within the `target` Scene by aligning the coordinate origins of the two scenes. Alternately, Scene Annotations may use `PointSelector` to place the origin of the resource Scene at a specified coordinate within the `target` Scene.


As with other containers in IIIF, Annotations are used to target the Scene to place content such as 3d models into the scene. Annotations are also used to add lights and cameras. A Scene can have multiple models, lights, cameras and other resources, allowing them to be grouped together. Scenes and other IIIF containers, such as Canvases, may also be embedded within Scenes, as described below in the nesting section [fwd-ref-to-nesting]. 

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



Whale bone with a camera and a light


## Annotations and State

### Annotations

non-painting

Comments, tags, etc

transcripts (and back ref to OCR on images etc)


### State

Content State

Activating annos


## Navigation

### navXXXX

These are just extracts as examples

```json
"navDate": "1776-01-01T00:00:00+00:00",
```

See this in Periodicals



```json
"navPlace": {
  "id": "https://iiif.io/api/cookbook/recipe/0318-navPlace-navDate/feature-collection/1",
  "type": "FeatureCollection",
  "features": [
    {
      "id": "https://iiif.io/api/cookbook/recipe/0318-navPlace-navDate/feature/1",
      "type": "Feature",
      "properties": {
        "label": { "en": ["Castel Sant'Angelo, Rome"] }
      },
      "geometry": {
        "type": "Point",
        "coordinates": [12.4663, 41.9031]
      }
    }
  ]
}
```
Map example

navDate
??? example


### Ranges

Periodical example - with navDate again
Table of Contents as simple example
thumbnail-nav
sequence


### Collections

Multi-vol work
Archive example
back ref to periodical?

Paged collections and conceptual collections




## Protocol



## Terminology

The principles of [Linked Data][org-linked-data] and the [Architecture of the Web][org-w3c-webarch] are adopted in order to provide a distributed and interoperable framework. The [Shared Canvas data model][shared-canvas] and [JSON-LD][org-w3c-json-ld] are leveraged to create an easy-to-implement, JSON-based format.

This specification uses the following terms:

* __embedded__: When a resource (A) is embedded within an embedding resource (B), the complete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will not result in additional information. Example: Canvas A is embedded in Manifest B.
* __referenced__: When a resource (A) is referenced from a referencing resource (B), an incomplete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will result in additional information. Example:  Manifest A is referenced from Collection B.
* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

The terms _array_, _JSON object_, _number_, _string_, and _boolean_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].
