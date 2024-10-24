# Presentation 4

## Introduction

Manifests, Containers, Annotations oh my!
Manifest as unit of distribution

 - 

## Content Resources

There is stuff that we want to show - images, video, audio, 3D models etc

## Containers

This is where we put content resources
"painting"

And we can also put other things:
"supplementing"

And we can nest them
"Nesting" (see 3d draft)

As multiple models, lights, cameras, and other resources can be associated with and placed within a Scene container, Scenes provide a straightforward way of grouping content resources together within a space. Scenes, as well as other IIIF containers such as Canvases, can also be embedded within a Scene, allowing for the nesting of content resources. 

A Scene or a Canvas may be treated as a content resource, referenced or described within the `body` of an Annotation. As with models and other resources, the Annotation is associated with a Scene into which the Scene or Canvas is to be nested through an Annotation `target`. The content resource Scene will be placed within the `target` Scene by aligning the coordinate origins of the two scenes. Alternately, Scene Annotations may use `PointSelector` to place the origin of the resource Scene at a specified coordinate within the `target` Scene.

As with other resources, it may be appropriate to modify the initial scale, rotation, or translation of a content resource Scene prior to painting it within another Scene. Scenes associated with SpecificResources may be manipulated through the transforms described in [Transforms](transforms_section). 

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


Content resources of the appropriate dimension(s) may be annotated into a Container that has those dimensions.


### Timeline

A Container that represents a bounded temporal range, without any spatial coordinates.

* has continuous duration in seconds
 for all or part of its duration.


A Timeline _MUST_ have a `duration` property that defines its length in seconds.  The `duration` value must be a positive floating point number.  

An annotation that targets a Scene using a PointSelector without any temporal refinement implicitly targets the Scene's entire duration.

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





### Canvas

A Container that represents a bounded, two-dimensional space and has content resources associated with all or parts of it. It may also have a bounded temporal range in the same manner as a Timeline.

* has integer, unitless width and height
* has optional continuous duration in seconds

### Scene

A Container that represents a boundless three-dimensional space and has content resources positioned at locations within it. Rendering a Scene requires the use of Cameras and Lights. It may also have a bounded temporal range in the same manner as a Timeline.

* has continuous, unitless x,y,z cartesian coordinate space
* has optional continuous duration in seconds

A Scene in IIIF is a virtual container that represents a boundless three-dimensional space and has content resources, lights and cameras positioned at locations within it. It may also have a duration to allow the sequencing of events and timed media. Scenes have infinite height (y axis), width (x axis) and depth (z axis), where 0 on each axis (the origin of the coordinate system) is treated as the center of the scene's space. 
The positive y axis points upwards, the positive x axis points to the right, and the positive z axis points forwards (a [right-handed cartesian coordinate system](link to wikipedia)).

The axes of the coordinate system are measured in arbitrary units and these units do not necessarily correspond to any physical unit of measurement. This allows arbitrarily scaled models to be used, including very small or very large, without needing to deal with very small or very large values. If there is a correspondence to a physical scale, then this can be asserted using the [physical dimensions pattern](fwd-ref-to-phys-dims).

<img src="https://raw.githubusercontent.com/IIIF/3d/eds/assets/images/right-handed-cartesian.png" title="Right handed cartesian coordinate system" alt="diagram of Right handed cartesian coordinate system" width=200 />


As with other containers in IIIF, Annotations are used to target the Scene to place content such as 3d models into the scene. Annotations are also used to add lights and cameras. A Scene can have multiple models, lights, cameras and other resources, allowing them to be grouped together. Scenes and other IIIF containers, such as Canvases, may also be embedded within Scenes, as described below in the [nesting section][fwd-ref-to-nesting]. 

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



## Putting stuff into Containers (composition)

### Annotation


Annotations follow the [Web Annotation][org-w3c-webanno] data model and are used to associate models, lights, cameras, and IIIF containers such as Canvases, with Scenes. They have a `type` of "Annotation", a `body` (being the resource to be added to the scene) and a `target` (being the scene or a position within the scene). They must have a `motivation` property with the value of "painting" to assert that the resource is being painted into the Scene, rather than the Annotation being a comment about the Scene.

A construct called a Selector is used to select a part of a resource, such as a point within a Scene. The use of a Selector necessitates the creation of a `SpecificResource` that groups together the resource being selected (the `source`) and the instance of the Selector. This SpecificResource can then be used as either the `body` or the `target` of the Annotation.

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

