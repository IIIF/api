

Most basic case: put the model in the center of the scene
```
{
  "id": "https://example.org/iiif/3d/anno1",
  "type": "Annotation",
  "motivation": ["painting"],
  "body": {"id":"pawn-model.glb","type":"Model"},
  "target": "https://example.org/iiif/scene1/page/p1/1"
}
```


Positioning: Position the model not at the center of the scene
```
{
  "id": "https://example.org/iiif/3d/anno1",
  "type": "Annotation",
  "motivation": ["painting"],
  "body": {"id":"pawn-model.glb","type":"Model"},
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
          "__comment": "position at the right point in the scene's space",
	      "type": "PointSelector",
          "x": 0.0,
          "y": -25.0,
          "z": 100.0
        }
      ]
    }
}
```


Transform the model before putting into the scene (at the center)
```
{
  "id": "https://example.org/iiif/3d/anno1",
  "type": "Annotation",
  "motivation": ["painting"],
  "body": {
    "id": "",
    "type": "SpecificResource",
    "source": [
      {
        "id": "pawn-model.glb",
        "type": "Model",
        "format": "application/glb"
      }
    ],
    "transforms": [
      {
        "__comment": "scale to the right size in the model's space",
        "type": "ScaleTransform",
        "x": 10.0,
        "y": 10.0,
        "z": 10.0
      }
    ]
  },
  "target": "https://example.org/iiif/scene1/page/p1/1"
}
```


Transform the model and position it in the scene
```
{
  "id": "https://example.org/iiif/3d/anno1",
  "type": "Annotation",
  "motivation": ["painting"],
  "body": {
    "id": "",
    "type": "SpecificResource",
    "source": [
      {
        "id": "pawn-model.glb",
        "type": "Model",
        "format": "application/glb"
      }
    ],
    "transforms": [
      {
        "__comment": "scale to the right size in the model's space",
        "type": "ScaleTransform",
        "x": 10.0,
        "y": 10.0,
        "z": 10.0
      }
    ]
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
          "__comment": "position at the right point in the scene's space",
	      "type": "PointSelector",
          "x": 0.0,
          "y": -25.0,
          "z": 100.0
        }
      ]
    }
}
```


Transform the model, including translation, before positioning in the scene
```
{
  "id": "https://example.org/iiif/3d/anno1",
  "type": "Annotation",
  "motivation": ["painting"],
  "body": {
    "id": "",
    "type": "SpecificResource",
    "source": [
      {
        "id": "pawn-model.glb",
        "type": "Model",
        "format": "application/glb"
      }
    ],
    "transforms": [
      {
        "__comment": "translate to the right place in the model's space",
        "type": "TranslateTransform",
        "x": -10.0,
        "y": 0.0,
        "z": 10.0
      }, 
      {
        "__comment": "scale to the right size in the model's space",
        "type": "ScaleTransform",
        "x": 10.0,
        "y": 10.0,
        "z": 10.0
      }
    ]
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
          "__comment": "position at the right point in the scene's space",
	      "type": "PointSelector",
          "x": 0.0,
          "y": -25.0,
          "z": 100.0
        }
      ]
    }
}
```

Create and rotate a light, before positioning in the scene
```
{
  "id": "https://example.org/iiif/3d/anno1",
  "type": "Annotation",
  "motivation": ["painting"],
  "body": {
    "id": "",
    "type": "SpecificResource",
    "source": [
      {
        "type": "DirectionalLight",
        "color": "yellow",
        "intensity": 1.0
      }
    ],
    "transforms": [
      {
        "__comment": "rotate to the right direction in the model's space",
        "type": "RotateTransform",
        "x": -45.0,
        "y": -45.0,
        "z": 0.0
      }
    ]
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
          "__comment": "position at the right point in the scene's space",
	      "type": "PointSelector",
          "x": 500.0,
          "y": 500.0,
          "z": 500.0
        }
      ]
    }
}
