---
title: "Presentation API 4.0 Properties"
title_override: "IIIF Presentation API 4.0 Properties"
id: presentation-api-properties
layout: spec
cssversion: 3
tags: [specifications, presentation-api]
major: 4
minor: 0
patch: 0
pre: 
redirect_from:
  - /presentation/properties.html
  - /presentation/4/properties.html
editors:
  - name: Michael Appleby
    ORCID: https://orcid.org/0000-0002-1266-298X
    institution: Yale University
  - name: Tom Crane
    ORCID: https://orcid.org/0000-0003-1881-243X
    institution: Digirati
  - name: Robert Sanderson
    ORCID: https://orcid.org/0000-0003-4441-6852
    institution: Yale University
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

# IIIF Presentation API Data Model

## Introduction


### Terminology

This specification uses the following terms:

* __embedded__: When a resource (A) is embedded within an embedding resource (B), the complete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will not result in additional information. Example: Canvas A is embedded in Manifest B.
* __referenced__: When a resource (A) is referenced from a referencing resource (B), an incomplete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will result in additional information. Example:  Manifest A is referenced from Collection B.
* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

The terms _array_, _JSON object_, _number_, _string_, and _boolean_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].



## JSON Considerations

This section describes features applicable to all of the Presentation API content.

### Case Sensitivity

Keys in JSON objects are [case sensitive][org-w3c-json-ld-case].  The cases of properties and enumerated values in IIIF Presentation API responses _MUST_ match those used in this specification. For example to specify that a resource is a Manifest, the property _MUST_ be given as `type` and not `Type` or `tYpE`, and the value _MUST_ be given as `Manifest` and not `manifest` or `manIfEsT`.

### Properties with Multiple Values

Any of the properties in the API that can have multiple values _MUST_ always be given as an array of values, even if there is only a single item in that array.

{% include api/code_header.html %}
``` json-doc
{
  "thumbnail": [
    {
      "id": "https://example.org/images/thumb1.jpg",
      "type": "Image",
      "format": "image/jpeg"
    }
  ]
}
```