#### URI Fragments

The point may instead be defined using a short-hand form of a URI Fragment at the end of the `id` of the Scene as the `target` of the Annotation. The name of the fragment parameter is `xyz` and its value is the x, y and z values separated by commas. Each value can be expressed as either an integer or a floating point number.

The annotation above could be expressed as its fragment-based equivalent:

```json 
{
    "id": "https://example.org/iiif/3d/anno1",
    "type": "Annotation",
    "motivation": ["painting"],
    "body": {
        "id": "https://example.org/iiif/assets/model1.glb",
        "type": "Model"
    },
    "target": "https://example.org/iiif/scene1#xyz=-1,0,1"
}
```





"non-painting"

"target" and "body"


### Annotation Page

### Annotation Collection


### Manifest

### Collection

#### Paging

### Range

## Content State

(introduce motivation and reasons)

Separate Content State Sharing spec (protocols for sharing annotations)

content state intended to:

 - load a view of some resource (existing spec)
 - load a view of some resource AND modify the Container (show you my new anno, add camera)
 - modify the Container in a particular context (`scope`, storytelling)
 - contribute additional information permanently (rerum **inbox** - move to protocol doc)


## Selectors

### SpecificResource

### PointSelector


## Scene-Specific Resources

### 3D considerations / principles

"models" (content resources in 3D)
"local coordinate spaces"

### Camera

A Camera provides a view of a region of the Scene's space from a particular position within the Scene; the client constructs a viewport into the Scene and uses the view of one or more Cameras to render that region. The size and aspect ratio of the viewport is client and device dependent.

<div style="background: #A0F0A0; padding: 10px; padding-left: 30px; margin-bottom: 10px">
❓Does this prevent extension cameras from requiring a fixed aspect ratio? 
</div>

This specification defines two types of Camera:

| Class               | Description  |
| ------------------- | ------------ |
| `PerspectiveCamera` | `PerspectiveCamera` mimics the way the human eye sees, in that objects further from the camera are smaller |
| `OrthographicCamera` | `OrthographicCamera` removes visual perspective, resulting in object size remaining constant regardless of its distance from the camera |

Cameras are positioned within the Scene facing in a specified direction. Both position and direction are defined through the Annotation which adds the Camera to the Scene, described below in the sections on [Painting Annotations][] and [Transforms][]. If either the position or direction is not specified, then the position defaults to the origin, and direction defaults to facing along the z axis towards negative infinity.

The region of the Scene's space that is observable by the camera is bounded by two planes orthogonal to the direction the camera is facing, given in the `near` and `far` properties, and a vertical projection angle that provides the top and bottom planes of the region.

The `near` property defines the minimum distance from the camera at which something in the space must exist in order to be viewed by the camera. Anything nearer to the camera than this distance will not be viewed. Conversely, the `far` property defines a maximum distance from the camera at which something in the space must exist in order to be viewed by the camera. Anything further away will not be viewed.

For PerspectiveCameras, the vertical projection angle is specificed using the full angular extent in degrees from the top plane to the bottom plane using the `fieldOfView` property. The `fieldOfView` angle MUST be greater than 0 and less than 180. For OrthographicCameras, the vertical projection is always parallel and thus not defined. 

If any of these properties are not specified explicitly, they default to the choice of the client implementation.

<img src="https://raw.githubusercontent.com/IIIF/3d/eds/assets/images/near-far.png" title="Diagram showing near and far properties"  alt="drawing of a geometrical frustrum truncated by near and far distances" width="300" />


If the Scene does not have any Cameras defined within it, then the client MUST provide a default Camera. The type, properties and position of this default camera are client-dependent.

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

It is useful to be able to rotate a light or camera resource such that it is facing another object or point in the Scene, rather than calculating the angles within the Scene's coordinate space. This is accomplished with a property called `lookAt`, valid on DirectionalLight, SpotLight, and all Cameras. The value of the property is either a PointSelector or the URI of an Annotation which paints something into the current Scene.

If the value is a PointSelector, then the light or camera resource is rotated around the x and y axes such that it is facing the given point. If the value is an Annotation which targets a point via a PointSelector, URI fragment or other mechanism, then the direction the resource is facing that point.

