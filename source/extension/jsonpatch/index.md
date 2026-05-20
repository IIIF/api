


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


# Classes


#### JSONPatch
{: #JSONPatch}

TODO


# Properties

### operations
{: operations}

TODO

(An array of JSONPatch operations as defined in that spec.)
Guard rails?



### patchTarget
{: patchTarget}

TODO - guard rails on patchTarget





## Activating Annotations

* If the body has the `type` "JSONPatch", apply the patch operations listed in `operations` to the resource identified by `patchTarget`. (see [ref]).


## Storytelling example

* Something really cool that brings a lot of things together!
* Use JSONPatch to move a model too.