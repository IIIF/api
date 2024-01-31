### 2.1. Defined Types

##### Scene

{: #overview-scene}

A virtual container that represents a three-dimensional space and has content resources associated with it or with locations inside it. The Scene provides a frame of reference for the layout of the content, both spatially and temporally.

###  3.2. Technical Properties

[...]

##### type

The value _MUST_ be a string.

 * All resource types _MUST_ have the `type` property.<br/>
   Clients _MUST_ process, and _MAY_ render, `type` on any resource type.

| Class         | Description                      |
| ------------- | -------------------------------- |
[...]
| `PerspectiveCamera` |  |
| `OrthoCamera` |  |
| `AmbientLight` |  |
| `DirectionalLight` |  |
| `PointLight` |  |
| `Spotlight` |  |
{: .api-table #table-type}

{% include api/code_header.html %}
``` json-doc
{ "type": "Image" }
```

##### backgroundColor

applicable with Scenes (and Canvases?) -- rgb values, default is up to viewer

##### behavior

The value _MUST_ be an array of strings.

 * Any resource type _MAY_ have the `behavior` property with at least one item.<br/>
   Clients _SHOULD_ process `behavior` on any resource type.

| Value | Description |
| ----- | ----------- |
[...]
| | **Miscellaneous Behaviors** |
| `hidden` | Valid on Annotation Collections, Annotation Pages, Annotations, Specific Resources and Choices. If this behavior is provided, then the client _SHOULD NOT_ render the resource by default, but allow the user to turn it on and off. This behavior does not inherit, as it is not valid on Collections, Manifests, Ranges or Canvases. |
| | **3D Behaviors** |
| ``| |
{: .api-table #table-behavior}

{% include api/code_header.html %}
``` json-doc
{ "behavior": [ "auto-advance", "individuals" ] }
```

##### fieldOfView

perspectiveCamera -- angle, degrees, top-to-bottom - defaults?

##### near/far

cameras; single float point, optional, coordinates distance

##### lookAt

cameras & lighting

##### angle

degrees (between 0 and 180 if fov)

##### color

all lighting, rgb, default is white

##### intensity

all lighting
–	value 0-1, relative
–	unit + value
–	default

##### transforms
(add table?)

##### cameraOn

true/false - default true

##### lightingOn

true/false - default true

[...]

## new 3D section?

### Scene summary

### Cameras summary

with table for relevant properties, etc.

### Lighting summary

with table for relevant properties, etc.

##  5. Resource Structure

###  5.3. Scene (moves the others down)