<div style="background: #A0F0A0; padding: 10px; padding-left: 30px; margin-bottom: 10px">
❓What happens if the Annotation targets a Polygon or other non-Point? Calculate centroid? Error? First point given in the Poly / center of a sphere?
</div>

This rotation happens after the resource has been added to the Scene, and thus after any transforms have taken place in the local coordinate space. As the z axis is not affected by the rotation, any RotateTransform that changes z will be retained, but any change to x or y will be lost.

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



## Advanced Association Features

### Nesting

A Canvas can be painted into a Scene as an Annotation, but the 2D nature of Canvases requires special consideration due to important differences between Canvases and Scenes. A Canvas describes a bounded 2D space with finite `height` and `width` measured in pixels with a pixel origin at the top-left corner of the Canvas, while Scenes describe a boundless 3D space with x, y, and z axes of arbitrary coordinate units and a coordinate origin at the center of the space. It is important to note that in many cases the pixel scale used by a Canvas or a 2D image content resource will not be in proportion to the desired 3D coordinate unit scale in a Scene. 

When a Canvas is painted as an Annotation targeting a Scene, the top-left corner of the Canvas (the pixel origin) is aligned with the 3D coordinate origin of the Scene. The top edge of the Canvas is aligned with (e.g., is colinear to) the positive x axis extending from the coordinate origin. The left edge of the Canvas is aligned with (e.g., is colinear to) the negative y axis extending from the coordinate origin. The Canvas is scaled to the Scene such that the pixel dimensions correspond to 3D coordinate units - a Canvas 200 pixels wide and 400 pixels high will extend 200 coordinate units across the x axis and 400 coordinate units across the y axis. Please note: direction terms "top", "bottom", "right", and "left" used in this section refer to the frame of reference of the Canvas itself, not the Scene into which the Canvas is painted.

A Canvas in a Scene has a specific forward face and a backward face. By default, the forward face of a Canvas should point in the direction of the positive z axis. If the property `backgroundColor` is used, this color should be used for the backward face of the Canvas. Otherwise, a reverse view of the forward face of the Canvas should be visible on the backward face.

<div style="background: #A0F0A0; padding: 10px; padding-left: 30px; margin-bottom: 10px">
  To Do: Add an image demonstrating default Canvas placement in Scene
</div>

A `PointSelector` can be used to modify the point at which the Canvas will be painted, by establishing a new point to align with the top-left corner of the Canvas instead of the Scene coordinate origin. Transforms can also be used to modify Canvas rotation, scale, or translation.

It may be desirable to exercise greater control over how the Canvas is painted into the Scene by selecting the coordinate points in the Scene that should correspond to each corner of the Canvas. This provides fine-grained manipulation of Canvas placement and/or scale, and for optionally introducing Canvas distortion or skew. Annotations may use a type of Selector called a `PolygonZSelector` to select different points in the Scene to align with the top-left, bottom-left, bottom-right, and top-right corners of the Canvas. PolygonZSelectors have a single property, `value`, which is a string listing a WKT `POLYGONZ` expression containing four coordinate points, with each coordinate separated by commas, and axes within a coordinate separated by spaces. The four Scene coordinates should be listed beginning with the coordinate corresponding to the top-left corner of the Canvas, and should proceed in a counter-clockwise winding order around the Canvas, with coordinates corresponding to bottom-left, bottom-right, and top-right corners in order respectively. The use of PolygonZSelector overrides any use of Transforms on the Canvas Annotation.

Example placing top-left at (0, 1, 0); bottom-left at (0, 0, 0); bottom-right at (1, 0, 0); and top-right at (1, 1, 0):
```json
"selector": [
  {
    "type": "PolygonZSelector",
    "value": "POLYGONZ((0 1 0, 0 0 0, 1 0 0, 1 1 0))"
  }
]
```


### Segments

### Embedded Content

### Choice of Alternative Resources

### Non Rectangular Segments

### Style

### Rotation

### Comment Annotations

### Hotspot Linking

### Activation

### Using Content State

 - modify the Container in a particular context (`scope`, storytelling)



### Physical Dimension Service



## HTTP Requests and Responses

### URI Recommendations

### Requests

### Responses

### Authentication


## Appendices

### Summary of Property Requirements

### Example Manifest Response

### Versioning

### Acknowledgements

### Change Log

"Exclude Audio"