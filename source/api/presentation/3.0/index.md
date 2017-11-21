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

  * **[Michael Appleby](https://orcid.org/0000-0002-1266-298X)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-1266-298X), [_Yale University_](http://www.yale.edu/)
  * **[Tom Crane](https://orcid.org/0000-0003-1881-243X)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0003-1881-243X), [_Digirati_](http://digirati.com/)
  * **[Robert Sanderson](https://orcid.org/0000-0003-4441-6852)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0003-4441-6852), [_J. Paul Getty Trust_](http://www.getty.edu/)
  * **[Jon Stroop](https://orcid.org/0000-0002-0367-1243)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-0367-1243), [_Princeton University Library_](https://library.princeton.edu/)
  * **[Simeon Warner](https://orcid.org/0000-0002-7970-7855)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-7970-7855), [_Cornell University_](https://www.cornell.edu/)
  {: .names}

{% include copyright.md %}

__Status Warning__
This is a work in progress and may change without any notices. Implementers should be aware that this document is not stable. Implementers are likely to find the specification changing in incompatible ways. Those interested in implementing this document before it reaches beta or release stages should join the [mailing list][iiif-discuss] and take part in the discussions, and follow the [emerging issues][prezi3-milestone] on Github.
{: .warning}

----

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

##  1. Introduction

Access to image-based resources is fundamental to many research disciplines, scholarship and the transmission of cultural knowledge. Digital images are a container for much of the information content in the Web-based delivery of digitized cultural heritage objects. Collections of born-digital images can also benefit from a standardized method to structure their layout and presentation, such as slideshows, image carousels, web comics, and more.

This document describes how the structure and layout of a complex image-based object can be made available in a standard manner. Many different styles of viewer can be implemented that consume the information to enable a rich and dynamic experience, consuming content from across collections and hosting institutions.

An object may comprise a series of pages, surfaces or other views; for example the single view of a painting, the two sides of a photograph, four cardinal views of a statue, or the many pages of an edition of a newspaper or book. The primary requirements for the Presentation API are to provide an order for these views, the resources needed to display a representation of the view, and the descriptive information needed to allow the user to understand what is being seen.

The principles of [Linked Data][linked-data] and the [Architecture of the Web][web-arch] are adopted in order to provide a distributed and interoperable system. The [Shared Canvas data model][shared-canvas] and [JSON-LD][json-ld] are leveraged to create an easy-to-implement, JSON-based format.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]

### 1.1. Objectives and Scope

The objective of the IIIF (pronounced "Triple-Eye-Eff") Presentation API is to provide the information necessary to allow a rich, online viewing environment for primarily image-based objects to be presented to a human user, likely in conjunction with the [IIIF Image API][image-api]. This is the sole purpose of the API and therefore the descriptive information is given in a way that is intended for humans to read, but not semantically available to machines. In particular, it explicitly does __not__ aim to provide metadata that would drive discovery of the digitized objects.

The following are within the scope of the current document:

  * The display of digitized images associated with a particular physical object, or born-digital compound object.
  * Navigation between multiple views of the object.
  * The display of text, and resources of other media types, associated with the object views – this includes descriptive information about the object, labels that can aid navigation such as numbers associated with individual pages, copyright or attribution information, etc.

The following are __not__ within scope:

  * The discovery or selection of interesting digitized objects is not directly supported; however hooks to reference further resources are available.
  * Search within the object; which is described by the [IIIF Content Search API][search-api].

Note that in the following descriptions, "object" (or "physical object") is used to refer to a physical object that has been digitized or a born-digital compound object, and "resources" refer to the digital resources that are the result of that digitization or digital creation process.

###  1.2. Motivating Use Cases

There are many different types of digitized or digital compound objects, from ancient scrolls to modern newspapers, from medieval manuscripts to online comics, and from large maps to small photographs. Many of them bear texts, sometimes difficult to read either due to the decay of the physical object or lack of understanding of the script or language.  These use cases are described in a separate [document][use-case-doc].

Collectively the use cases require a model in which one can characterize the object (via the _Manifest_ resource), the order(s) in which individual views are presented (the _Sequence_ resource), and the individual views (_Canvas_ resources). Each Canvas may have images and/or other content resources associated with it (_Content_ resources) to allow the view to be rendered. An object may also have parts; for example, a book may have chapters where several pages may be associated with a single chapter (a _Range_ resource) and there may be groups of objects (_Collection_ resources).  These resource types, along with their properties, make up the IIIF Presentation API.

### 1.3. Terminology

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][rfc-2119].


##  2. Resource Type Overview

This section provides an overview of the resource types (or classes) that are used in the specification.  They are each presented in more detail in [Section 5][resource-structure-prezi30].

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

An ordered list of Manifests, and/or further Collections.  Collections allow easy navigation among the Manifests in a hierarchical structure, potentially each with its own descriptive information.

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

This specification defines properties in five distinct areas. Most of the properties may be associated with any of the resource types described above, and may have more than one value.  The property relates to the resource that it is associated with, so a `description` property on a Manifest is a description of the object, whereas a `description` property on a Canvas is a description of that particular view.

The requirements for which classes have which properties are summarized in [Appendix A][appendixa-prezi30].

Other properties are allowed, either via custom extensions or endorsed by IIIF. If a client discovers properties that it does not understand, then it _MUST_ ignore them.  Other properties _SHOULD_ consist of a prefix and a name in the form "`prefix:name`" to ensure it does not collide with a property defined by IIIF specifications.

###  3.1. Descriptive Properties

##### label
A human readable label, name or title for the resource. This property is intended to be displayed as a short, textual surrogate for the resource if a human needs to make a distinction between it and similar resources, for example between pages or between a choice of images to display.

The value of the property _MUST_ be a JSON object, as described in the [languages][languages-prezi30] section.

 * A Collection _MUST_ have at least one `label`.<br/>
   Clients _MUST_ render `label` on a Collection.
 * A Manifest _MUST_ have at least one `label`.<br/>
   Clients _MUST_ render `label` on a Manifest.
 * A Sequence  _MAY_ have one or more `label`s, and if there are multiple Sequences in a single Manifest then they _MUST_ each have at least one `label`.<br/>
   Clients _SHOULD_ support multiple Sequences, and if they do, _MUST_ render `label` on a Sequence. Clients _MAY_ render `label` on a single Sequence.
 * A Canvas _SHOULD_ have at least one `label`.<br/>
   Clients _MUST_ render `label` on a Canvas, and _MUST_ generate a `label` for Canvases that do not have them.
 * A content resource _MAY_ have one or more `label`s, and if there is a choice of content resource for the same Canvas, then they _SHOULD_ each have at least one `label`.<br/>
   Clients _MAY_ render `label` on content resources, and _MUST_ render them when part of a Choice.
 * A Range _SHOULD_ have at least one `label`. <br/>
   Clients _MUST_ render `label` on a Range.
 * An AnnotationCollection _MUST_ have at least one `label`.<br/>
   Clients _MUST_ render `label` on an AnnotationCollection.
 * Other resource types _MAY_ have `label`s.<br/>
   Clients _MAY_ render `label` on other resource types.

``` json-doc
{"label": {"en": ["Example Object Title"]}}
```

##### metadata
A list of descriptive entries, given as pairs of human readable `label` and `value` to be displayed to the user. There are no semantics conveyed by this information, only strings to present to the user.  A pair might be used to convey to the user information such as information about the creation of the object, a physical description, or ownership information, amongst other use cases.

The value of the `metadata` property _MUST_ be an array of objects, where each object has both `label` and `value` properties. The values of both `label` and `value` _MUST_ be JSON objects, as described in the [languages][languages-prezi30] section.

 * A Collection _SHOULD_ have one or more metadata pairs associated with it.<br/>
   Clients _MUST_ render `metadata` on a Collection.
 * A Manifest _SHOULD_ have one or more metadata pairs associated with it.<br/>
   Clients _MUST_ render `metadata` on a Manifest.
 * A Canvas _MAY_ have one or more metadata pairs associated with it.<br/>
   Clients _SHOULD_ render `metadata` on a Canvas.
 * Other resource types _MAY_ have one or more metadata pairs.<br/>
   Clients _MAY_ render `metadata` on other resource types.

Clients _SHOULD_ display the pairs in the order provided. Clients _SHOULD NOT_ use `metadata` for indexing and discovery purposes, as there are intentionally no consistent semantics. Clients _SHOULD_ expect to encounter long texts in the `value` field, and render them appropriately, such as with an expand button, or in a tabbed interface.

``` json-doc
{"metadata": [ {"label": {"en": ["Creator"]}, "value": {"en": ["Anne Artist (1776-1824)"]}} ]}
```

##### description
A short textual description or summary of the resource that the property is attached to, intended to be conveyed to the user when the `metadata` fields are not being displayed.

The value of the property _MUST_ be a JSON object, as described in the [languages][languages-prezi30] section.

 * A Collection _SHOULD_ have one or more `description`s.<br/>
   Clients _SHOULD_ render `description` on a Collection.
 * A Manifest _SHOULD_ have one or more `description`s.
   Clients _SHOULD_ render `description` on a Manifest.
 * A Canvas _MAY_ have one or more `description`s.<br/>
   Clients _SHOULD_ render `description` on a Canvas.
 * Other resource types _MAY_ have one or more `description`.<br/>
   Clients _MAY_ render `description` on other resource types.

``` json-doc
{"description": {"en": ["This is a summary of the object."]}}
```

##### thumbnail
A content resource that represents the IIIF resource, such as a small image or short audio clip.  It is _RECOMMENDED_ that a [IIIF Image API][image-api] service be available for images to enable manipulations such as resizing. The same resource _MAY_ have multiple thumbnails with the same or different `type` and `format`.

The value _MUST_ be a JSON array, with each item in the array being a JSON object that _MUST_ have an `id` property and _SHOULD_ have at least one of `type` and `format`.

 * A Collection _SHOULD_ have exactly one `thumbnail`, and _MAY_ have more than one.<br/>
   Clients _SHOULD_ render `thumbnail` on a Collection.
 * A Manifest _SHOULD_ have exactly one `thumbnail`, and _MAY_ have more than one.<br/>
   Clients _SHOULD_ render `thumbnail` on a Manifest.
 * A Sequence _MAY_ have one or more `thumbnail`s.<br/>
   Clients _SHOULD_ render `thumbnail` on a Sequence.
 * A Canvas _MAY_ have one or more `thumbnail`s and _SHOULD_ have at least one `thumbnail` if there are multiple resources that make up the representation.<br/>
   Clients _SHOULD_ render `thumbnail` on a Canvas.
 * A content resource _MAY_ have one or more `thumbnail`s and _SHOULD_ have at least one `thumbnail` if it is an option in a Choice of resources.<br/>
   Clients _SHOULD_ render `thumbnail` on a content resource.
 * Other resource types _MAY_ have one or more `thumbnail`s.<br/>
   Clients _MAY_ render `thumbnail` on other resource types.

``` json-doc
{"thumbnail": [{"id": "https://example.org/img/thumb.jpg", "type": "Image"}]}
```

##### navDate
A date that the client can use for navigation purposes when presenting the resource to the user in a time-based user interface, such as a calendar or timeline.  The value _MUST_ be an `xsd:dateTime` literal in UTC, expressed in the form "YYYY-MM-DDThh:mm:ssZ".  If the exact time is not known, then "00:00:00" _SHOULD_ be used. Similarly, the month or day _SHOULD_ be 01 if not known.  There _MUST_ be at most one `navDate` associated with any given resource.  More descriptive date ranges, intended for display directly to the user, _SHOULD_ be included in the `metadata` property for human consumption.  

 * A Collection or Manifest _MAY_ have exactly one navigation date associated with it.<br/>
   Clients _MAY_ render `navDate` on Collections or Manifests.
 * Other resource types _MUST NOT_ have navigation dates.<br/>
   Clients _SHOULD_ ignore `navDate` on other resource types.

``` json-doc
{"navDate": "2010-01-01T00:00:00Z"}
```

###  3.2. Rights and Licensing Properties

The following properties ensure that the interests of the owning or publishing institutions are conveyed regardless of the viewing environment. Given the wide variation of potential client user interfaces, it will not always be possible to display all or any of the properties to the user in the client's initial state. If initially hidden, the method of revealing them _MUST_ be obvious, such as a button or scroll bar.

##### attribution
Text that must be displayed when the resource it is associated with is displayed or used. For example, this could be used to present copyright or ownership statements, or simply an acknowledgement of the owning and/or publishing institution.

The value of the property _MUST_ be a JSON object, as described in the [languages][languages-prezi30] section.

 * Any resource type _MAY_ have one or more `attribution`s.<br/>
   Clients _MUST_ render `attribution` on every resource type.

``` json-doc
{"attribution": {"en": ["Provided courtesy of Example Institution"]}}
```

##### rights

A link to an external resource that describes the license or rights statement under which the resource may be used. The rationale for this being a URI and not a human readable label is that typically there is one license for many resources, and the text is too long to be displayed to the user along with the object. If displaying the text is a requirement, then it is _RECOMMENDED_ to include the information using the `attribution` property instead or in `metadata`.

The value _MUST_ be an array of JSON objects, each of which _MUST_ have an `id` and _SHOULD_ have at least one of `type` and `format`.

 * Any resource type _MAY_ have one or more rights statements or licenses associated with it.<br/>
   Clients _MUST_ render `rights` on every resource type.

``` json-doc
{"rights": [{"id": "http://example.org/rights/copyright.html", "type": "Text", "format": "text/html"}]}
```

##### logo
A small image that represents an individual or organization associated with the resource it is attached to.  This could be the logo of the owning or hosting institution. The logo _MUST_ be clearly rendered when the resource is displayed or used, without cropping, rotating or otherwise distorting the image. It is _RECOMMENDED_ that a [IIIF Image API][image-api] service be available for this image for other manipulations such as resizing.

The value _MUST_ be an array of JSON objects, each of which _MUST_ have an `id` and _SHOULD_ have at least one of `type` and `format`.

 * Any resource type _MAY_ have one or more `logo`s associated with it.<br/>
   Clients _MUST_ render `logo` on every resource type.

``` json-doc
{"logo": [{"id": "https://example.org/img/logo.jpg", "type": "Image"}]}
```

###  3.3. Technical Properties

##### id

The URI that identifies the resource. It is _RECOMMENDED_ that an HTTPS URI be used for all resources.

The value _MUST_ be a string.

 * A Collection _MUST_ have exactly one `id`, and it _MUST_ be the http(s) URI at which it is published.<br/>
   Clients _SHOULD_ render `id` on a Collection.
 * A Manifest _MUST_ have exactly one `id`, and it _MUST_ be the http(s) URI at which it is published.<br/>
   Clients _SHOULD_ render `id` on a Manifest.
 * A Sequence _MAY_ have an `id` and _MUST NOT_ have more than one.<br/>
   Clients _MAY_ render `id` on a Sequence.
 * A Canvas _MUST_ have exactly one `id`, and it _MUST_ be an http(s) URI.  The Canvas's JSON representation _MAY_ be published at that URI.<br/>
   Clients _SHOULD_ render `id` on a Canvas.
 * A content resource _MUST_ have exactly one `id`, and it _MUST_ be the http(s) URI at which the resource is published.<br/>
   Clients _MAY_ render `id` on content resources.
 * A Range _MUST_ have exactly one `id`, and it _MUST_ be an http(s) URI.<br/>
   Clients _MAY_ render `id` on a Range.
 * An AnnotationCollection _MUST_ have exactly one `id`, and it _MUST_ be an http(s) URI.<br/>
   Clients _MAY_ render `id` on an AnnotationCollection.
 * An AnnotationPage _MUST_ have exactly one `id`, and it _MUST_ be the http(s) URI at which it is published.<br/>
   Clients _MAY_ render `id` on an AnnotationPage.
 * An Annotation _MUST_ have exactly one `id`, and the Annotation's representation _SHOULD_ be published at that URI.<br/>
   Clients _MAY_ render `id` on an Annotation.

``` json-doc
{"id": "https://example.org/iiif/1/manifest"}
```

##### type

The type of the resource.  For the resource types defined by this specification, the value of `type` will be described in the sections below.  For content resources, the type are drawn from other vocabularies. Recommendations for basic types such as image, text or audio are also given in the sections below.

The value _MUST_ be a string.

 * All resource types _MUST_ have exactly one `type`.<br/>
   Clients _MUST_ process, and _MAY_ render, `type` on any resource type.

> | Class         | Description                      |
| ------------- | -------------------------------- |
| `Application` | Software intended to be executed |
| `Dataset`     | Data not intended to be rendered to humans directly |
| `Image`       | Two dimensional visual resources primarily intended to be seen |
| `Sound`       | Auditory resources primarily intended to be heard |
| `Text`        | Resources primarily intended to be read |
| `Video`       | Moving images, with or without accompanying audio |
{: .api-table #table-type}

``` json-doc
{"type": "Dataset"}
```

##### format
The specific media type (often called a MIME type) of a content resource, for example "image/jpeg". This is important for distinguishing text in XML from plain text, for example.

The value _MUST_ be a string.

 * A content resource _SHOULD_ have exactly one `format`, and if so, it _SHOULD_ be the value of the `Content-Type` header returned when the resource is dereferenced.<br/>
   Clients _MAY_ render the `format` of any content resource.
 * Other resource types _MUST NOT_ have a `format`.<br/>
   Clients _SHOULD_ ignore `format` on other resource types.

Note that this is different to the `formats` property in the [Image API][image-api], which gives the extension to use within that API.  It would be inappropriate to use in this case, as `format` can be used with any content resource, not just images.

``` json-doc
{"type": "Dataset", "format": "application/xml"}
```

##### profile

A schema or named set of functionality available from the resource.  The profile can further clarify the `type` and/or `format` of an external resource or service, allowing clients to customize their handling of the resource.

The value _MUST_ be a string, either taken from the table below or a URI.

* Services and resources referenced by `seeAlso` _SHOULD_ have exactly one `profile`.
  Clients _SHOULD_ process the `profile` of a service or external resource.
* Other resource types _MAY_ have exactly one `profile`.
  Clients _MAY_ process the `profile` of other resource types.

``` json-doc
{
  "type": "Dataset",
  "format": "application/xml",
  "profile": "info:srw/schema/1/mods-v3.3"
}
```

__Specification Management Warning:__
Should there really be a table in the specification? But otherwise how do we keep it up to date between versions?  If it's external, how do clients stay up to date? URIs are always okay... should it instead always be a URI?
{: .warning}

##### height
The height of a Canvas or content resource. For content resources, the value is in pixels. For Canvases, the value does not have a unit. In combination with the width, it conveys an aspect ratio for the space in which content resources are located.

The value _MUST_ be a non-negative integer or floating point number.

 * A Canvas _SHOULD_ have exactly one `height`, and _MUST NOT_ have more than one. If it has a `height`, it _MUST_ also have a `width`.<br/>
   Clients _MUST_ process, and _MAY_ render, `height` on a Canvas.
 * Content resources _MAY_ have exactly one `height`, given in pixels, if appropriate.<br/>
   Clients _SHOULD_ process, and _MAY_ render, `height` on content resources.
 * Other resource types _MUST NOT_ have a `height`.<br/>
   Clients _SHOULD_ ignore `height` on other resource types.

``` json-doc
{"height": 1800}
```

##### width
The width of a Canvas or content resource. For content resources, the value is in pixels. For Canvases, the value does not have a unit. In combination with the height, it conveys an aspect ratio for the space in which content resources are located.

The value _MUST_ be a non-negative integer or floating point number.

 * A Canvas _SHOULD_ have exactly one `width`, and _MUST NOT_ have more than one. If it has a `width`, it _MUST_ also have a `height`.<br/>
   Clients _MUST_ process, and _MAY_ render, `width` on a Canvas.
 * Content resources _MAY_ have exactly one `width`, given in pixels, if appropriate.<br/>
   Clients _SHOULD_ process, and _MAY_ render, `width` on content resources.
 * Other resource types _MUST NOT_ have a `width`.<br/>
   Clients _SHOULD_ ignore `width` on other resource types.

``` json-doc
{"width": 1200}
```

##### duration
The duration of a Canvas or content resource, given in seconds.  

The value _MUST_ be a non-negative floating point number.

 * A Canvas _MAY_ have exactly one `duration`, and _MUST NOT_ have more than one.<br/>
   Clients _MUST_ process, and _MAY_ render, `duration` on a Canvas.
 * Content resources _MAY_ have exactly one `duration`, and _MUST NOT_ have more than one.<br/>
   Clients _SHOULD_ process, and _MAY_ render, `duration` on content resources.
 * Other resource types _MUST NOT_ have a `duration`.<br/>
   Clients _SHOULD_ ignore `duration` on other resource types.

``` json-doc
{"duration": 125.0}
```

##### renderingDirection
The direction that a set of Canvases _SHOULD_ be displayed to the user. This specification defines four direction values in the table below. Others may be defined externally and given as a full URI.

The value _MUST_ be a string, taken from the table below or a full URI.

 * A Collection _MAY_ have exactly one `renderingDirection`, and if so, it applies to the order in which its members are rendered.<br/>
   Clients _SHOULD_ process `renderingDirection` on a Collection.
 * A Manifest _MAY_ have exactly one `renderingDirection`, and if so, it applies to all of its sequences unless the sequence specifies its own value.<br/>
   Clients _SHOULD_ process `renderingDirection` on a Manifest.
 * A Sequence _MAY_ have exactly one `renderingDirection`.<br/>
   Clients _SHOULD_ process `renderingDirection` on a Sequence.
 * A Range _MAY_ have exactly one `renderingDirection`.<br/>
   Clients _MAY_ process `renderingDirection` on a Range.
 * Other resource types _MUST NOT_ have a `renderingDirection`.<br/>
   Clients _SHOULD_ ignore `renderingDirection` on other resource types.

> | Value | Description |
| ----- | ----------- |
| `left-to-right` | The object is displayed from left to right. The default if not specified. |
| `right-to-left` | The object is displayed from right to left. |
| `top-to-bottom` | The object is displayed from the top to the bottom. |
| `bottom-to-top` | The object is displayed from the bottom to the top. |
{: .api-table #table-direction}

``` json-doc
{"renderingDirection": "left-to-right"}
```

##### renderingHint
A hint to the client as to the most appropriate method of displaying the resource. This specification defines the values specified in the table below. Others may be defined externally, and would be given as a full URI.

The value _MUST_ be an array of strings, taken from the table below or a full URI.

 * Any resource type _MAY_ have one or more `renderingHint`s.<br/>
   Clients _SHOULD_ process `renderingHint` on any resource where it is valid, unless otherwise stated in the table below (e.g. `non-paged`, `facing-pages`).

> | Value | Description |
| ----- | ----------- |
| `individuals` | Valid on Collection, Manifest, Sequence and Range. For Collections with this hint, each of the included Manifests are distinct objects. For Manifest, Sequence and Range, the included Canvases are distinct views, and _SHOULD NOT_ be presented in a page-turning interface. This is the default `renderingHint` if none are specified. |
| `paged` | Valid on Manifest, Sequence and Range. Canvases with this hint represent pages in a bound volume, and _SHOULD_ be presented in a page-turning interface if one is available.  The first canvas is a single view (the first recto) and thus the second canvas likely represents the back of the object in the first canvas. If this is not the case, see the `non-paged` hint. |
| `continuous` | Valid on Manifest, Sequence and Range.  A Canvas with this hint is a partial view and an appropriate rendering might display all of the Canvases virtually stitched together, such as a long scroll split into sections. This hint has no implication for audio resources. The `renderingDirection` of the Sequence or Manifest will determine the appropriate arrangement of the Canvases. |
| `multi-part` | Valid only for Collection. Collections with this hint consist of multiple Manifests that each form part of a logical whole, such as multi-volume books or a set of journal issues. Clients might render the Collection as a table of contents, rather than with thumbnails. |
| `non-paged` | Valid only for Canvas. Canvases with this hint _MUST NOT_ be presented in a page turning interface, and _MUST_ be skipped over when determining the page sequence. This hint _MUST_ be ignored if the current Sequence or Manifest does not have the 'paged' renderingHint. |
| `facing-pages` | Valid only for Canvas. Canvases with this hint, in a Sequence or Manifest with the "paged" `renderingHint`, _MUST_ be displayed by themselves, as they depict both parts of the opening.  If all of the Canvases are like this, then page turning is not possible, so simply use "individuals" instead. |
| `none` | Valid on AnnotationCollection, AnnotationPage, Annotation, SpecificResource and Choice. If this hint is provided, then the client _SHOULD NOT_ render the resource by default, but allow the user to turn it on and off.|
| `no-nav` | Valid only for Range. Ranges with this hint _MUST NOT_ be displayed to the user in a navigation hierarchy. This allows for Ranges to be present that capture unnamed regions with no interesting content. |
| `auto-advance` | Valid on Collection, Manifest, Sequence and Canvas. When the client reaches the end of a Canvas with a duration dimension that has (or is within a resource that has) this hint, it _SHOULD_ immediately proceed to the next Canvas and render it. If there is no subsequent Canvas in the current context, then this hint should be ignored. When applied to a Collection, the client should treat the first Canvas of the next Manifest as following the last Canvas of the previous Manifest, respecting any `startCanvas` specified.|
| `together` | Valid only for Collection. A client _SHOULD_ present all of the child Manifests to the user at once in a separate viewing area with its own controls. Clients _SHOULD_ catch attempts to create too many viewing areas. The `together` value _SHOULD NOT_ be interpreted as applying to the members any child resources.|
{: .api-table #table-behavior}

``` json-doc
{"renderingHint": ["auto-advance", "individuals"]}
```

##### timeMode

A mode associated with an Annotation that is to be applied to the rendering of any time-based media, or otherwise could be considered to have a duration, used as a body resource of that Annotation. Note that the association of `timeMode` with the Annotation means that different resources in the body cannot have different values. This specification defines the values specified in the table below. Others may be defined externally, and would be given as a full URI.

The value _MUST_ be a string, taken from the table below or a full URI.

* An Annotation _MAY_ have exactly one `timeMode` property.<br/>
  Clients _SHOULD_ process `timeMode` on an Annotation.

> | Value | Description |
| ----- | ----------- |
| `trim` | (default, if not supplied) If the content resource has a longer duration than the duration of portion of the Canvas it is associated with, then at the end of the Canvas's duration, the playback of the content resource _MUST_ also end. If the content resource has a shorter duration than the duration of the portion of the Canvas it is associated with, then, for video resources, the last frame _SHOULD_ persist on-screen until the end of the Canvas portion's duration. For example, a video of 120 seconds annotated to a Canvas with a duration of 100 seconds would play only the first 100 seconds and drop the last 20 second. |
| `scale` | Fit the duration of content resource to the duration of the portion of the Canvas it is associated with by scaling. For example, a video of 120 seconds annotated to a Canvas with a duration of 60 seconds would be played at double-speed. |
| `loop` | If the content resource is shorter than the `duration` of the Canvas, it _MUST_ be repeated to fill the entire duration. Resources longer than the `duration` _MUST_ be trimmed as described above. For example, if a 20 second duration audio stream is annotated onto a Canvas with duration 30 seconds, it will be played one and a half times. |
{: .api-table #table-timemode}

``` json-doc
{"timeMode": "trim"}
```

###  3.4. Linking Properties

#### 3.4.1 External Links

##### related
A link to an external resource that describes or is about the IIIF resource. The external resource _MUST_ be able to be displayed directly to the user. Examples might include a video or academic paper about the resource, a website, an HTML description, and so forth.

The value _MUST_ be an array of JSON objects. Each object _MUST_ have the `id`, `type` and `label` properties, and _SHOULD_ have a `format` property.

 * Any resource type _MAY_ have one or more external resources related to it.<br/>
   Clients _SHOULD_ render `related` on a Collection, Manifest or Canvas, and _MAY_ render `related` on other resource types.

``` json-doc
{"related": [{
  "id": "https://example.com/info/",
  "type": "Text",
  "label": "Related Web Page",
  "format": "text/html"}]}
```

##### rendering
A link to an external resource that is an alternative, non-IIIF representation of the IIIF resource. The external resource _MUST_ be able to be displayed directly to a human user, and _MUST NOT_ have a splash page or other interstitial resource that gates access to it. If access control is required, then the [IIIF Authentication API][auth] is _RECOMMENDED_. Examples might include the preferred viewing environment for the IIIF resource, such as a viewer page on the publisher's web site. Other uses include a rendering of a manifest as a PDF or EPUB with the images and text of the book, or a slide deck with images of the museum object.

The value _MUST_ be an array of JSON objects. Each object _MUST_ have the `id`, `type` and `label` properties, and _SHOULD_ have a `format` property.

 * Any resource type _MAY_ have one or more external rendering resources.<br/>
   Clients _SHOULD_ render `rendering` on a Collection, Manifest or Canvas, and _MAY_ render `rendering` on other resource types.

``` json-doc
{"rendering": [{
  "id": "https://example.org/1.pdf",
  "type": "Text",
  "label": "PDF Rendering of Book",
  "format": "application/pdf"}]}
```

##### service
A link to an external service that the client might interact with directly, such as from an image to the base URI of an associated [IIIF Image API][image-api] service. The service resource _SHOULD_ have additional information associated with it in order to allow the client to determine how to make appropriate use of it. Please see the [Service Profiles][annex] document for currently known service types.

The value _MUST_ be an array of JSON objects. Each object _MUST_ have the `id` and `type` properties, and _SHOULD_ have the `label` and `profile` properties.

 * Any resource type _MAY_ have one or more links to an external service.<br/>
   Clients _MAY_ process `service` on any resource type, and _SHOULD_ process the IIIF Image API service.

``` json-doc
{"service": [
  {"id": "https://example.org/service",
   "type": "Service",
   "profile": "http://example.org/docs/service"
  }]}
```

##### seeAlso
A link to a machine readable document that is related to the resource with the `seeAlso` property, such as an XML or RDF description. Properties of the document should be given to help the client select between multiple descriptions (if provided), and to make appropriate use of the document. If the relationship between the resource and the document needs to be more specific, then the document should include that relationship rather than the IIIF resource. Other IIIF resources, such as a related Manifest, are valid targets for `seeAlso`. The URI of the document _MUST_ identify a single representation of the data in a particular format. For example, if the same data exists in JSON and XML, then separate resources should be added for each representation, with distinct `id` and `format` properties.

The value _MUST_ be an array of JSON objects. Each object _MUST_ have the `id` and `type` properties, and _SHOULD_ have the `label`, `format` and `profile` properties.

 * Any resource type _MAY_ have one or more external documents related to it.<br/>
   Clients _MAY_ process `seeAlso` on any resource type.

``` json-doc
{"seeAlso" : [{
    "id": "http://example.org/library/catalog/book1.xml",
    "type": "Dataset",
    "format": "text/xml",
    "profile": "http://example.org/profiles/bibliographic"
  }]}
```

#### 3.4.2. Internal Links

##### within
A link to another resource that contains the current resource, such as a Manifest within a Collection.

The value _MUST_ be an array of JSON objects.  Each object _MUST_ have the `id` and `type` properties, and _SHOULD_ have the `label` property.

 * Collections or AnnotationPages that serve as [pages][paging-prezi30] _MUST_ be within exactly one paged resource.<br/>
   Clients _SHOULD_ render `within` on a Collection or AnnotationPage.
 * Other resource types, including Collections or AnnotationPages not serving as pages, _MAY_ be within one or more containing resources.<br/>
   Clients _MAY_ render `within` on other resource types.

``` json-doc
{"within": [{"id": "https://example.org/iiif/1", "type": "Manifest"}]}
```

##### startCanvas
A link from a Manifest, Sequence or Range to a Canvas that is contained within it. On seeing this relationship, a client _SHOULD_ advance to the specified Canvas when beginning navigation through the Sequence/Range.  This allows the client to begin with the first Canvas that contains interesting content rather than requiring the user to skip past blank or empty Canvases manually.  The Canvas _MUST_ be included in the first Sequence embedded within the Manifest.

The value _MUST_ be a JSON object, which _MUST_ have the `id` and `type` properties.

 * A Manifest, Sequence or Range _MAY_ have exactly one Canvas as its starting Canvas.
   Clients _SHOULD_ process `startCanvas` on a Manifest, Sequence or Range.
 * Other resource types _MUST NOT_ have a starting Canvas.
   Clients _SHOULD_ ignore `startCanvas` on other resource types.

``` json-doc
{"startCanvas": {"id": "https://example.org/iiif/1/canvas/1", "type": "Canvas"}}
```

##### includes
A link from a Range to an AnnotationCollection that includes the Annotations of content resources for that Range.  Clients might use this to present content to the user from a different Canvas when interacting with the Range, or to jump to the next part of the Range within the same Canvas.  

The value _MUST_ be a JSON object, which _MUST_ have the `id` and `type` properties, and the `type` _MUST_ be `AnnotationCollection`.

 * A Range _MAY_ have exactly one `includes` property.<br/>
   Clients _MAY_ process `includes` on a Range.
 * Other resource types _MUST NOT_ have the `includes` property.<br/>
   Clients _SHOULD_ ignore `includes` on other resource types.

``` json-doc
{"includes": {"id": "https://example.org/iiif/1/annos/1", "type": "AnnotationCollection"}}
```

###  3.5. Paging Properties

##### first
A link from a resource with pages, such as a Collection or AnnotationCollection, to its first page resource, another Collection or an AnnotationPage respectively.

The value _MUST_ be a JSON object, which _MUST_ have the `id` and `type` properties, and _SHOULD_ have the `label` property.

 * A Collection _MAY_ have exactly one Collection as its first page.<br/>
   Clients _SHOULD_ process, and _MAY_ render, `first` on a Collection.
 * An AnnotationCollection _MAY_ have exactly one AnnotationPage as its first page.<br/>
   Clients _SHOULD_ process, and _MAY_ render, `first` on an AnnotationCollection.
 * Other resource types _MUST NOT_ have a first page.<br/>
   Clients _SHOULD_ ignore `first` on other resource types.

``` json-doc
{"first": {"id": "https://example.org/iiif/1/annos/1", "type": "AnnotationPage"}}
```

##### last
A link from a resource with pages to its last page resource.

The value _MUST_ be a JSON object, which _MUST_ have the `id` and `type` properties, and _SHOULD_ have the `label` property.

 * A Collection _MAY_ have exactly one Collection as its last page.<br/>
   Clients _MAY_ render `last` on a Collection.
 * An AnnotationCollection _MAY_ have exactly one AnnotationPage as its last page.<br/>
   Clients _MAY_ render `last` on an AnnotationCollection.
 * Other resource types _MUST NOT_ have a last page.<br/>
   Clients _SHOULD_ ignore `last` on other resource types.

``` json-doc
{"last": {"id": "https://example.org/iiif/1/annos/23", "type": "AnnotationPage"}}
```

##### total
The total number of leaf resources in a paged list, such as the number of Annotations within an AnnotationCollection.

The value _MUST_ be a non-negative integer.

 * A Collection _MAY_ have exactly one total, which _MUST_ be the total number of Collections and Manifests in its list of pages.<br/>
   Clients _MAY_ render `total` on a Collection.
 * An AnnotationCollection _MAY_ have exactly one total, which _MUST_ be the total number of Annotations in its list of pages.<br/>
   Clients _MAY_ render `total` on an AnnotationCollection.
 * Other resource types _MUST NOT_ have a total.<br/>
   Clients _SHOULD_ ignore `total` on other resource types.

``` json-doc
{"total": 2217}
```

##### next
A link from a page resource to the next page resource that follows it in order.

The value _MUST_ be a JSON object, which _MUST_ have the `id` and `type` properties, and _SHOULD_ have the `label` property.

 * A Collection _MAY_ have exactly one Collection as its next page.<br/>
   Clients _SHOULD_ process, and _MAY_ render `next` on a Collection.
 * An AnnotationPage _MAY_ have exactly one AnnotationPage as its next page.<br/>
   Clients _SHOULD_ process, and _MAY_ render `next` on an AnnotationPage.
 * Other resource types _MUST NOT_ have next pages.<br/>
   Clients _SHOULD_ ignore `next` on other resource types.

``` json-doc
{"next": {"id": "https://example.org/iiif/1/annos/3", "type": "AnnotationPage"}}
```

##### prev
A link from a page resource to the previous page resource that precedes it in order.

The value _MUST_ be a JSON object, which _MUST_ have the `id` and `type` properties, and _SHOULD_ have the `label` property.

 * A Collection _MAY_ have exactly one Collection as its previous page.<br/>
   Clients _SHOULD_ process, and _MAY_ render `prev` on a Collection.
 * An AnnotationPage _MAY_ have exactly one AnnotationPage as its previous page.<br/>
   Clients _SHOULD_ process, and _MAY_ render `prev` on an AnnotationPage.
 * Other resource types _MUST NOT_ have previous pages.<br/>
   Clients _SHOULD_ ignore `prev` on other resource types.

``` json-doc
{"prev": {"id": "https://example.org/iiif/1/annos/2", "type": "AnnotationPage"}}
```

##### startIndex
The 0 based index of the first included resource in the current page, relative to the parent paged resource.

The value _MUST_ be a non-negative integer.

 * A Collection _MAY_ have exactly one `startIndex`, which _MUST_ be the index of its first Collection or Manifest relative to the order established by its parent paging Collection.<br/>
   Clients _MAY_ process or render `startIndex` on a Collection.
 * An AnnotationPage _MAY_ have exactly one `startIndex`, which _MUST_ be the index of its first Annotation relative to the order established by its parent paging AnnotationCollection.<br/>
   Clients _MAY_ process or render `startIndex` on an AnnotationPage.
 * Other resource types _MUST NOT_ have a `startIndex`.<br/>
   Clients _SHOULD_ ignore `startIndex` on other resource types.

``` json-doc
{"startIndex": 300}
```

### 3.6. Structural Properties

These properties define the structure of the object being represented in IIIF by allowing the inclusion of child resources within parents, such as a Canvas within a Sequence, or a Manifest within a Collection.  The majority of cases use `items`, however there are two special cases for different sorts of structures.

##### items

Much of the functionality of the IIIF Presentation API is simply recording the order in which child resources occur within a parent resource, such as Collections or Manifests within a parent Collection, Sequences within a Manifest, or Canvases within a Sequence.  All of these situations are covered with a single property, `items`.  

The value _MUST_ be an array of objects.

* A Collection _MUST_ have a list of zero or more Collections and/or Manifests in `items`.<br/>
  Clients _MUST_ process `items` on a Collection.
* A Manifest _MUST_ have a list of one or more Sequences in `items`.<br/>
  Clients _MUST_ process `items` on a Manifest.
* A Sequence _MUST_ have a list of one or more Canvases in `items`.<br/>
  Clients _MUST_ process `items` on a Sequence.
* A Canvas _SHOULD_ have a list of one or more AnnotationPages in `items`.<br/>
  Clients _MUST_ process `items` on a Canvas.
* An AnnotationPage _MUST_ have a list of zero or more Annotations in `items`.<br/>
  Clients _MUST_ process `items` on an AnnotationPage.
* A Range _MUST_ have a list of one or more Ranges and/or Canvases in `items`.<br/>
  Clients _SHOULD_ process `items` on a Range.


```json-doc
{"items": [{ ... }]}
```

##### structures

The structure of an object represented as a Manifest can be described using a hierarchy of Ranges. Ranges can be used to describe the "table of contents" of the object or other structures that the user can interact with beyond a simple linear progression described in the Sequence. The hierarchy is built by nesting the child Range resources in the `items` array of the higher level Range. The top level Ranges of these hierarchies are given in the `structures` property. 

The value _MUST_ be an array of objects.

* A Manifest _MAY_ have a list of one or more Ranges in `structures`.<br/>
  Clients _SHOULD_ process `structures` on a Manifest. The first hierarchy _SHOULD_ be presented to the user by default, and further hierarchies _SHOULD_ be able to be selected as alternative structures by the user.

```json-doc
{"structures": [
  {
    "id": "http://example.org/iiif/range/1",
    "type": "Range",
    "items": [{ ... }]
  }
]}
```

##### annotations

The value _MUST_ be an array of objects. Each object _MUST_ have at least the `id` and `type` properties.

* Any resource type Canvas _SHOULD_ have a list of one or more AnnotationPages in `content`.<br/>
  Clients _MUST_ process `content` on a Canvas.

```json-doc
{"annotations": [
  {
    "id": "http://example.org/iiif/annotationPage/1",
    "type": "AnnotationPage",
    "items": [{ ... }]
  }
]}
```

##  4. JSON-LD Considerations

This section describes features applicable to all of the Presentation API content.  For the most part, these are features of the JSON-LD specification that have particular uses within the API and recommendations about URIs to use.

### 4.1. HTTPS URI Scheme

It is strongly _RECOMMENDED_ that all URIs use the HTTPS scheme, and be available via that protocol.  All URIs _MUST_ be either HTTPS or HTTP, described more simply as "http(s)".

### 4.2. URI Representation

Resource descriptions _SHOULD_ be embedded within higher-level descriptions, and _MAY_ also be available via separate requests from http(s) URIs linked in the responses. These URIs are in the `id` property for the resource. Links to resources _MUST_ be given as a JSON object with the `id` property and at least one other property, typically either `type`, `format` or `profile` to give a hint as to what sort of resource is being referred to. Other URI schemes _MAY_ be used if the resource is not able to be retrieved via HTTP.

``` json-doc
{
  "thumbnail": [
    {"id": "http://example.org/images/thumb1.jpg", "type": "Image"}
  ]
}
```

### 4.3. Repeatable Properties

Any of the properties in the API that can have multiple values _MUST_ always be given as an array of values, even if there is only a single item in that array.

``` json-doc
{
  "seeAlso": [
    {"id": "http://example.org/images/thumb1.jpg", "type": "Image"},
    {"id": "http://example.org/videos/thumb1.pmg", "type": "Video"}   
  ]
}
```

### 4.4. Language of Property Values

Language _MAY_ be associated with strings that are intended to be displayed to the user for the `label`, `description`, `attribution` fields, plus the `label` and `value` fields of the `metadata` construction.

The values of these fields _MUST_ be JSON objects, with the keys being the [RFC 5646][rfc5646] language code for the language, or if the language is either not known or the string does not have a language, then the key must be `"@none"`. The associated values _MUST_ be arrays of strings, where each string is the content in the given language.

``` json-doc
{"label": {
    "en": ["Whistler's Mother",
           "Arrangement in Grey and Black No. 1: The Artist's Mother"],
    "fr": ["Arrangement en gris et noir no 1",
           "Portrait de la mère de l'artiste",
           "La Mère de Whistler"],
    "@none": ["Whistler (1871)"]
  }
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

Minimal HTML markup _MAY_ be included in the `description`, `attribution` properties and the `value` property of a `label`/`value` pair in `metadata`.  It _MUST NOT_ be used in `label` or other properties. This is included to allow manifest creators to add links and simple formatting instructions to blocks of text. The content _MUST_ be well-formed XML and therefore must be wrapped in an element such as `p` or `span`.  There _MUST NOT_ be whitespace on either side of the HTML string, and thus the first character in the string _MUST_ be a '<' character and the last character _MUST_ be '>', allowing a consuming application to test whether the value is HTML or plain text using these.  To avoid a non-HTML string matching this, it is _RECOMMENDED_ that an additional whitespace character be added to the end of the value in situations where plain text happens to start and end this way.

In order to avoid HTML or script injection attacks, clients _MUST_ remove:

  * Tags such as `script`, `style`, `object`, `form`, `input` and similar.
  * All attributes other than `href` on the `a` tag, `src` and `alt` on the `img` tag.
  * CData sections.
  * XML Comments.
  * Processing instructions.

Clients _SHOULD_ allow only `a`, `b`, `br`, `i`, `img`, `p`, `small`, `span`, `sub` and `sup` tags. Clients _MAY_ choose to remove any and all tags, therefore it _SHOULD NOT_ be assumed that the formatting will always be rendered.

``` json-doc
{"description": {"en-latn": ["<p>Short summary <b>description</b></p>"]}}
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

The JSON representation _MUST NOT_ include the `@graph` key at the top level. This key might be created when serializing directly from RDF data using the JSON-LD compaction algorithm. Instead, JSON-LD framing and/or custom code should be used to ensure the structure of the document is as described by this specification.

Embedded JSON-LD data that uses a JSON-LD version 1.0 context definition, such as references to older external services or extensions, _MAY_ require the context to be included within the service description, rather than listed in the top resource.  Care should be taken to use the mappings defined by those contexts, especially with regard to `id` versus `@id`, and `type` versus `@type`, to ensure that clients receive the keys that they are expecting to process.

##  5. Resource Structure

This section provides detailed description of the resource types used in this specification. [Section 2][type-overview-prezi30] provides an overview of the resource types and figures illustrating allowed relationships between them, and [Appendix A][appendixa-prezi30] provides summary tables of the property requirements.

###  5.1. Manifest

The Manifest resource typically represents a single object and any intellectual work or works embodied within that object. In particular it includes the descriptive, rights and linking information for the object. It then embeds the Sequence(s) of Canvases that should be rendered to the user. The Manifest response contains sufficient information for the client to initialize itself and begin to display something quickly to the user.

The identifier in `id` _MUST_ be able to be dereferenced to retrieve the JSON description of the Manifest, and thus _MUST_ use the http(s) URI scheme.

Along with the descriptive information, there is an `items` section, which is a list of JSON-LD objects. Each object describes a [Sequence][sequence-prezi30], discussed in the next section, that represents the order of the parts of the work, each represented by a [Canvas][canvas-prezi30].  There _MUST_ be at least one Sequence, and the first Sequence _MUST_ be included within the Manifest as well as optionally being available from its own URI. Subsequent Sequences _MAY_ be embedded within the Manifest, or referenced with their identifier (`id`), class (`type`) and label (`label`).

There _MAY_ also be a `structures` section listing one or more [Ranges][range-prezi30] which describe additional structure of the content, such as might be rendered as a table of contents.

Finally, the Manifest _MAY_ have an `annotations` list, which includes AnnotationPage resources where the Annotations are have the Manifest as their `target`.  These will typically be comment style annotations, and _MUST NOT_ have `painting` as their `motivation`. The `annotations` property may also be found on any other resource type with these same restrictions.

The example below includes only the Manifest-level information, however actual implementations _MUST_ embed at least the first Sequence, Canvas and content information.

``` json-doc
{
  // Metadata about this manifest file
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
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
  "description": {"en": ["Book 1, written be Anne Author, published in Paris around 1400."]},

  "thumbnail": [{
    "id": "http://example.org/images/book1-page1/full/80,100/0/default.jpg",
    "type": "Image",
    "service": {
      "id": "http://example.org/images/book1-page1",
      "type": "ImageService3",
      "profile": "level1"
    }
  }],

  // Presentation Information
  "renderingDirection": "right-to-left",
  "renderingHint": ["paged"],
  "navDate": "1856-01-01T00:00:00Z",

  // Rights Information
  "rights": [{
    "id":"http://example.org/license.html",
    "type": "Text",
    "language": "en",
    "format": "text/html"}],
  "attribution": {"en": ["Provided by Example Organization"]},
  "logo": {
    "id": "http://example.org/logos/institution1.jpg",
    "service": {
        "id": "http://example.org/service/inst1",
        "type": "ImageService3",
        "profile": "level2"
    }
  },

  // Links
  "related": [{
    "id": "http://example.org/videos/video-book1.mpg",
    "type": "Video",
    "label": {"en":["Video discussing this book"]},
    "format": "video/mpeg"
  }],
  "service": [{
    "id": "http://example.org/service/example",
    "type": "Service",
    "profile": "http://example.org/docs/example-service.html"
  }],
  "seeAlso": [{
    "id": "http://example.org/library/catalog/book1.xml",
    "type": "Dataset",
    "format": "text/xml",
    "profile": "http://example.org/profiles/bibliographic"
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
  "startCanvas": {
    "id": "http://example.org/iiif/book1/canvas/p2",
    "type": "Canvas"
  },

  // List of Sequences
  "items": [
      {
        "id": "http://example.org/iiif/book1/sequence/normal",
        "type": "Sequence",
        "label": {"en": ["Current Page Order"]}
        // Sequence's page order should be included here
      }
      // Any additional Sequences can be included or linked here
  ],

  // structure of the resource, described with Ranges
  "structure": [
    {
      "id": "http://example.org/iiif/book1/range/top",
      "type": "Range"
      // Ranges members should be included here
    }
    // Any additional top level Ranges can be included here
  ],

  // Commentary Annotations on the Manifest
  "annotations": [
    {
      "id": "http://example.org/iiif/book1/annotations/p1",
      "type": "AnnotationPage",
      "items": [
        // Annotations about the Manifest are included here
      ]
    }
  ]
}
```

###  5.2. Sequence

The Sequence conveys the ordering of the views of the object. The default Sequence (and typically the only Sequence) _MUST_ be embedded within the Manifest as the first object in the `items` property, and _MAY_ also be available from its own URI.  This Sequence _SHOULD_ have a URI to identify it. Any additional Sequences _MAY_ be included, or referenced externally from the Manifest.  All external Sequences _MUST_ have an http(s) URI, and the description of the Sequence _MUST_ be available by dereferencing that URI.

Sequences _MAY_ have their own descriptive, rights and linking metadata using the same fields as for Manifests. The `label` property _MAY_ be given for Sequences and _MUST_ be given if there is more than one referenced from a Manifest. After the metadata, the set of views of the object, represented by Canvas resources, _MUST_ be listed in order in the `items` property.  There _MUST_ be at least one Canvas given.

``` json-doc
{
  // Metadata about this sequence
  "id": "http://example.org/iiif/book1/sequence/normal",
  "type": "Sequence",
  "label": {"en": ["Current Page Order"]},

  "renderingDirection": "left-to-right",
  "renderingHint": ["paged"],
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

The Canvas represents an individual page or view and acts as a central point for laying out the different content resources that make up the display. Canvases _MUST_ be identified by a URI and it _MUST_ be an http(s) URI. The URI of the canvas _MUST NOT_ contain a fragment (a `#` followed by further characters), as this would make it impossible to refer to a segment of the Canvas's area using the `#xywh=` syntax. Canvases _MAY_ be able to be dereferenced separately from the Manifest via their URIs as well as being embedded within the Sequence.

Every Canvas _SHOULD_ have a `label` to display. If one is not provided, the client _SHOULD_ automatically generate one for use based on the Canvas's position within the current Sequence.

A Canvas _MUST_ have a rectangular aspect ratio (described with the `height` and `width` properties) and/or a `duration` to provide an extent in time. These dimensions allow resources to be associated with specific regions of the Canvas, within the space and/or time extents provided. Content _MUST NOT_ be associated with space or time outside of the Canvas's dimensions, such as at coordinates below 0,0, greater than the height or width, before 0 seconds, or after the duration.

Renderers _MUST_ scale content into the space represented by the Canvas, and _SHOULD_ follow any `timeMode` adjustment provided for time-based media.  If the Canvas represents a view of a physical object, the spatial dimensions of the Canvas _SHOULD_ be the same scale as that physical object, and images _SHOULD_ depict only the object.

Content resources are associated with the Canvas via Web Annotations. The Annotations are recorded in the `items` of one or more AnnotationPages, refered to in the `content` array of the Canvas. If the Annotation should be rendered quickly, in the view of the publisher, then it _SHOULD_ be embedded within the Manifest directly.  Other AnnotationPages can be referenced with just their `id`, `type` and optionally a `label`, and clients _SHOULD_ dereference these pages to discover further content.  Content in this case includes media assets such as images, video and audio, textual transcriptions or editions of the Canvas, as well as commentary about the object represented by the Canvas.  These different uses _MAY_ be split up across different AnnotationPages.


``` json-doc
{
  // Metadata about this canvas
  "id": "http://example.org/iiif/book1/canvas/p1",
  "type": "Canvas",
  "label": {"@none": ["p. 1"]},
  "height": 1000,
  "width": 750,
  "duration": 180.0,

  "items": [
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

These Annotations are collected together in AnnotationPage resources, which are included in the `items` list from the Canvas.  Each AnnotationPage can be embedded in its entirety, if the Annotations should be processed as soon as possible when the user navigates to that Canvas, or a reference to an external resource via `id`, `type`, and optionally `label`. All of the Annotations in the AnnotationPage _SHOULD_ have the Canvas as their `target`.  Embedded AnnotationPages _SHOULD_ be processed by the client first, before externally referenced pages.

The AnnotationPage _MUST_ have an http(s) URI given in `id`, and the JSON representation _MUST_ be returned when that URI is dereferenced.  They _MAY_ have any of the other fields defined in this specification, or the Web Annotation specification.  The Annotations are listed in an `items` list of the AnnotationPage.

``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ],
  "id": "http://example.org/iiif/book1/list/p1",
  "type": "AnnotationPage",

  "items": [
    {
      "id": "http://example.org/iiif/book1/list/p1/a1",
      "type": "Annotation"
      // ...
    },
    {
      "id": "http://example.org/iiif/book1/list/p1/a2",
      "type": "Annotation"
      // ...
    }
  ]
}
```

### 5.5. Annotations

Annotations follow the [Web Annotation][webanno] data model.  The description provided here is a summary plus any IIIF specific requirements. It must be noted that the W3C standard is the official documentation.

Annotations _MUST_ have their own http(s) URIs, conveyed in the `id` property. The JSON-LD description of the Annotation _SHOULD_ be returned if the URI is dereferenced, according to the [Web Annotation Protocol][webannoprotocol].

Annotations that associate content that is part of the representation of the view _MUST_ have the `motivation` field and the value _MUST_ be "painting". This is in order to distinguish it from commentary style Annotations. Text may be thus either be associated with the Canvas via a "painting" annotation, meaning the content is part of the representation, or with another `motivation`, meaning that it is somehow about the view.

The content resource is linked in the `body` of the Annotation. The content resource _MUST_ have an `id` field, with the value being the URI at which it can be obtained. If a IIIF Image service is available for an image, then the URI _MUST_ be the complete URI to a particular size of the image content, such as `http://example.org/image1/full/1000,/0/default.jpg`. It _MUST_ have a `type` of "Image". Its media type _MAY_ be listed in `format`, and its height and width _MAY_ be given as integer values for `height` and `width` respectively. The image then _SHOULD_ have the service referenced from it.

Although it might seem redundant, the URI of the Canvas _MUST_ be repeated in the `target` field of the Annotation. This is to ensure consistency with Annotations that target only part of the resource, described in more detail below, and to remain faithful to the Web Annotation specification, where `target` is mandatory.

The type of the content resource _MUST_ be included, and _SHOULD_ be taken from the table listed under the definition of `type`. The format of the resource _SHOULD_ be included and, if so, _SHOULD_ be the media type that is returned when the resource is dereferenced. The content resources _MAY_ also have any of the other fields defined in this specification, including commonly `label`, `description`, `metadata`, `license` and `attribution`.

Additional features of the [Web Annotation][webanno] data model _MAY_ also be used, such as selecting a segment of the Canvas or content resource, or embedding the comment or transcription within the Annotation. The use of these advanced features sometimes results in situations where the `target` is not a content resource, but instead a `SpecificResource`, a `Choice`, or other non-content object. Implementations should check the `type` of the resource and not assume that it is always content to be rendered.


``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ],
  "id": "http://example.org/iiif/book1/annotation/p0001-image",
  "type": "Annotation",
  "motivation": "painting",
  "body": {
    "id": "http://example.org/iiif/book1/res/page1.jpg",
    "type": "Image",
    "format": "image/jpeg",
    "service": {
      "id": "http://example.org/images/book1-page1",
      "type": "ImageService3",
      "profile": "level2"
    },
    "height":2000,
    "width":1500
  },
  "target": "http://example.org/iiif/book1/canvas/p1"
}
```

###  5.6. Range

Ranges are used to describe additional structure within an object, such as newspaper articles that span pages or chapters within a book. Ranges can include Canvases, parts of Canvases, or other Ranges, creating a nested tree structure such as a table of contents.

The intent of adding a Range to the Manifest is to allow the client to display a hierarchical navigation interface to enable the user to quickly move through the object's content. Clients _SHOULD_ present only Ranges with the `label` property and without the "no-nav" `renderingHint` to the user. Clients _SHOULD NOT_ render Canvas labels as part of the navigation, and a Range that wraps the Canvas _MUST_ be created if this is the desired presentation.

Ranges _MUST_ have URIs and they _SHOULD_ be http(s) URIs.  Ranges are embedded or referenced within the Manifest in a `structures` property. Ranges then embed or reference other Ranges, Canvases or parts of Canvases in the `items` field.  Each entry in the `items` field _MUST_ be a JSON object, and it _MUST_ have the `id` and `type` properties.

All of the Canvases or parts that should be considered as being part of a Range _MUST_ be included within the Range's members, or a descendant Range's members.

The Canvases and parts of Canvases may or may not be contiguous or in the same order as any Sequence.  Examples include newspaper articles that are continued in different sections, or simply a chapter that starts half way through a page. Parts of Canvases _MUST_ be rectangular and are described using the `xywh=` fragment approach.

Ranges _MAY_ link to an AnnotationCollection that has the content of the Range using the `includes` property. The referenced AnnotationCollection will contain Annotations that target areas of Canvases within the Range, and provide the content resources.


``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ],
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
      "items": [
        {
          "id": "http://example.org/iiif/book1/canvas/cover",
          "type": "Canvas"
        },
        {
          "id": "http://example.org/iiif/book1/range/r1",
          "type": "Range",
          "label": "Introduction",
          "includes": "http://example.org/iiif/book1/layer/introTexts",
          "items": [
            {
              "id": "http://example.org/iiif/book1/canvas/p1",
              "type": "Canvas"
            },
            {
              "id": "http://example.org/iiif/book1/canvas/p2",
              "type": "Canvas"
            },
            {
              "id": "http://example.org/iiif/book1/canvas/p3#xywh=0,0,750,300",
              "type": "Canvas"
            }  
          ]
        },
        {
          "id": "http://example.org/iiif/book1/canvas/backCover",
          "type": "Canvas"
        }
      ]
    }
  ]
}
```

###  5.7. AnnotationCollection

AnnotationCollections represent groupings of AnnotationPages that should be managed as a single whole, regardless of which Canvas or resource they target. This allows, for example, all of the Annotations that make up a particular translation of the text of a book to be collected together. A client might then present a user interface that allows all of the Annotations in an AnnotationCollection to be displayed or hidden according to the user's preference.

AnnotationCollections _MUST_ have a URI, and it _SHOULD_ be an HTTP URI.  They _MUST_ have a `label` and _MAY_ have any of the other descriptive, linking or rights properties.


``` json-doc
{
  "@context": [],
  "id": "http://example.org/iiif/book1/list/l1",
  "type": "AnnotationPage",
  "partOf": {
    "id": "http://example.org/iiif/book1/annocolls/transcription",
    "type": "AnnotationCollection",
    "label": {"en": ["Diplomatic Transcription"]}
  }
}
```

// ...

``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ],
  "id": "http://example.org/iiif/book1/annocolls/transcription",
  "type": "AnnotationCollection",
  "label": {"en": ["Diplomatic Transcription"]},

  "first": {"id": "http://example.org/iiif/book1/list/l1", "type": "AnnotationPage"},
  "last": {"id": "http://example.org/iiif/book1/list/l120", "type": "AnnotationPage"}
}
```


###  5.8. Collection

Collections are used to list the manifests available for viewing, and to describe the structures, hierarchies or curated collections that the objects are part of.  Collections _MAY_ include both other Collections and Manifests, in order to form a tree-structured hierarchy.  

Collection objects _MAY_ be embedded inline within other collection objects, such as when the collection is used primarily to subdivide a larger one into more manageable pieces, however manifests _MUST NOT_ be embedded within collections. An embedded collection _SHOULD_ also have its own URI from which the description is available.

Manifests or Collections _MAY_ appear within more than one collection. For example, an institution might define four collections: one for modern works, one for historical works, one for newspapers and one for books.  The manifest for a modern newspaper would then appear in both the modern collection and the newspaper collection.  Alternatively, the institution may choose to have two separate newspaper collections, and reference each as a sub-collection of modern and historical.

The intended usage of collections is to allow clients to:

  * Load a pre-defined set of manifests at initialization time.
  * Receive a set of manifests, such as search results, for rendering.
  * Visualize lists or hierarchies of related manifests.
  * Provide navigation through a list or hierarchy of available manifests.


An empty collection, with no member resources, is allowed but discouraged.

An example collection document:

``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ],
  "id": "http://example.org/iiif/collection/top",
  "type": "Collection",
  "label": "Top Level Collection for Example Organization",
  "renderingHint": "top",
  "description": "Description of Collection",
  "attribution": "Provided by Example Organization",

  "items": []

}
```

### 5.9. Paging

In some situations, annotation lists or the list of manifests in a collection may be very long or expensive to create. The latter case is especially likely to occur when responses are generated dynamically. In these situations the server may break up the response using [paging properties][paging-prezi30]. The length of a response is left to the server's discretion, but the server should take care not to produce overly long responses that would be difficult for clients to process.

When breaking a response into pages, the paged resource _MUST_ link to the `first` page resource, and _MUST NOT_ include the `items` property.

The linked page resource _SHOULD_ refer back to the containing paged resource using `within`. If there is a page resource that follows it (the next page), then it _MUST_ include a `next` link to it.  If there is a preceding page resource, then it _SHOULD_ include a `prev` link to it.

The paged resource _MAY_ use the `total` property to list the total number of leaf resources that are contained within its pages.  This would be the total number of annotations in a layer, or the total number of manifests in a collection.  Conversely, the page resources _MAY_ include the `startIndex` property with index of the first resource in the page, counting from zero relative to the containing paged resource.

The linked page resources _MAY_ have different properties from the paged resource, including different rights and descriptive properties.  Clients _MUST_ take into account any requirements derived from these properties, such as displaying `logo` or `attribution`.

##### Example Paged Layer

A layer representing a long transcription with almost half a million annotations, perhaps where each annotation paints a single word on the canvas:

``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ],
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
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ],
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
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ],
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
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ],
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
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ],
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

