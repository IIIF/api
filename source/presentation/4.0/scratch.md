
In the example Manifest above the first Container is a Timeline. One content resource, an MP3 file, is associated with the Timeline via a Painting Annotation for its entire duration. Typically the duration of the Timeline matches the duration of its content. This is the simplest time-based use case. The `target` property of the Painting Annotation is the whole Timeline, because it is simply the `id` of the Timeline without further qualification. In this simple case, playing the Timeline is the same as playing the MP3.

The second Container is a Canvas, representing a 2D surface. In this case the Canvas represents an artwork, and there is no duration property. The content resource, a JPEG image of the artwork, is associated with the Canvas via a Painting Annotation. The unit integer coordinates of the Canvas (12000 x 9000) are not the same as the pixel dimensions of the JPEG image (4000 x 3000), but they are proportional - the Canvas has a 4:3 landscape aspect ratio, and so does the JPEG image. The `target` property of the Annotation is the Canvas `id`, unqualified by any particular region; this is taken to mean the content (the image) should fill the Canvas completely. As the Canvas and the image are the same aspect ratio, no distortion will occur. This approach allows the current image to be replaced by a higher resolution image in future, on the same Canvas. The Canvas dimensions establish a coordinate system for _painting annotations_ and other kinds of annotation that link content with the Canvas; they are not pixels of images.

The third Container is a Scene. Unlike a Canvas, it is not a bounded spatial extent, but may be a bounded temporal extent if it has the optional duration property. It still establishes a coordinate space (x, y, z) but doesn't need any spatial properties to do so as it is always the same, infinite unbounded space. The Annotation paints the astronaut model into the Scene. As no further qualification is given, the astronaut model is placed at the (0,0,0) origin of the Scene. Later examples will show how to control the lighting and camera position(s) and properties, but this is not required; a IIIF viewer is expected to supply ambient light and a default camera position in the absence of specific values.


This requires careful consideration of the URI schemes for `id` properties of Containers and their Manifests to ensure they remain referenceable in the future.


use this in an example:
The point around which RotateTransform rotates the space is the origin. This "pivot point" cannot be changed directly, but instead a TranslateTransform can be used to move the desired pivot point to the be at the origin, then the RotateTransform applied.




                  "body": [
                    {
                      "type": "TextualBody",
                      "value": "A label for the activation may be provided as a TextualBody"
                    },
                    {
                      "type": "SpecificResource",
                      "source": {
                        "id": "https://example.org/iiif/scene1/scene-with-activation",
                        "type": "Scene"
                      },
                      "transform": [
                        {
                          "type": "PropertyTransform",
                          "propertyName": "backgroundColor",
                          "propertyValue": "#FF99AA"
                        }
                      ]
                    }
                  ],


_removed whole content state section_




# Content State

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

The term _Content State_ is used for any arbitrary fragments of IIIF such as the above when they are used in the particular ways defined by this specification. A Content State is **usually** carried by the `target` of an annotation with the motivation `contentState`, or `body` of an annotation with the motivation `activating`, but in some scenarios may be transferred between client applications without an enclosing annotation, as a "bare" URI (see Content State Protocol API 2.0 specification).

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




## Chains of activation

Chaining together activating annotations can then allow the implementation of, at least:

* Specific camera position to look at an Annotation
* Multi-step linear stories
* Animations, including as part of stories without disrupting the flow, and looping animations (they activate themselves)
* Interactive components such as light switches (enable/disable a light), jukeboxes (enable/disable Audio Emitter)


## Storytelling example

* Something really cool that brings a lot of things together!


# Auth of Presentation API resources

It may be necessary to restrict access to the descriptions made available via the Presentation API. As the primary means of interaction with the descriptions is by web browsers using XmlHttpRequests across domains, there are some considerations regarding the most appropriate methods for authenticating users and authorizing their access. The approach taken is described in the [Authentication][iiif-auth] specification, and requires requesting a token to add to the requests to identify the user. This token might also be used for other requests defined by other APIs.



_removed content state use case:_

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

# Activating by entering (or interacting with) a volume:

```json
{
  "id": "https://example.org/iiif/3d/anno9",
  "type": "Annotation",
  "motivation": ["activating"],
  "target": [
    {
        "id": "https://example.org/iiif/3d/anno9",
        "type": "SpecificResource",
        "selector": [
            {
                "type": "WktSelector",
                "wktLiteral": "POLYHEDRALSURFACE Z (blah blah)"
            }
        ],
        "source": "https://example.org/iiif/3d/Scene1"
    }
  ],
  "body": [
    {
      "type": "JSONPatch that turns on the light"
    }
  ]
}
```


# Controlling a video that is not painted into duration (or not even painted at all)

```json
{
  "id": "https://example.org/iiif/3d/box-opening-activating-anno",
  "type": "Annotation",
  "motivation": ["activating"],
  "disables": ["https://example.org/iiif/3d/commenting-anno-for-video"],
  "target": [
    {
      "id": "https://example.org/iiif/3d/third-man-from-left",
      "type": "Annotation"
    }
  ],
  "body": [
    {
      "type": "SpecificResource",
      "source": "https://example.org/iiif/3d/commenting-anno-for-video",
      "action": ["stop", "reset"]
    }
  ]
}
```

# actions for disable and enable (yes)

```json
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
```

# Lightswitch enables and disables as props (no)

```json
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
```

# Animation with action

```json
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
```

# Verbose form of scope

```json
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

```

...is equivalent to this on the commenting anno:

```jsonc
    "scope": [           // <= ["show", "enable", "select"]
      {
        "id": "https://example.org/iiif/3d/anno-that-paints-desired-camera-to-view-tooth",
        "type": "Annotation"
      }
    ],
```