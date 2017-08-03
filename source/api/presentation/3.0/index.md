---
title: "Presentation API 3.0 ALPHA DRAFT"
title_override: "IIIF Presentation API 3.0 ALPHA DRAFT"
id: presentation-api
layout: spec
cssversion: 2
tags: [specifications, presentation-api]
major: 3
minor: 0
patch: 0
pre: ALPHA
redirect_from:
  - /api/presentation/index.html
  - /api/presentation/3/index.html
---

## Status of this Document
{:.no_toc}
__This Version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest Stable Version:__ [{{ site.presentation_api.latest.major }}.{{ site.presentation_api.latest.minor }}.{{ site.presentation_api.latest.patch }}][stable-version]

__Previous Version:__ [2.1.1][prev-version]

**Editors**

  * **[Michael Appleby](https://orcid.org/0000-0002-1266-298X)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0002-1266-298X), [_Yale University_](http://www.yale.edu/)
  * **[Tom Crane](https://orcid.org/0000-0003-1881-243X)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0003-1881-243X), [_Digirati_](http://digirati.com/)
  * **[Robert Sanderson](https://orcid.org/0000-0003-4441-6852)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0003-4441-6852), [_J. Paul Getty Trust_](http://www.getty.edu/)
  * **[Jon Stroop](https://orcid.org/0000-0002-0367-1243)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0002-0367-1243), [_Princeton University Library_](https://library.princeton.edu/)
  * **[Simeon Warner](https://orcid.org/0000-0002-7970-7855)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0002-7970-7855), [_Cornell University_](https://www.cornell.edu/)
  {: .names}

{% include copyright.md %}

__Status warning__
This is a work in progress and may change without any notices. Implementers should be aware that this document is not stable. Implementers are likely to find the specification changing in incompatible ways. Those interested in implementing this document before it reaches beta or release stages should join the [mailing list][iiif-discuss] and take part in the discussions, and follow the [emerging issues][prezi3-milestone] on Github.
{: .warning}

----

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

##  1. Introduction

Access to image-based resources is fundamental to many research disciplines, scholarship and the transmission of cultural knowledge. Digital images are a container for much of the information content in the Web-based delivery of museum objects, books, newspapers, letters, manuscripts, maps, scrolls, and digital surrogates of textiles, realia and ephemera. Collections of born-digital images can also benefit from a standardized method to structure their layout and presentation, such as slideshows, image carousels, web comics, and more.

This document describes how the structure and layout of a complex image-based object can be made available in a standard manner. Many different styles of viewer can be implemented that consume the information to enable a rich and dynamic experience, consuming content from across collections and hosting institutions.

An object may comprise a series of pages, surfaces or other views; for example the single view of a painting, the two sides of a photograph, four cardinal views of a statue, or the many pages of an edition of a newspaper or book. The primary requirements for the Presentation API are to provide an order for these views, the resources needed to display a representation of the view, and the descriptive information needed to allow the user to understand what is being seen.

The principles of [Linked Data][linked-data] and the [Architecture of the Web][web-arch] are adopted in order to provide a distributed and interoperable system. The [Shared Canvas data model][shared-canvas] and [JSON-LD][json-ld] are leveraged to create an easy-to-implement, JSON-based format.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]

### 1.1. Objectives and Scope

The objective of the IIIF (pronounced "Triple-Eye-Eff") Presentation API is to provide the information necessary to allow a rich, online viewing environment for primarily image-based objects to be presented to a human user, likely in conjunction with the [IIIF Image API][image-api]. This is the sole purpose of the API and therefore the descriptive information is given in a way that is intended for humans to read, but not semantically available to machines. In particular, it explicitly does __not__ aim to provide metadata that would drive discovery of the digitized objects.

The following are within the scope of the current document:

  * The display of digitized images associated with a particular physical object, or born-digital compound object.
  * Navigation between the pages, surfaces or views of the object.
  * The display of text, and resources of other media types, associated with the object or its pages – this includes descriptive information about the object, labels that can aid navigation such as numbers associated with individual pages, copyright or attribution information, etc.

The following are __not__ within scope:

  * The discovery or selection of interesting digitized objects is not directly supported; however hooks to reference further resources are available.
  * Search within the object; which is described by the [IIIF Content Search API][search-api].

Note that in the following descriptions, "object" (or "physical object") is used to refer to a physical object that has been digitized or a born-digital compound object, and "resources" refer to the digital resources that are the result of that digitization or digital creation process.


###  1.2. Motivating Use Cases

There are many different types of digitized or digital compound objects, from ancient scrolls to modern newspapers, from medieval manuscripts to online comics, and from large maps to small photographs. Many of them bear texts, sometimes difficult to read either due to the decay of the physical object or lack of understanding of the script or language.  These use cases are described in a separate [document][use-case-doc].

Collectively the use cases require a model in which one can characterize the object (via the _Manifest_ resource), the order in which individual surfaces or views are presented (the _Sequence_ resource), and the individual surfaces or views (_Canvas_ resources). Each Canvas may have images and/or other content resources associated with it (_Content_ resources) to allow the view to be rendered. An object may also have parts; for example, a book may have chapters where several pages may be associated with a single chapter (a _Range_ resource) and there may be groups of objects (_Collection_ resources).  These resource types, along with their properties, make up the IIIF Presentation API.

### 1.3. Terminology

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][rfc-2119].


##  2. Resource Type Overview

This section provides an overview of the resource types (or classes) that are used in the specification.  They are each presented in more detail in [Section 5][resource-structure].

### 2.1. Basic Types

This specification makes use of the following primary resource types:

![Primary Resource Types](img/objects.png){: .h400px}
{: .floatRight}

##### Manifest
{: #overview-manifest}

The overall description of the structure and properties of the digital representation of an object. It carries information needed for the viewer to present the digitized content to the user, such as a title and other descriptive information about the object or the intellectual work that it conveys. Each Manifest describes how to present a single object such as a book, a photograph, or a statue.

##### Sequence
{: #overview-sequence}

The order of the views of the object. Multiple Sequences are allowed to cover situations when there are multiple equally valid orders through the content, such as when a manuscript's pages are rebound or archival collections are reordered.

##### Canvas
{: #overview-canvas}

A virtual container that represents a page or view and has content resources associated with it or with parts of it. The Canvas provides a frame of reference for the layout of the content. The concept of a Canvas is borrowed from standards like PDF and HTML, or applications like Photoshop and Powerpoint, where the display starts from a blank display and images, video, text and other resources are "painted" on to it.

##### Content
{: #overview-content}

Content resources such as images, audio, video or text that are associated with a Canvas.

### 2.2. Additional Types

##### Collection
{: #overview-collection}

An ordered list of Manifests, and/or further Collections.  Collections allow easy advertising and browsing of the Manifests in a hierarchical structure, potentially with its own descriptive information.  They can also provide clients with a means to locate all of the Manifests known to the publishing institution.

##### AnnotationPage
{: #overview-annotationpage}

An ordered list of Annotations in a single response, typically associated with a single Canvas, and can be part of an AnnotationCollection.

##### Annotation
{: #overview-annotation}

Content resources and commentary are associated with a Canvas via an Annotation.  This provides a single, coherent method for aligning information, and provides a standards based framework for distinguishing parts of resources and parts of Canvases.  As Annotations can be added later, it promotes a distributed system in which publishers can align their content with the descriptions created by others.

##### AnnotationCollection
{: #overview-annotationcollection}

An ordered list of AnnotationPages.  AnnotationCollections allow higher level groupings of Annotations to be recorded. For example, all of the English translation Annotations of a medieval French document could be kept separate from the transcription or an edition in modern French.

##### Range
{: #overview-range}

An ordered list of Canvases, and/or further Ranges.  Ranges allow Canvases, or parts thereof, to be grouped together in some way. This could be for textual reasons, such as to distinguish books, chapters, verses, sections, non-content-bearing pages, the table of contents or similar. Equally, physical features might be important such as quires or gatherings, sections that have been added later and so forth.


##  3. Resource Properties

This specification defines properties in five distinct areas. Most of the properties may be associated with any of the resource types described above, and may have more than one value.  The property relates to the resource that it is associated with, so a `description` property on a Manifest is a description of the object, whereas a `description` property on a Canvas is a description of that particular page or view of the object.

The requirements for the use of the properties are summarized in [Appendix B][appendixB].

Other properties are allowed, either via custom extensions or endorsed by IIIF. If a client discovers properties that it does not understand, then it _MUST_ ignore them.  Other properties _SHOULD_ consist of a prefix and a name in the form "`prefix:name`" to ensure it does not collide with a property defined by IIIF specifications.

####  3.1. Descriptive Properties

##### label
A human readable label, name or title for the resource. This property is intended to be displayed as a short, textual surrogate for the resource if a human needs to make a distinction between it and similar resources, for example between pages or between a choice of images to display. The value of the property _MUST_ be a JSON object, as described in the [languages][languages] section.

 * A Collection _MUST_ have at least one label.
 * A Manifest _MUST_ have at least one label, such as the name of the object or title of the intellectual work that it embodies.
 * A Sequence  _MAY_ have one or more labels, and if there are multiple Sequences in a single manifest then they _MUST_ each have at least one label.
 * A Canvas _MUST_ have at least one label, such as the page number or short description of the view.
 * A content resource _MAY_ have one or more labels, and if there is a choice of content resource for the same Canvas, then they _SHOULD_ each have at least one label.
 * A Range _SHOULD_ have at least one label. 
 * An AnnotationCollection _MUST_ have at least one label.
 * Other resource types _MAY_ have labels.

``` json-doc
{"label": {"en": ["Label Value"]}}
```

##### metadata
A list of short descriptive entries, given as pairs of human readable `label` and `value` to be displayed to the user. The value of both `label` and `value` _MUST_ be a JSON object, as described in the [languages][languages] section. There are no semantics conveyed by this information, and clients _SHOULD NOT_ use it for discovery or other purposes. This list of descriptive pairs _SHOULD_ be able to be displayed in a tabular form in the user interface. Clients _SHOULD_ have a way to display the information about Manifests and Canvases, and _MAY_ have a way to view the information about other resources. The client _SHOULD_ display the pairs in the order provided by the description. A pair might be used to convey the author of the work, information about its creation, a brief physical description, or ownership information, amongst other use cases. The client is not expected to take any action on this information beyond displaying the label and value. An example pair of label and value might be a label of "Author" and a value of "Jehan Froissart".

 * A Collection _SHOULD_ have one or more metadata pairs associated with it.
 * A Manifest _SHOULD_ have one or more metadata pairs associated with it describing the object or work.
 * Other resource types _MAY_ have one or more metadata pairs.

``` json-doc
{"metadata": [ {"label": {"en": ["Label"]}, "value": {"en": ["Value"]}} ]}
```

##### description
A longer-form prose description of the object or resource that the property is attached to, intended to be conveyed to the user as a full text description, rather than a simple label and value. The value of the property _MUST_ be a JSON object, as described in the [languages][languages] section.  It can duplicate any of the information from the `metadata` fields, along with additional information required to understand what is being displayed. Clients _SHOULD_ have a way to display the descriptions of Manifests and Canvases, and _MAY_ have a way to view the information about other resources.

 * A Collection _SHOULD_ have one or more descriptions.
 * A Manifest _SHOULD_ have one or more descriptions.
 * Other resource types _MAY_ have one or more description.

``` json-doc
{"description": {"en": ["Description Value"]}}
```

##### thumbnail
A small image that depicts or pictorially represents the resource that the property is attached to, such as the title page, a significant image or rendering of a Canvas with multiple content resources associated with it.  It is _RECOMMENDED_ that a [IIIF Image API][image-api] service be available for this image for manipulations such as resizing. If a resource has multiple thumbnails, then each of them _SHOULD_ be different. The value _MUST_ be a JSON array, with each item in the array being a JSON object with at least an `id` and `type` property.

 * A Collection _SHOULD_ have exactly one thumbnail image, and _MAY_ have more than one.
 * A Manifest _SHOULD_ have exactly one thumbnail image, and _MAY_ have more than one.
 * A Sequence _MAY_ have one or more thumbnails and _SHOULD_ have at least one thumbnail if there are multiple Sequences in a single Manifest.
 * A Canvas _MAY_ have one or more thumbnails and _SHOULD_ have at least one thumbnail if there are multiple images or resources that make up the representation.
 * A content resource _MAY_ have one or more thumbnails and _SHOULD_ have at least one thumbnail if it is an option in a choice of resources.
 * Other resource types _MAY_ have one or more thumbnails.

``` json-doc
{"thumbnail": [{"id": "https://example.org/img/thumb.jpg", "type": "Image"}]}
```

##### navDate
A date that the client can use for navigation purposes when presenting the resource to the user in a time-based user interface, such as a calendar or timeline.  The value _MUST_ be an `xsd:dateTime` literal in UTC, expressed in the form "YYYY-MM-DDThh:mm:ssZ".  If the exact time is not known, then "00:00:00" _SHOULD_ be used. Similarly, the month or day _SHOULD_ be 01 if not known.  There _MUST_ be at most one `navDate` associated with any given resource.  More descriptive date ranges, intended for display directly to the user, _SHOULD_ be included in the `metadata` property for human consumption.  

 * A Collection or Manifest _MAY_ have exactly one navigation date associated with it.
 * Other resource types _MUST NOT_ have navigation dates.

``` json-doc
{"navDate": "2010-01-01T00:00:00Z"}
```

####  3.2. Rights and Licensing Properties

The following properties ensure that the interests of the owning or publishing institutions are conveyed regardless of the viewing environment, and a client _MUST_ make these properties clearly available to the user. Given the wide variation of potential client user interfaces, it will not always be possible to display all or any of the properties to the user in the client's initial state. If initially hidden, the method of revealing them _MUST_ be obvious, such as a button or scroll bars.

##### attribution
Text that _MUST_ be shown when the resource it is associated with is displayed or used. For example, this could be used to present copyright or ownership statements, or simply an acknowledgement of the owning and/or publishing institution. The value of the property _MUST_ be a JSON object, as described in the [languages][languages] section.

 * Any resource type _MAY_ have one or more attribution labels.

``` json-doc
{"attribution": {"en": ["Attribution Text"]}}
```

##### rights 

A link to an external resource that describes the license or rights statement under which the resource may be used. The rationale for this being a URI and not a human readable label is that typically there is one license for many resources, and the text is too long to be displayed to the user along with the object. If displaying the text is a requirement, then it is _RECOMMENDED_ to include the information using the `attribution` property instead. The value _MUST_ be an array of strings, each being a URI.

 * Any resource type _MAY_ have one or more rights statements or licenses associated with it.

``` json-doc
{"rights": [{"id": "http://example.org/rights/copyright.html", "format": "text/html"}]}
```

##### logo
A small image that represents an individual or organization associated with the resource it is attached to.  This could be the logo of the owning or hosting institution. The logo _MUST_ be clearly rendered when the resource is displayed or used, without cropping, rotating or otherwise distorting the image. It is _RECOMMENDED_ that a [IIIF Image API][image-api] service be available for this image for manipulations such as resizing.

 * Any resource type _MAY_ have one or more logos associated with it.

``` json-doc
{"logo": [{"id": "https://example.org/img/logo.jpg", "type": "Image"}]}
```

####  3.3. Technical Properties

##### id

The URI that identifies the resource. It is _RECOMMENDED_ that an HTTP URI be used for all resources. URIs from any [registered scheme][iana-uri-schemes] _MAY_ be used, and implementers may find it convenient to use a [UUID URN][rfc-4122] of the form: `"urn:uuid:uuid-goes-here-1234"`.  Resources that do not require URIs _MAY_ be assigned [blank node identifiers][rdf11-blank-nodes]; this is the same as omitting `id`.

 * A Collection _MUST_ have exactly one id, and it _MUST_ be the http(s) URI at which it is published.
 * A Manifest _MUST_ have exactly one id, and it _MUST_ be the http(s) URI at which it is published.
 * A Sequence _MAY_ have an id and _MUST NOT_ have more than one.
 * A Canvas _MUST_ have exactly one id, and it _MUST_ be an http(s) URI.  The Canvas's JSON representation _SHOULD_ be published at that URI.
 * A content resource _MUST_ have exactly one id unless it is embedded in the response, and it _MUST_ be the http(s) URI at which the resource is published.
 * A Range _MUST_ have exactly one id, and it _MUST_ be an http(s) URI.
 * An AnnotationCollection _MUST_ have exactly one id, and it _MUST_ be an http(s) URI.
 * An AnnotationPage _MUST_ have exactly one id, and it _MUST_ be the http(s) URI at which it is published.
 * An Annotation _MUST_ have exactly one id, and the Annotation's representation _SHOULD_ be published at that URI. 

``` json-doc
{"id": "https://example.org/iiif/1/manifest"}
```

##### type

The type of the resource.  For the resource types defined by this specification, the value of `type` will be described in the sections below.  For content resources, the type may be drawn from other vocabularies. Recommendations for basic types such as image, text or audio are also given in the sections below.

 * All resource types _MUST_ have exactly one type specified.

``` json-doc
{"type": "Image"}
```

##### format
The specific media type (often called a MIME type) of a content resource, for example "image/jpeg". This is important for distinguishing text in XML from plain text, for example.

 * A content resource _MAY_ have exactly one format, and if so, it _MUST_ be the value of the `Content-Type` header returned when the resource is dereferenced.
 * Other resource types _MUST NOT_ have a format.

This is different to the `formats` property in the [Image API][image-api], which gives the extension to use within that API.  It would be inappropriate to use in this case, as `format` can be used with any content resource, not just images.

``` json-doc
{"format": "image/jpeg"}
```

##### height
The height of a Canvas or content resource. For content resources, the value is in pixels. For Canvases, the value does not have a unit. In combination with the width, it conveys an aspect ratio for the space in which content resources are located.

 * A Canvas _SHOULD_ have exactly one height, and _MUST NOT_ have more than one. If it has a height, it _MUST_ also have a width.
 * Content resources _MAY_ have exactly one height, given in pixels, if appropriate.
 * Other resource types _MUST NOT_ have a height.

``` json-doc
{"height": 1800}
```

##### width
The width of a Canvas or content resource. For content resources, the value is in pixels. For Canvases, the value does not have a unit. In combination with the height, it conveys an aspect ratio for the space in which content resources are located.

 * A Canvas _SHOULD_ have exactly one width, and _MUST NOT_ have more than one. If it has a width, it _MUST_ also have a height.
 * Content resources _MAY_ have exactly one width, given in pixels, if appropriate.
 * Other resource types _MUST NOT_ have a width.

``` json-doc
{"width": 1200}
```

##### duration
The duration of a Canvas or content resource, given in seconds as a non-negative floating point number. 

 * A Canvas _MAY_ have exactly one duration, and _MUST NOT_ have more than one.
 * Content resources _MAY_ have exactly one duration, and _MUST NOT_ have more than one.
 * Other resource types _MUST NOT_ have a duration.

``` json-doc
{"duration": 125.6}
```

##### viewingDirection
The direction that a set of Canvases _SHOULD_ be displayed to the user. This specification defines four viewing direction values in the table below. Other values _MAY_ also be used, and they _MUST_ be full URIs.

 * A Manifest _MAY_ have exactly one viewing direction, and if so, it applies to all of its sequences unless the sequence specifies its own viewing direction.
 * A Sequence _MAY_ have exactly one viewing direction.
 * A Range _MAY_ have exactly one viewing direction.
 * Other resource types _MUST NOT_ have a viewing direction.

> | Value | Description |
| ----- | ----------- |
| `left-to-right` | The object is displayed from left to right. The default if not specified. |
| `right-to-left` | The object is displayed from right to left. |
| `top-to-bottom` | The object is displayed from the top to the bottom. |
| `bottom-to-top` | The object is displayed from the bottom to the top. |
{: .api-table}

``` json-doc
{"viewingDirection": "left-to-right"}
```

##### viewingHint
A hint to the client as to the most appropriate method of displaying the resource. This specification defines the values specified in the table below. Other values _MAY_ be given, and if they are, they _MUST_ be URIs.

 * Any resource type _MAY_ have one or more viewing hints.

> | Value | Description |
| ----- | ----------- |
| `individuals` | Valid on Collection, Manifest, Sequence and Range. When used as the `viewingHint` of a Collection, the client should treat each of the Manifests as distinct individual objects. For Manifest, Sequence and Range, the Canvases referenced are all distinct individual views, and _SHOULD NOT_ be presented in a page-turning interface. Examples include a gallery of paintings, a set of views of a 3 dimensional object, or a set of the front sides of photographs in a museum collection. |
| `paged` | Valid on Manifest, Sequence and Range. Canvases with this `viewingHint` represent pages in a bound volume, and _SHOULD_ be presented in a page-turning interface if one is available.  The first canvas is a single view (the first recto) and thus the second canvas represents the back of the object in the first canvas. |
| `continuous` | Valid on Manifest, Sequence and Range.  A Canvas with this `viewingHint` is a partial view and an appropriate rendering might display either the Canvases individually, or all of the Canvases virtually stitched together in the display.  Examples when this would be appropriate include long scrolls, rolls, or objects designed to be displayed adjacent to each other.  If this `viewingHint` is present, then the resource _MUST_ also have a `viewingDirection` which will determine the arrangement of the canvases. Note that this does not allow for both sides of a scroll to be included in the same Manifest with this `viewingHint`.  To accomplish that, the Manifest should be "individuals" and have two Ranges, one for each side, which are "continuous".  |
| `multi-part` | Valid only for Collection. Collections with this `viewingHint` consist of multiple Manifests that each form part of a logical whole. Clients might render the Collection as a table of contents, rather than with thumbnails. Examples include multi-volume books or a set of journal issues or other serials. |
| `non-paged` | Valid only for Canvas. Canvases with this `viewingHint` _MUST NOT_ be presented in a page turning interface, and _MUST_ be skipped over when determining the page sequence. This viewing hint _MUST_ be ignored if the current Sequence or Manifest does not have the 'paged' viewing hint. |
| `top` | Valid on Collection and Range. A Collection or Range with this `viewingHint` is the top-most node in a hierarchy that represents a structure to be rendered by the client to assist in navigation. For example, a table of contents within a paged object, major sections of a 3d object, the textual areas within a single scroll, and so forth.  Other Ranges that are descendants of the "top" Range are the entries to be rendered in the navigation structure.  There _MAY_ be multiple Ranges marked with this hint. If so, the client _SHOULD_ display a choice of multiple structures to navigate through. |
| `facing-pages` | Valid only for Canvas. Canvases with this `viewingHint`, in a Sequence or Manifest with the "paged" viewing hint, _MUST_ be displayed by themselves, as they depict both parts of the opening.  If all of the Canvases are like this, then page turning is not possible, so simply use "individuals" instead. |
| `none` | Valid on AnnotationCollection, AnnotationPage, Annotation, SpecificResource and Choice. If this hint is provided, then the client should not render the resource by default, but allow the user to turn it on and off.|
| `auto-advance` | Valid on Collection, Manifest, Sequence and Canvas. When the client reaches the end of a Canvas with a duration dimension that has (or is within a resource that has) this `viewingHint`, it _SHOULD_ immediately proceed to the next Canvas and render it. If there is no subsequent Canvas in the current context, then this `viewingHint` should be ignored. When applied to a Collection, the client should treat the first Canvas of the next Manifest as following the last Canvas of the previous Manifest, respecting any `startCanvas` specified.|
| `together` | Valid only for Collection. A client _SHOULD_ present all of the child Manifests to the user at once in a separate viewing area with its own controls. Clients _SHOULD_ catch attempts to create too many viewing areas. The `together` value _SHOULD NOT_ be interpreted as applying to the members any child resources.|
{: .api-table}

``` json-doc
{"viewingHint": ["auto-advance", "individuals"]}
```

##### choiceHint

A hint associated with a Choice resource that a client can use to determine the publisher's intent as to which agent _SHOULD_ make the choice between the different options.  In the absence of any `choiceHint` value, the rendering application can use any algorithm or process to make the determination.  This specification defines the two values specified in the table below. Other values _MAY_ be given, and if they are, they _MUST_ be URIs.

* A Choice _MAY_ have exactly one `choiceHint`.

> | Value | Description |
| ----- | ----------- |
| `client` | The client software is expected to select an appropriate option without user interaction. |
| `user` | The client software is expected to present an interface to allow the user to explicitly select an option. |

``` json-doc
{"choiceHint": "client"}
```

##### timeMode

A mode associated with an Annotation that is to be applied to the rendering of any time-based media, or otherwise could be considered to have a duration, used as a body resource of that Annotation. Note that the association of `timeMode` with the Annotation means that different resources in the body cannot have different values. This specification defines the values specified in the table below. Other values _MAY_ be given, and if they are, they _MUST_ be URIs.

* An Annotation _MAY_ have exactly one `timeMode` property.

> | Value | Description |
| ----- | ----------- |
| `trim` | (default, if not supplied) If the content resource has a longer duration than the duration of portion of the Canvas it is associated with, then at the end of the Canvas's duration, the playback of the content resource _MUST_ also end. If the content resource has a shorter duration than the duration of the portion of the Canvas it is associated with, then, for video resources, the last frame _SHOULD_ persist on-screen until the end of the Canvas portion's duration. For example, a video of 120 seconds annotated to a Canvas with a duration of 100 seconds would play only the first 60 seconds at normal speed. |
| `scale` | Fit the duration of content resource to the duration of the portion of the Canvas it is associated with by scaling. For example, a video of 120 seconds annotated to a Canvas with a duration of 60 seconds would be played at double-speed. |
| `loop` | If the content resource is shorter than the `duration` of the Canvas, it _MUST_ be repeated to fill the entire duration. Resources longer than the `duration` _MUST_ be trimmed as described above. For example, if a 20 second duration audio stream is annotated onto a Canvas with duration 30 seconds, it will be played one and a half times. |

``` json-doc
{"timeMode": "trim"}
```

####  3.4. Linking Properties

##### related
A link to an external resource intended to be displayed directly to the user, and is related to the resource that has the `related` property. Examples might include a video or academic paper about the resource, a website, an HTML description, and so forth. A label and the format of the related resource _SHOULD_ be given to assist clients in rendering the resource to the user.

 * Any resource type _MAY_ have one or more external resources related to it.

``` json-doc
{"related": [{"id": "https://example.com/info/", "format": "text/html"}]}
```

##### rendering
A link to an external resource intended for display or download by a human user. This property can be used to link from a manifest, collection or other resource to the preferred viewing environment for that resource, such as a viewer page on the publisher's web site. Other uses include a rendering of a manifest as a PDF or EPUB with the images and text of the book, or a slide deck with images of the museum object. A label and the format of the rendering resource _MUST_ be supplied to allow clients to present the option to the user.

 * Any resource type _MAY_ have one or more external rendering resources.

``` json-doc
{"rendering": [{"id": "https://example.org/1.pdf", "format": "application/pdf"}]}
```

##### service
A link to a service that makes more functionality available for the resource, such as from an image to the base URI of an associated [IIIF Image API][image-api] service. The service resource _SHOULD_ have additional information associated with it in order to allow the client to determine how to make appropriate use of it, such as a `profile` link to a service description. It _MAY_ also have relevant information copied from the service itself. This duplication is permitted in order to increase the performance of rendering the object without necessitating additional HTTP requests. Please see the [Service Profiles][annex] document for known services.

 * Any resource type _MAY_ have one or more links to an external service.

``` json-doc
{"service": [
  {"id": "https://example.org/service", 
   "profile": ["http://example.org/docs/service"]
  }]
}
```

##### seeAlso
A link to a machine readable document that semantically describes the resource with the `seeAlso` property, such as an XML or RDF description.  This document could be used for search and discovery or inferencing purposes, or just to provide a longer description of the resource. The `profile` and `format` properties of the document _SHOULD_ be given to help the client select between multiple descriptions (if provided), and to make appropriate use of the document.

 * Any resource type _MAY_ have one or more external descriptions related to it.

``` json-doc
{"rendering": [{"id": "https://example.org/1.xml", "format": "text/xml"}]}
```

##### within
A link to a resource that contains the current resource, such as annotation lists within a layer. This also allows linking upwards to collections that allow browsing of the digitized objects available.

 * Collections or AnnotationPages that serve as [pages][paging] _MUST_ be within exactly one paged resource.
 * Other resource types, including Collections or AnnotationPages not serving as pages, _MAY_ be within one or more containing resources.

``` json-doc
{"within": [{"id": "https://example.org/iiif/1", "type": "Manifest"}]}
```

##### startCanvas
A link from a Sequence or Range to a Canvas that is contained within it.  The value of `startCanvas` _MUST_ be a string containing the URI of the Canvas.  On seeing this relationship, a client _SHOULD_ advance to the specified Canvas when beginning navigation through the Sequence/Range.  This allows the client to begin with the first Canvas that contains interesting content rather than requiring the user to skip past blank or empty Canvases manually.  The Canvas _MUST_ be included in the first Sequence embedded within the Manifest.

 * A Sequence or Range _MAY_ have exactly one Canvas as its starting Canvas.
 * Other resource types _MUST NOT_ have a starting Canvas.

``` json-doc
{"startCanvas": "https://example.org/iiif/1/canvas/1"}
```

##### contentAnnotations
A link from a Range to an AnnotationCollection that includes the Annotations of content resources for that Range.  The value of `contentAnnotations` _MUST_ be a string containing the URI of the AnnotationCollection. Clients might use this to present content to the user from a different Canvas when interacting with the Range, or to jump to the next part of the Range within the same Canvas.  

 * A Range _MAY_ have exactly one AnnotationCollection as its content.
 * Other resource types _MUST NOT_ have `contentAnnotations`.

``` json-doc
{"contentAnnotations": "https://example.org/iiif/1/annos/1"}
```

####  3.5. Paging Properties

##### first
A link from a resource with pages, such as a Collection or AnnotationCollection, to its first page resource, another Collection or an AnnotationPage respectively. The page resource _MUST_ be referenced as an object with at least `id` and `type` properties.

 * A Collection _MAY_ have exactly one Collection as its first page.
 * An AnnotationCollection _MAY_ have exactly one AnnotationPage as its first page.
 * Other resource types _MUST NOT_ have a first page.

``` json-doc
{"first": {"id": "https://example.org/iiif/1/annos/1", "type": "AnnotationPage"}]}
```

##### last
A link from a resource with pages to its last page resource. The page resource _MUST_ be referenced as an object with at least `id` and `type` properties.

 * A collection _MAY_ have exactly one collection as its last page.
 * A layer _MAY_ have exactly one annotation list as its last page.
 * Other resource types _MUST NOT_ have a last page.

``` json-doc
{"last": {"id": "https://example.org/iiif/1/annos/23", "type": "AnnotationPage"}]}
```

##### total
The total number of leaf resources in a paged list, such as the number of Annotations within an AnnotationCollection. The value _MUST_ be a non-negative integer.

 * A Collection _MAY_ have exactly one total, which _MUST_ be the total number of Collections and Manifests in its list of pages.
 * An AnnotationCollection _MAY_ have exactly one total, which _MUST_ be the total number of Annotations in its list of pages.
 * Other resource types _MUST NOT_ have a total.

``` json-doc
{"total": 2217}
```

##### next
A link from a page resource to the next page resource that follows it in order. The page resource _MUST_ be referenced as an object with at least `id` and `type` properties.

 * A Collection _MAY_ have exactly one Collection as its next page.
 * An AnnotationPage _MAY_ have exactly one AnnotationPage as its next page.
 * Other resource types _MUST NOT_ have next pages.

``` json-doc
{"next": {"id": "https://example.org/iiif/1/annos/3", "type": "AnnotationPage"}]}
```

##### prev
A link from a page resource to the previous page resource that precedes it in order. The page resource _MUST_ be referenced as an object with at least `id` and `type` properties.

 * A Collection _MAY_ have exactly one Collection as its previous page.
 * An AnnotationPage _MAY_ have exactly one AnnotationPage as its previous page.
 * Other resource types _MUST NOT_ have previous pages.

``` json-doc
{"prev": {"id": "https://example.org/iiif/1/annos/2", "type": "AnnotationPage"}]}
```

##### startIndex
The 0 based index of the first included resource in the current page, relative to the parent paged resource. The value _MUST_ be a non-negative integer.

 * A Collection _MAY_ have exactly one startIndex, which _MUST_ be the index of its first Collection or Manifest relative to the order established by its parent paging Collection.
 * An AnnotationPage _MAY_ have exactly one startIndex, which _MUST_ be the index of its first Annotation relative to the order established by its parent paging AnnotationCollection.
 * Other resource types _MUST NOT_ have a startIndex.

``` json-doc
{"startIndex": 300}
```

#### 3.6. Structural Properties

These properties define the structure of the object being represented in IIIF by allowing the inclusion of child resources within parents, such as a Canvas within a Sequence, or a Manifest within a Collection.  The majority of cases use `items`, however there are two special cases for different sorts of structures.

##### items

Much of the functionality of the IIIF Presentation API is simply recording the order in which child resources occur within a parent resource, such as Collections or Manifests within a parent Collection, Sequences within a Manifest, or Canvases within a Sequence.  All of these situations are covered with a single property, `items`.  The value _MUST_ be an array of objects.

* A Collection _MUST_ have a list of Collections and/or Manifests as its items.
* A Manifest _MUST_ have a list of Sequences as its items.
* A Sequence _MUST_ have a list of Canvases as its items.
* A Range _MUST_ have a list of Ranges and/or Canvases as its items.
* An AnnotationPage _MUST_ have a list of Annotations as its items.

```json-doc
{"items": [{"id": "..."}]}
```

##### structure

The structure of an object represented as a Manifest can be described using a hierarchy of Ranges.  The top level Ranges of these hierarchies are given in the `structure` property.

* A Manifest _MAY_ have one or more Ranges in the `structure` property.

```json-doc
{"structure": [
  {
    "id": "http://example.org/iiif/range/1",
    "type": "Range",
    "viewingHint": ["top"]
  }
]}
```

##### content

The resources associated with a Canvas via Annotations are given in the `content` property of the Canvas.  Each resource in the list is an AnnotationPage, and can either be embedded in its entirety or referenced via its `id` and `type`.

* A Canvas _SHOULD_ have one or more AnnotationPages in the `content` property. 

```json-doc
{"content": [
  {
    "id": "http://example.org/iiif/annotationPage/1",
    "type": "AnnotationPage",
    "items": [ ... ]
  }
]}
```

##  4. Linked Data Considerations

This section describes features applicable to all of the Presentation API content.  For the most part, these are features of the JSON-LD specification that have particular uses within the API and recommendations about URIs to use.

### 4.1. HTTPS URI Scheme

It is strongly _RECOMMENDED_ that all URIs use the HTTPS scheme, and be available via that protocol.  All URIs _MUST_ be either HTTPS or HTTP, henceforth described more simply as http(s).

### 4.2. URI Representation

Resource descriptions _SHOULD_ be embedded within higher-level descriptions, and _MAY_ also be available via separate requests from http(s) URIs linked in the responses. These URIs are in the `id` property for the resource. Links to resources _MUST_ be given as a JSON object with the `id` property and at least one other property, typically either `type`, `format` or `profile` to give a hint as to what sort of resource is being referred to. Other URI schemes _MAY_ be used if the resource is not able to be retrieved via HTTP. 

``` json-doc
{
  "seeAlso": [
    {"id": "http://example.org/descriptions/book1.xml", "format": "text/xml"}
  ]
}
```

### 4.3. Repeatable Properties

Any of the properties in the API that can be repeated _MUST_ always be given as an array of values, even if there is only a single item in that array.

``` json-doc
{
  "seeAlso": [
    {"id": "http://example.org/descriptions/book1.xml", "format": "text/xml"},
    {"id": "http://example.org/descriptions/book1.json", "format": "application/json"}   
  ]
}
```

### 4.4. Language of Property Values

Language _MAY_ be associated with strings that are intended to be displayed to the user for the `label`, `description`, `attribution` fields, plus the `label` and `value` fields of the `metadata` construction. 

The values of these fields _MUST_ be JSON objects, with the keys being the [RFC 5646][rfc5646] language code for the language, or if the language is either not known or the string does not have a language, then the key must be `"@none"`. The associated values _MUST_ be arrays of strings, where each string is the content in the given language.

``` json-doc
{"description": {
    "en": ["Here is the description of the object in English", 
           "And a second description"],
    "fr": ["Voici la description de l'objet en français"],
    "@none": ["A description in an unknown language"]
}
```

Note that [RFC 5646][rfc5646] allows the script of the text to be included after a hyphen, such as `ar-latn`, and clients should be aware of this possibility. This allows for full internationalization of the user interface components described in the response, as the labels as well as values may be translated in this manner; examples are given below.

In the case where multiple values are supplied, clients _MUST_ use the following algorithm to determine which values to display to the user.  

* If all of the values are in the `@none` list, treated as not having a language associated with them, the client _MUST_ display all of those values.
* Else, the client should try to determine the user's language preferences, or failing that use some default language preferences. Then:
  * If any of the values have a language associated with them, the client _MUST_ display all of the values associated with the language that best matches the language preference.
  * If all of the values have a language associated with them, and none match the language preference, the client _MUST_ select a language and display all of the values associated with that language.
  * If some of the values have a language associated with them, but none match the language preference, the client _MUST_ display all of the values that do not have a language associated with them.

Note that this does not apply to embedded textual bodies in Annotations, which use the Web Annotation pattern of `value` and `langauge` as separate properties.

### 4.5. HTML Markup in Property Values

Minimal HTML markup _MAY_ be included in the `description`, `attribution` properties and the `value` property of a `label`/`value` pair in `metadata`.  It _MUST NOT_ be used in `label` or other properties. This is included to allow manifest creators to add links and simple formatting instructions to blocks of text. The content _MUST_ be well-formed XML and therefore must be wrapped in an element such as `p` or `span`.  There _MUST NOT_ be whitespace on either side of the HTML string, and thus the first character in the string _MUST_ be a '<' character and the last character _MUST_ be '>', allowing a consuming application to test whether the value is HTML or plain text using these.  To avoid a non-HTML string matching this, it is _RECOMMENDED_ that an additional whitespace character be added to the end of the value.

In order to avoid HTML or script injection attacks, clients _MUST_ remove:

  * Tags such as `script`, `style`, `object`, `form`, `input` and similar.
  * All attributes other than `href` on the `a` tag, `src` and `alt` on the `img` tag.
  * CData sections.
  * XML Comments.
  * Processing instructions.

Clients _SHOULD_ allow only `a`, `b`, `br`, `i`, `img`, `p`, and `span` tags. Clients _MAY_ choose to remove any and all tags, therefore it _SHOULD NOT_ be assumed that the formatting will always be rendered. 

``` json-doc
{"description": {"en-latn": ["<p>Some <b>description</b></p>"]}
```

### 4.6. Linked Data Context and Extensions

The top level resource in the response _MUST_ have the `@context` property, and it _SHOULD_ appear as the very first key/value pair of the JSON representation. This tells Linked Data processors how to interpret the information. The IIIF Presentation API context, below, _MUST_ occur exactly once per response, and be omitted from any embedded resources. For example, when embedding a sequence without any extensions within a manifest, the sequence _MUST NOT_ have the `@context` field.

The value of the `@context` property _MUST_ be a list, and the __last__ two values _MUST_ be the Web Annotation context and the Presentation API context, in that order.  And further contexts _MUST_ be added at the beginning of the list.

``` json-doc
{"@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ]
}
```

Any additional fields beyond those defined in this specification or the Web Annotation Data Model _SHOULD_ be mapped to RDF predicates using further context documents.   If possible, these extensions _SHOULD_ be added to the top level `@context` field, and _MUST_ be added before the above contexts.  The JSON-LD 1.1 functionality of type and predicate specific context definitions _SHOULD_ be used if possible to try to minimize any cross-extension collisions.


##  5. Resource Structure

This section provides detailed description of the resource types used in this specification. [Section 2][type-overview] provides an overview of the resource types and figures illustrating allowed relationships between them, and [Appendix B][appendixb] provides summary tables of the property requirements.

###  5.1. Manifest

The Manifest response contains sufficient information for the client to initialize itself and begin to display something quickly to the user. The Manifest resource represents a single object and any intellectual work or works embodied within that object. In particular it includes the descriptive, rights and linking information for the object. It then embeds the Sequence(s) of Canvases that should be rendered to the user.

The identifier in `id` _MUST_ be able to be dereferenced to retrieve the JSON description of the Manifest, and thus _MUST_ use the http(s) URI scheme.

Along with the descriptive information, there is an `items` section, which is a list of JSON-LD objects. Each object describes a [Sequence][sequence], discussed in the next section, that represents the order of the parts of the work, each represented by a [Canvas][canvas].  The first such Sequence _MUST_ be included within the Manifest as well as optionally being available from its own URI. Subsequent Sequences _MAY_ be embedded within the Manifest, or referenced with their identifier (`id`), class (`type`) and label (`label`).

There _MAY_ also be a `structures` section listing one or more [Ranges][range] which describe additional structure of the content, such as might be rendered as a table of contents.

The example below includes only the Manifest-level information, however actual implementations _MUST_ embed at least the first Sequence, Canvas and content information.

``` json-doc
{
  // Metadata about this manifest file
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/2/context.json"
  ],
  "id": "http://example.org/iiif/book1/manifest",
  "type": "Manifest",

  // Descriptive metadata about the object/work
  "label": {"en": ["Book 1"]},
  "metadata": [
    {"label": {"en": ["Author"]}, 
     "value": {"@none": ["Anne Author"]}},
    {"label": {"en": ["Published"]}, 
     "value": {
        "en": ["Paris, circa 1400"],
        "fr": ["Paris, environ 1400"]}
    },
    {"label": {"en": ["Notes"]}, 
     "value": {"en": ["Text of note 1", "Text of note 2"]}},
    {"label": {"en": ["Source"]},
     "value": {"@none": ["<span>From: <a href=\"http://example.org/db/1.html\">Some Collection</a></span>"]}}
  ],
  "description": {"en": ["A longer description of this example book. It should give some real information."]},

  "thumbnail": [{
    "id": "http://example.org/images/book1-page1/full/80,100/0/default.jpg",
    "type": "Image",
    "service": {
      "@context": "http://iiif.io/api/image/{{ site.image_api.latest.major }}/context.json",
      "id": "http://example.org/images/book1-page1",
      "type": "Service",
      "profile": ["http://iiif.io/api/image/{{ site.image_api.latest.major }}/level1.json"]
    }
  }],

  // Presentation Information
  "viewingDirection": "right-to-left",
  "viewingHint": ["paged"],
  "navDate": "1856-01-01T00:00:00Z",

  // Rights Information
  "rights": [{
    "id":"http://example.org/license.html", 
    "type": "Text",
    "format": "text/html"}],

  "attribution": {"en": ["Provided by Example Organization"]},

  "logo": {
    "id": "http://example.org/logos/institution1.jpg",
    "service": {
        "@context": "http://iiif.io/api/image/2/context.json",
        "id": "http://example.org/service/inst1",
        "type": "Service",
        "profile": ["http://iiif.io/api/image/2/profiles/level2.json"]
    }
  },

  // Links
  "related": [{
    "id": "http://example.org/videos/video-book1.mpg",
    "type": "Video",
    "format": "video/mpeg"
  }],
  "service": [{
    "@context": "http://example.org/ns/jsonld/context.json",
    "id": "http://example.org/service/example",
    "type": "Service",
    "profile": ["http://example.org/docs/example-service.html"]
  }],
  "seeAlso": [{
    "id": "http://example.org/library/catalog/book1.xml",
    "type": "Dataset",
    "format": "text/xml",
    "profile": ["http://example.org/profiles/bibliographic"]
  }],
  "rendering": [{
    "id": "http://example.org/iiif/book1.pdf",
    "type": "Text",
    "label": {"en": ["Download as PDF"]},
    "format": "application/pdf"
  }],
  "within": [{
    "id": "http://example.org/collections/books/",
    "type": "Collection"
  }],

  // List of Sequences
  "items": [
      {
        "id": "http://example.org/iiif/book1/sequence/normal",
        "type": "Sequence",
        "label": {"en": ["Current Page Order"]}
        // Sequence's page order should be included here
      }
      // Any additional Sequences can be included here
  ],

  // structure of the resource, described with Ranges
  "structure": [
    {
      "id": "http://example.org/iiif/book1/range/top",
      "type": "Range",
      "viewingHint": ["top"]
      // Ranges members should be included here
    }
    // Any additional top level Ranges can be included here
  ]
}
```

###  5.2. Sequence

The Sequence conveys the ordering of the views of the object. The default Sequence (and typically the only Sequence) _MUST_ be embedded within the Manifest as the first object in the `items` property, and _MAY_ also be available from its own URI.  This Sequence _SHOULD_ have a URI to identify it. Any additional Sequences _MAY_ be included, or referenced externally from the Manifest.  All external Sequences _MUST_ have an http(s) URI, and the description of the Sequence _MUST_ be available by dereferencing that URI.

Sequences _MAY_ have their own descriptive, rights and linking metadata using the same fields as for Manifests. The `label` property _MAY_ be given for Sequences and _MUST_ be given if there is more than one referenced from a Manifest. After the metadata, the set of views of the object, represented by Canvas resources, _MUST_ be listed in order in the `items` property.  There _MUST_ be at least one Canvas given.

Sequences _MAY_ have a `startCanvas` with a single value containing the URI of a Canvas resource that is contained within the Sequence.  This is the Canvas that a viewer _SHOULD_ initialize its display with for the user.  If it is not present, then the viewer _SHOULD_ use the first Canvas in the Sequence.

In the Manifest example above, the Sequence is referenced by its URI and contains only the basic information of `label`, `type` and `id`. The default sequence should be written out in full within the Manifest file, as below.

``` json-doc
{
  // Metadata about this sequence
  "id": "http://example.org/iiif/book1/sequence/normal",
  "type": "Sequence",
  "label": {"en": ["Current Page Order"]},

  "viewingDirection": "left-to-right",
  "viewingHint": ["paged"],
  "startCanvas": "http://example.org/iiif/book1/canvas/p2",

  // The order of the canvases
  "items": [
    {
      "id": "http://example.org/iiif/book1/canvas/p1",
      "type": "Canvas",
      "label": {"@none": ["p. 1"]}
      // ...
    },
    {
      "id": "http://example.org/iiif/book1/canvas/p2",
      "type": "Canvas",
      "label": {"@none": ["p. 2"]}
      // ...
    },
    {
      "id": "http://example.org/iiif/book1/canvas/p3",
      "type": "Canvas",
      "label": {"@none": ["p. 3"]}
      // ...
    }
  ]
}
```

###  5.3. Canvas

The Canvas represents an individual page or view and acts as a central point for laying out the different content resources that make up the display. Canvases _MUST_ be identified by a URI and it _MUST_ be an http(s) URI. The URI of the canvas _MUST NOT_ contain a fragment (a `#` followed by further characters), as this would make it impossible to refer to a segment of the Canvas's area using the `#xywh=` syntax. Canvases _SHOULD_ be able to be dereferenced separately from the Manifest via their URIs as well as being embedded within the Sequence.

Every Canvas _SHOULD_ have a `label` to display. If one is not provided, the client _MAY_ automatically generate one for use based on the Canvas's position within the current Sequence.

A Canvas _MUST_ have a rectangular aspect ratio (described with the `height` and `width` properties) and/or a `duration` to provide an extent in time. These dimensions allow resources to be associated with specific regions of the Canvas, within the space and/or time extents provided. Content _MUST NOT_ be associated with space or time outside of the Canvas's dimensions, such as at coordinates below 0,0, greater than the height or width, before 0 seconds, or after the duration.
 
Renderers _MUST_ scale content into the space/time represented by the Canvas, following any `timeMode` adjustment provided for time-based media.  If the Canvas represents a view of a physical object, the dimensions of the Canvas _SHOULD_ be the same scale as that physical object, and images _SHOULD_ depict only the object.

Content resources are associated with the Canvas via Web Annotations. The Annotations are recorded in the `items` of one or more AnnotationPages, refered to in the `content` array of the Canvas. If the Annotation should be rendered quickly, in the view of the publisher, then it _SHOULD_ be embedded within the Manifest directly.  Other AnnotationPages can be referenced with just their `id`, `type` and optionally a `label`, and clients _SHOULD_ dereference these pages to discover further content.  Content in this case includes media assets such as images, video and audio, textual transcriptions or editions of the Canvas, as well as commentary about the object represented by the Canvas.  These different uses _MAY_ be split up across different AnnotationPages.


__Where should the following paragraph actually live?__

> In a sequence with the `viewingHint` value of "paged" and presented in a book viewing user interface, the first canvas _SHOULD_ be presented by itself -- it is typically either the cover or first recto page. Thereafter, the canvases represent the sides of the leaves, and hence may be presented with two canvases displayed as an opening of the book.  If there are canvases which are in the sequence but would break this ordering, then they _MUST_ have the `viewingHint` property with a value of "non-paged".  Similarly if the first canvas is not a single up, it _MUST_ be marked as "non-paged" or an empty canvas added before it.

``` json-doc
{
  // Metadata about this canvas
  "id": "http://example.org/iiif/book1/canvas/p1",
  "type": "Canvas",
  "label": {"@none": ["p. 1"]},
  "height": 1000,
  "width": 750,

  "content": [
    {
      "id": "http://example.org/iiif/book1/page/p1/1",
      "type": "AnnotationPage",
      "items": [
        // Annotations on the Canvas are included here
      ]
    }
  ]
}
```

###  5.4. Annotation Pages

Association of images and other content with their respective Canvases is done via Annotations. Traditionally Annotations are used for associating commentary with the resource the Annotation's text or body is about, the [Web Annotation][webanno] model allows any resource to be associated with any other resource, or parts thereof, and it is reused for both commentary and painting resources on the Canvas. Other resources beyond images might include the full text of the object, musical notations, musical performances, diagram transcriptions, commentary annotations, tags, video, data and more.

These Annotations are collected together in AnnotationPage resources, which are included in the `content` list from the Canvas.  Each AnnotationPage can be embedded in its entirety, if the Annotations should be processed as soon as possible when the user navigates to that Canvas, or a reference to an external resource via `id`, `type`, and optionally `label`. All of the Annotations in the AnnotationPage __SHOULD__ have the Canvas as their `target`.

The AnnotationPage _MUST_ have an http(s) URI given in `id`, and the JSON representation _MUST_ be returned when that URI is dereferenced.  They _MAY_ have any of the other fields defined in this specification, or the Web Annotation specification.  The Annotations are listed in an `items` list of the AnnotationPage.

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/3/context.json",
  "id": "http://example.org/iiif/book1/list/p1",
  "type": "AnnotationPage",

  "items": [
    {
      "id": "",
      "type": "Annotation",
      "motivation": "painting",
      "body":{
        "id": "http://example.org/iiif/book1/res/music.mp3",
        "type": "Sound",
        "format": "audio/mpeg"
      },
      "target": "http://example.org/iiif/book1/canvas/p1"
    },
    {
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "id": "http://example.org/iiif/book1/res/tei-text-p1.xml",
        "type": "Text",
        "format": "application/tei+xml"
      },
      "target": "http://example.org/iiif/book1/canvas/p1"
    }
    // ... and so on
  ]
}
```

### 5.5. Annotations

Annotations follow the [Web Annotation][webanno] data model.  The description provided here is a summary plus any IIIF specific requirements. It must be noted that the W3C standard is the official documentation.

Annotations _MUST_ have their own http(s) URIs, conveyed in the `id` property. The JSON-LD description of the Annotation _SHOULD_ be returned if the URI is dereferenced, according to the [Web Annotation Protocol][webannoprotocol].

Annotations that associate content _MUST_ have the `motivation` field and the value _MUST_ be "painting". This is in order to distinguish it from comment Annotations, described in further detail below.  Note that all resources which are to be displayed as part of the representation are given the motivation of "painting", regardless of whether they are images or not.  For example, a transcription of the text in a page is considered "painting" as it is a representation of the object, whereas a textual comment about the page is not.

The content resource, such as an image, is linked in the `body` property of the Annotation. The content resource _MUST_ have an `id` field, with the value being the URI at which it can be obtained. If a IIIF Image service is available for an image, then the URI _MUST_ be the complete URI to a particular size of the image content, such as `http://example.org/image1/full/1000,/0/default.jpg`. It _MUST_ have a `type` of "Image". Its media type _MAY_ be listed in `format`, and its height and width _MAY_ be given as integer values for `height` and `width` respectively.

Although it might seem redundant, the URI of the Canvas _MUST_ be repeated in the `target` field of the Annotation. This is to ensure consistency with Annotations that target only part of the resource, described in more detail below, and to remain faithful to the Web Annotation specification, where `target` is mandatory.

The format of the resource _MUST_ be included and _MUST_ be the media type that is returned when the resource is dereferenced. The type of the content resource _SHOULD_ be taken from this [list in the Open Annotation specification][openannotypes], or a similar well-known resource type ontology. For resources that are displayed as part of the rendering (such as images, text transcriptions, performances of music from the manuscript and so forth) the motivation _MUST_ be "painting". The content resources _MAY_ also have any of the other fields defined in this specification, including commonly `label`, `description`, `metadata`, `license` and `attribution`.

Additional features of the [Web Annotation][webanno] data model _MAY_ also be used, such as selecting a segment of the Canvas or content resource, or embedding the comment or transcription within the Annotation. The use of advanced features sometimes results in situations where the `target` is not a content resource, but instead a `SpecificResource`, a `Choice`, or other non-content object. Implementations should check the `type` of the resource and not assume that it is always content to be rendered.

__Move the below para to the annotation document__

> If a [IIIF Image API][image-api] service is available for the image, then a link to the service's base URI _SHOULD_ be included. The base URI is the URI up to the identifier, but not including the trailing slash character or any of the subsequent parameters. A reference to the Image API context document _MUST_ be included and the conformance level profile of the service _SHOULD_ be included. Additional fields from the Image Information document _MAY_ be included in this JSON object to avoid requiring it to be downloaded separately. See the [annex][annex] on using external services for more information.


``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/annotation/p0001-image",
  "type": "Annotation",
  "motivation": "painting",
  "body": {
    "id": "http://example.org/iiif/book1/res/page1.jpg",
    "type": "Image",
    "format": "image/jpeg",
    "service": {
      "@context": "http://iiif.io/api/image/{{ site.image_api.latest.major }}/context.json",
      "id": "http://example.org/images/book1-page1",
      "profile": "http://iiif.io/api/image/{{ site.image_api.latest.major }}/profiles/level2.json"
    },
    "height":2000,
    "width":1500
  },
  "target": "http://example.org/iiif/book1/canvas/p1"
}
```

###  5.6. Range

It may be important to describe additional structure within an object, such as newspaper articles that span pages, the range of non-content-bearing pages at the beginning of a work, or chapters within a book. These are described using ranges in a similar manner to sequences. Ranges _MUST_ have URIs and they _SHOULD_ be http(s) URIs. The intent of adding a range to the manifest is to allow the client to display a structured hierarchy to enable the user to navigate within the object without merely stepping through the current sequence.  The rationale for separating ranges from sequences is that there is likely to be overlap between different ranges, such as the physical structure of a book compared to the textual structure of the work.  An example would be a newspaper with articles that are continued in different sections, or simply a section that starts half way through a page.

Ranges are linked or embedded within the manifest in a `structures` field.  It is a flat list of objects, even if there is only one range.

Ranges have three list based properties to express membership:

##### items
A combined list of both ranges and canvases.  If the range contains both other ranges and canvases, and the ordering of the different types of resource is significant, the range _SHOULD_ instead use the `members` property.  The property's value is an array of canvases, parts of canvases or other ranges.  Each item in the array _MUST_ be an object, and it _MUST_ have the `id`, `type`, and `label` properties.


A range will typically include one or more canvases or, unlike sequences, parts of canvases. The part must be rectangular, and is given using the `xywh=` fragment approach. This allows for selecting, for example, the areas within two newspaper pages where an article is located.

In order to present a table of the different ranges to allow a user to select one, every range _MUST_ have a label and the top most range in the table _SHOULD_ have a `viewingHint` with the value "top". A range that is the top of a hierarchy does not need to list all of the canvases in the sequence, and _SHOULD_ only give the list of ranges below it.  Ranges _MAY_ also have any of the other properties defined in this specification, including the `startCanvas` relationship to the first canvas within the range to start with, if it is not the first listed in `canvases` or `members`.

Ranges _MAY_ also link to a layer, described in the next section, that has the content of the range using the `contentLayer` linking property. The referenced layer will contain one or more annotation lists, each of which contains annotations that target the areas of canvases within the range, and provide the content resources. This allows, for example, the range representing a newspaper article that is split across multiple pages to be linked with the text of the article. Rendering clients might use this to display all of the article text, regardless of which canvas is being viewed.

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/manifest",
  "type": "Manifest",
  // Metadata here ...

  "sequences": [
    // Sequences here ...
  ],

  "structures": [
    {
      "id": "http://example.org/iiif/book1/range/r0",
      "type": "Range",
      "label": "Table of Contents",
      "viewingHint": "top",
      "members": [
        {
          "id": "http://example.org/iiif/book1/canvas/cover",
          "type": "Canvas",
          "label": "Front Cover"
        },
        {
          "id": "http://example.org/iiif/book1/range/r1",
          "type": "Range",
          "label": "Introduction",
          "contentLayer": "http://example.org/iiif/book1/layer/introTexts"
        },
        {
          "id": "http://example.org/iiif/book1/canvas/backCover",
          "type": "Canvas",
          "label": "Back Cover"
        }
      ]
    },
    {
      "id": "http://example.org/iiif/book1/range/r1",
      "type": "Range",
      "label": "Introduction",
      "ranges": ["http://example.org/iiif/book1/range/r1-1"],
      "canvases": [
        "http://example.org/iiif/book1/canvas/p1",
        "http://example.org/iiif/book1/canvas/p2",
        "http://example.org/iiif/book1/canvas/p3#xywh=0,0,750,300"
      ]
    },
    {
      "id": "http://example.org/iiif/book1/range/r1-1",
      "type": "Range",
      "label": "Objectives and Scope",
      "canvases": ["http://example.org/iiif/book1/canvas/p2#xywh=0,0,500,500"]
    }
  ]
}
```

###  5.7. AnnotationCollection

AnnotationCollections represent groupings of AnnotationPages that should be managed as a single whole, regardless of which canvas they target, such as all of the annotations that make up a particular translation of the text of a book.  Without the layer construction, it would be impossible to determine which annotations belonged together across canvases. A client might then present a user interface that allows all of the annotations in a layer to be displayed or hidden according to the user's preference.

Layers _MUST_ have a URI, and it _SHOULD_ be an HTTP URI.  They _MUST_ have a `label` and _MAY_ have any of the other descriptive, linking or rights properties.

Each annotation list _MAY_ be part of one or more layers. If the annotation list is part of a layer, then this _MUST_ be recorded using the `within` relationship in the annotation list response.  It _MAY_ also be included in the reference to the annotation list in the manifest response.  In the manifest response, the description of the layer _MAY_ be omitted after the first use, and just the URI given as a string.  Clients should refer to the first description given, based on the URI.

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/list/l1",
  "type": "AnnotationList",
  "within": {
    "id": "http://example.org/iiif/book1/layer/transcription",
    "type": "Layer",
    "label": "Diplomatic Transcription"
  }
}
```

The layer _MAY_ be able to be dereferenced if it has an HTTP URI.  If a representation is available, it _MUST_ follow all of the requirements for JSON representations in this specification.  All of the properties of the layer _SHOULD_ be included in the representation.  

The annotation lists are referenced from the layer in an `otherContent` array, in the same way as they are referenced from a canvas.  The annotation lists _SHOULD_ be given as just URIs, but _MAY_ be objects with more information about them, such as in the [Canvas][canvas] example.

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/layer/transcription",
  "type": "Layer",
  "label": "Diplomatic Transcription",
  // Other properties here ...

  "otherContent": [
    "http://example.org/iiif/book1/list/l1",
    "http://example.org/iiif/book1/list/l2",
    "http://example.org/iiif/book1/list/l3",
    "http://example.org/iiif/book1/list/l4"
    // More AnnotationLists here ...
  ]
}
```


###  5.8. Collection

Collections are used to list the manifests available for viewing, and to describe the structures, hierarchies or curated collections that the physical objects are part of.  The collections _MAY_ include both other collections and manifests, in order to form a hierarchy of objects with manifests at the leaf nodes of the tree.  Collection objects _MAY_ be embedded inline within other collection objects, such as when the collection is used primarily to subdivide a larger one into more manageable pieces, however manifests _MUST NOT_ be embedded within collections. An embedded collection _SHOULD_ also have its own URI from which the description is available.

It is _RECOMMENDED_ that the topmost collection from which all other collections are discoverable by following links within the hierarchy be named `top`, if there is one.

Manifests or Collections _MAY_ appear within more than one collection. For example, an institution might define four collections: one for modern works, one for historical works, one for newspapers and one for books.  The manifest for a modern newspaper would then appear in both the modern collection and the newspaper collection.  Alternatively, the institution may choose to have two separate newspaper collections, and reference each as a sub-collection of modern and historical.

The intended usage of collections is to allow clients to:

  * Load a pre-defined set of manifests at initialization time.
  * Receive a set of manifests, such as search results, for rendering.
  * Visualize lists or hierarchies of related manifests.
  * Provide navigation through a list or hierarchy of available manifests.

As such, collections _MUST_ have a label, and _SHOULD_ have `metadata` and `description` properties to be displayed by the client such that the user can understand the structure they are interacting with.  If a collection does not have these properties, then a client is not required to render the collection to the user directly.

Collections have three list-based properties to express membership:

##### items
In cases where the order of a collection is significant, `members` can be used to interleave both collection and manifest resources. This is especially useful when a collection of books contains single- and multi-volume works (i.e. collections with the "multi-part" viewingHint), and when modeling archival material where original order is significant. Each entry in the `members` list _MUST_ be an object and _MUST_ include `id`, `type`, and `label`. If the entry is a collection, then `viewingHint` _MUST_ also be present.

At least one of `collections`, `manifests` and `members` _SHOULD_ be present in the response.  An empty collection, with no member resources, is allowed but discouraged.

An example collection document:

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/collection/top",
  "type": "Collection",
  "label": "Top Level Collection for Example Organization",
  "viewingHint": "top",
  "description": "Description of Collection",
  "attribution": "Provided by Example Organization",

  "collections": [
    {
      "id": "http://example.org/iiif/collection/sub1",
      "type": "Collection",
      "label": "Sub-Collection 1",

      "members": [  
        {
          "id": "http://example.org/iiif/collection/part1",
          "type": "Collection",
          "label": "My Multi-volume Set",
          "viewingHint": "multi-part"
        },
        {
          "id": "http://example.org/iiif/book1/manifest1",
          "type": "Manifest",
          "label": "My Book"
        },
        {
          "id": "http://example.org/iiif/collection/part2",
          "type": "Collection",
          "label": "My Sub Collection",
          "viewingHint": "individuals"
        }
      ]
    },
    {
      "id": "http://example.org/iiif/collection/part2",
      "type": "Collection",
      "label": "Sub Collection 2"
    }
  ],

  "manifests": [
    {
      "id": "http://example.org/iiif/book1/manifest",
      "type": "Manifest",
      "label": "Book 1"
    }
  ]
}
```

### 5.9. Paging

In some situations, annotation lists or the list of manifests in a collection may be very long or expensive to create. The latter case is especially likely to occur when responses are generated dynamically. In these situations the server may break up the response using [paging properties][paging]. The length of a response is left to the server's discretion, but the server should take care not to produce overly long responses that would be difficult for clients to process.

When breaking a response into pages, the paged resource _MUST_ link to the `first` page resource, and _MUST NOT_ include the corresponding list property (`collections` for a collection, `otherContent` for a layer). For example, a paged layer would link only to an annotation list as its first page.  If known, the resource _MAY_ also link to the last page.

The linked page resource _SHOULD_ refer back to the containing paged resource using `within`. If there is a page resource that follows it (the next page), then it _MUST_ include a `next` link to it.  If there is a preceding page resource, then it _SHOULD_ include a `prev` link to it.

The paged resource _MAY_ use the `total` property to list the total number of leaf resources that are contained within its pages.  This would be the total number of annotations in a layer, or the total number of manifests in a collection.  Conversely, the page resources _MAY_ include the `startIndex` property with index of the first resource in the page, counting from zero relative to the containing paged resource.

The linked page resources _MAY_ have different properties from the paged resource, including different rights and descriptive properties.  Clients _MUST_ take into account any requirements derived from these properties, such as displaying `logo` or `attribution`.

##### Example Paged Layer

A layer representing a long transcription with almost half a million annotations, perhaps where each annotation paints a single word on the canvas:

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/layer/transcription",
  "type": "Layer",
  "label": "Example Long Transcription",

  "total": 496923,
  "first": "http://example.org/iiif/book1/list/l1"
}
```

And the corresponding first annotation list:

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/list/l1",
  "type": "AnnotationList",

  "startIndex": 0,
  "within": "http://example.org/iiif/book1/layer/transcription",
  "next": "http://example.org/iiif/book1/list/l2",

  "resources": [
    // Annotations live here ...
  ]
}
```

Note that it is still expected that canvases will link directly to the annotation lists.  For example, a particular canvas might refer to the first two annotation lists within a layer:

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/canvas/c1",
  "type": "Canvas",

  "height": 1000,
  "width": 1000,
  "label": "Page 1",

  "otherContent": [
    "http://example.org/iiif/book1/list/l1",
    "http://example.org/iiif/book1/list/l2"
  ]
}
```

##### Example Paged Collection

An example large collection with some 9.3 million objects in it:

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/collection/top",
  "type": "Collection",
  "label": "Example Big Collection",

  "total": 9316290,
  "first": "http://example.org/iiif/collection/c1"
}
```

And the corresponding first page of manifests:

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/collection/c1",
  "type": "Collection",

  "within": "http://example.org/iiif/collection/top",
  "startIndex": 0,
  "next": "http://example.org/iiif/collection/c2",

  "manifests": [
    // Manifests live here ...
  ]
}
```

## 6. HTTP Requests and Responses

This section describes the _RECOMMENDED_ request and response interactions for the API. The REST and simple HATEOAS approach is followed where an interaction will retrieve a description of the resource, and additional calls may be made by following links obtained from within the description. All of the requests use the HTTP GET method; creation and update of resources is not covered by this specification.

###  6.1. Requests

Clients _MUST NOT_ construct resource URIs by themselves, instead they _MUST_ follow links from within retrieved descriptions.

In the situation where the JSON documents are maintained in a filesystem with no access to the web server's configuration, then including ".json" on the end of the URI is suggested to ensure that the correct content-type response header is sent to the client.

###  6.2. Responses

The format for all responses is JSON, and the following sections describe the structure to be returned.

The content-type of the response _MUST_ be either `application/json` (regular JSON),

``` none
Content-Type: application/json
```
{: .urltemplate}

or "application/ld+json" (JSON-LD) with the `profile` parameter given as the context document: `http://iiif.io/api/presentation/3/context.json`.

``` none
Content-Type: application/ld+json;profile="http://iiif.io/api/presentation/3/context.json"
```
{: .urltemplate}

If the client explicitly wants the JSON-LD content-type, then it _MUST_ specify this in an Accept header, otherwise the server _MUST_ return the regular JSON content-type.

The HTTP server _SHOULD_, if at all possible, send the Cross Origin Access Control header (often called "CORS") to allow clients to download the manifests via AJAX from remote sites. The header name is `Access-Control-Allow-Origin` and the value of the header _SHOULD_ be `*`.

``` none
Access-Control-Allow-Origin: *
```
{: .urltemplate}

Responses _SHOULD_ be compressed by the server as there are significant performance gains to be made for very repetitive data structures.

Recipes for enabling CORS and the conditional Content-type header are provided in the [Apache HTTP Server Implementation Notes][apache-notes].


## 7. Authentication

It may be necessary to restrict access to the descriptions made available via the Presentation API.  As the primary means of interaction with the descriptions is by web browsers using XmlHttpRequests across domains, there are some considerations regarding the most appropriate methods for authenticating users and authorizing their access.  The approach taken is described in the [Authentication][auth] specification, and requires requesting a token to add to the requests to identify the user.  This token might also be used for other requests defined by other APIs.

It is possible to include Image API service descriptions within the manifest, and within those it is also possible to include links to the Authentication API's services that are needed to interact with the image content. The first time an Authentication API service is included within a manifest, it _MUST_ be the complete description. Subsequent references _SHOULD_ be just the URL of the service, and clients are expected to look up the details from the full description by matching the URL.  Clients _MUST_ anticipate situations where the Authentication service description in the manifest is out of date: the source of truth is the Image Information document, or other system that references the Authentication API services.

## Appendices

### A. Summary of Metadata Requirements

| Field                      | Meaning     |
| -------------------------- | ----------- |
| ![required][icon-req]      | Required    |
| ![recommended][icon-recc]  | Recommended |
| ![optional][icon-opt]      | Optional    |
| ![not allowed][icon-na]    | Not Allowed |
{: .api-table}

__Descriptive and Rights Properties__

|                | label                  | metadata                     | description                 | thumbnail                   | attribution            | license                 | logo                     |
| -------------- | ---------------------- | ---------------------------- | --------------------------- | ----------------------------| ---------------------- | ----------------------- | ------------------------ |
| Collection     | ![required][icon-req]  | ![recommended][icon-recc]    | ![recommended][icon-recc]   | ![recommended][icon-recc]   | ![optional][icon-opt]  | ![optional][icon-opt]   | ![optional][icon-opt]    |
| Manifest       | ![required][icon-req]  | ![recommended][icon-recc]    | ![recommended][icon-recc]   | ![recommended][icon-recc]   | ![optional][icon-opt]  | ![optional][icon-opt]   | ![optional][icon-opt]    |
| Sequence       | ![optional][icon-opt]  | ![optional][icon-opt]        | ![optional][icon-opt]       | ![optional][icon-opt]       | ![optional][icon-opt]  | ![optional][icon-opt]   | ![optional][icon-opt]    |
| Canvas         | ![required][icon-req]  | ![optional][icon-opt]        | ![optional][icon-opt]       | ![recommended][icon-recc]   | ![optional][icon-opt]  | ![optional][icon-opt]   | ![optional][icon-opt]    |
| Annotation     | ![optional][icon-opt]  | ![optional][icon-opt]        | ![optional][icon-opt]       | ![optional][icon-opt]       | ![optional][icon-opt]  | ![optional][icon-opt]   | ![optional][icon-opt]    |
| AnnotationList | ![optional][icon-opt]  | ![optional][icon-opt]        | ![optional][icon-opt]       | ![optional][icon-opt]       | ![optional][icon-opt]  | ![optional][icon-opt]   | ![optional][icon-opt]    |
| Range          | ![required][icon-req]  | ![optional][icon-opt]        | ![optional][icon-opt]       | ![optional][icon-opt]       | ![optional][icon-opt]  | ![optional][icon-opt]   | ![optional][icon-opt]    |
| Layer          | ![required][icon-req]  | ![optional][icon-opt]        | ![optional][icon-opt]       | ![optional][icon-opt]       | ![optional][icon-opt]  | ![optional][icon-opt]   | ![optional][icon-opt]    |
| Image Content  | ![optional][icon-opt]  | ![optional][icon-opt]        | ![optional][icon-opt]       | ![optional][icon-opt]       | ![optional][icon-opt]  | ![optional][icon-opt]   | ![optional][icon-opt]    |
| Other Content  | ![optional][icon-opt]  | ![optional][icon-opt]        | ![optional][icon-opt]       | ![optional][icon-opt]       | ![optional][icon-opt]  | ![optional][icon-opt]   | ![optional][icon-opt]    |
{: .api-table}

__Technical Properties__

|                | id                       | type                 | format                  | height                    | width                     | viewingDirection        | viewingHint            | navDate                  |
| -------------- | ------------------------- | --------------------- | ----------------------- | ------------------------- | ------------------------- | ----------------------- | ---------------------- | ------------------------ |
| Collection     | ![required][icon-req]     | ![required][icon-req] | ![not allowed][icon-na] | ![not allowed][icon-na]   | ![not allowed][icon-na]   | ![not allowed][icon-na] | ![optional][icon-opt]  | ![optional][icon-opt]    |
| Manifest       | ![required][icon-req]     | ![required][icon-req] | ![not allowed][icon-na] | ![not allowed][icon-na]   | ![not allowed][icon-na]   | ![optional][icon-opt]   | ![optional][icon-opt]  | ![optional][icon-opt]    |
| Sequence       | ![optional][icon-opt]     | ![required][icon-req] | ![not allowed][icon-na] | ![not allowed][icon-na]   | ![not allowed][icon-na]   | ![optional][icon-opt]   | ![optional][icon-opt]  | ![not allowed][icon-na]  |
| Canvas         | ![required][icon-req]     | ![required][icon-req] | ![not allowed][icon-na] | ![required][icon-req]     | ![required][icon-req]     | ![not allowed][icon-na] | ![optional][icon-opt]  | ![not allowed][icon-na]  |
| Annotation     | ![recommended][icon-recc] | ![required][icon-req] | ![not allowed][icon-na] | ![not allowed][icon-na]   | ![not allowed][icon-na]   | ![not allowed][icon-na] | ![optional][icon-opt]  | ![not allowed][icon-na]  |
| AnnotationList | ![required][icon-req]     | ![required][icon-req] | ![not allowed][icon-na] | ![not allowed][icon-na]   | ![not allowed][icon-na]   | ![not allowed][icon-na] | ![optional][icon-opt]  | ![not allowed][icon-na]  |
| Range          | ![required][icon-req]     | ![required][icon-req] | ![not allowed][icon-na] | ![not allowed][icon-na]   | ![not allowed][icon-na]   | ![optional][icon-opt]   | ![optional][icon-opt]  | ![not allowed][icon-na]  |
| Layer          | ![required][icon-req]     | ![required][icon-req] | ![not allowed][icon-na] | ![not allowed][icon-na]   | ![not allowed][icon-na]   | ![optional][icon-opt]   | ![optional][icon-opt]  | ![not allowed][icon-na]  |
| Image Content  | ![required][icon-req]     | ![required][icon-req] | ![optional][icon-opt]   | ![recommended][icon-opt]  | ![recommended][icon-opt]  | ![not allowed][icon-na] | ![optional][icon-opt]  | ![not allowed][icon-na]  |
| Other Content  | ![required][icon-req]     | ![required][icon-req] | ![optional][icon-opt]   | ![optional][icon-opt]     | ![optional][icon-opt]     | ![not allowed][icon-na] | ![optional][icon-opt]  | ![not allowed][icon-na]  |
{: .api-table}

__Linking Properties__

|                | seeAlso                | service                | related                | rendering              | within                 | startCanvas             |
| -------------- | ---------------------- | ---------------------- | ---------------------- | ---------------------- | ---------------------- | ----------------------- |
| Collection     | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![not allowed][icon-na] |
| Manifest       | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![not allowed][icon-na] |
| Sequence       | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]   |
| Canvas         | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![not allowed][icon-na] |
| Annotation     | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![not allowed][icon-na] |
| AnnotationList | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![not allowed][icon-na] |
| Range          | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]   |
| Layer          | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![not allowed][icon-na] |
| Image Content  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![not allowed][icon-na] |
| Other Content  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![not allowed][icon-na] |
{: .api-table}

__Paging Properties__

|                | first                | last                | total                | next              | prev                 | startIndex             |
| -------------- | ---------------------- | ---------------------- | ---------------------- | ---------------------- | ---------------------- | ----------------------- |
| Collection     | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt] |
| Manifest       | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na] |
| Sequence       | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]   |
| Canvas         | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na] |
| Annotation     | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na] |
| AnnotationList | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt] |
| Range          | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]   |
| Layer          | ![optional][icon-opt]  | ![optional][icon-opt]  | ![optional][icon-opt]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na] |
| Image Content  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na] |
| Other Content  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na]  | ![not allowed][icon-na] |
{: .api-table}

