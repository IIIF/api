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
6. Storytelling and exhibitions      (State, annotations)

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

Manifests have descriptive, technical and linking properties. The required properties of Manifests are `id`, `type`, `items` and `label`. Other commonly used properties include `summary`, `metadata`, `rights`, `thumbnail`, `homepage` and `provider`.

(👀) [Model Documentation](model/#manifest)

```
Manifest JSON
```


### Containers

A Container is a frame of reference that allows the relative positioning of Content Resources, a concept borrowed from standards like PDF and HTML, or applications like Photoshop and PowerPoint, where an initially blank display surface has images, video, text and other content "painted" on to it. The frame is defined by a set of dimensions, with different types of Container having different dimensions. This specification defines three sub-classes of Container: Timeline (which only has a duration), Canvas (which has bounded height and width, and may have a duration), and Scene (which has infinite height, width and depth, and may have a duration). 

The required properties of all Containers are `id`, and `type`. Most Containers also have the `items` and `label` properties. Further properties are required for the different types of Container.

The defined Container types are: 

#### Timeline

A Container that represents a bounded temporal range, without any spatial coordinates. It is typically used for audio-only content.

Timelines have an additional required property of `duration`, which gives the extent of the Timeline as a floating point number of seconds.


#### Canvas

A Container that represents a bounded, two-dimensional space, optionally with a bounded temporal range. Canvases are typically used for Image and Video content.

Canvases have two additional required properties: `height` and `width`, which give the spatial extent as unitless integers. Canvases may also have the `duration` property in the same manner as Timelines.

#### Scene

A Container that represents a boundless three-dimensional space, optionally with a bounded temporal range. Scenes are typically used for rendering 3D models, and can additionally have Cameras and Lights.

Scenes may also have the `duration` property in the same manner as Timelines.

(👀) [Model Documentation](model/#containers)

```json
Manifest JSON with a Timeline, a Canvas and a Scene
```

### Annotations

IIIF uses the concept of _Annotation_ to link resources together from around the web. This specification uses a World Wide Web Consortium (W3C) standard for this called the [Web Annotation Data Model][org-web-anno]. This is a structured linking mechanism useful for making comments about Content Resources, but IIIF's primary use of it is to associate the images, audio and other Content Resources with their Containers for presentation.

Different uses of Annotation are distinguished through their `motivation` property. This specification defines a value for `motivation` called `painting` for associating Content Resources with Containers, which this specification calls a Painting Annotation. The verb "paint" is also used to refer to the associating of a Content Resource with a Container by a Painting Annotation. This is from the notion of painting onto a canvas, a metaphor borrowed from art and used for image-based digital applications, and expanded by IIIF into "painting" any Content Resource into a Container of any number of dimensions.

The same linking mechanism is also used in IIIF with other motivations for transcriptions, commentary, tags and other content. This provides a single, unified method for aligning content, and provides a standards-based framework for referencing parts of resources. As Annotations can be added later, it promotes a distributed system in which further content such as commentary can be aligned with the objects published on the web.

The required properties of Annotations are `id`, `type`, `motivation`, and `target`. Most Annotations also have the `body` property.

The relationship between a Container and a painting annotation is not direct. Annotations are grouped within the `items` property of an Annotation Page, and the `items` property of the Container is a list of Annotation Pages. 

(👀) [Model Documentation](model/#annotations)

```
JSON of painting anno - image to canvas
```

### Content Resources

Content Resources are external web resources, including images, video, audio, 3D models, data, web pages or any other format. Typically these are the resources that will be "painted" onto a Container using a Painting Annotation.

The required properties of Content Resources are `id` and `type`. Other commonly used properties include `format`, and `width`, `height` and `duration` as appropriate to the Content Resource format.


#### Containers as Content Resources

Containers may also be treated as Content Resources and painted into other Containers. This allows rich composition of content, such as painting a Canvas bearing a Video into a Scene, or painting a 3D model along with its associated Lights into an encompassing Scene.

#### Referencing Parts of Resources

A common requirement is to refer to only part of a resource, either a Container or a Content Resource. There are two primary methods for achieving this: adding a fragment to the end of the URI for the resource, or creating a Specific Resource that describes the method for selecting the desired part.

##### Fragments

Parts of resources on the Web are identified using URIs with a fragment component that both describes how to select the part from the resource, and, as a URI, also identifies it. In HTML this is frequently used to refer to part of the web page, called an anchor. The URI with the fragment can be used in place of the URI without the fragment in order to refer to this part.

There are different types of fragment based on the format of the resource. The most commonly used type in IIIF is the W3C's Media Fragments specification, as it can define a temporal and 2D spatial region.

```
comment annotation about part of the previous example's Canvas using #Fragment
```


##### Specific Resource

URIs with fragments are insufficient for complex referencing, like circular regions or arbitrary text spans, and do not support other useful features such as describing styling or transformation. The Web Annotation Data Model introduces a class called `SpecificResource` that represents the resource in a specific context or role, which IIIF uses to describe these more complex requirements. The Specific Resource then identifies the part, and the description of how to extract it is given as an instance of a `Selector` class associated with it.

Several different classes of Selector are used in IIIF, including an alternative implementation of the fragment pattern called `FragmentSelector`. The fragment is given in the `value` property of the `FragmentSelector`, and the resource it should be applied to is given in `source`.

The required properties of Specific Resources are `id`, `type`, and `source`. Other commonly used properties include `selector`, `transform`, and `scope`.

```
comment annotation about part of the previous example's Canvas using FragmentSelector
```


## Presenting Content Resources

This section of the specification uses the use cases listed in the introduction to demonstrate the use of the IIIF Presentation API and introduce additional features.


### Images

#### Use Case 1: Artwork

This example is a Manifest with one Canvas, with an image of an artwork "painted" onto the Canvas. It demonstrates the use of the common descriptive properties `label` for the title of the artwork, `metadata` for additional information to display to the user, `summary` for a brief description of the artwork, `rights` to assert a rights statement or license from a controlled vocabulary, `homepage` to link to the artwork's specific web page, `thumbnail` to provide a small image to stand for the Manifest, and `provider` to give information about the publisher of the Manifest.

```
Example: a painting {}
Will demonstrate:

Manifest -> items -> Canvas -> items -> AnnoPage -> items -> Anno -> body -> Image
label, summary, metadata, rights, provider, homepage, thumbnail
```

Notice that the painting Annotation is a member of the `items` property of an Annotation Page. While in this case there is only one Annotation Page and one Annotation, the mechanism is needed for consistency when there are multiple Annotation Pages, and it allows for Annotation Pages in general to be separate resources on the web.


#### Example 2: Book

This example is a Manifest with multiple Canvases, each of which represents a page of a book. It demonstrates the use of the `behavior` property to indicate to a client that the object is _paged_: this helps a client generate the correct user experience. The `viewingDirection` property indicates that the book is read left-to-right. In this case, the property is redundant as `left-to-right` is the default value. The Manifest has a `rendering` property linking to a PDF representation; typically a client would offer this as a download or "view as" option. The `start` property is used to tell a client to initialize the view on a particular Canvas, useful if the digitized work contains a large amount of irrelevant front matter or blank pages. The `requiredStatement` is a message that a client MUST show to the user when presenting the Manifest.

```
Example: a paged thing - a book
requiredStatement, behavior, viewingDirection, (no Ranges), rendering - PDF version, start
```



### Audio and Video

#### Example: a 45 single with one Timeline per song/side

This example is a Manifest with two Timelines, each of which represent a temporal extent during which a song is played. As in most cases, the Timeline `duration` is the same length as that of Content Resource painted into it. This example is a recording digitized from a 45 RPM 7 inch single. It demonstrates the use of `format` for the audio files' content type, `language` (One song is in English and one is in German), `behavior` with value "autoPlay" that tells a client to automatically advance to the second Timeline after playing the first, `annotations` that link to Annotation Pages of annotations with the motivation `supplementing` that provide the lyrics (one example is given afterwards) - and an `accompanyingContainer` that carries a picture of the single's cover that is shown while the songs are playing.


```
Timeline
duration, autoPlay, format, annotations (transcript), language, accompanyingContainer
```

```
...
  (A single supplementing annotation for a line of the song) t= fragment
...
```

#### Example: a movie with subtitles

This example is a Manifest with one Canvas that represents the temporal extent of the movie (the Canvas `duration`) and its aspect ratio (given by the `width` and `height` of the Canvas). The example demonstrates the use of a `Choice` annotation body to give two alternative versions of the movie, the `timeMode` property ..., and `placeholderContainer` that provides a poster image to show in place of the video file before the user initiates playback.

```
Canvas
duration, behavior=autoplay, format, Choice of video 720p, 4K? (forward ref), timeMode, placeholderContainer
```

{
  Canvas
      duration: 3600
          movie.mp4
              duration: 3599.68
          movie.flv
              duration: 3600.8

}

Sometimes, two different formats derived from the same source may have slightly different durations, perhaps a few milliseconds out. What to do...


### 3D

Need to get PointSelector in early


Scenes have infinite height (y axis), width (x axis) and depth (z axis), where 0 on each axis (the origin of the coordinate system) is treated as the center of the scene's space. 
The positive y axis points upwards, the positive x axis points to the right, and the positive z axis points forwards (a [right-handed cartesian coordinate system](https://en.wikipedia.org/wiki/Right-hand_rule)).

The axes of the coordinate system are measured in arbitrary units and these units do not necessarily correspond to any physical unit of measurement. This allows arbitrarily scaled models to be used, including very small or very large, without needing to deal with very small or very large values. If there is a correspondence to a physical scale, then this can be asserted using the physical dimensions pattern(fwd-ref-to-phys-dims).

<img src="https://raw.githubusercontent.com/IIIF/3d/eds/assets/images/right-handed-cartesian.png" title="Right handed cartesian coordinate system" alt="diagram of Right handed cartesian coordinate system" width=200 />


```
```

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
                "refinedBy": {
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

The Annotation's [`timeMode` property](https://iiif.io/api/presentation/3.0/#timemode) can be used to indicate the desired behavior when the duration of the content resource that is not equal to the temporal region targeted by the annotation.

It is an error to select a temporal region of a Scene that does not have a `duration`, or to select a temporal region that is not within the Scene's temporal extent.  A Canvas or Scene with a `duration` may not be annotated as a content resource into a Scene that does not itself have a `duration`.


An annotation that targets a Scene using a PointSelector without any temporal refinement implicitly targets the Scene's entire duration.


All resources that can be added to a Scene have an implicit (e.g. Lights, Cameras) or explicit (e.g. Models, Scenes), local coordinate space. If a resource does not have an explicit coordinate space, then it is positioned at the origin of its coordinate space. In order to add a resource with its local coordinate space into a Scene with its own coordinate space, these spaces must be aligned. This done by aligning the origins of the two coordinate spaces.

Annotations may use a type of Selector called a `PointSelector` to align the Annotation to a point within the Scene that is not the Scene's origin. PointSelectors have three spatial properties, `x`, `y` and `z` which give the value on that axis. They also have a temporal property `instant` which can be used if the Scene has a duration, which gives the temporal point in seconds from the start of the duration, the use of which is defined in the [section on Scenes with Durations]().

Example Annotation that positions a model at a point within a Scene:

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
            "y": 0.0,
            "z": 1.0
          }
        ]
    }
}
```

Annotations may alternately use a type of Selector called a `WktSelector` to align the Annotation to a region with the Scene that is not the Scene's origin. WktSelectors have a single property, `value`, which is a string conforming to a WKT Linestring, LineStringZ, Polygon, or PolygonZ list of 2D or 3D coordinate points. Whether and how a region defined by a WktSelector may be translated to a single 2D or 3D coordinate point, for targeting or other purposes, is client-dependent.

<div style="background: #A0F0A0; padding: 10px; padding-left: 30px; margin-bottom: 10px">
❓Does WKTSelector have a duration/instant property? 
</div>

Example Annotation that comments on a 3D polygon within a Scene:

```
Todo add example
```



## Scene-Specific Resources

### 3D considerations / principles

"models" (content resources in 3D)
"local coordinate spaces"

### Camera

A Camera provides a view of a region of the Scene's space from a particular position within the Scene; the client constructs a viewport into the Scene and uses the view of one or more Cameras to render that region. The size and aspect ratio of the viewport is client and device dependent.

This specification defines two types of Camera:

| Class               | Description  |
| ------------------- | ------------ |
| `PerspectiveCamera` | `PerspectiveCamera` mimics the way the human eye sees, in that objects further from the camera are smaller |
| `OrthographicCamera` | `OrthographicCamera` removes visual perspective, resulting in object size remaining constant regardless of its distance from the camera |

Cameras are positioned within the Scene facing in a specified direction. Both position and direction are defined through the Annotation which adds the Camera to the Scene, described below in the sections on [Painting Annotations][], [Transforms][], and [Relative Rotation][]. If either the position or direction is not specified, then the position defaults to the origin, and facing direction defaults to pointing along the z axis towards negative infinity. The camera's up direction by default points along the y axis towards positive infinity, but this may be modified by transforms.   

The region of the Scene's space that is observable by the camera is bounded by two planes orthogonal to the direction the camera is facing, given in the `near` and `far` properties, and a vertical projection angle that provides the top and bottom planes of the region.

The `near` property defines the minimum distance from the camera at which something in the space must exist in order to be viewed by the camera. Anything nearer to the camera than this distance will not be viewed. Conversely, the `far` property defines a maximum distance from the camera at which something in the space must exist in order to be viewed by the camera. Anything further away will not be viewed.

For PerspectiveCameras, the vertical projection angle is specificed using the full angular extent in degrees from the top plane to the bottom plane using the `fieldOfView` property. The `fieldOfView` angle MUST be greater than 0 and less than 180. For OrthographicCameras, the vertical projection is always parallel and thus not defined. 

If any of these properties are not specified explicitly, they default to the choice of the client implementation.

<img src="https://raw.githubusercontent.com/IIIF/3d/eds/assets/images/near-far.png" title="Diagram showing near and far properties"  alt="drawing of a geometrical frustrum truncated by near and far distances" width="300" />


The first Camera defined and not hidden in a Scene is the default Camera used to display Scene contents. If the Scene does not have any Cameras defined within it, then the client MUST provide a default Camera. The type, properties and position of this default camera are client-dependent.

```json
{
  "id": "https://example.org/iiif/camera/1",
  "type": "PerspectiveCamera",
  "near": 1.0,
  "far": 100.0,
  "fieldOfView": 45.0    
}
```



### Light

One or more Lights MUST be present within the Scene in order to have objects within it be visible to the Cameras. 

This specification defines four types of Light:

| Class | Description  |
| ----- | ------------ |
| `AmbientLight` | AmbientLight evenly illuminates all objects in the scene, and does not have a direction or position. |
| `DirectionalLight` | DirectionalLight emits in a specific direction as if it is infinitely far away and the rays produced from it are all parallel. It does not have a specific position. |
| `PointLight` | PointLight emits from a single point within the scene in all directions. |
| `SpotLight` | SpotLight emits a cone of light from a single point in a given direction. |

Lights defined in this specification have a `color` and an `intensity`. The color is given as an RGB value, such as "#FFFFFF" for white. The intensity is the strength or brightness of the light, and described using a `Value` construct.

SpotLight has an additional property of `angle`, specified in degrees, which is the angle from the direction that the Light is facing to the outside extent of the cone. 

<img src="https://raw.githubusercontent.com/IIIF/3d/eds/assets/images/angle-of-cone.png" title="Angle of cone" alt="diagram of cone geometry showing how the angle of the cone is defined" width="250"/>

Lights that require a position and/or direction have these through the Annotation which associates them with the Scene, described below in the sections on [Painting Annotations][] and [Transforms][]. If a Light does not have an explicit direction, then the default is in the negative y direction (downwards). If a Light does not have an explicit position in the coordinate space, then the default is at the origin.

This specification does not define other aspects of Lights, such as the rate of decay of the intensity of the light over a distance, the maximum range of the light, or the penumbra of a cone. Implementation of these aspects is client-dependent.

If there are no Lights present within the Scene, then the viewer MUST add at least one Light. The types and properties of Lights added in this way are client-dependent.

```json
{
  "id": "https://example.org/iiif/light/1",
  "type": "AmbientLight",
  "color": "#FFFFFF",
  "intensity": {"type": "Value", "value": 0.6, "unit": "relativeUnit"}
}
```



### Transforms

The Annotation with a Selector on the target can paint a resource at a point other than the origin, however it will be at its initial scale and rotation, which may not be appropriate for the scene that is being constructed.

This specification defines a new class of manipulations for SpecificResources called a `Transform`, with three specific sub-classes. Each Transform has three properties, `x`, `y` and `z` which determine how the Transform affects that axis in the local coordinate space.


| Class           | Description  |
| --------------- | ------------ |
| ScaleTransform  | A ScaleTransform applies a multiplier to one or more axes in the local coordinate space. A point that was at 3.5, after applying a ScaleTransform of 2.0 would then be at 7.0. If an axis value is not specified, then it is not changed, resulting in a default of 1.0 |
| RotateTransform | A RotateTransform rotates the local coordinate space around the given axis in a counter-clockwise direction around the axis itself (e.g. around a pivot point of 0 on the axis). A point that was at x=1,y=1 and was rotated 90 degrees around the x axis would be at x=1,y=0,z=1. If an axis value is not specified, then it is not changed, resulting in a default of 0.0 |
| TranslateTransform | A TranslateTransform moves all of the objects in the local coordinate space the given distance along the axis. A point that was at x=1.0, after applying a TranslateTransform of x=1.0 would be at x=2.0. If an axis value is not specified then it is not changed, resulting in a default of 0.0 |

Transforms are added to a SpecificResource using the `transform` property. The value of the property is an array, which determines the order in which the transforms are to be applied. The resulting state of the first transform is the input state for the second transform, and so on. Different orders of the same set of transforms can have different results, so attention must be paid when creating the array and when processing it.

The point around which RotateTransform rotates the space is the origin. This "pivot point" cannot be changed directly, but instead a TranslateTransform can be used to move the desired pivot point to the be at the origin, then the RotateTransform applied.

Transforms are only used in the Presentation API when the SpecificResource is the `body` of the Annotation, and are applied before the resource is painted into the scene at the point given in the `target`.

```json
{
    "type": "SpecificResource",
    "source": {
        "id": "https://example.org/iiif/assets/model1.glb",
        "type": "Model"
    },
    "transform": [
      {
        "type": "RotateTransform",
        "x": 0.0,
        "y": 180.0,
        "z": 0.0
      },
      {
        "type": "TranslateTransform",
        "x": 1.0,
        "y": 0.0,
        "z": 0.0
      }
    ]
}
```


#### Relative Rotation

It is useful to be able to rotate a light or camera resource such that it is facing another object or point in the Scene, rather than calculating the angles within the Scene's coordinate space. This is accomplished with a property called `lookAt`, valid on DirectionalLight, SpotLight, and all Cameras. The value of the property is either a PointSelector, a WktSelector, the URI of an Annotation which paints something into the current Scene, or a Specific Resource with a selector identifying a point or region in an arbitrary container.

If the value is a PointSelector, then the light or camera resource is rotated around the x and y axes such that it is facing the given point. If the value is a WktSelector, then the resource should be rotated to face the given region. If the value is an Annotation which targets a point via a PointSelector, URI fragment or other mechanism, then the resource should be rotated to face that point. If the value is a Specific Resource, the source container for the Specific Resource must be painted into the current Scene, and the Specific Resource selector should identify a point or region in the source container. In this case, the light or camera resource should be rotated to face the point or region in the source container where the point or region is located within the current Scene's coordinate space. This allows light or camera resources to face a specific 2D point on a Canvas painted into a 3D scene.

This rotation happens after the resource has been added to the Scene, and thus after any transforms have taken place in the local coordinate space.

```json
"lookAt": {
    "type": "PointSelector",
    "x": 3,
    "y": 0,
    "z": -10
}
```


#### Excluding

Just as a Scene may contain multiple Annotations with model, light, and camera resources, a single 3D model file may contain a collection of 3D resources, including model geometry, assemblages of lights, and/or multiple cameras, with some of these potentially manipulated by animations. When painting Scenes or models that themselves may contain groups of resources within a single Scene, it may not always be appropriate to include all possible cameras, lights, or other resources, and it may be desirable to opt not to import some of these resources. This is accomplished through the Annotation property `exclude`, which prevents the import of audio, lights, cameras, or animations from a particular Scene or model prior to the Annotation being painted into a Scene. When `exclude` is used, the excluded resource type should not be loaded into the Scene, and it is not possible to reactivate or turn on these excluded resources after loading. 

Painting a Scene into another while excluding import of several types of resources:
```json
{
    "id": "https://example.org/iiif/3d/anno1",
    "type": "Annotation",
    "motivation": ["painting"],
    "exclude": ["Audio", "Lights", "Cameras", "Animations"],
    "body": {
        "id": "https://example.org/iiif/scene1",
        "type": "Scene"
    },
    "target": "https://example.org/iiif/scene2"
}
```







### Nesting

A Canvas can be painted into a Scene as an Annotation, but the 2D nature of Canvases requires special consideration due to important differences between Canvases and Scenes. A Canvas describes a bounded 2D space with finite `height` and `width` measured in pixels with a pixel origin at the top-left corner of the Canvas, while Scenes describe a boundless 3D space with x, y, and z axes of arbitrary coordinate units and a coordinate origin at the center of the space. It is important to note that in many cases the pixel scale used by a Canvas or a 2D image content resource will not be in proportion to the desired 3D coordinate unit scale in a Scene. 

When a Canvas is painted as an Annotation targeting a Scene, the top-left corner of the Canvas (the pixel origin) is aligned with the 3D coordinate origin of the Scene. The top edge of the Canvas is aligned with (e.g., is colinear to) the positive x axis extending from the coordinate origin. The left edge of the Canvas is aligned with (e.g., is colinear to) the negative y axis extending from the coordinate origin. The Canvas is scaled to the Scene such that the pixel dimensions correspond to 3D coordinate units - a Canvas 200 pixels wide and 400 pixels high will extend 200 coordinate units across the x axis and 400 coordinate units across the y axis. Please note: direction terms "top", "bottom", "right", and "left" used in this section refer to the frame of reference of the Canvas itself, not the Scene into which the Canvas is painted.

A Canvas in a Scene has a specific forward face and a backward face. By default, the forward face of a Canvas should point in the direction of the positive z axis. If the property `backgroundColor` is used, this color should be used for the backward face of the Canvas. Otherwise, a reverse view of the forward face of the Canvas should be visible on the backward face.

<div style="background: #A0F0A0; padding: 10px; padding-left: 30px; margin-bottom: 10px">
  To Do: Add an image demonstrating default Canvas placement in Scene
</div>

A `PointSelector` can be used to modify the point at which the Canvas will be painted, by establishing a new point to align with the top-left corner of the Canvas instead of the Scene coordinate origin. Transforms can also be used to modify Canvas rotation, scale, or translation.

It may be desirable to exercise greater control over how the Canvas is painted into the Scene by selecting the coordinate points in the Scene that should correspond to each corner of the Canvas. This provides fine-grained manipulation of Canvas placement and/or scale, and for optionally introducing Canvas distortion or skew. Annotations may use a WktSelector to select different points in the Scene to align with the top-left, bottom-left, bottom-right, and top-right corners of the Canvas. In this case, the four Scene coordinates should be listed beginning with the coordinate corresponding to the top-left corner of the Canvas, and should proceed in a counter-clockwise winding order around the Canvas, with coordinates corresponding to bottom-left, bottom-right, and top-right corners in order respectively. The use of WktSelector for this purpose overrides any use of Transforms on the Canvas Annotation.

Example placing top-left at (0, 1, 0); bottom-left at (0, 0, 0); bottom-right at (1, 0, 0); and top-right at (1, 1, 0):
```json
"selector": [
  {
    "type": "WktSelector",
    "value": "POLYGONZ((0 1 0, 0 0 0, 1 0 0, 1 1 0))"
  }
]
```

When a Scene is nested into another Scene, the `backgroundColor` of the Scene to be nested should be ignored as it is non-sensible to import. All Annotations painted into the Scene to be nested will be painted into the Scene into which content is being nested, including Light or Camera resources. If the Scene to be nested has one or more Camera Annotations while the Scene into which content is being nested does not, the first Camera Annotation from the nested Scene will become the default Camera for the overall Scene. 


















Whale bone with a camera and a light


## Annotations and State

### Annotations

non-painting

Comments, tags, etc

transcripts (and back ref to OCR on images etc)


### Comment Annotations



### Choice of Alternative Resources

Multispectral here


### Embedded Content

e.g., painting TextualBody on Canvas

Todo: This is mostly copy-pasted from properties, is it needed here?
It is important to be able to position the textual body of an annotation within the Container's space that the annotation also targets. For example, a description of part of an image in a Canvas should be positioned such that it does not obscure the image region itself and labels to be displayed as part of a Scene should not be rendered such that the text is hidden by the three dimensional geometry of the model. The positioning of the textual body in a container is accomplished through the `position` property, which has as a value a Specific Resource identifying the targeted container as the source and a selector defining how the textual body should be positioned in the targeted container. If this property is not supplied, then the client should do its best to ensure the content is visible to the user.





### Non Rectangular Segments

SvgSelector - move to SpecificResource too ^^


### Style

Move to SpecificResource


### Rotation


### Hotspot Linking and Activation

Move to SpecificResource




#### Annotation Page

"Overlapping elements with a larger z-index cover those with a smaller one."
link to https://developer.mozilla.org/en-US/docs/Web/CSS/z-index



#### Annotation Collection

deal with this:
https://github.com/IIIF/api/pull/2304/files#diff-cc70f02818f6bed2b14dfbf8bf3206e0825047951c8e83ad56fc73e489f82ac4R1757

use totalItems? https://iiif.io/api/discovery/1.0/#totalitems 








## Navigation

### Collection

IIIF Collections are ordered lists of Manifests, Collections, and/or Specific Resources. Collections allow these resources to be grouped in a hierarchical structure for navigation and other purposes.

:eyes: 

### Range

IIIF Ranges are used to represent structure _WITHIN_ a Manifest beyond the default order of the Containers in the `items` property. Example uses include newspaper sections or articles, chapters within a book for a table of contents, or movements within a piece of music. Ranges can include Containers, parts of Containers via Specific Resources or fragment URIs, or other Ranges, creating a tree structure like a table of contents. The typical intent of adding a Range to the Manifest is to allow the client to display a linear or hierarchical navigation interface to enable the user to quickly move through the object's content.

:eyes:

### Example: Periodical

This example demonstrates the use of IIIF Collections to group Manifests into a hierarchy. In this case, there is a Collection for a publishing run of the _The Tombstone Epitaph_ from 1880 to 1920. This contains 41 child Collections each representing a year's worth of issues. Each of these year Collections in turn has one Manifest for each daily issue of the newspaper.

Within each Manifest, the `structures` property provides Ranges which are used to identify individual sections of the Newspaper, and individual stories within the sections which may be spread across multiple columns and pages.

Each Manifest has a `navDate` property that could be used to plot the issues on a calendar-style user interface. 
The top level Collection has a `navPlace` property that could be used on a "Newspapers of America" map to allow users to view newspapers by location. Each story's Range links to an Annotation Collection that provides the text of the story via the `supplementary` property.


```
demonstrates navDate, navPlace, structures (Ranges), supplementary, Collections
...
```



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


thumbnail-nav
sequence



## Integration

seeAlso, service(s), extensions
mention search, image api, auth

profile for seeAlso

partOf - 




## State


## Content State

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

### Load a particular view of a resource or group of resources

In this usage, an annotation with the motivation `contentState` is passed to a client to initialize it with a particular view of a resource. Almost all IIIF Clients initialize from the very simplest form of Content State - a Manifest URI. A more complex Content State might target a particular region of a particular canvas within a Manifest, as in the second example above. A client initialized from such a Content State would load the Manifest, show the particular Canvas, and perhaps zoom in on the target region.

The mechanisms for passing Content State into a client, and exporting a Content State from a client, are given in the [Content State Protocol API 2.0](content-state-2) specification, which describes the scenarios in which a URI, or Content State not carried by an annotation, should be interpreted by a Client as a Content State.


### Load a particular view of some resource and modify it

In the previous usage, the fragment of IIIF carried by the annotation with the motivation `contentState` provides enough information for a Client to load a resource and show it. This fragment can also carry additional IIIF Presentation API resources not shown in the referred-to resource. For example, in the following example the Content State carries additional annotations not present in the original published Manifest. A client initializing from this Content State would show these additional annotations to the user:

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

As well as adding resources not present in the referred-to resource, the Content State can also remove parts of the referred-to resource from the user's view by applying the behavior `hidden` to them:

```jsonc
{
  // What does this actually look like? I want to load bnf_chateauroux example but HIDE the illumination
  // ...
  "id": "https://iiif.io/api/cookbook/recipe/0036-composition-from-multiple-images/annotation/p0001-image",
  "type": "Annotation",
  "motivation": "painting",
  "behavior": ["hidden"]
}
```

TODO: what is the processing algorithm for applying incoming `hidden` ?

When a Content State annotation carries a Scene, a view might be initialized from a Content State that introduces an additional Camera that shows the user the point of interest. 


### Modify the Container in a particular context

The techniques in the previous example are also used within a published IIIF Manifest to modify the contents of a Container in the contexts of different annotations on that Container. This technique allows IIIF to be used for _storytelling_ and other narrative applications beyond simply conveying a static Digital Object into a viewer and leaving subsequent interactions entirely in the control of the user. The `scope` property indicates to the client that the Content State provides valuable context for displaying some aspect of a Scene or other Container. In the case of a commenting annotation, this means that the Content State should be loaded when the commenting annotation is selected or otherwise highlighted. 


Consider a Scene with two models, and two `commenting` annotations:

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
          "id": "https://example.org/iiif/3d/anno7",
          "type": "Annotation",
          "motivation": ["commenting"],
          "bodyValue": "Mandibular tooth",
          "target": { 
            // SpecificResource with PointSelector
          }
        },
        {
          "id": "https://example.org/iiif/3d/anno5",
          "type": "Annotation",
          "motivation": ["commenting"],
          "bodyValue": "Right pterygoid hamulus",
          "target": { 
            // SpecificResource with PointSelector
          }
        }
      ]
    }
  ]
}
```

In that form, the user is left to interpret the commenting annotations and explore the Scene. The client will render a UI that presents the two commenting annotation in some form and allow the user to navigate between them. The commenting annotations are ordered; while the user might explore them freely in the Scene they might also go "forward" from the first to the second commenting annotation and "back" to the first from the second. 

In many complex 3D Scenes, it may not be clear what or how to look at a particular point of interest even when the commenting annotation targets a particular point. The view may be occluded by parts of the model, or other models in the Scene. It may be useful to light the Scene differently in different contexts.

In the same way an incoming Content State can modify a Scene as it initializes the client, so can a Content State attached to each (non-`painting`) annotation target modify the Scene as the user moves between different annotations.

The `scope` property of an annotation `target` provides _contextual_ Content State - the viewer should modify the Scene by applying the Content State carried by the `scope` property _only when the user is in the context of that annotation_.

Taking the first commenting annotation from the above example and adding a `scope` property, whose value is an annotation with the motivation `contentState`, we can introduce a new Camera specifically for this particular annotation, so that when the user selects this comment, the client will switch the view to this camera. This example also changes the background color of the Scene:

```jsonc
{
  "id": "https://example.org/iiif/3d/anno7",
  "type": "Annotation",
  "motivation": ["commenting"],
  "bodyValue": "Mandibular tooth",
  "target": {

    // SpecificResource with PointSelector
    // "type": "SpecificResource",
    // "source": ... the Scene...
    // "selector": ... a point ...

    "scope": {  // a modification to the Scene, only in the context of this annotation

      "id": "https://example.org/iiif/3d/anno4",
      "type": "Annotation",
      "motivation": ["contentState"],
      "target": {
        "id": "https://example.org/iiif/scene1/page/p1/1",
        "type": "Scene",
        "backgroundColor": "yellow",
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
          }
        ]
      }
    }
  }
}
```

In a storytelling or exhibition scenario, the non-painting `annotations` might be carrying informative text, or even rich HTML bodies. They can be considered to be _steps_ in the story. The use of `scope` allows a precise storytelling experience to be specified, including:

 - providing a specific viewpoint for each step of the narrative (or even a choice of viewpoints)
 - modifying the lighting of the Scene for each step, for example shining a spotlight on a point of interest
 - hiding parts of the Scene for a step
 - introducing additional models at a particular step
 - (and many more!)

Use of `scope` is permitted in annotations on any Container type, not just Scenes. For example, a 2D narrative around a Canvas might show or hide different `painting` annotations at each step.






#### The `sequence` behavior

// Is this right? Language...

While all AnnotationPage `items` are inherently ordered, an Annotation Page with the behavior `sequence` is explicitly a narrative, and clients should prevent (dissuade) users from jumping about. The presence of `sequence` affects the way a client should interpret the `reset` property described below.

### Content States on Manifests

When an annotation with the motivation `contentState` is provided via the `annotations` property of a Manifest, rather than contextually via `scope`, it is assumed to be generally available for selection by the user at any time. A client may present such as annotations as a menu of views, allowing arbitrary jumping into any Scene (or Canvas or Timeline) from any other point.

// Is there some overlap here with Range?

### Processing Content States in Scopes: reset

// This may not be what we have discussed...

When a Content State is applied to a Container such as a Scene, it is assumed to be a "diff" - for example if 3 cameras and 4 lights are already present in the Scene, and a Content State asserts a single new Camera, the default behavior is to add this fourth Camera to the Scene and leave the existing resources as they are.

The client should reset the Container to its original state before applying the diff operation. However, for narratives that cumulatively build a Scene this may lead to excessively verbose Manifests. When moving through the items of an Annotation page with the behavior `sequence`, the Container is not reset and the diff is cumulative; modifications from one `scope` persist into the next. If this behavior is not wanted, the `reset` property of the content state annotation should be set to `true`:

```json
{
  "type": "Annotation",
  "motivation": ["contentState"],
  "reset": true
}
```

Before applying the content state to the Scene, the client should reset the Scene to its original state as provided by the Manifest.

// I am assuming reset is always true except in `sequence` - otherwise it's completely unpredictable!! or is it... arbitrary navigation, state provided by initialization content states, etc...

### Contribute additional information permanently

Rerum inbox scenario - should be covered in CS2 protocol

### activating - animation and interactions

Annotations with the motivation `activating` are referred to as _activating_ annotations.

There are two uses of `activating` annotations:

#### Triggering a content state

An activating annotation links a painting annotation to a content state. When a user interacts with the painting annotation - whether through clicking it, tapping it, or other client-specific behaviors - the linked content state should be processed to modify the Scene or other Container, as in the previous examples. The painting annotation is the target of the activating annotation, and the content state is the body value. Only one content state may be specified in the body array, but the body array may include a `TextualBody` to provide a label for the interaction. The pattern is the same as for the `linking` motivation, but rather than the client opening a new browser window on the resource specified in the `body`, it applies the modification provided by the Content State.

The activating annotation is provided in a Container's `annotations` property. In this (contrived for brevity) example, if the user clicks the mandible model, the Scene background changes color:

```jsonc
{
  "id": "https://example.org/iiif/3d/activating.json",
  "type": "Manifest",
  "label": { "en": ["Whale Cranium and Mandible with Dynamic Commenting Annotations and Custom Per-Anno Views"] },
  "items": [
    {
      "id": "https://example.org/iiif/scene1/scene-with-activation",
      "type": "Scene",
      "label": { "en": ["A Scene Containing a Whale Cranium and Mandible"] },
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
                  "id": "https://example.org/iiif/3d/anno2",
                  "type": "Annotation",
                  "motivation": ["activating"],
                  "body": [
                    {
                      "type": "TextualBody",
                      "value": "A label for the activation may be provided as a TextualBody"
                    },
                    {
                      // A body where the type is a IIIF Resource (eg Scene) is the Content State to apply
                      "id": "https://example.org/iiif/scene1/scene-with-activation",
                      "type": "Scene",
                      "backgroundColor": "#FF99AA"
                    }
                  ],
                  "target": {
                    "id": "https://example.org/iiif/3d/painting-anno-for-mandible",
                    "type": "Annotation"
                  }
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

// Can you put activating annotations in `manifest.annotations`? They would work there too, you have all the information.



#### Triggering a named animation in a model

Sometimes a model file has inbuilt animations. While a description of these is outside the scope of IIIF, because it is 3D-implementation-specific, as long as there is a way to refer to a model's animation(s) by name, we can connect the animation to IIIF resources.

This pattern is similar to the above, except that:

 - There is no Content State in the `body`, but there _MUST_ be a TextualBody to label the interaction. (?? must?)
 - The `target` selects a _named animation_ in the model. The `target` MUST be a SpecificResource, where the `source` is the painting annotation that paints the model, and the `selector` is of type `AnimationSelector` with the `value` being a string that corresponds to the animation in the model.

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
                  "id": "https://example.org/iiif/3d/anno2",
                  "type": "Annotation",
                  "motivation": ["activating"],
                  "body": [
                    {
                      "type": "TextualBody",
                      "value": "Click the box to open the lid"
                    }
                  ],
                  "target": [
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

// TODO

activating to apply a content state and activating to trigger a named animation - use of body and target... what if we want to click a painting anno to trigger the animation?
Can we ADD that to the target, alongside the SpecificResource with the AnimationSelector?

if the `target` is an AnimationSelector, then the `body` can ONLY be TextualBody (or list of TextualBody)?

There is a more general rule here!

### reset

See above...










## Conveying Physical Dimensions

(why is this important!?)

(move the props to vocab doc)

### spatialScale

### temporalScale


```
{
    "spatialScale": {
        "factor": 22.0,
        "units": "m"
    },

    
    // this would be rarely used
    "temporalScale": {
        "factor": 0.00001
    }

}
```

`factor`	Required	A floating point ratio.
`units`	    Required	A real-world measuring unit. Always seconds for temporalScale. Possible values for spatialScale include: "m", "ft". (is that it?)

For a Canvas, it's the physical "size" of each cartesian integer unit.
For a Scene, it's the physical size of the unit vector. 
For a timeline it's the ratio of time in the recording to time in the real world.


(define props in the Vocabulary doc)




## Protocol



## HTTP Requests and Responses

### URI Recommendations

### Requests

### Responses

### Authentication






## Accessibility

(new section)

`provides`
`provides[]`







## Terminology

The principles of [Linked Data][org-linked-data] and the [Architecture of the Web][org-w3c-webarch] are adopted in order to provide a distributed and interoperable framework. The [Shared Canvas data model][shared-canvas] and [JSON-LD][org-w3c-json-ld] are leveraged to create an easy-to-implement, JSON-based format.

This specification uses the following terms:

* __embedded__: When a resource (A) is embedded within an embedding resource (B), the complete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will not result in additional information. Example: Canvas A is embedded in Manifest B.
* __referenced__: When a resource (A) is referenced from a referencing resource (B), an incomplete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will result in additional information. Example:  Manifest A is referenced from Collection B.
* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

The terms _array_, _JSON object_, _number_, _string_, and _boolean_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].



## Appendices

### Versioning

### Acknowledgements

### Change Log

"Exclude Audio"