### 6.1 URI Recommendations

While any URI is technically acceptable for any of the resources in the API, there are several best practices for designing the URIs for the resources.

* The URI _SHOULD_ use the HTTPS scheme, not HTTP.
* The URI _SHOULD NOT_ include query parameters or fragments.
* Once published, they _SHOULD_ be as persistent and unchanging as possible.
* Special characters _MUST_ be encoded.

###  6.2. Requests

Clients _MUST NOT_ attempt to construct resource URIs by themselves, instead they _MUST_ follow links from within retrieved descriptions or elsewhere.

###  6.3. Responses

The format for all responses is JSON, as described above.  The different requirements for which resources _MUST_ provide a response is summarized in [Appendix A][appendixa-prezi30]. While some resources do not require their URI to provide the description, it is good practice if possible.

The HTTP `Content-Type` header of the response _SHOULD_ have the value "application/ld+json" (JSON-LD) with the `profile` parameter given as the context document: `http://iiif.io/api/presentation/3/context.json`.

``` none
Content-Type: application/ld+json;profile="http://iiif.io/api/presentation/3/context.json"
```
{: .urltemplate}

If this cannot be generated due to server configuration details, then the content-type _MUST_ instead be `application/json` (regular JSON), without a `profile` parameter.

``` none
Content-Type: application/json
```
{: .urltemplate}