__Structural Properties__

|                | collections             | manifests               | members                 | sequences               | structures              | canvases                | resources               | otherContent            | images                  | ranges                  |
| -------------- | ----------------------- | ----------------------- | ----------------------- | ----------------------- | ----------------------- | ----------------------- | ----------------------- | ----------------------- | ----------------------- | ----------------------- |
| Collection     | ![optional][icon-opt]   | ![optional][icon-opt]   | ![optional][icon-opt]   | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] |
| Manifest       | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![required][icon-req]   | ![optional][icon-opt]   | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] |
| Sequence       | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![required][icon-req]   | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] |
| Canvas         | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![optional][icon-opt]   | ![optional][icon-opt]   | ![not allowed][icon-na] |
| Annotation     | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] |
| AnnotationList | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![optional][icon-opt]   | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] |
| Range          | ![not allowed][icon-na] | ![not allowed][icon-na] | ![optional][icon-opt]   | ![not allowed][icon-na] | ![not allowed][icon-na] | ![optional][icon-opt]   | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![optional][icon-opt]   |
| Layer          | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![optional][icon-opt]   | ![not allowed][icon-na] | ![not allowed][icon-na] |
| Image Content  | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] |
| Other Content  | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] | ![not allowed][icon-na] |
{: .api-table}