### Language of Property Values
{: #language-of-property-values}

Language _SHOULD_ be associated with strings that are intended to be displayed to the user for the `label` and `summary` properties, plus the `label` and `value` properties of the `metadata` and `requiredStatement` objects.

The values of these properties _MUST_ be JSON objects, with the keys being the [BCP 47][org-bcp-47] language code for the language, or if the language is either not known or the string does not have a language, then the key _MUST_ be the string `none`. The associated values _MUST_ be arrays of strings, where each item is the content in the given language.

{% include api/code_header.html %}
``` json-doc
{
  "label": {
    "en": [
      "Whistler's Mother",
      "Arrangement in Grey and Black No. 1: The Artist's Mother"
    ],
    "fr": [
      "Arrangement en gris et noir no 1",
      "Portrait de la mère de l'artiste",
      "La Mère de Whistler"
    ],
    "none": [ "Whistler (1871)" ]
  }
}
```

Note that [BCP 47][org-bcp-47] allows the script of the text to be included after a hyphen, such as `ar-latn`, and clients should be aware of this possibility.

In the case where multiple values are supplied, clients _MUST_ use the following algorithm to determine which values to display to the user.

* If all of the values are associated with the `none` key, the client _MUST_ display all of those values.
* Else, the client should try to determine the user's language preferences, or failing that use some default language preferences. Then:
  * If any of the values have a language associated with them, the client _MUST_ display all of the values associated with the language that best matches the language preference.
  * If all of the values have a language associated with them, and none match the language preference, the client _MUST_ select a language and display all of the values associated with that language.
  * If some of the values have a language associated with them, but none match the language preference, the client _MUST_ display all of the values that do not have a language associated with them.

Note that this does not apply to [embedded][prezi30-terminology] textual bodies in Annotations, which use the Web Annotation pattern of `value` and `language` as separate properties.

### HTML Markup in Property Values

Minimal HTML markup _MAY_ be included for processing in the `summary` property and the `value` property in the `metadata` and `requiredStatement` objects. It _MUST NOT_ be used in `label` or other properties. This is included to allow content publishers to add links and simple formatting instructions to blocks of text. The content _MUST_ be well-formed XML and therefore _MUST_ be wrapped in an element such as `p` or `span`. There _MUST NOT_ be whitespace on either side of the HTML string, and thus the first character in the string _MUST_ be a '<' character and the last character _MUST_ be '>', allowing a consuming application to test whether the value is HTML or plain text using these. To avoid a non-HTML string matching this, it is _RECOMMENDED_ that an additional whitespace character be added to the end of the value in situations where plain text happens to start and end this way.

In order to avoid HTML or script injection attacks, clients _MUST_ remove:

  * Tags such as `script`, `style`, `object`, `form`, `input` and similar.
  * All attributes other than `href` on the `a` tag, `src` and `alt` on the `img` tag.
  * All `href` attributes that start with the strings other than "http:", "https:", and "mailto:".
  * CData sections.
  * XML Comments.
  * Processing instructions.

Clients _SHOULD_ allow only `a`, `b`, `br`, `i`, `img`, `p`, `small`, `span`, `sub` and `sup` tags. Clients _MAY_ choose to remove any and all tags, therefore it _SHOULD NOT_ be assumed that the formatting will always be rendered.  Note that publishers _MAY_ include arbitrary HTML content for processing using customized or experimental applications, and the requirements for clients assume an untrusted or unknown publisher.

{% include api/code_header.html %}
``` json-doc
{ "summary": { "en": [ "<p>Short <b>summary</b> of the resource.</p>" ] } }
```

### JSON Description Availability

JSON descriptions _SHOULD_ be [embedded][prezi30-terminology] within the JSON of parent resources, and _MAY_ also be available via separate requests from the HTTP(S) URI given in the resource's `id` property. Links to Content Resources _MUST_ be given as a JSON object with the `id` and `type` properties and _SHOULD_ have `format` or `profile` to give a hint as to what sort of resource is being referred to.

{% include api/code_header.html %}
``` json-doc
{
  "rendering": [
    {
      "id": "https://example.org/content/book.pdf",
      "type": "Text",
      "label": { "en": [ "Example Book (pdf)" ] },
      "format": "application/pdf"
    }
  ]
}
```



## Classes

The following sub-sections define the classes used in the IIIF Presentation Data Model. Only the semantics and core structural requirements are defined within this section, along with any deviations from other specifications that the classes might be drawn from. The descriptions do not define how the classes are used together, which is done in the Presentation API Overview.

The name of each class is given at the top of its definition below. The exact string _MUST_ be used as the value of `type` in the JSON for the class.

### Collection
{: #Collection}

`"type": "Collection"`

A Collection is an ordered list of Manifests, and/or Collections.

The identifier in `id` _MUST_ be able to be dereferenced to retrieve the JSON description of the Collection, and thus _MUST_ use the HTTP(S) URI scheme.

The members of a Collection are typically listed in the `items` property. The members _MAY_ include both other Collections and Manifests, in order, to form a tree-structured hierarchy.

If there are too many members in the collection to fit within a single document, then the members _MAY_ be listed in Collection Pages. A reference to the first page of members is given in the `first` property, and the last page in the `last` property. In this case, the Collection _MUST NOT_ use the `items` property.

Member Collections _MAY_ be [embedded][prezi30-terminology] inline within other Collections, such as when the Collection is used primarily to subdivide a larger one into more manageable pieces, however Manifests _MUST NOT_ be [embedded][prezi30-terminology] within Collections. An [embedded][prezi30-terminology] Collection _SHOULD_ also have its own URI from which the JSON description is available.

Manifests or Collections _MAY_ be [referenced][prezi30-terminology] from more than one Collection. For example, an institution might define four Collections: one for modern works, one for historical works, one for newspapers and one for books. The Manifest for a modern newspaper would then appear in both the modern Collection and the newspaper Collection. Alternatively, the institution may choose to have two separate newspaper Collections, and reference each as a sub-Collection of modern and historical.

Collections with an empty `items` property are allowed but discouraged.  For example, if the user performs a search that matches no Manifests, then the server _MAY_ return a Collection response with no Manifests.

Collections or Manifests [referenced][prezi30-terminology] in the `items` property _MUST_ have the `id`, `type` and `label` properties. They _SHOULD_ have the `thumbnail` property.


#### Collection Page
{: #CollectionPage}

`"type": "CollectionPage"`

A Collection Page is an arbitrary division of members within the Collection to make it easier to consume.

A Collection Page _MUST_ have an HTTP(S) URI given in `id`. It _MUST_ be able to be dereferenced to retrieve the JSON description of the Collection Page.

Collection Pages follow the ActivityStreams model, as also used in Annotation Collections, the IIIF Change Discovery API, and the IIIF Search API.


### Manifest

`"type": "Manifest"`

A Manifest is the primary unit of distribution of IIIF and provides a description of the structure and properties of a single item to be presented to the user.

Manifests _MUST_ be identified by a URI and it _MUST_ be an HTTP(S) URI, given in the `id` property. It _MUST_ be able to be dereferenced to retrieve the JSON description of the Manifest.

The members of a Manifest are listed in the `items` property. The members of Manifests _MUST_ be Containers, defined below, and are embedded within the Manifest. The Manifest _MAY_ have a `structures` property listing one or more [Ranges][#range] which describe additional structure of the content, such as might be rendered as a table of contents. The Manifest _MAY_ have an `annotations` property, which includes Annotation Page resources where the Annotations have the Manifest as their `target`. These Annotations _MUST NOT_ have `painting` as their `motivation`.


__Properties__<br/>
A Manifest _MUST_ have the following properties: [id](#id), [type](#type), [label](#label), and [items](#items)<br/><br/>
A Manifest _SHOULD_ have the following properties: [metadata](#metadata), [summary](#summary), [provider](#provider), and [thumbnail](#thumbnail)<br/><br/>
A Manifest _MAY_ have the following properties: [requiredStatement](#requiredStatement), [rights](#rights), [navDate](#navDate), [navPlace](#navPlace), [placeholderContainer](#placeholderContainer), [accompanyingContainer](#accompanyingContainer), [viewingDirection](#viewingDirection), [behavior](#behavior), [seeAlso](#seeAlso), [service](#service), [services](#services), [homepage](#homepage), [rendering](#rendering), [partOf](#partOf), [start](#start), [structures](#structures), and [annotations](#annotations).
{: .note}

### Container Classes
{: #containers}

A Container is a frame of reference that allows the relative positioning of content.

All Containers _MUST_ be identified by a URI and it _MUST_ be an HTTP(S) URI. The URI of the Container _MUST NOT_ contain a fragment (a `#` followed by further characters), as this would make it impossible to refer to a segment of the Container's area using the [media fragment syntax][org-w3c-media-frags] of `#xywh=` for spatial regions, and/or `#t=` for temporal segments. The temporal segment _MUST_ be expressed using seconds. Containers _MAY_ be able to be dereferenced separately from the Manifest via their URIs as well as being [embedded][prezi30-terminology].

Containers _MUST_ have an `items` property which is a list of Annotation Pages. Each Annotation Page, defined below, maintains a list of Annotations, which associate Content Resources to be rendered as part of the Container. Annotations that do not associate content to be rendered, but instead are about the Container such as a comment or tag, are recorded using Annotation Pages in the `annotations` property of the Container.

FIXME: It is an error to select a temporal region of a Scene that does not have a `duration`, or to select a temporal region that is not within the Scene's temporal extent.  A Canvas or Scene with a `duration` may not be annotated as a content resource into a Scene that does not itself have a `duration`.




#### Timeline

`"type": "Timeline"`

A Timeline is a Container that represents only a temporal duration, measured in seconds. Timelines allow audio content to be presented, but do not allow anything with a height or width like an image or video.  The duration of the Timeline is given in the `duration` property.

#### Canvas

`"type": "Canvas"`

A Canvas is a Container that represents a particular rectangular 2 dimensional view of the object and has content resources associated with it or with parts of it. This aspect ratio is defined by the `height` and `width` properties. A Canvas _MAY_ also have a duration, given in the `duration` property, allowing audio and video to be correctly positioned in time as well as the 2 dimensional space.

FIXME: arbitrary units

#### Scene

`"type": "Scene"`

A Scene is a Container that represents an infinitely large three-dimensional space, with an optional `duration` property. Scenes have infinite height (y axis), width (x axis) and depth (z axis), where 0 on each axis (the origin of the coordinate system) is treated as the center of the scene's space. From a perspective looking along the z axis towards negative infinity, the positive y axis points upwards and the positive x axis points to the right (a [right-handed Cartesian coordinate system](https://en.wikipedia.org/wiki/Right-hand_rule)).

<img src="https://raw.githubusercontent.com/IIIF/3d/eds/assets/images/right-handed-cartesian.png" title="Right handed cartesian coordinate system" alt="diagram of Right handed cartesian coordinate system" width=200 />

The axes of the coordinate system are measured in arbitrary units and these units do not necessarily correspond to any physical unit of measurement, unless `spatialScale` is supplied.

All resources that can be added to a Scene have an implicit (e.g. Lights, Cameras) or explicit (e.g. Models, Scenes), local coordinate space.





### Annotation Classes
{: #annotations}

The following set of classes are defined by the W3C's [Web Annotation Data Model][org-w3c-webanno] and Vocabulary, and are heavily used within the IIIF Data Model. Any necessary deviations from those specifications are explicitly noted and explained, such as the need for internationalization of labels.

#### Annotation

`"type": "Annotation"`

Annotations are used to associate content resources with Containers, as well as for transcriptions, commentary, tags and the association of other content. This provides a single, unified method for aligning information, and provides a standards-based framework for distinguishing parts of resources and parts of Canvases.

Annotations _MUST_ have their own HTTP(S) URIs, conveyed in the `id` property. The JSON-LD description of the Annotation _SHOULD_ be returned if the URI is dereferenced, according to the [Web Annotation Protocol][org-w3c-webanno-protocol].

When Annotations are used to associate content resources with a Canvas, the content resource is linked in the `body` of the Annotation. The URI of the Canvas _MUST_ be repeated in the `target` property of the Annotation, or the `source` property of a Specific Resource used in the `target` property.

Content that is to be rendered as part of the Container _MUST_ be associated by an Annotation that has the `motivation` value `painting`.

Note that the Web Annotation data model defines different patterns for the `value` property compared to IIIF, when used within an Annotation. The `value` of a Textual Body or a Fragment Selector, for example, are strings rather than JSON objects with languages and values. Care must be taken to use the correct string form in these cases.


#### Annotation Collection

`"type": "AnnotationCollection"`

Annotation Collections allow groups of Annotations to be recorded. For example, all of the English translation Annotations of a medieval French document could be kept separate from the transcription or an edition in modern French, or the director's commentary on a film can be separated from the script.

Annotation Collections _MUST_ have a URI, and it _SHOULD_ be an HTTP(S) URI. They _SHOULD_ have a `label` and _MAY_ have any of the other descriptive, linking or rights properties.

Annotation Collections are paged rather than enumerated. The first page of items is linked using the `first` property, and the last page with the `last` property. The pages link to the next and previous pages in a chain, using the `next` and `prev` properties respectively.


#### Annotation Page

`"type": "AnnotationPage"`

An ordered list of Annotations, typically associated with a Container, but may be referenced from other types of resource as well. Annotation Pages enumerate and order lists of Annotations, in the same way that Collection Pages order lists of Manifests and Collections within the containing Collection.

An Annotation Page _MUST_ have an HTTP(S) URI given in `id`, and _MAY_ have any of the other properties defined in this specification or the Web Annotation specification. The Annotations are listed in the `items` property of the Annotation Page.

Annotations are embedded within an Annotation Page in the `items` property.

__Incompatibility Warning__<br/>
The definition of `label` in the Web Annotation specification does not produce JSON conformant with the structure defined in this specification for languages. Given the absolute requirement for internationalized labels and the strong desire for consistently handling properties, the `label` property on Annotation model classes does not conform to the string requirement of the Web Annotation Data Model.  This [issue has been filed with the W3C][github-webanno-437] and will hopefully be addressed in a future version of the standard.
{: .warning}


#### Specific Resource

`"type": "SpecificResource"`

A Specific Resource is a resource in the context of an Annotation. They are used to record further properties or relationships needed to understand the particular contextual use, such as which part of the resource is used or how it should be rendered. In IIIF, the Specific Resource model from the Web Annotation Data Model has some additional properties beyond those defined by the W3C, such as `transform`.

#### Textual Body

`"type": "TextualBody"`

A Textual Body is an embedded resource within an Annotation that carries, as the name suggests, a text as the body of the Annotation. It is defined by the Web Annotation Data Model, and this specification defines a new property for `position` that allows it to be positioned within a Container.

#### Choice

`"type": "Choice"`

A Choice is a Web Annotation construction that allows one entry from a list to be selected for processing or display. This specification allows `behavior` to be added to a Choice to influence how it is processed.


### Content Resources

Content resources are resources on the Web such as images, audio, video, or text which can be associated with a Container via an Annotation, or provide a representation of any resource.

Content resources _MUST_ have an `id` property, with the value being the URI at which the resource can be obtained.

The type of the content resource _MUST_ be included, and _SHOULD_ be taken from the table listed under the definition of `type`. The `format` of the resource _SHOULD_ be included and, if so, _SHOULD_ be the media type that is returned when the resource is dereferenced. The `profile` of the resource, if it has one, _SHOULD_ also be included.

If the content resource is an Image, and a IIIF Image service is available for it, then the `id` property of the content resource _MAY_ be a complete URI to any particular representation supported by the Image Service, such as `https://example.org/image1/full/1000,/0/default.jpg`, but _MUST NOT_ be just the URI of the IIIF Image service. Its `type` value _MUST_ be the string `Image`. Its media type _MAY_ be listed in `format`, and its height and width _MAY_ be given as integer values for `height` and `width` respectively. The Image _SHOULD_ have the service [referenced][prezi30-terminology] from it using the `service` property.

If there is a need to distinguish between content resources, then the resource _SHOULD_ have the `label` property.

Containers _MAY_ be treated as content resources for the purposes of annotating on to other Containers. In this situation, the Container _MAY_ be [embedded][prezi30-terminology] within the Annotation, be a reference within the same Manifest, or require dereferencing to obtain its description.


### Audio Content





### Selectors

The Web Annotation Data Model defines several Selectors, which describe how to find a specific segment of that resource to be used. As noted, the nature of Selectors are dependent on the type of resources that they select out of, and the methods needed for those descriptions will vary. The Selectors from the Web Annotation Data Model and other sources can be used within the IIIF Data Model. This specification defines additional Selector classes for use.

#### Point Selector

`"type": "PointSelector"`

There are common use cases in which a point, rather than a range or area, is the target of the Annotation. For example, putting a pin in a map should result in an exact point, not a very small rectangle. Points in time are not very short durations, and user interfaces should also treat these differently. This is particularly important when zooming in (either spatially or temporally) beyond the scale of the frame of reference.


* FIXME: either supply instant, or all applicable dimensions for the source
   list properties here like manifest


```json
{
  "id": "https://example.org/selectors/1",
  "type": "PointSelector",
  "x": 0.001,
  "y": 12.3,
  "z": 0,
  "instant": 180.0
}
```


#### WKT Selector

`"type": "WktSelector"`

Well-known text, or WKT, is an ISO standard method for describing 2 and 3 dimensional geometries. This selector thus goes beyond what the Web Annotation's SvgSelector enables by incorporating the z axis, as well as additional types of selection such as MultiPolygon. Additional types, such as CIRCULARSTRING may also be supported.

WKT Selectors _MUST_ have a `value` property, which is the WKT string that defines the geometry to be selected.

```json
{
  "id": "https://example.org/selectors/2",
  "type": "WktSelector",
  "value": "POLYGON Z (0 0 0, 10 0.5 3.2 10 5.0 0, 0 0 0)"
}
```

<!-- Yes, Wkt not WKT, c.f. CssStyle, SvgSelector, ImageApiSelector, etc -->


#### Audio Content Selector

`"type": "AudioContentSelector"`

Video content resources consist of both visual and audio content within the same bit-level representation. There are situations when it is useful to refer to only one aspect of the content – either the visual or the audio, but not both. For example, an Annotation might associate only the visual content of a video that has spoken English in the audio, and an audio file that has the translation of that content in Spanish. The Audio Content Selector selects all of the audio content from an A/V content resource, and may be further refined with subsequent selectors to select a segment of it.


```json
{
  "id": "https://example.org/selectors/3",
  "type": "AudioContentSelector"
}
```


#### Visual Content Selector

`"type": "VisualContentSelector"`

Similar to Audio Content Selectors, Visual Content Selectors select the visual aspects of the content of an A/V content resource. They may be further refined by subsequent selectors that select an area or temporal segment of it.

```json
{
  "id": "https://example.org/selectors/4",
  "type": "VisualContentSelector"
}
```


#### Animation Selector

`"type": "AnimationSelector"`

More interactive content resources, such as 3D models, may have animations or similar features that can be _activated_ by user interaction. For example, a model of a box might have an animation that opens the lid and a second animation that closes the lid. In order to activate those animations, they need to be selectable, and thus the specification defines an Animation Selector.

Animation Selectors _MUST_ have a `value` property, which is the identity of the animation in whichever form is used by the source resource.

```json
{
  "id": "https://example.org/selectors/5",
  "type": "AnimationSelector",
  "value": "opening-1"
}
```

#### IIIF Image API Selector

`"type": "ImageApiSelector"`

FIXME: write this




### Range

`"type": "Range"`

Ranges are used to represent structure within a Manifest beyond the default order of the Containers in the `items` property.

Ranges _MUST_ have URIs and they _SHOULD_ be HTTP(S) URIs. Top level Ranges are [embedded][prezi30-terminology] or externally [referenced][prezi30-terminology] within the Manifest in a `structures` property. These top level Ranges then embed or reference other Ranges, Containers or parts of Containers in the `items` property. Each entry in the `items` property _MUST_ be a JSON object, and it _MUST_ have the `id` and `type` properties. If a top level Range needs to be dereferenced by the client, then it _MUST NOT_ have the `items` property, such that clients are able to recognize that it should be retrieved in order to be processed.

The included Containers and parts of Containers need not be contiguous or in the same order as in the Manifest's `items` property or any other Range. Examples include newspaper articles that are continued in different sections, a chapter that starts half way through a page, or time segments of a single canvas that represent different sections of a piece of music.

Ranges _MAY_ link to an Annotation Collection that has the content of the Range using the `supplementary` property. The [referenced][prezi30-terminology] Annotation Collection will contain Annotations that target the Containers within the Range and link content resources to those Containers.


### Scene Components

#### Cameras

A Camera provides a view of a region of the Scene's space from a particular position within the Scene; the client constructs a viewport into the Scene and uses the view of one or more Cameras to render that region. The size and aspect ratio of the viewport is client and device dependent.

FIXME: If either the position or direction is not specified, then the position defaults to the origin, and facing direction defaults to pointing along the z axis towards negative infinity.

The region of the Scene's space that is observable by the camera is bounded by two planes orthogonal to the direction the camera is facing, given in the `near` and `far` properties, (PERSPECTIVE) and a vertical projection angle that provides the top and bottom planes of the region. (viewHeight?)


##### Orthographic Camera

`"type": "OrthographicCamera"`

`OrthographicCamera` removes visual perspective, resulting in object size remaining constant regardless of its distance from the camera


##### Perspective Camera

`"type": "PerspectiveCamera"`

`PerspectiveCamera` mimics the way the human eye sees, in that objects further from the camera are smaller

Properties...


```json
{
  "id": "https://example.org/iiif/camera/1",
  "type": "PerspectiveCamera",
  "near": 1.0,
  "far": 100.0,
  "fieldOfView": 45.0
}
```











#### Lights



##### Ambient Light

`"type": "AmbientLight"`

Ambient Lights evenly illuminates all objects in the scene, and does not have a direction or position.


##### Directional Light

`"type": "DirectionalLight"`

Directional Lights emits in a specific direction as if it is infinitely far away and the rays produced from it are all parallel. It does not have a specific position.

If a DirectionalLight does not have an explicit direction, then the default is in the negative y direction (downwards).

This is really that the light always has a direction of (-y) and is rotated from there. So no rotation = "default" direction.



##### Point Light

`"type": "PointLight"`

Point Lights emits from a single point within the scene in all directions.


##### Spot Light

`"type": "SpotLight"`

Spot Lights emit a cone of light from a single point in a given direction.

If a SpotLight does not have an explicit direction, then the default is in the negative y direction (downwards).



#### Audio in Scenes

All have `source`, `volume`

##### Ambient Audio

`"type": "AmbientAudio"`


##### Point Audio

`"type": "PointAudio"`

##### Spot Audio

`"type": "SpotAudio"`

```json
{
  "id": "iiif/my/spotAudio",
  "type": "SpotAudio",
  "source": {
    "id": "/path/to/my.mp3",
    "type": "Audio",
    "format": "audio/mp3"
  },
  "angle": 45.0
}
```

No default direction, MUST provide a Rotate Transform.




#### Transforms

here are the rules about transforms?



##### Rotate Transform

`"type": "RotateTransform"`

A RotateTransform rotates the local coordinate space around the given axis in a counter-clockwise direction around the axis itself (e.g. around a pivot point of 0 on the axis). A point that was at x=1,y=1 and was rotated 90 degrees around the x axis would be at x=1,y=0,z=1. If an axis value is not specified, then it is not changed, resulting in a default of 0.0


##### Scale Transform

`"type": "ScaleTransform"`

A ScaleTransform applies a multiplier to one or more axes in the local coordinate space. A point that was at 3.5, after applying a ScaleTransform of 2.0 would then be at 7.0. If an axis value is not specified, then it is not changed, resulting in a default of 1.0

##### Translate Transform

`"type": "TranslateTransform"`

A TranslateTransform moves all of the objects in the local coordinate space the given distance along the axis. A point that was at x=1.0, after applying a TranslateTransform of x=1.0 would be at x=2.0. If an axis value is not specified then it is not changed, resulting in a default of 0.0


### Utility Classes

#### Agent

`"type": "Agent"`

#### Service

`"type": "Service"`

#### Unit Value

`"type": "UnitValue"`



## Properties


### accompanyingContainer
{: #accompanyingContainer}

A Container that provides additional content for use while the resource that has the `accompanyingContainer` property is shown or played. Examples include an image to show while a duration-only Canvas is playing audio; or background audio to play while a user is navigating an image-only Manifest.

Clients _MAY_ display the content of an accompanying Container when presenting the resource. As with `placeholderContainer` above, when more than one accompanying Container is available, the client _SHOULD_ pick the one most specific to the content. Publishers _SHOULD NOT_ assume that the accompanying Container will be processed by all clients. Clients _SHOULD_ take care to avoid conflicts between time-based media in the accompanying Container and the content of the resource that has the `accompanyingContainer` property.

The value of `accompanyingContainer` _MUST_ be a JSON object with the `id` and `type` properties.  The value of `type` _MUST_ be a Container type.  The JSON object _MAY_ have other properties valid for that Container type.

 * A Collection _MAY_ have the `accompanyingContainer` property.<br/>
   Clients _MAY_ render `accompanyingContainer` on a Collection.
 * A Manifest _MAY_ have the `accompanyingContainer` property.<br/>
   Clients _MAY_ render `accompanyingContainer` on a Manifest.
 * All Container types _MAY_ have the `accompanyingContainer` property.<br/>
   Clients _MAY_ render `accompanyingContainer` on Containers.
 * A Range _MAY_ have the `accompanyingContainer` property.<br/>
   Clients _MAY_ render `accompanyingContainer` on a Range.
 * Other types of resource _MUST NOT_ have the `accompanyingContainer` property.<br/>
   Clients _SHOULD_ ignore `accompanyingContainer` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "accompanyingContainer": {
    "id": "https://example.org/iiif/1/timeline/accompany",
    "type": "Timeline",
    "duration": 180.0
  }
}
```

### angle
{: #angle}

!!! warning "Need more info"

The value _MUST_ be a floating point number greater than 0 and less than 90, and is measure in degrees. If this property is not specified, then the default value is client-dependent.

* A SpotLight _SHOULD_ have the `angle` property.<br/>
  Clients _SHOULD_ process the `angle` property on SpotLights.

```json
  "angle": 15.0
```

### annotations
{: #annotations}

An ordered list of Annotation Pages that contain commentary or other Annotations about this resource, separate from the Annotations that are used to paint content on to a Canvas. The `motivation` of the Annotations _MUST NOT_ be `painting`, and the target of the Annotations _MUST_ include this resource or part of it.

The value _MUST_ be an array of JSON objects. Each item _MUST_ have at least the `id` and `type` properties.

 * A Collection _MAY_ have the `annotations` property with at least one item.<br/>
   Clients _SHOULD_ process `annotations` on a Collection.
 * A Manifest _MAY_ have the `annotations` property with at least one item.<br/>
   Clients _SHOULD_ process `annotations` on a Manifest,.
 * A Canvas _MAY_ have the `annotations` property with at least one item.<br/>
   Clients _SHOULD_ process `annotations` on a Canvas.
 * A Range _MAY_ have the `annotations` property with at least one item.<br/>
   Clients _SHOULD_ process `annotations` on a Range.
 * A content resource _MAY_ have the `annotations` property with at least one item.<br/>
   Clients _SHOULD_ process `annotations` on a content resource.
 * Other types of resource _MUST NOT_ have the `annotations` property.<br/>
   Clients _SHOULD_ ignore `annotations` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "annotations": [
    {
      "id": "https://example.org/iiif/annotationPage/1",
      "type": "AnnotationPage",
      "items": [ { ... } ]
    }
  ]
}
```

### backgroundColor
{: #backgroundColor}

This property sets the background color behind any painted resources on a spatial Container, such as a Canvas or Scene.

The value _MUST_ be string, which defines an RGB color. It SHOULD be a hex value starting with "#" and is treated in a case-insensitive fashion. If this property is not specified, then the default value is client-dependent.

 * A Canvas _MAY_ have the `backgroundColor` property<br/>
   Clients _SHOULD_ render `backgroundColor` on any resource type.
 * A Scene _MAY_ have the `backgroundColor` property<br/>
   Clients _SHOULD_ render `backgroundColor` on any resource type.
 * Other resources _MUST NOT_ have the `backgroundColor` property.

```json-doc
{ "backgroundColor": "#FFFFFF" }
```

##### behavior
{: #behavior}

A set of user experience features that the publisher of the content would prefer the client to use when presenting the resource. This specification defines the values in the table below. Others may be defined externally as an [extension][prezi30-ldce].

In order to determine the behaviors that are governing a particular resource, there are four inheritance rules from resources that reference the current resource:
* Collections inherit behaviors from their referencing Collection.
* Manifests **DO NOT** inherit behaviors from any referencing Collections.
* Containers inherit behaviors from their referencing Manifest, but **DO NOT** inherit behaviors from any referencing Ranges, as there might be several with different behaviors.
* Ranges inherit behaviors from any referencing Range and referencing Manifest.

Clients should interpret behaviors on a Range only when that Range is selected or is in some other way the context for the user's current interaction with the resources. A Range with the `behavior` value `continuous`, in a Manifest with the `behavior` value `paged`, would mean that the Manifest's Containers should be rendered in a paged fashion, unless the range is selected to be viewed, and its included Containers would be rendered in that context only as being virtually stitched together. This might occur, for example, when a physical scroll is cut into pages and bound into a codex with other pages, and the publisher would like to provide the user the experience of the scroll in its original form.

The descriptions of the behavior values have a set of which other values they are disjoint with, meaning that the same resource _MUST NOT_ have both of two or more from that set. In order to determine which is in effect, the client _SHOULD_ follow the inheritance rules above, taking the value from the closest resource. The user interface effects of the possible permutations of non-disjoint behavior values are client dependent, and implementers are advised to look for relevant recipes in the [IIIF cookbook][annex-cookbook].

The value _MUST_ be an array of strings.

 * Any resource type _MAY_ have the `behavior` property with at least one item.<br/>
   Clients _SHOULD_ process `behavior` on any resource type.


!!! Could continuous stitch together Timelines?

TODO: Address https://github.com/IIIF/api/issues/2318

| Value | Description |
| ----- | ----------- |
|| **Temporal Behaviors** |
| `auto-advance`{: style="white-space:nowrap;"} | Valid on Collections, Manifests, Containers, and Ranges that include or are Containers with at least the `duration` dimension. When the client reaches the end of a Canvas, or segment thereof as specified in a Range, with a duration dimension that has this behavior, it _SHOULD_ immediately proceed to the next Container or segment and render it. If there is no subsequent Container in the current context, then this behavior should be ignored. When applied to a Collection, the client should treat the first Container of the next Manifest as following the last Container of the previous Manifest, respecting any `start` property specified. Disjoint with `no-auto-advance`. |
| `no-auto-advance`{: style="white-space:nowrap;"} | Valid on Collections, Manifests, Containers, and Ranges that include or are Containers with at least the `duration` dimension. When the client reaches the end of a Container or segment with a duration dimension that has this behavior, it _MUST NOT_ proceed to the next Container, if any. This is a default temporal behavior if not specified. Disjoint with `auto-advance`.|
| `repeat` | Valid on Collections and Manifests, that include Containers that have at least the `duration` dimension. When the client reaches the end of the duration of the final Container in the resource, and the `behavior` value `auto-advance`{: style="white-space:nowrap;"} is also in effect, then the client _SHOULD_ return to the first Container, or segment of a Container, in the resource that has the `behavior` value `repeat` and start playing again. If the `behavior` value `auto-advance` is not in effect, then the client _SHOULD_ render a navigation control for the user to manually return to the first Container or segment. Disjoint with `no-repeat`.|
| `no-repeat` | Valid on Collections and Manifests, that include Containers that have at least the `duration` dimension. When the client reaches the end of the duration of the final Container in the resource, the client _MUST NOT_ return to the first Container, or segment of Container. This is a default temporal behavior if not specified. Disjoint with `repeat`.|
| | **Layout Behaviors** |
| `unordered` | Valid on Collections, Manifests and Ranges. The resources included in resources that have this behavior have no inherent order, and user interfaces _SHOULD_ avoid implying an order to the user. Disjoint with `individuals`, `continuous`, and `paged`.|
| `individuals` | Valid on Collections, Manifests, and Ranges. For Collections that have this behavior, each of the included Manifests are distinct objects in the given order. For Manifests and Ranges, the included Containers are distinct views, and _SHOULD NOT_ be presented in a page-turning interface. This is the default layout behavior if not specified. Disjoint with `unordered`, `continuous`, and `paged`. |
| `continuous` | Valid on Collections, Manifests and Ranges, which include Canvases. Canvases included in resources that have this behavior are partial views and an appropriate rendering might display all of the Canvases virtually stitched together, such as a long scroll split into sections. This behavior has no implication for audio resources. The `viewingDirection` of the Manifest will determine the appropriate arrangement of the Canvases. Disjoint with `unordered`, `individuals` and `paged`. |
| `paged` | Valid on Collections, Manifests and Ranges, which include Canvases. Canvases included in resources that have this behavior represent views that _SHOULD_ be presented in a page-turning interface if one is available. The first canvas is a single view (the first recto) and thus the second canvas likely represents the back of the object in the first canvas. If this is not the case, see the `behavior` value `non-paged`. Disjoint with `unordered`, `individuals`, and `continuous`. |
| `facing-pages`{: style="white-space:nowrap;"} | Valid only on Canvases. Canvases that have this behavior, in a Manifest that has the `behavior` value `paged`, _MUST_ be displayed by themselves, as they depict both parts of the opening. If all of the Canvases are like this, then page turning is not possible, so simply use `individuals` instead. Disjoint with `non-paged`.|
| `non-paged` | Valid only on Canvases. Canvases that have this behavior _MUST NOT_ be presented in a page-turning interface, and _MUST_ be skipped over when determining the page order. This behavior _MUST_ be ignored if the current Manifest does not have the `behavior` value `paged`. Disjoint with `facing-pages`. |
| | **Collection Behaviors** |
| `multi-part` | Valid only on Collections. Collections that have this behavior consist of multiple Manifests or Collections which together form part of a logical whole or a contiguous set, such as multi-volume books or a set of journal issues. Clients might render these Collections as a table of contents rather than with thumbnails, or provide viewing interfaces that can easily advance from one member to the next. Disjoint with `together`.|
| `together` | Valid only on Collections. A client _SHOULD_ present all of the child Manifests to the user at once in a separate viewing area with its own controls. Clients _SHOULD_ catch attempts to create too many viewing areas. This behavior _SHOULD NOT_ be interpreted as applying to the members of any child resources. Disjoint with `multi-part`.|
| | **Navigation Behaviors** |
| `sequence` | Valid only on Ranges, where the Range is [referenced][prezi30-terminology] in the `structures` property of a Manifest. Ranges that have this behavior represent different orderings of the Containers listed in the `items` property of the Manifest, and user interfaces that interact with this order _SHOULD_ use the order within the selected Range, rather than the default order of `items`. Disjoint with `thumbnail-nav` and `no-nav`.|
| `thumbnail-nav`{: style="white-space:nowrap;"} | Valid only on Ranges. Ranges that have this behavior _MAY_ be used by the client to present an alternative navigation or overview based on thumbnails, such as regular keyframes along a timeline for a video, or sections of a long scroll. Clients _SHOULD NOT_ use them to generate a conventional table of contents. Child Ranges of a Range with this behavior _MUST_ have a suitable `thumbnail` property. Disjoint with `sequence` and `no-nav`.|
| `no-nav` | Valid only on Ranges. Ranges that have this behavior _MUST NOT_ be displayed to the user in a navigation hierarchy. This allows for Ranges to be present that capture unnamed regions with no interesting content, such as the set of blank pages at the beginning of a book, or dead air between parts of a performance, that are still part of the Manifest but do not need to be navigated to directly. Disjoint with `sequence` and `thumbnail-nav`.|
| `linear-nav` | FIXME: ... |
| | **Miscellaneous Behaviors** |
| `hidden` | Valid on Annotation Collections, Annotation Pages, Annotations, Specific Resources, Lights, Cameras and Choices. If this behavior is provided, then the client _SHOULD NOT_ render the resource by default, but allow the user to turn it on and off. This behavior does not inherit, as it is not valid on Collections, Manifests, Ranges or Canvases. |
| `reset` | Valid on Annotations with a scope property. FIXME: ...  |
| `no-reset` | Valid on Annotations with a scope property. FIXME: ... |
{: .api-table #table-behavior}

{% include api/code_header.html %}
``` json-doc
{ "behavior": [ "auto-advance", "individuals" ] }
```

##### color
{: #color}

This property sets the color of a Light.

The value _MUST_ be string, which defines an RGB color. It SHOULD be a hex value starting with "#" and is treated in a case-insensitive fashion. If this property is not specified, then the default value is "#FFFFFF".

 * A Light _SHOULD_ have the `color` property<br/>
   Clients _SHOULD_ render `color` on any resource type.
 * Other resources _MUST NOT_ have the `color` property.

```json
"color": "#FFA0A0"
```

##### duration
{: #duration}

The duration of a container or external content resource, given in seconds.

The value _MUST_ be a positive floating point number.

 * A Timeline _MUST_ have the `duration` property.<br/>
   Clients _MUST_ process `duration` on a Timeline.
 * A Canvas or Scene _MAY_ have the `duration` property.<br/>
   Clients _MUST_ process `duration` on a Canvas or Scene, if present.
 * Content resources _SHOULD_ have the `duration` property, if appropriate to the resource type.<br/>
   Clients _SHOULD_ process `duration` on content resources.
 * Other types of resource _MUST NOT_ have a `duration`.<br/>
   Clients _SHOULD_ ignore `duration` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "duration": 125.0 }
```

##### exclude
{: #exclude}

_Summary here_

Just as a Scene may contain multiple Annotations with model, light, and camera resources, a single 3D model file may contain a collection of 3D resources, including model geometry, assemblages of lights, and/or multiple cameras, with some of these potentially manipulated by animations. When painting Scenes or models that themselves may contain groups of resources within a single Scene, it may not always be appropriate to include all possible cameras, lights, or other resources, and it may be desirable to opt not to import some of these resources. This is accomplished through the Annotation property `exclude`, which prevents the import of audio, lights, cameras, or animations from a particular Scene or model prior to the Annotation being painted into a Scene. When `exclude` is used, the excluded resource type should not be loaded into the Scene, and it is not possible to reactivate or turn on these excluded resources after loading.


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

##### far
{: #far}

This property gives the distance from the camera after which objects are no longer visible. Objects further from the camera than the `far` distance cannot be seen.

The value is a non-negative floating point number, in the coordinate space of the Scene in which the Camera is positioned. The value _MUST_ be greater than the value for `near` of the same Camera. If this property is not specified, then the default value is client-dependent.

* A Camera _MAY_ have the `far` property<br/>
  Clients _SHOULD_ process the `far` property on Cameras.

```json-doc
{ "far": 200.0 }
```

##### first


##### fieldOfView
{: #fieldOfView}

The angle which a PerspectiveCamera can "see".

!!! warning "Need more info"

The value _MUST_ be a floating point number greater than 0 and less than 180, and is measured in degrees. If this property is not specified, then the default value is client-dependent.

* A PerspectiveCamera _SHOULD_ have the `fieldOfView` property.<br/>
  Clients _SHOULD_ process the `fieldOfView` property on Cameras.

```json-doc
{ "fieldOfView": 50.0 }
```
##### format
{: #format}

The specific media type (often called a MIME type) for a content resource, for example `image/jpeg`. This is important for distinguishing different formats of the same overall type of resource, such as distinguishing text in XML from plain text.

Note that this is different to the `formats` property in the [Image API][image-api], which gives the extension to use within that API. It would be inappropriate to use in this case, as `format` can be used with any content resource, not just images.

The value _MUST_ be a string, and it _SHOULD_ be the value of the `Content-Type` header returned when the resource is dereferenced.

 * A content resource _SHOULD_ have the `format` property.<br/>
   Clients _MAY_ render the `format` of any content resource.
 * Other types of resource _MUST NOT_ have the `format` property.<br/>
   Clients _SHOULD_ ignore `format` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "format": "application/xml" }
```
##### height
{: #height}

The height of the Canvas or external content resource. For content resources, the value is in pixels. For Canvases, the value does not have a unit. In combination with the width, it conveys an aspect ratio for the space in which content resources are located.

The value _MUST_ be a positive integer.

 * A Canvas _MUST_ have the `height` property.<br/>
   Clients _MUST_ process `height` on a Canvas.
 * Content resources _SHOULD_ have the `height` property, with the value given in pixels, if appropriate to the resource type.<br/>
   Clients _SHOULD_ process `height` on content resources.
 * Other types of resource _MUST NOT_ have the `height` property.<br/>
   Clients _SHOULD_ ignore `height` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "height": 1800 }
```
##### homepage
{: #homepage}

A web page that is about the object represented by the resource that has the `homepage` property. The web page is usually published by the organization responsible for the object, and might be generated by a content management system or other cataloging system. The resource _MUST_ be able to be displayed directly to the user. Resources that are related, but not home pages, _MUST_ instead be added into the `metadata` property, with an appropriate `label` or `value` to describe the relationship.

The value of this property _MUST_ be an array of JSON objects, each of which _MUST_ have the `id`, `type`, and `label` properties, _SHOULD_ have a `format` property, and _MAY_ have the `language` property.

 * Any resource type _MAY_ have the `homepage` property.<br/>
   Clients _SHOULD_ render `homepage` on a Collection, Manifest or Canvas, and _MAY_ render `homepage` on other types of resource.

__Model Alignment__<br/>
Please note that this specification has stricter requirements about the JSON pattern used for the `homepage` property than the [Web Annotation Data Model][org-w3c-webanno]. The IIIF requirements are compatible, but the home page of an Agent found might have only a URI, or might be a JSON object with other properties. See the section on [collisions between contexts][prezi30-context-collisions] for more information.
{: .note}

{% include api/code_header.html %}
``` json-doc
{
  "homepage": [
    {
      "id": "https://example.com/info/",
      "type": "Text",
      "label": { "en": [ "Homepage for Example Object" ] },
      "format": "text/html",
      "language": [ "en" ]
    }
  ]
}
```
##### id
{: #id}

The URI that identifies the resource. If the resource is only available embedded  within another resource (see the [terminology section][prezi30-terminology] for an explanation of "embedded"), such as a Range within a Manifest, then the URI _MAY_ be the URI of the embedding resource with a unique fragment on the end. This is not true for Canvases, which _MUST_ have their own URI without a fragment.

The value _MUST_ be a string, and the value _MUST_ be an HTTP(S) URI for resources defined in this specification. If the resource is retrievable via HTTP(S), then the URI _MUST_ be the URI at which it is published. External resources, such as profiles, _MAY_ have non-HTTP(S) URIs defined by other communities.

The existence of an HTTP(S) URI in the `id` property does not mean that the URI will always be dereferencable.  If the resource with the `id` property is [embedded][prezi30-terminology], it _MAY_ also be dereferenceable. If the resource is referenced (again, see the [terminology section][prezi30-terminology] for an explanation of "referenced"), it _MUST_ be dereferenceable. The [definitions of the Resources][prezi30-resource-structure] give further guidance.

 * All resource types _MUST_ have the `id` property.<br/>
   Clients _MAY_ render `id` on any resource type, and _SHOULD_ render `id` on Collections, Manifests and Canvases.

{% include api/code_header.html %}
``` json-doc
{ "id": "https://example.org/iiif/1/manifest" }
```

##### instant
{: #instant}

A number (floating point) giving the time of the point in seconds, relative to the duration of the source resource

FIXME: fix


##### intensity
{: #intensity}

This property sets the strength or brightness of a Light.

The value _MUST_ be a JSON object, that has the `type`, `value` and `unit` properties. All three properties are required. The value of `type` _MUST_ be the string "UnitValue". The value of `value` is a floating point number. The value of `unit` is a string, drawn from a controlled vocabulary of units. If this property is not specified, then the default intensity value is client-dependent.

This specification defines the unit value of "relative" which constrains the value to be a linear scale between 0.0 (no brightness) and 1.0 (as bright as the client will render).

* A Light _SHOULD_ have the `intensity` property.<br/>
  Clients _SHOULD_ process the `intensity` property on Lights.

```json
{
 "intensity": {"id": "", "type": "UnitValue", "value": 0.5, "unit": "relative"}
}
```
##### interactionMode
{: #interactionMode}

*within* the Scene, whereas viewingDirection and behavior are across containers.

* Containers _MAY_ have the `interactionMode`

Table here with values


locked
orbit
hemisphere-orbit
free
free-direction

other examples: no-zoom, no-scrub, rti-mode
##### items
{: #items}

Much of the functionality of the IIIF Presentation API is simply recording the order in which child resources occur within a parent resource, such as Collections or Manifests within a parent Collection, or Canvases within a Manifest. All of these situations are covered with a single property, `items`.

The value _MUST_ be an array of JSON objects. Each item _MUST_ have the `id` and `type` properties. The items will be resources of different types, as described below.

 * A Collection _MUST_ have the `items` property. Each item _MUST_ be either a Collection or a Manifest.<br/>
   Clients _MUST_ process `items` on a Collection.
 * A Manifest _MUST_ have the `items` property with at least one item. Each item _MUST_ be a Canvas.<br/>
   Clients _MUST_ process `items` on a Manifest.
 * A Canvas _SHOULD_ have the `items` property with at least one item. Each item _MUST_ be an Annotation Page.<br/>
   Clients _MUST_ process `items` on a Canvas.
 * An Annotation Page _SHOULD_ have the `items` property with at least one item. Each item _MUST_ be an Annotation.<br/>
   Clients _MUST_ process `items` on an Annotation Page.
 * A Range _MUST_ have the `items` property with at least one item. Each item _MUST_ be a Range, a Canvas or a Specific Resource where the source is a Canvas.<br/>
   Clients _SHOULD_ process `items` on a Range.
 * Other types of resource _MUST NOT_ have the `items` property.<br/>
   Clients _SHOULD_ ignore `items` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "items": [
    {
      "id": "https://example.org/iiif/manifest1",
      "type": "Manifest"
    },
    {
      "id": "https://example.org/iiif/collection1",
      "type": "Collection"
    }
    // ...
  ]
}
```
##### label
{: #label}

A human readable label, name or title. The `label` property is intended to be displayed as a short, textual surrogate for the resource if a human needs to make a distinction between it and similar resources, for example between objects, pages, or options for a choice of images to display. The `label` property can be fully internationalized, and each language can have multiple values.  This pattern is described in more detail in the [languages][prezi40-languages] section.

The value of the property _MUST_ be a JSON object, as described in the [languages][prezi40-languages] section.

 * A Collection _MUST_ have the `label` property with at least one entry.<br/>
   Clients _MUST_ render `label` on a Collection.
 * A Manifest _MUST_ have the `label` property with at least one entry.<br/>
   Clients _MUST_ render `label` on a Manifest.
 * All Container types _SHOULD_ have the `label` property with at least one entry.<br/>
   Clients _MUST_ render `label` on Container types, and _SHOULD_ generate a `label` for Containers that do not have them.
 * All Content Resource types _MAY_ have the `label` property with at least one entry. If there is a Choice of Content Resource for the same Container, then they _SHOULD_ each have the `label` property with at least one entry.<br/>
   Clients _MAY_ render `label` on Content Resources, and _SHOULD_ render them when part of a Choice.
 * A Range _SHOULD_ have the `label` property with at least one entry. <br/>
   Clients _MUST_ render `label` on a Range.
 * An Annotation Collection _SHOULD_ have the `label` property with at least one entry.<br/>
   Clients _SHOULD_ render `label` on an Annotation Collection.
 * Other types of resource _MAY_ have the `label` property with at least one entry.<br/>
   Clients _MAY_ render `label` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "label": { "en": [ "Example Object Title" ] } }
```
##### language
{: #language}

The language or languages used in the content of this external resource. This property is already available from the Web Annotation model for content resources that are the body or target of an Annotation, however it _MAY_ also be used for resources [referenced][prezi30-terminology] from `homepage`, `rendering`, and `partOf`.

The value _MUST_ be an array of strings. Each item in the array _MUST_ be a valid language code, as described in the [languages section][prezi30-languages].

 * An external resource _SHOULD_ have the `language` property with at least one item.<br/>
   Clients _SHOULD_ process the `language` of external resources.
 * Other types of resource _MUST NOT_ have the `language` property.<br/>
   Clients _SHOULD_ ignore `language` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "language": [ "en" ] }
```

##### last

##### logo
{: #logo}

A small image resource that represents the Agent resource it is associated with. The logo _MUST_ be clearly rendered when the resource is displayed or used, without cropping, rotating or otherwise distorting the image. It is _RECOMMENDED_ that a [IIIF Image API][image-api] service be available for this image for other manipulations such as resizing.

When more than one logo is present, the client _SHOULD_ pick only one of them, based on the information in the logo properties. For example, the client could select a logo of appropriate aspect ratio based on the `height` and `width` properties of the available logos. The client _MAY_ decide on the logo by inspecting properties defined as [extensions][prezi30-ldce].

The value of this property _MUST_ be an array of JSON objects, each of which _MUST_ have `id` and `type` properties, and _SHOULD_ have `format`. The value of `type` _MUST_ be `Image`.

 * Agent resources _SHOULD_ have the `logo` property.<br/>
   Clients _MUST_ render `logo` on Agent resources.


{% include api/code_header.html %}
``` json-doc
{
  "logo": [
    {
      "id": "https://example.org/img/logo.jpg",
      "type": "Image",
      "format": "image/jpeg",
      "height": 100,
      "width": 120
    }
  ]
}
```

##### lookAt
{: #lookAt}

_Summary here_
It is useful to be able to rotate a light or camera or audio resource such that it is facing another object or point in the Scene, rather than calculating the angles within the Scene's coordinate space. This is accomplished with a property called `lookAt`, valid on DirectionalLight, SpotLight, and all Cameras. The value of the property is either a PointSelector, a WktSelector, the URI of an Annotation which paints something into the current Scene, or a Specific Resource with a selector identifying a point or region in an arbitrary container.

If the value is a PointSelector, then the light or camera resource is rotated around the x and y axes such that it is facing the given point. If the value is a WktSelector, then the resource should be rotated to face the given region. If the value is an Annotation which targets a point via a PointSelector, URI fragment or other mechanism, then the resource should be rotated to face that point. If the value is a Specific Resource, the source container for the Specific Resource must be painted into the current Scene, and the Specific Resource selector should identify a point or region in the source container. In this case, the light or camera resource should be rotated to face the point or region in the source container where the point or region is located within the current Scene's coordinate space. This allows light or camera resources to face a specific 2D point on a Canvas painted into a 3D scene.

This rotation happens after the resource has been added to the Scene, and thus after any transforms have taken place in the local coordinate space.


The value _MUST_ be a JSON object, conforming to either a reference to an Annotation, or an embedded PointSelector. If this property is not specified, then the default value for cameras is to look straight backwards (-Z) and for lights to point straight down (-Y).

* A Camera _MAY_ have the `lookAt` property.<br/>
  Clients _SHOULD_ process the `lookAt` property on Cameras.
* A SpotLight or a DirectionalLight _SHOULD_ have the `lookAt` property.<br/>
* A SpotSound _SHOULD_ have the `lookAt` property.


```json
"lookAt": {
    "type": "PointSelector",
    "x": 3,
    "y": 0,
    "z": -10
}
```
##### metadata
{: #metadata}

An ordered list of descriptions to be displayed to the user when they interact with the resource, given as pairs of human readable `label` and `value` entries. The content of these entries is intended for presentation only; descriptive semantics _SHOULD NOT_ be inferred. An entry might be used to convey information about the creation of the object, a physical description, ownership information, or other purposes.

The value of the `metadata` property _MUST_ be an array of JSON objects, where each item in the array has both `label` and `value` properties. The values of both `label` and `value` _MUST_ be JSON objects, as described in the [languages][prezi40-languages] section.

 * A Collection _SHOULD_ have the `metadata` property with at least one item. <br/>
   Clients _MUST_ render `metadata` on a Collection.
 * A Manifest _SHOULD_ have the `metadata` property with at least one item.<br/>
   Clients _MUST_ render `metadata` on a Manifest.
 * All Container types _MAY_ have the `metadata` property with at least one item.<br/>
   Clients _SHOULD_ render `metadata` on Containers.
 * Other types of resource _MAY_ have the `metadata` property with at least one item.<br/>
   Clients _MAY_ render `metadata` on other types of resource.

Clients _SHOULD_ display the entries in the order provided. Clients _SHOULD_ expect to encounter long texts in the `value` property, and render them appropriately, such as with an expand button, or in a tabbed interface.

{% include api/code_header.html %}
``` json-doc
{
  "metadata": [
    {
      "label": { "en": [ "Creator" ] },
      "value": { "en": [ "Anne Artist (1776-1824)" ] }
    }
  ]
}
```
##### navDate
{: #navDate}

A date that clients may use for navigation purposes when presenting the resource to the user in a date-based user interface, such as a calendar or timeline. More descriptive date ranges, intended for display directly to the user, _SHOULD_ be included in the `metadata` property for human consumption. If the resource contains Canvases that have the `duration` property, the datetime given corresponds to the navigation datetime of the start of the resource. For example, a Range that includes a Canvas that represents a set of video content recording a historical event, the `navDate` is the datetime of the first moment of the recorded event.

The value _MUST_ be an [XSD dateTime literal][org-w3c-xsd-datetime]. The value _MUST_ have a timezone, and _SHOULD_ be given in UTC with the `Z` timezone indicator, but _MAY_ instead be given as an offset of the form `+hh:mm`.

 * A Collection _MAY_ have the `navDate` property.<br/>
   Clients _MAY_ render `navDate` on a Collection.
 * A Manifest _MAY_ have the `navDate` property.<br/>
   Clients _MAY_ render `navDate` on a Manifest.
 * A Range _MAY_ have the `navDate` property.<br/>
   Clients _MAY_ render `navDate` on a Range.
 * All Container types _MAY_ have the `navDate` property.<br/>
   Clients _MAY_ render `navDate` on Containers.
* Annotations _MAY_ have the `navDate` property.
   Clients _MAY_ render `navDate` on Annotations.
 * Other types of resource _MUST NOT_ have the `navDate` property.<br/>
   Clients _SHOULD_ ignore `navDate` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "navDate": "2010-01-01T00:00:00Z" }
```
##### navPlace
{: #navPlace}

A geographic location that clients may use for navigation purposes when presenting the resource to the user in a map-based user interface. The location is identified using structured data, described below, with latitude and longitude based points or polygons. If the location is only textual, then the information should instead be included in the `metadata` property.

The value of the property _MUST_ be a [GeoJSON Feature Collection] [link] containing one or more [Features] [link].  The value _SHOULD_ be embedded and _MAY_ be a reference. Feature Collections referenced in the `navPlace` property _MUST_ have the `id` and `type` properties and _MUST NOT_ have the `features` property.

*   A Collection _MAY_ have the `navPlace` property.<br/>
   Clients _MAY_ render `navPlace` on a Collection.
*   A Manifest _MAY_ have the `navPlace` property.<br/>
   Clients _MAY_ render `navPlace` on a Manifest.
*   A Range _MAY_ have the `navPlace` property.<br/>
   Clients _MAY_ render `navPlace` on a Range.
* All Container types _MAY_ have the `navPlace` property.<br/>
   Clients _MAY_ render `navPlace` on Containers.
* Annotations _MAY_ have the `navPlace` property.
   Clients _MAY_ render `navPlace` on Annotations.
*   Other types of resource _MUST NOT_ have the `navPlace` property.<br/>
   Clients _SHOULD_ ignore `navPlace` on other types of resource.


{% include api/code_header.html %}
```json-doc
{
   "navPlace":{
      "id": "https://example.com/feature-collection/1",
      "type": "FeatureCollection",
      "features":[
         {
            "id": "https://example.com/feature/1",
            "type": "Feature",
            "geometry":{
               "id": "https://example.com/geometry/1",
               "type": "Point",
               "coordinates":[
                  9.938,
                  51.533
               ]
            }
         }
      ]
   }
}
```

##### near
{: #near}

This property gives the distance from the camera from which objects are visible. Objects closer to the camera than the `near` distance cannot be seen.

The value is a non-negative floating point number, in the coordinate space of the Scene in which the Camera is positioned. The value _MUST_ be less than the value for `far` for the same Camera. If this property is not specified, then the default value is client-dependent.

* A Camera _MAY_ have the `near` property<br/>
  Clients _SHOULD_ process the `near` property on Cameras.

```json-doc
{ "near": 1.5 }
```

##### next

...


##### partOf
{: #partOf}

A containing resource that includes the resource that has the `partOf` property. When a client encounters the `partOf` property, it might retrieve the [referenced][prezi30-terminology] containing resource, if it is not [embedded][prezi30-terminology] in the current representation, in order to contribute to the processing of the contained resource. For example, the `partOf` property on a Canvas can be used to reference an external Manifest in order to enable the discovery of further relevant information. Similarly, a Manifest can reference a containing Collection using `partOf` to aid in navigation.

The value _MUST_ be an array of JSON objects. Each item _MUST_ have the `id` and `type` properties, and _SHOULD_ have the `label` property.

 * Any resource type _MAY_ have the `partOf` property with at least one item<br/>
   Clients _MAY_ render `partOf` on any resource type.

{% include api/code_header.html %}
``` json-doc
{ "partOf": [ { "id": "https://example.org/iiif/1", "type": "Manifest" } ] }
```

The resources referred to by the `accompanyingContainer` and `placeholderContainer` properties are `partOf` that referring Container.

##### placeholderContainer
{: #placeholderContainer}

A single Container that provides additional content for use before the main content of the resource that has the `placeholderContainer` property is rendered, or as an advertisement or stand-in for that content. Examples include images, text and sound standing in for video content before the user initiates playback; or a film poster to attract user attention. The content provided by `placeholderContainer` differs from a thumbnail: a client might use `thumbnail` to summarize and navigate multiple resources, then show content from `placeholderContainer` as part of the initial presentation of a single resource. A placeholder Container is likely to have different dimensions to those of the Container(s) of the resource that has the `placeholderContainer` property. A placeholder Container may be of a different type from the resource that has the `placeholderContainer` property. For example, a `Scene` may have a placeholder Container of type `Canvas`.

Clients _MAY_ display the content of a linked placeholder Container when presenting the resource. When more than one such Container is available, for example if `placeholderContainer` is provided for the currently selected Range and the current Manifest, the client _SHOULD_ pick the one most specific to the content. Publishers _SHOULD NOT_ assume that the placeholder Container will be processed by all clients. Clients _SHOULD_ take care to avoid conflicts between time-based media in the rendered placeholder Container and the content of the resource that has the `placeholderContainer` property.

The value of `placeholderContainer` _MUST_ be a JSON object with the `id` and `type` properties.  The value of `type` _MUST_ be a Container type.  The JSON object _MAY_ have other properties valid for that Container type.

  * A Collection _MAY_ have the `placeholderContainer` property.<br/>
    Clients _MAY_ render `placeholderContainer` on a Collection.
  * A Manifest _MAY_ have the `placeholderContainer` property.<br/>
    Clients _MAY_ render `placeholderContainer` on a Manifest.
  * All Container types _MAY_ have the `placeholderContainer` property.<br/>
    Clients _MAY_ render `placeholderContainer` on Containers.
  * A Range _MAY_ have the `placeholderContainer` property.<br/>
    Clients _MAY_ render `placeholderContainer` on a Range.
  * Other types of resource _MUST NOT_ have the `placeholderContainer` property.<br/>
    Clients _SHOULD_ ignore `placeholderContainer` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "placeholderContainer": {
    "id": "https://example.org/iiif/1/canvas/placeholder",
    "type": "Canvas",
    "height": 1400,
    "width": 1200
  }
}
```
##### position
{: #position}

It is important to be able to position the (textual) body of an annotation within the Container's space that the annotation also targets. For example, a description of part of an image in a Canvas should be positioned such that it does not obscure the image region itself and labels to be displayed as part of a Scene should not be rendered such that the text is hidden by the three dimensional geometry of the model. If this property is not supplied, then the client should do its best to ensure the content is visible to the user.

The value of this property _MUST_ be a JSON object conforming to the `SpecificResource` pattern of the Web Annotation Model. The Specific Resource _MUST_ have a `source` property that refers to a Container, and a `selector` that describes a point or region within the Container.

* A TextualBody _MAY_ have the `position` property.<br/>
  Clients _SHOULD_ process the `position` property on TextualBody instances.
* Other classes _MUST NOT_ have the `position` property.<br/>
  Clients _MUST_ ignore the `position` property on all other classes.

```json-doc
{ "position": {
    "type": "SpecificResource",
      "source": [{
        "id": "https://example.org/iiif/scene1",
        "type": "Scene"
        }],
      "selector": [{
        "type": "PointSelector",
        "x": 1.0,
        "y": 19.2,
        "z": 2.7
      }]
    }
}

```

##### prev


##### profile
{: #profile}

A schema or named set of functionality available from the resource. The profile can further clarify the `type` and/or `format` of an external resource or service, allowing clients to customize their handling of the resource that has the `profile` property.

The value _MUST_ be a string, either taken from the [profiles registry][registry-profiles] or a URI.

* Resources [referenced][prezi30-terminology] by the `seeAlso` or `service` properties _SHOULD_ have the `profile` property.<br/>
  Clients _SHOULD_ process the `profile` of a service or external resource.
* Other types of resource _MAY_ have the `profile` property.<br/>
  Clients _MAY_ process the `profile` of other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "profile": "https://example.org/profile/statuary" }
```
##### provider
{: #provider}

An organization or person that contributed to providing the content of the resource. Clients can then display this information to the user to acknowledge the provider's contributions.  This differs from the `requiredStatement` property, in that the data is structured, allowing the client to do more than just present text but instead have richer information about the people and organizations to use in different interfaces.

The organization or person is represented as an `Agent` resource.

* Agents _MUST_ have the `id` property, and its value _MUST_ be a string. The string _MUST_ be a URI that identifies the agent.
* Agents _MUST_ have the `type` property, and its value _MUST_ be the string `Agent`.
* Agents _MUST_ have the `label` property, and its value _MUST_ be a JSON object as described in the [languages][prezi30-languages] section.
* Agents _SHOULD_ have the `homepage` property, and its value _MUST_ be an array of JSON objects as described in the [homepage][prezi30-homepage] section.
* Agents _SHOULD_ have the `logo` property, and its value _MUST_ be an array of JSON objects as described in the [logo][prezi30-logo] section.
* Agents _MAY_ have the `seeAlso` property, and its value _MUST_ be an array of JSON object as described in the [seeAlso][prezi30-seealso] section.

The value _MUST_ be an array of JSON objects, where each item in the array conforms to the structure of an Agent, as described above.

 * A Collection _SHOULD_ have the `provider` property with at least one item. <br/>
   Clients _MUST_ render `provider` on a Collection.
 * A Manifest _SHOULD_ have the `provider` property with at least one item. <br/>
   Clients _MUST_ render `provider` on a Manifest.
 * Other types of resource _MAY_ have the `provider` property with at least one item. <br/>
   Clients _SHOULD_ render `provider` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "provider": [
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
      ],
      "seeAlso": [
        {
          "id": "https://data.example.org/about/us.jsonld",
          "type": "Dataset",
          "format": "application/ld+json",
          "profile": "https://schema.org/"
        }
      ]
    }
  ]
}
```
##### provides
{: #provides}

A set of features or additional functionality that a linked resource enables relative to the linking or including resource, which is not defined by the `type`, `format` or `profile` of the linked resource. It provides information as to why and how a client might want to interact with the resource, rather than what the resource is. For example, a text file (linked resource) that `provides` a `closedCaptions` for a Video (context resource), or an audio file (linked resource) that `provides` an `audioDescription` of a Canvas (context resource).

The value _MUST_ be an array of strings, each string identifies a particular feature and _MUST_ be taken from the table below or the [provides registry][link].

Note that the majority of the values have been selected from [accessibility feature spec][link] and thus use the original form rather than being consistent with the hyphen-based form of the values of `behavior` and `viewingDirection`.


* Annotations with the `painting` motivation _SHOULD NOT_ have the `provides` property.<br/>
  Clients _SHOULD_ ignore the `provides` property on Annotations with the `painting` motivation.
* Any resource linked to or included in another resource _MAY_ have the `provides` property.<br/>
  Clients _SHOULD_ process the `provides` property on these resources.

| Value | Description |
| ----- | ----------- |
| `closedCaptions` | ... |
| `alternativeText` | ... |
| `audioDescription` | ... |
| `longDescription` | ... |
| `signLanguage` | ... |
| `highContrastAudio` | ... |
| `highContrastDisplay` | ... |
| `braille` | ... |
| `tactileGraphic` | ... |
| `transcript` | ... |
| `translation` | (IIIF Defined) ... |
| `subtitles` | (IIIF Defined) ... |
{: .api-table #table-behavior}

{% include api/code_header.html %}
``` json-doc
{ "provides": [ "closedCaption" ] }
```

!!! warning "This breaks the graph as the file doesn't provide X in all contexts"
##### rendering
{: #rendering}

A resource that is an alternative, non-IIIF representation of the resource that has the `rendering` property. Such representations typically cannot be painted onto a single Canvas, as they either include too many views, have incompatible dimensions, or are compound resources requiring additional rendering functionality. The `rendering` resource _MUST_ be able to be displayed directly to a human user, although the presentation may be outside of the IIIF client. The resource _MUST NOT_ have a splash page or other interstitial resource that mediates access to it. If access control is required, then the [IIIF Authentication API][iiif-auth] is _RECOMMENDED_. Examples include a rendering of a book as a PDF or EPUB, a slide deck with images of a building, or a 3D model of a statue.

The value _MUST_ be an array of JSON objects. Each item _MUST_ have the `id`, `type` and `label` properties, and _SHOULD_ have the `format` and `language` properties.

 * Any resource type _MAY_ have the `rendering` property with at least one item.<br/>
   Clients _SHOULD_ render `rendering` on a Collection, Manifest or Canvas, and _MAY_ render `rendering` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "rendering": [
    {
      "id": "https://example.org/1.pdf",
      "type": "Text",
      "label": { "en": [ "PDF Rendering of Book" ] },
      "format": "application/pdf"
    }
  ]
}
```
##### requiredStatement
{: #requiredStatement}

Text that _MUST_ be displayed when the resource is displayed or used. For example, the `requiredStatement` property could be used to present copyright or ownership statements, an acknowledgement of the owning and/or publishing institution, or any other text that the publishing organization deems critical to display to the user. Given the wide variation of potential client user interfaces, it will not always be possible to display this statement to the user in the client's initial state. If initially hidden, clients _MUST_ make the method of revealing it as obvious as possible.

The value of the property _MUST_ be a JSON object, that has the `label` and `value` properties, in the same way as a `metadata` property entry. The values of both `label` and `value` _MUST_ be JSON objects, as described in the [languages][prezi40-languages] section.

 * Any resource type _MAY_ have the `requiredStatement` property.<br/>
   Clients _MUST_ render `requiredStatement` on every resource type.

{% include api/code_header.html %}
``` json-doc
{
  "requiredStatement": {
    "label": { "en": [ "Attribution" ] },
    "value": { "en": [ "Provided courtesy of Example Institution" ] }
  }
}
```
##### rights
{: #rights}

A string that identifies a license or rights statement that applies to the content of the resource, such as the JSON of a Manifest or the pixels of an image. The value _MUST_ be drawn from the set of [Creative Commons][org-cc-licenses] license URIs, the [RightsStatements.org][org-rs-terms] rights statement URIs, or those added via the [extension][prezi40-ldce] mechanism. The inclusion of this property is informative, and for example could be used to display an icon representing the rights assertions.

!!! registration not extension

If displaying rights information directly to the user is the desired interaction, or a publisher-defined label is needed, then it is _RECOMMENDED_ to include the information using the `requiredStatement` property or in the `metadata` property.

The value _MUST_ be a string. If the value is drawn from Creative Commons or RightsStatements.org, then the string _MUST_ be a URI defined by that specification.

 * Any resource type _MAY_ have the `rights` property.<br/>
   Clients _MAY_ render `rights` on any resource type.

{% include api/code_header.html %}
``` json-doc
{ "rights": "http://creativecommons.org/licenses/by/4.0/" }
```

__Machine actionable URIs and links for users__<br/>
The machine actionable URIs for both Creative Commons licenses and RightsStatements.org right statements are `http` URIs. In both cases, human readable descriptions are available from equivalent `https` URIs. Clients may wish to rewrite links presented to users to use these equivalent `https` URIs.
{: .note}

##### seeAlso
{: #seeAlso}

A machine-readable resource such as an XML or RDF description that is related to the current resource that has the `seeAlso` property. Properties of the resource should be given to help the client select between multiple descriptions (if provided), and to make appropriate use of the document. If the relationship between the resource and the document needs to be more specific, then the document should include that relationship rather than the IIIF resource. Other IIIF resources are also valid targets for `seeAlso`, for example to link to a Manifest that describes a related object. The URI of the document _MUST_ identify a single representation of the data in a particular format. For example, if the same data exists in JSON and XML, then separate resources should be added for each representation, with distinct `id` and `format` properties.

The value _MUST_ be an array of JSON objects. Each item _MUST_ have the `id` and `type` properties, and _SHOULD_ have the `label`, `format` and `profile` properties.

 * Any resource type _MAY_ have the `seeAlso` property with at least one item.<br/>
   Clients _MAY_ process `seeAlso` on any resource type.

{% include api/code_header.html %}
``` json-doc
{
  "seeAlso": [
    {
      "id": "https://example.org/library/catalog/book1.xml",
      "type": "Dataset",
      "label": { "en": [ "Bibliographic Description in XML" ] },
      "format": "text/xml",
      "profile": "https://example.org/profiles/bibliographic"
    }
  ]
}
```


##### service
{: #service}

A service that the client might interact with directly and gain additional information or functionality for using the resource that has the `service` property, such as from an Image to the base URI of an associated [IIIF Image API][image-api] service. The service resource _SHOULD_ have additional information associated with it in order to allow the client to determine how to make appropriate use of it. Please see the [Service Registry][registry-services] document for the details of currently known service types.

The value _MUST_ be an array of JSON objects. Each object will have properties depending on the service's definition, but _MUST_ have either the `id` or `@id` and `type` or `@type` properties. Each object _SHOULD_ have a `profile` property.

 * Any resource type _MAY_ have the `service` property with at least one item.<br/>
   Clients _MAY_ process `service` on any resource type, and _SHOULD_ process the IIIF Image API service.

{% include api/code_header.html %}
``` json-doc
{
  "service": [
    {
      "id": "https://example.org/service",
      "type": "ExampleExtensionService",
      "profile": "https://example.org/docs/service"
    }
  ]
}
```

For cross-version consistency, this specification defines the following values for the `type` or `@type` property for backwards compatibility with other IIIF APIs. Future versions of these APIs will define their own types. These `type` values are necessary extensions for compatibility of the older versions.

| Value                | Specification |
| -------------------- | ------------- |
| ImageService1        | [Image API version 1][image11]  |
| ImageService2        | [Image API version 2][image21]  |
| SearchService1       | [Search API version 1][search1] |
| AutoCompleteService1 | [Search API version 1][search1-autocomplete] |
| AuthCookieService1   | [Authentication API version 1][auth1-cookie-service] |
| AuthTokenService1    | [Authentication API version 1][auth1-token-service] |
| AuthLogoutService1   | [Authentication API version 1][auth1-logout-service] |
{: .api-table #table-service-types}

Implementations _SHOULD_ be prepared to recognize the `@id` and `@type` property names used by older specifications, as well as `id` and `type`. Note that the `@context` key _SHOULD NOT_ be present within the `service`, but instead included at the beginning of the document. The example below includes both version 2 and version 3 IIIF Image API services.

{% include api/code_header.html %}
``` json-doc
{
  "service": [
    {
      "@id": "https://example.org/iiif2/image1/identifier",
      "@type": "ImageService2",
      "profile": "http://iiif.io/api/image/2/level2.json"
    },
    {
      "id": "https://example.org/iiif3/image1/identifier",
      "type": "ImageService3",
      "profile": "level2"
    }
  ]
}
```
##### services
{: #services}

A list of one or more service definitions on the top-most resource of the document, that are typically shared by more than one subsequent resource. This allows for these shared services to be collected together in a single place, rather than either having their information duplicated potentially many times throughout the document, or requiring a consuming client to traverse the entire document structure to find the information. The resource that the service applies to _MUST_ still have the `service` property, as described above, where the service resources have at least the `id` and `type` or `@id` and `@type` properties. This allows the client to know that the service applies to that resource. Usage of the `services` property is at the discretion of the publishing system.

A client encountering a `service` property where the definition consists only of an `id` and `type` _SHOULD_ then check the `services` property on the top-most resource for an expanded definition.  If the service is not present in the `services` list, and the client requires more information in order to use the service, then it _SHOULD_ dereference the `id` (or `@id`) of the service in order to retrieve a service description.

The value _MUST_ be an array of JSON objects. Each object _MUST_ be a service resource, as described above.

* A Collection _MAY_ have the `services` property, if it is the topmost Collection in a response document.<br/>
  Clients _SHOULD_ process `services` on a Collection.
* A Manifest _MAY_ have the `services` property.<br/>
  Clients _SHOULD_ process `services` on a Manifest.

{% include api/code_header.html %}
``` json-doc
{
  "services": [
    {
      "@id": "https://example.org/iiif/auth/login",
      "@type": "AuthCookieService1",
      "profile": "http://iiif.io/api/auth/1/login",
      "label": "Login to Example Institution",
      "service": [
        {
          "@id": "https://example.org/iiif/auth/token",
          "@type": "AuthTokenService1",
          "profile": "http://iiif.io/api/auth/1/token"
        }
      ]
    }
  ]
}
```
##### start
{: #start}

A Canvas, or part of a Canvas, which the client _SHOULD_ show on initialization for the resource that has the `start` property. The reference to part of a Canvas is handled in the same way that Ranges reference parts of Canvases. This property allows the client to begin with the first Canvas that contains interesting content rather than requiring the user to manually navigate to find it.

The value _MUST_ be a JSON object, which _MUST_ have the `id` and `type` properties.  The object _MUST_ be either a Canvas (as in the first example below), or a Specific Resource with a Selector and a `source` property where the value is a Canvas (as in the second example below).

 * A Manifest _MAY_ have the `start` property.<br/>
   Clients _SHOULD_ process `start` on a Manifest.
 * A Range _MAY_ have the `start` property.<br/>
   Clients _SHOULD_ process `start` on a Range.
 * Other types of resource _MUST NOT_ have the `start` property.<br/>
   Clients _SHOULD_ ignore `start` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "start": { "id": "https://example.org/iiif/1/canvas/1", "type": "Canvas" } }
```

{% include api/code_header.html %}
``` json-doc
{
  "start": {
    "id": "https://example.org/iiif/1/canvas-segment/1",
    "type": "SpecificResource",
    "source": "https://example.org/iiif/1/canvas/1",
    "selector": {
      "type": "PointSelector",
      "t": 14.5
    }
  }
}
```
##### structures
{: #structures}

The structure of an object represented as a Manifest can be described using a hierarchy of Ranges. Ranges can be used to describe the "table of contents" of the object or other structures that the user can interact with beyond the order given by the `items` property of the Manifest. The hierarchy is built by nesting the child Range resources in the `items` array of the higher level Range. The top level Ranges of these hierarchies are given in the `structures` property.

The value _MUST_ be an array of JSON objects. Each item _MUST_ have the `id` and `type` properties, and the `type` _MUST_ be `Range`.

 * A Manifest _MAY_ have the `structures` property.<br/>
   Clients _SHOULD_ process `structures` on a Manifest. The first hierarchy _SHOULD_ be presented to the user by default, and further hierarchies _SHOULD_ be able to be selected as alternative structures by the user.
 * Other types of resource _MUST NOT_ have the `structures` property.<br/>
   Clients _SHOULD_ ignore `structures` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "structures": [
    {
      "id": "https://example.org/iiif/range/1",
      "type": "Range",
      "items": [ { ... } ]
    }
  ]
}
```
##### summary
{: #summary}

A short textual summary intended to be conveyed to the user when the `metadata` entries for the resource are not being displayed. This could be used as a brief description for item level search results, for small-screen environments, or as an alternative user interface when the `metadata` property is not currently being rendered. The `summary` property follows the same pattern as the `label` property described above.

The value of the property _MUST_ be a JSON object, as described in the [languages][prezi40-languages] section.

 * A Collection _SHOULD_ have the `summary` property with at least one entry.<br/>
   Clients _SHOULD_ render `summary` on a Collection.
 * A Manifest _SHOULD_ have the `summary` property with at least one entry.<br/>
   Clients _SHOULD_ render `summary` on a Manifest.
 * All Container types _MAY_ have the `summary` property with at least one entry.<br/>
   Clients _SHOULD_ render `summary` on Containers.
 * Other types of resource _MAY_ have the `summary` property with at least one entry.<br/>
   Clients _MAY_ render `summary` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "summary": { "en": [ "This is a summary of the object." ] } }
```

##### supplementary
{: #supplementary}

A link from this Range to an Annotation Collection that includes the `supplementing` Annotations of content resources for the Range. Clients might use this to present additional content to the user from a different Canvas when interacting with the Range, or to jump to the next part of the Range within the same Canvas.  For example, the Range might represent a newspaper article that spans non-sequential pages, and then uses the `supplementary` property to reference an Annotation Collection that consists of the Annotations that record the text, split into Annotation Pages per newspaper page. Alternatively, the Range might represent the parts of a manuscript that have been transcribed or translated, when there are other parts that have yet to be worked on. The Annotation Collection would be the Annotations that transcribe or translate, respectively.

The value _MUST_ be a JSON object, which _MUST_ have the `id` and `type` properties, and the `type` _MUST_ be `AnnotationCollection`.

 * A Range _MAY_ have the `supplementary` property.<br/>
   Clients _MAY_ process `supplementary` on a Range.
 * Other types of resource _MUST NOT_ have the `supplementary` property.<br/>
   Clients _SHOULD_ ignore `supplementary` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "supplementary": { "id": "https://example.org/iiif/1/annos/1", "type": "AnnotationCollection" } }
```

##### thumbnail
{: #thumbnail}

A content resource, such as a small image or short audio clip, that represents the resource that has the `thumbnail` property. A resource _MAY_ have multiple thumbnail resources that have the same or different `type` and `format`.

The value _MUST_ be an array of JSON objects, each of which _MUST_ have the `id` and `type` properties, and _SHOULD_ have the `format` property. Images and videos _SHOULD_ have the `width` and `height` properties, and time-based media _SHOULD_ have the `duration` property. It is _RECOMMENDED_ that a [IIIF Image API][image-api] service be available for images to enable manipulations such as resizing.

 * A Collection _SHOULD_ have the `thumbnail` property with at least one item.<br/>
   Clients _SHOULD_ render `thumbnail` on a Collection.
 * A Manifest _SHOULD_ have the `thumbnail` property with at least one item.<br/>
   Clients _SHOULD_ render `thumbnail` on a Manifest.
 * All Container types _SHOULD_ have the `thumbnail` property with at least one item.<br/>
   Clients _SHOULD_ render `thumbnail` on Containers.
 * Content Resource types _MAY_ have the `thumbnail` property with at least one item. Content Resources _SHOULD_ have the `thumbnail` property with at least one item if it is an option in a Choice of resources.<br/>
   Clients _SHOULD_ render `thumbnail` on a content resource.
 * Other types of resource _MAY_ have the `thumbnail` property with at least one item.<br/>
   Clients _MAY_ render `thumbnail` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "thumbnail": [
    {
      "id": "https://example.org/img/thumb.jpg",
      "type": "Image",
      "format": "image/jpeg",
      "width": 300,
      "height": 200
    }
  ]
}
```

##### timeMode
{: #timeMode}

A mode associated with an Annotation that is to be applied to the rendering of any time-based media, or otherwise could be considered to have a duration, used as a body resource of that Annotation. Note that the association of `timeMode` with the Annotation means that different resources in the body cannot have different values. This specification defines the values specified in the table below. Others may be defined externally as an [extension][prezi30-ldce].

The value _MUST_ be a string.

 * An Annotation _MAY_ have the `timeMode` property.<br/>
   Clients _SHOULD_ process `timeMode` on an Annotation.

| Value | Description |
| ----- | ----------- |
| `trim` | (default, if not supplied) If the content resource has a longer duration than the duration of the portion of the Canvas it is associated with, then at the end of the Canvas's duration, the playback of the content resource _MUST_ also end. If the content resource has a shorter duration than the duration of the portion of the Canvas it is associated with, then, for video resources, the last frame _SHOULD_ persist on-screen until the end of the Canvas portion's duration. For example, a video of 120 seconds annotated to a Canvas with a duration of 100 seconds would play only the first 100 seconds and drop the last 20 seconds. |
| `scale` | Fit the duration of content resource to the duration of the portion of the Canvas it is associated with by scaling. For example, a video of 120 seconds annotated to a Canvas with a duration of 60 seconds would be played at double-speed. |
| `loop` | If the content resource is shorter than the `duration` of the Canvas, it _MUST_ be repeated to fill the entire duration. Resources longer than the `duration` _MUST_ be trimmed as described above. For example, if a 20 second duration audio stream is annotated onto a Canvas with a duration of 30 seconds, it will be played one and a half times. |
{: .api-table #table-timemode}

{% include api/code_header.html %}
``` json-doc
{ "timeMode": "trim" }
```


##### totalItems

For compatability with the Web Annotation Data Model, clients _SHOULD_ also accept `total` as the name of this property when used on the `AnnotationCollection` class.


##### transform
{: #transform}

_Summary here_

The value of this property is an array of JSON objects, each of which is a Transform.

Process them in order given.



##### type
{: #type}

The type or class of the resource. For classes defined for this specification, the value of `type` will be described in the sections below describing each individual class.

For content resources, the value of `type` is drawn from other specifications. Recommendations for common content types such as image, text or audio are given in the table below.

The JSON objects that appear in the value of the `service` property will have many different classes, and can be used to distinguish the sort of service, with specific properties defined in a [registered context document][prezi30-ldce].

The value _MUST_ be a string.

 * All resource types _MUST_ have the `type` property.<br/>
   Clients _MUST_ process, and _MAY_ render, `type` on any resource type.

| Class         | Description                      |
| ------------- | -------------------------------- |
| `Audio`       | Auditory resources primarily intended to be heard, such as might be rendered with an &lt;audio> HTML tag |
| `Dataset`     | Data not intended to be rendered to humans directly, such as a CSV, an RDF serialization or a zip file |
| `Image`       | Two dimensional visual resources primarily intended to be seen, such as might be rendered with an &lt;img> HTML tag |
| `Model`       | A three dimensional spatial model intended to be visualized, such as might be rendered with a 3d javascript library |

| `Text`        | Resources primarily intended to be read |
| `Video`       | Moving images, with or without accompanying audio, such as might be rendered with a &lt;video> HTML tag |
{: .api-table #table-type}

!!! note
For compatibility with previous versions, clients _SHOULD_ accept `Sound` as a synonym for `Audio`.


{% include api/code_header.html %}
``` json-doc
{ "type": "Image" }
```

##### unit

FIXME: possible values are 'm' and 's' and 'relative'


##### value


metadata:

{label: value: {"en": ["foo"]}}

UnitValue

unit: value: 0.1234123

FIXME: use scoped context for UnitValue to change the meaning of `value`



##### viewingDirection
{: #viewingDirection}

!!! Rewrite to be where is the navigation control to step to the next/ previous in the items of hte manifest


The direction in which a list of Containers _SHOULD_ be displayed to the user. This specification defines four direction values in the table below. Others may be defined externally [as an extension][prezi30-ldce]. For example,
if the `viewingDirection` value is `left-to-right`, then backwards in the list is to the left, and forwards in the
list is to the right.

The value _MUST_ be a string.

 * A Collection _MAY_ have the `viewingDirection` property.<br/>
   Clients _SHOULD_ process `viewingDirection` on a Collection.
 * A Manifest _MAY_ have the `viewingDirection` property.<br/>
   Clients _SHOULD_ process `viewingDirection` on a Manifest.
 * A Range _MAY_ have the `viewingDirection` property.<br/>
   Clients _MAY_ process `viewingDirection` on a Range.
 * Other types of resource _MUST NOT_ have the `viewingDirection` property.<br/>
   Clients _SHOULD_ ignore `viewingDirection` on other types of resource.

| Value | Description |
| ----- | ----------- |
| `left-to-right` | The object is displayed from left to right. The default if not specified. |
| `right-to-left` | The object is displayed from right to left. |
| `top-to-bottom` | The object is displayed from the top to the bottom. |
| `bottom-to-top` | The object is displayed from the bottom to the top. |
{: .api-table #table-direction}

{% include api/code_header.html %}
``` json-doc
{ "viewingDirection": "left-to-right" }
```

##### width
{: #width}

The width of the Canvas or external content resource. For content resources, the value is in pixels. For Canvases, the value does not have a unit. In combination with the height, it conveys an aspect ratio for the space in which content resources are located.

The value _MUST_ be a positive integer.

 * A Canvas _MUST_ have the `width` property.<br/>
   Clients _MUST_ process `width` on a Canvas.
 * Content resources _SHOULD_ have the `width` property, with the value given in pixels, if appropriate to the resource type.<br/>
   Clients _SHOULD_ process `width` on content resources.
 * Other types of resource _MUST NOT_ have the `width` property.<br/>
   Clients _SHOULD_ ignore `width` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "width": 1200 }
```

##### x
{: #x}

A number (floating point or integer) giving the x coordinate of the point, relative to the dimensions of the source resource


##### y
{: #y}

A number (floating point or integer) giving the y coordinate of the point, relative to the dimensions of the source resource

##### z
{: #z}

A number (floating point) giving the z coordinate of the point, relative to the dimensions of the source resource



### 3.5. Values

##### Values for motivation

This specification defines two values for the Web Annotation property of `motivation`, or `purpose` when used on a Specific Resource or Textual Body.

While any resource _MAY_ be the `target` of an Annotation, this specification defines only motivations for Annotations that target Canvases. These motivations allow clients to determine how the Annotation should be rendered, by distinguishing between Annotations that provide the content of the Canvas, from ones with externally defined motivations which are typically comments about the Canvas.

Additional motivations may be added to the Annotation to further clarify the intent, drawn from [extensions][prezi30-ldce] or other sources. Clients _MUST_ ignore motivation values that they do not understand. Other motivation values given in the Web Annotation specification _SHOULD_ be used where appropriate, and examples are given in the [Presentation API Cookbook][annex-cookbook].

| Value | Description |
| ----- | ----------- |
| `painting` | Resources associated with a Container by an Annotation that has the `motivation` value `painting`  _MUST_ be presented to the user as the representation of the Container. The content can be thought of as being _of_ the Container. The use of this motivation with target resources other than Containers is undefined. For example, an Annotation that has the `motivation` value `painting`, a body of an Image and the target of a Canvas is an instruction to present that Image as (part of) the visual representation of the Canvas. Similarly, a textual body is to be presented as (part of) the visual representation of the Container and not positioned in some other part of the user interface.|
| `supplementing` | Resources associated with a Container by an Annotation that has the `motivation` value `supplementing`  _MAY_ be presented to the user as part of the representation of the Container, or _MAY_ be presented in a different part of the user interface. The content can be thought of as being _from_ the Container. The use of this motivation with target resources other than Containers is undefined. For example, an Annotation that has the `motivation` value `supplementing`, a body of an Image and the target of part of a Canvas is an instruction to present that Image to the user either in the Canvas's rendering area or somewhere associated with it, and could be used to present an easier to read representation of a diagram. Similarly, a textual body is to be presented either in the targeted region of the Container or otherwise associated with it, and might be OCR, a manual transcription or a translation of handwritten text, or captions for what is being said in a Timeline with audio content. |
| `contentState` | An annotation with the motivation `contentState` has any valid IIIF Resource, or list of IIIF resources, or references to IIIF resources as its `target` property. The client either loads the resource(s) indicated by the Content State annotation `target`, or modifies the view of a currently loaded resource by applying the changes implied by the annotation target - for example, adding a new Light to a Scene where the Light is first introduced in the annotation `target`. The expected interaction depends on how the annotation is linked to the resource the client is currently rendering, or how the annotation is introduced to the client. The _Content State Protocol API 2.0_ describes the ways in which a Content State may be conveyed into a Client or exported from a Client, e.g., as an initialization parameter, or as an exported "Share..." state. Other parts (...) of this specification describe how a Content State in the context of a `commenting` or other annotation modifies the Container when the user selects that annotation, such as changing the camera, lighting or even the models in a Scene as the user progresses though the steps of a narrative conveyed by `describing` annotations. |
| `activating`   | An annotation with the motivation `activating` has any valid IIIF Resource, or list of IIIF resources, or references to IIIF resources as its `target` property. It indicates that a user interaction will trigger a change in either the Container itself, or play a named animation in a Model. If the `body` of the Annotation is of type `TextualBody` and the `target` is of type `SpecificResource` with a `selector` property of type `AnimationSelector`, then the client offers a UI such that when the user selects an interactive element labelled by the TextualBody, the named animation in the model painted by the `source` is played. If the `body` contains IIIF resources, then the body is interpreted as a Content State, and when the user interacts with the IIIF resource provided by the `target`, the content state is applied to modify the Container.   |

// See notes on activating in index

{: .api-table #table-motivations}



## JSON-LD and Extensions

### JSON-LD Contexts and Extensions

The top level resource in the response _MUST_ have the `@context` property, and it _SHOULD_ appear as the very first key/value pair of the JSON representation. This tells Linked Data processors how to interpret the document. The IIIF Presentation API context, below, _MUST_ occur once per response in the top-most resource, and thus _MUST NOT_ appear within [embedded][prezi30-terminology] resources. For example, when embedding a Canvas within a Manifest, the Canvas will not have the `@context` property.

The value of the `@context` property _MUST_ be either the URI `http://iiif.io/api/presentation/{{ page.major }}/context.json` or a JSON array with the URI `http://iiif.io/api/presentation/{{ page.major }}/context.json` as the last item. Further contexts, such as those for local or [registered extensions][registry], _MUST_ be added at the beginning of the array.

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/presentation/{{ page.major }}/context.json"
}
```

Any additional properties beyond those defined in this specification or the Web Annotation Data Model _SHOULD_ be mapped to RDF predicates using further context documents. These extensions _SHOULD_ be added to the top level `@context` property, and _MUST_ be added before the above context. The JSON-LD 1.1 functionality of predicate specific context definitions, known as [scoped contexts][org-w3c-json-ld-scoped-contexts], _MUST_ be used to minimize cross-extension collisions. Extensions intended for community use _SHOULD_ be [registered in the extensions registry][registry], but registration is not mandatory.

{% include api/code_header.html %}
``` json-doc
{
  "@context": [
    "http://example.org/extension/context.json",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ]
}
```

The JSON representation _MUST NOT_ include the `@graph` key at the top level. This key might be created when serializing directly from RDF data using the JSON-LD 1.0 compaction algorithm. Instead, JSON-LD framing and/or custom code should be used to ensure the structure of the document is as defined by this specification.

### Term Collisions between Contexts

There are some common terms used in more than one JSON-LD context document. Every attempt has been made to minimize these collisions, but some are inevitable. In order to know which specification is in effect at any given point, the class of the resource that has the property is the primary governing factor. Thus properties on Annotation based resources use the context from the [Web Annotation Data Model][org-w3c-webanno], whereas properties on classes defined by this specification use the IIIF Presentation API context's definition.

There is one property that is in direct conflict - the `label` property is defined by both and is available for every resource. The use of `label` in IIIF follows modern best practices for internationalization by allowing the language to be associated with the value using the language map construction [described above][prezi30-languages], also allowing multiple languages to be used. The Web Annotation Data Model uses it only for [Annotation Collections][prezi30-annocoll], and mandates the format is a string. For this property, the API overrides the definition from the Annotation model to ensure that labels can consistently be represented in multiple languages.

The following properties are defined by both, and the IIIF representation is more specific than the Web Annotation Data Model but are not in conflict, or are never used on the same resource:

* `homepage`: In IIIF the home page of a resource is represented as a JSON object, whereas in the Web Annotation Data Model it can also be a string.
* `type`: In IIIF the type is singular, whereas in the Web Annotation Data Model there can be more than one type.
* `format`: In IIIF the format of a resource is also singular, whereas in the Web Annotation Data Model there can be more than one format.
* `language`: In IIIF the `language` property always takes an array, whereas in the Web Annotation Data Model it can be a single string.
* `start`: The `start` property is used on a Manifest to refer to the start Canvas or part of a Canvas and thus is a JSON object, whereas in the Web Annotation Data Model it is used on a TextPositionSelector to give the start offset into the textual content and is thus an integer.

The `rights`, `partOf`, and `items` properties are defined by both in the same way.

### Keyword Mappings

The JSON-LD keywords `@id`, `@type` and `@none` are mapped to `id`, `type` and `none` by the Presentation API [linked data context][prezi30-ldce]. Thus in content conforming to this version of the Presentation API, the only JSON key beginning with `@` will be `@context`. However, the content may include data conforming to older specifications or external specifications that use keywords beginning with `@`. Clients should expect to encounter both syntaxes.

### Registries of Values

FIXME: Describe the registries