The HTTP server _MUST_ follow the [CORS requirements][w3c-cors] to enable browser-based clients to retrieve the descriptions. In particular, the response _MUST_ include the `Access-Control-Allow-Origin` header, and the value _SHOULD_ be `*`.

``` none
Access-Control-Allow-Origin: *
```
{: .urltemplate}

Responses _SHOULD_ be compressed by the server as there are significant performance gains to be made for very repetitive data structures.

Recipes for enabling CORS, conditional Content-Type headers and other technical details are provided in the [Apache HTTP Server Implementation Notes][apache-notes].


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
{: .api-table #table-reqs-icons} 

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
{: .api-table #table-reqs-1}

__Technical Properties__

|                | id                       | type                 | format                  | height                    | width                     | renderingDirection        | renderingHint            | navDate                  |
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
{: .api-table #table-reqs-2}

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
{: .api-table #table-reqs-3}

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
{: .api-table #table-reqs-4}

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
{: .api-table #table-reqs-5}


__Protocol Behavior__

|                | id is dereferenceable |         
| -------------- | ---------------------- |
| Collection     | ![required][icon-req]  |
| Manifest       | ![required][icon-req]  |
| Sequence       | ![optional][icon-opt]  |
| Canvas         | ![recommended][icon-recc]  |
| Annotation     | ![recommended][icon-recc]  |
| AnnotationList | ![required][icon-req]  |
| Range          | ![optional][icon-opt]  |
| Layer          | ![optional][icon-opt]  |
| Image Content  | ![required][icon-req]  |
| Other Content  | ![required][icon-req]  |
{: .api-table #table-reqs-deref}

### B. Example Manifest Response

Rebuild the example
{: .warning}


### C. Versioning

Starting with version 2.0, this specification follows [Semantic Versioning][semver]. See the note [Versioning of APIs][versioning] for details regarding how this is implemented.

### D. Acknowledgements

Many thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### E. Change Log

| Date       | Description           |
| ---------- | --------------------- |
| XXXX-YY-ZZ | Version 3.0 |
| 2017-06-09 | Version 2.1.1 [View change log][change-log-30] |
| 2016-05-12 | Version 2.1 (Hinty McHintface) [View change log][change-log-21] |
| 2014-09-11 | Version 2.0 (Triumphant Giraffe) [View change log][change-log-20] |
| 2013-08-26 | Version 1.0 (unnamed) |
| 2013-06-14 | Version 0.9 (unnamed) |

{% include acronyms.md %}
{% include links.md %}