__Protocol Behavior__

|                | id is dereferenceable |         
| -------------- | ---------------------- |
| Collection     | ![required][icon-req]  |
| Manifest       | ![required][icon-req]  |
| Sequence (first)   | ![optional][icon-opt]  |
| Sequence (second+) | ![required][icon-req]  |
| Canvas         | ![recommended][icon-recc]  |
| Annotation     | ![recommended][icon-recc]  |
| AnnotationList | ![required][icon-req]  |
| Range          | ![optional][icon-opt]  |
| Layer          | ![optional][icon-opt]  |
| Image Content  | ![required][icon-req]  |
| Other Content  | ![required][icon-req]  |
{: .api-table}

### B. Example Manifest Response

URL: _http://example.org/iiif/book1/manifest_

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "type": "Manifest",
  "id": "http://example.org/iiif/book1/manifest",

  "label": "Book 1",
  "metadata": [
    {"label": "Author", "value": "Anne Author"},
    {"label": "Published", "value": [
        {"@value": "Paris, circa 1400", "@language": "en"},
        {"@value": "Paris, environ 14eme siecle", "@language": "fr"}
        ]
    }
  ],
  "description": "A longer description of this example book. It should give some real information.",
  "navDate": "1856-01-01T00:00:00Z",

  "license": "http://example.org/license.html",
  "attribution": "Provided by Example Organization",
  "service": {
    "@context": "http://example.org/ns/jsonld/context.json",
    "id": "http://example.org/service/example",
    "profile": "http://example.org/docs/example-service.html"
  },
  "seeAlso":
    {
      "id": "http://example.org/library/catalog/book1.marc",
      "format": "application/marc",
      "profile": "http://example.org/profiles/marc21"
    },
  "rendering": {
    "id": "http://example.org/iiif/book1.pdf",
    "label": "Download as PDF",
    "format": "application/pdf"
  },
  "within": "http://example.org/collections/books/",

  "sequences": [
      {
        "id": "http://example.org/iiif/book1/sequence/normal",
        "type": "Sequence",
        "label": "Current Page Order",
        "viewingDirection": "left-to-right",
        "viewingHint": "paged",
        "canvases": [
          {
            "id": "http://example.org/iiif/book1/canvas/p1",
            "type": "Canvas",
            "label": "p. 1",
            "height":1000,
            "width":750,
            "images": [
              {
                "type": "Annotation",
                "motivation": "painting",
                "resource":{
                    "id": "http://example.org/iiif/book1/res/page1.jpg",
                    "type": "dctypes:Image",
                    "format": "image/jpeg",
                    "service": {
                        "@context": "http://iiif.io/api/image/{{ site.image_api.latest.major }}/context.json",
                        "id": "http://example.org/images/book1-page1",
                        "profile": "http://iiif.io/api/image/{{ site.image_api.latest.major }}/level1.json"
                    },
                    "height":2000,
                    "width":1500
                },
                "on": "http://example.org/iiif/book1/canvas/p1"
              }
            ],
            "otherContent": [
              {
                "id": "http://example.org/iiif/book1/list/p1",
                "type": "AnnotationList",
                "within": {
                    "id": "http://example.org/iiif/book1/layer/l1",
                    "type": "Layer",
                    "label": "Example Layer"
                }
              }
            ]
        },
          {
            "id": "http://example.org/iiif/book1/canvas/p2",
            "type": "Canvas",
            "label": "p. 2",
            "height":1000,
            "width":750,
            "images": [
              {
                "type": "Annotation",
                "motivation": "painting",
                "resource":{
                    "id": "http://example.org/images/book1-page2/full/1500,2000/0/default.jpg",
                    "type": "dctypes:Image",
                    "format": "image/jpeg",
                    "height":2000,
                    "width":1500,
                    "service": {
                        "@context": "http://iiif.io/api/image/{{ site.image_api.latest.major }}/context.json",
                        "id": "http://example.org/images/book1-page2",
                        "profile": "http://iiif.io/api/image/{{ site.image_api.latest.major }}/level1.json",
                        "height":8000,
                        "width":6000,
                        "tiles": [{"width": 512, "scaleFactors": [1,2,4,8,16]}]
                    }
                },
                "on": "http://example.org/iiif/book1/canvas/p2"
              }
            ],
            "otherContent": [
              {
                "id": "http://example.org/iiif/book1/list/p2",
                "type": "AnnotationList",
                "within": "http://example.org/iiif/book1/layer/l1"  
              }
            ]
          },
          {
            "id": "http://example.org/iiif/book1/canvas/p3",
            "type": "Canvas",
            "label": "p. 3",
            "height":1000,
            "width":750,
            "images": [
              {
                "type": "Annotation",
                "motivation": "painting",
                "resource":{
                    "id": "http://example.org/iiif/book1/res/page3.jpg",
                    "type": "dctypes:Image",
                    "format": "image/jpeg",
                    "service": {
                        "@context": "http://iiif.io/api/image/{{ site.image_api.latest.major }}/context.json",
                        "id": "http://example.org/images/book1-page3",
                        "profile": "http://iiif.io/api/image/{{ site.image_api.latest.major }}/level1.json"
          },
                    "height":2000,
                    "width":1500
                },
                "on": "http://example.org/iiif/book1/canvas/p3"
              }
            ],
            "otherContent": [
              {
                "id": "http://example.org/iiif/book1/list/p3",
                "type": "AnnotationList",
                "within": "http://example.org/iiif/book1/layer/l1"               
              }
            ]
          }
        ]
      }
    ],
  "structures": [
    {
      "id": "http://example.org/iiif/book1/range/r1",
        "type": "Range",
        "label": "Introduction",
        "canvases": [
          "http://example.org/iiif/book1/canvas/p1",
          "http://example.org/iiif/book1/canvas/p2",
          "http://example.org/iiif/book1/canvas/p3#xywh=0,0,750,300"
        ]
    }
  ]
}
```


### C. Implementation Notes

* It is _RECOMMENDED_ that if there is (at the time of implementation) a single image that depicts the page, then the dimensions of the image are used as the dimensions of the canvas for simplicity. If there are multiple full images, then the dimensions of the largest image should be used. If the largest image's dimensions are less than 1200 pixels on either edge, then the canvas's dimensions _SHOULD_ be double those of the image.

### D. Versioning

Starting with version 2.0, this specification follows [Semantic Versioning][semver]. See the note [Versioning of APIs][versioning] for details regarding how this is implemented.

### E. Acknowledgements

The production of this document was generously supported by a grant from the [Andrew W. Mellon Foundation][mellon].

Many thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### F. Change Log

| Date       | Description           |
| ---------- | --------------------- |
| 2016-05-12 | Version 2.1 (Hinty McHintface) [View change log][change-log] |
| 2014-09-11 | Version 2.0 (Triumphant Giraffe) [View change log][change-log-20] |
| 2013-08-26 | Version 1.0 (unnamed) |
| 2013-06-14 | Version 0.9 (unnamed) |

[iiif-discuss]: mailto:iiif-discuss@googlegroups.com "Email Discussion List"
[prezi3-milestone]: https://github.com/iiif/iiif.io/issues?q=is%3Aopen+is%3Aissue+milestone%3A%22Presentation+3.0%22 "Presentation 3.0 Milestone" 
[shared-canvas]: /model/shared-canvas/{{ site.shared_canvas.latest.major}}.{{ site.shared_canvas.latest.minor }} "Shared Canvas Data Model"
[image-api]: /api/image/{{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }}/ "Image API"
[search-api]: /api/search/{{ site.search_api.latest.major}}.{{ site.search_api.latest.minor }}/ "Search API"
[annex]: /api/annex/services/ "Services Annex Document"
[change-log]: /api/presentation/2.1/change-log/ "Presentation API 2.1 Change Log"
[change-log-20]: /api/presentation/2.0/change-log/ "Presentation API 2.0 Change Log"
[iiif-community]: /community/ "IIIF Community"
[apache-notes]: /api/annex/notes/apache/ "Apache HTTP Server Implementation Notes"
[openanno]: http://www.openannotation.org/spec/core/ "Open Annotation"
[openannotypes]: http://www.openannotation.org/spec/core/core.html#BodyTargetType
[openannomulti]: http://www.openannotation.org/spec/core/multiplicity.html#Choice
[linked-data]: http://linkeddata.org/ "Linked Data"
[web-arch]: http://www.w3.org/TR/webarch/ "Architecture of the World Wide Web"
[json-ld]: http://www.w3.org/TR/json-ld/ "JSON-LD"
[json-ld-68]: http://www.w3.org/TR/json-ld/#interpreting-json-as-json-ld "Interpreting JSON as JSON-LD"
[rfc5646]: http://tools.ietf.org/html/rfc5646 "RFC 5646"
[media-frags]: http://www.w3.org/TR/media-frags/#naming-space "Media Fragments"
[xpath]: http://en.wikipedia.org/wiki/XPointer "XPath / XPointer"
[svg]: http://www.w3.org/TR/SVG/ "Scalabe Vector Graphics"
[css]: http://www.w3.org/TR/CSS/ "Cascading Style Sheets"
[semver]: http://semver.org/spec/v2.0.0.html "Semantic Versioning 2.0.0"
[mellon]: http://www.mellon.org/ "The Andrew W. Mellon Foundation"
[json-ld-compact]: http://www.w3.org/TR/json-ld-api/#compaction-algorithms "JSON-LD Compaction Algorithms"
[versioning]: /api/annex/notes/semver/ "Versioning of APIs"
[use-case-doc]: /api/presentation/usecases/ "Presentation API Use Cases"
[annex-frames]: /api/annex/notes/jsonld/ "JSON-LD Frames Implementation Notes"
[iana-uri-schemes]: http://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml "IANA URI Schemes"
[rdf11-blank-nodes]: http://www.w3.org/TR/rdf11-concepts/#section-blank-nodes "RDF 1.1 Concepts"
[rfc-4122]: http://tools.ietf.org/html/rfc4122 "URN UUID Scheme"
[rfc-2119]: http://tools.ietf.org/html/rfc2119
[oa-ext-annex]: /api/annex/openannotation/ "Open Annotation Extensions"
[auth]: /api/auth/

[stable-version]: /api/presentation/{{ site.presentation_api.latest.major }}.{{ site.presentation_api.latest.minor }}/
[appendixa]: #a-summary-of-recommended-uri-patterns "Appendix A"
[appendixb]: #b-summary-of-metadata-requirements "Appendix B"
[prev-version]: /api/presentation/2.0/
[sequence]: #sequence
[canvas]: #canvas
[range]: #range
[image-resources]: #image-resources
[annotation-lists]: #annotation-list
[type-overview]: #resource-type-overview

[ld-exts]: #linked-data-context-and-extensions
[paging]: #paging-properties
[resource-structure]: #resource-structure

[icon-req]: /img/metadata-api/required.png "Required"
[icon-recc]: /img/metadata-api/recommended.png "Recommended"
[icon-opt]: /img/metadata-api/optional.png "Optional"
[icon-na]: /img/metadata-api/not_allowed.png "Not allowed"

{% include acronyms.md %}
