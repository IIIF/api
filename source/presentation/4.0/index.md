# Presentation 4

## How this stuff works

Manifests, Containers, Annotations oh my!
Manifest as unit of distribution

## Content Resources

There is stuff that we want to show - images, video, audio, 3D models etc

## Containers

This is where we put content resources
"painting"

And we can also put other things:
"supplementing"

And we can nest them
"Nesting" (see 3d draft)


### Timeline

A Container that represents a bounded temporal range, without any spatial coordinates.

* has continuous duration in seconds

### Canvas

A Container that represents a bounded, two-dimensional space and has content resources associated with all or parts of it. It may also have a bounded temporal range in the same manner as a Timeline.

* has integer, unitless width and height
* has optional continuous duration in seconds

### Scene

A Container that represents a boundless three-dimensional space and has content resources positioned at locations within it. Rendering a Scene requires the use of Cameras and Lights. It may also have a bounded temporal range in the same manner as a Timeline.

* has continuous, unitless x,y,z cartesian coordinate space
* has optional continuous duration in seconds

Bring in https://github.com/IIIF/3d/blob/main/temp-draft-4.md#scenes 


## Putting stuff into Containers (composition)

### Annotation

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

### Light

### Transforms

#### ScaleTransform

#### RotateTransform

#### TranslateTransform

"Relative Rotation"

"Excluding"

## Advanced Association Features


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