# Vocabulary?

## Resource Properties

### Descriptive Properties

#### label (etc)



### Linking Properties

### Technical Properties

#### backgroundColor

This property sets the background color behind any painted resources on a spatial resource, such as a Canvas or Scene.

The value _MUST_ be string, which defines an RGB color. It SHOULD be a hex value starting with "#" and is treated in a case-insensitive fashion. If this property is not specified, then the default value is client-dependent.

 * A Canvas _MAY_ have the `backgroundColor` property<br/>
   Clients _SHOULD_ render `backgroundColor` on any resource type.
 * A Scene _MAY_ have the `backgroundColor` property<br/>
   Clients _SHOULD_ render `backgroundColor` on any resource type.
 * Other resources _MUST NOT_ have the `backgroundColor` property.

```json
"backgroundColor": "#FFFFFF"
```

<div style="background: #A0F0A0; padding: 10px; padding-left: 30px; margin-bottom: 10px">
❓Can you set bgColor on a transparent image? An area? Conflict with `style` on a SpecificResource?
</div>



##### near

This property gives the distance from the camera from which objects are visible. Objects closer to the camera than the `near` distance cannot be seen.

The value is a non-negative floating point number. If this property is not specified, then the default value is client-dependent.

* A Camera _MAY_ have the `near` property<br/>
  Clients _SHOULD_ process the `near` property on Cameras.

```json
"near": 1.5
```

##### far

This property gives the distance from the camera after which objects are no longer visible. Objects further from the camera than the `far` distance cannot be seen.

The value is a non-negative floating point number, and _MUST_ be greater than the value for `near` on the same camera. If this property is not specified, then the default value is client-dependent.

* A Camera _MAY_ have the `far` property<br/>
  Clients _SHOULD_ process the `far` property on Cameras.

```json
"far": 200.0
```

##### fieldOfView

_Summary here_

The value _MUST_ be a floating point number greater than 0 and less than 180. If this property is not specified, then the default value is client-dependent.

* A PerspectiveCamera _SHOULD_ have the `fieldOfView` property.<br/>
  Clients _SHOULD_ process the `fieldOfView` property on Cameras.

```json
  "fieldOfView": 50.0
```

##### angle

_Summary here_

The value _MUST_ be a floating point number greater than 0 and less than 90. If this property is not specified, then the default value is client-dependent.

* A SpotLight _SHOULD_ have the `angle` property.<br/>
  Clients _SHOULD_ process the `angle` property on SpotLights.

```json
  "angle": 15.0
```

##### lookAt

_Summary here_

The value _MUST_ be a JSON object, conforming to either a reference to an Annotation with an `id` and a `type` of "Anntoation", or a PointSelector. If this property is not specified, then the default value is null -- the camera or light is not looking at anything.

```json
"lookAt": {
    "type": "PointSelector",
    "x": 3,
    "y": 0,
    "z": -10
}
```

##### color

This property sets the color of a Light.

The value _MUST_ be string, which defines an RGB color. It SHOULD be a hex value starting with "#" and is treated in a case-insensitive fashion. If this property is not specified, then the default value is "#FFFFFF".

 * A Light _SHOULD_ have the `color` property<br/>
   Clients _SHOULD_ render `color` on any resource type.
 * Other resources _MUST NOT_ have the `color` property.

```json
"color": "#FFA0A0"
```

##### intensity

This property sets the strength or brightness of a Light.

The value _MUST_ be a JSON object, that has the `type`, `value` and `unit` properties. All three properties are required. The value of `type` _MUST_ be the string "Value". The value of `value` is a floating point number. The value of `unit` is a string, drawn from a controlled vocabulary of units. If this property is not specified, then the default intensity value is client-dependent.

This specification defines the unit value of "relative" which constrains the value to be a linear scale between 0.0 (no brightness) and 1.0 (as bright as the client will render).

* A Light _SHOULD_ have the `intensity` property.<br/>
  Clients _SHOULD_ process the `intensity` property on Lights.

```json
{
 "intensity": {"type": "Value", "value": 0.5, "unit": "relative"}
}
```

##### Exclude

_Summary here_

_On Annotation, a list of strings drawn from table_

| Value      | Description |
|------------|-------------|
| Audio      | |
| Animations | |
| Cameras    | |
| Lights     | |

```json
"exclude": [ "Audio", "Lights", "Cameras", "Animations" ]
```


##### transform

_Summary here_

The value of this property is an array of JSON objects, each of which is a Transform.

##### x

##### y

##### z



### Structural Properties

### Values



## JSON-LD Considerations

### Case Sensitivity

### Resource Representations

### Properties with Multiple Values

### Language of Property Values

### HTML Markup in Property Values

### Linked Data Context and Extensions

### Term Collisions between Contexts

### Keyword Mappings