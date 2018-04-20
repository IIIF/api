---
title: "Presentation API 3.0 Annotations ALPHA DRAFT"
title_override: "IIIF Presentation API 3.0 Annotations ALPHA DRAFT"
id: presentation-api
layout: spec
cssversion: 2
tags: [specifications, presentation-api]
major: 3
minor: 0
patch: 0
pre: alpha
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

----

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

##  1. Introduction

##  2. Annotation Features

The following sections describe known use cases for building representations of objects using the IIIF Presentation API, and clients _SHOULD_ expect to encounter them. Other use cases are likely to exist, and _MUST_ be encoded using the [Open Annotation's][openanno] context document mapping for any additional fields required.

###  6.1. Segments

It is important to be able to extract parts, or segments, of resources. In particular a very common requirement is to associate a resource with part of a canvas, or part of an image with either the entire canvas or part thereof. Secondly, as transcriptions are often made available in XML files, extracting the correct page to associate with the canvas, or line to associate with part of the canvas, is equally useful for reusing existing material. These can be accomplished using URI fragments for simple cases.

Note that if there are segments of both image and canvas, then the aspect ratio _SHOULD_ be the same, but there are circumstances where they _MAY_ be different.  In this case the rendering agent _SHOULD_ rescale the image segment to the dimensions provided on the canvas.

Segments of both static images and canvases may be selected by adding a [rectangular bounding box][media-frags] after the URI. The fragment _MUST_ take the form of `#xywh=` as per the example below where the four numbers are the x and y coordinates of the top left hand corner of the bounding box in the image or canvas, followed by the width and height. Thus the segment above is 300px wide, 50px high and starts at position 100,100. Note that only integers are allowed in this syntax, and this may limit accuracy of assignment to canvases with small dimensions.  

`http://www.example.com/iiif/book1/canvas/p1#xywh=100,100,300,50`
{: .urltemplate}

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/annotation/anno1",
  "type": "oa:Annotation",
  "motivation": "sc:painting",
  "resource":{
    // Crop out scanning bed
    "id": "http://example.org/iiif/book1/res/page1.jpg#xywh=40,50,1200,1800",
    "type": "dctypes:Image",
    "format": "image/jpeg"
  },
  // canvas size is 1200x1800
  "on": "http://example.org/iiif/book1/canvas/p1"
}
```

For image resources with a [IIIF Image API][image-api] service, it is _RECOMMENDED_ to instead use the Image API parameters rather than a fragment as above.  The following structure allows simple clients to use the image directly (the URL with the segment), and allows clients that implement the IIIF Image API to have sufficient information to construct appropriate URIs using the API.

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/annotation/anno1",
  "type": "oa:Annotation",
  "motivation": "sc:painting",
  "resource": {
    "id": "http://www.example.org/iiif/book1-page1/50,50,1250,1850/full/0/default.jpg",
    "type": "oa:SpecificResource",
    "full": {
      "id": "http://example.org/iiif/book1-page1/full/full/0/default.jpg",
      "type": "dctypes:Image",
      "service": {
        "@context": "http://iiif.io/api/image/2/context.json",
        "id": "http://example.org/iiif/book1-page1",
        "profile": "http://iiif.io/api/image/2/level2.json"
      }
    },
    "selector": {
      "@context": "http://iiif.io/api/annex/openannotation/context.json",
      "type": "iiif:ImageApiSelector",
      "region": "50,50,1250,1850"
    }
  },
  "on": "http://www.example.org/iiif/book1/canvas/p1#xywh=0,0,600,900"      
}
```

Segments of XML files may be extracted with [XPaths][xpath]. The fragment _MUST_ be structured as follows:

`http://www.example.com/iiif/book1/res/tei.xml#xpointer(/xpath/to/element)`
{: .urltemplate}

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/annotation/anno1",
  "type": "oa:Annotation",
  "motivation": "sc:painting",
  "resource":{
    "id": "http://example.org/iiif/book1/res/tei.xml#xpointer(//line[1])",
    "type": "dctypes:Text",
    "format": "application/tei+xml"
  },
  "on": "http://example.org/iiif/book1/canvas/p1#xywh=100,100,500,300"
}
```

###  6.2. Embedded Content

Instead of referencing transcription text externally, it is often easier to record it within the annotation itself. Equally, text based comments could also benefit from being included in the annotation that associates the comment with the canvas.

Content _MAY_ be embedded instead of referenced by using the following pattern within the annotation block:

``` json-doc
{"resource": {"type": "cnt:ContextAsText", "chars": "text here"}}
```

The media type _SHOULD_ be provided using the `format` field, and while any media type is possible, it is _RECOMMENDED_ that `text/plain` or `text/html` be used to maximize compatibility.

If it is desirable to describe the language of the content, then it _MUST_ be given with the `language` property not `@language`.

An example of this feature:

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/annotation/p1",
  "type": "oa:Annotation",
  "motivation": "sc:painting",
  "resource":{
    "type": "cnt:ContentAsText",
    "chars": "Here starts book one...",
    "format": "text/plain",
    "language": "en"
  },
  "on": "http://example.org/iiif/book1/canvas/p1#xywh=100,150,500,25"
}
```

###  6.3. Choice of Alternative Resources

A common requirement is to have a choice between multiple images that depict the page, such as being photographed under different lights or at different times. This can be accomplished by having a "oa:Choice" object as the resource, which then refers to the options to select from. It _MUST_ have one `default` and at least one further `item` to choose from. The images _SHOULD_ have a `label` for the viewer to display to the user so they can make their selection from among the options.

The same construction can be applied to a choice between other types of resources as well. This is described in the [Multiplicity section][openannomulti] of the Open Annotation specification.

Either the `default` or `item` _MAY_ have a value of "rdf:nil". This means that a valid option is not to display anything. This _MUST NOT_ have a label associated with it, viewers should either use "Nothing" or an appropriate label of their choice.

This can be used to model foldouts and other dynamic features of a page, by associating images of the different states with the canvas. Depending on the nature of the images, this can be done such that either the entire image is switched to change state, or only the section of the image that has to change is switched, if the appropriate segment information is known.

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/annotation/anno1",
  "type": "oa:Annotation",
  "motivation": "sc:painting",
  "resource":{
    "type": "oa:Choice",
    "default":{
      "id": "http://example.org/iiif/book1/res/page1.jpg",
      "type": "dctypes:Image",
      "label": "Color"
    },
    "item": [
      {
        "id": "http://example.org/iiif/book1/res/page1-blackandwhite.jpg",
        "type": "dctypes:Image",
        "label": "Black and White"
      }
    ]
  },
  "on": "http://example.org/iiif/book1/canvas/p1"
}
```

###  6.4. Non Rectangular Segments

The [Scalable Vector Graphics][svg] standard (SVG) is used to describe non-rectangular areas of canvas or image resources. While SVG can, of course, describe rectangles this is _NOT RECOMMENDED_, and either the [IIIF Image API][image-api] or the `xywh` bounding box described above _SHOULD_ be used instead.  This is recognized as an advanced use case and that clients may not support it.

In this pattern, the resource of the annotation is a "oa:SpecificResource" which has the complete image referenced in a `full` field and the SVG embedded in a `selector` field (as the SVG selects the part of the image needed). The SVG document is embedded using the same `ContentAsText` approach as for embedding comments or transcriptions.

If the section of an image is mapped to part of a canvas, as in the example below, then the target in `on` _MUST_ be the rectangular bounding box in which the SVG viewport should be placed. If the entire canvas is the target, then the SVG viewport is assumed to cover the entire canvas. If the dimensions of the viewport and the bounding box or canvas are not the same, then the SVG _MUST_ be scaled such that it covers the region. This may result in different scaling ratios for the X and Y dimensions.

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/annotation/anno1",
  "type": "oa:Annotation",
  "motivation": "sc:painting",
  "resource":{
    "type": "oa:SpecificResource",
    "full": {
      "id": "http://example.org/iiif/book1/res/page1.jpg",
      "type": "dctypes:Image"
    },
    "selector": {
      "type":["oa:SvgSelector","cnt:ContentAsText"],
      "chars": "<svg xmlns=\"...\"><path d=\"...\"/></svg>"
    }
  },
  "on": "http://example.org/iiif/book1/canvas/p1#xywh=100,100,300,300"
}
```

###  6.5. Style

The [Cascading Style Sheets][css] standard (CSS) is used to describe how the client should render a given resource to the user. The CSS information is embedded within the annotation using the same `ContentAsText` approach above. As a stylesheet may contain more than one style, and be reused between annotations, it is attached to the annotation directly in the same manner as a stylesheet being linked to an HTML document. Then the name of the style class is attached to the resource that should be styled, again in the same manner as the class attribute in html, although we use `style` to avoid confusion with object classes.

In the example below, the text should be colored red.

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/annotation/anno1",
  "type": "oa:Annotation",
  "motivation": "sc:painting",
  "stylesheet":{
    "type": ["oa:CssStyle", "cnt:ContextAsText"],
    "chars": ".red {color: red;}"
  },
  "resource":{
    "type": "oa:SpecificResource",
    "style": "red",
    "full": {
      "type": "cnt:ContentAsText",
      "chars": "Rubrics are Red, ..."
    }
  },
  "on": "http://example.org/iiif/book1/canvas/p1#xywh=100,150,500,30"
}
```


###  6.6. Rotation

CSS may also be used for rotation of images which are not correctly aligned with the canvas. In the example below, after the image is located within the 500 wide by 30 high space within the canvas, it is then rotated by the rendering client application around the top left corner by 45 degrees anti-clockwise.

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/annotation/anno1",
  "type": "oa:Annotation",
  "motivation": "sc:painting",
  "stylesheet":{
    "type": ["oa:CssStyle", "cnt:ContextAsText"],
    "chars": ".rotated {transform-origin: top left; transform: rotate(-45deg);}"
  },
  "resource":{
    "type": "oa:SpecificResource",
    "style": "rotated",
    "full": {
      "id": "http://example.org/iiif/book1/res/page1-detail.png",
      "type": "dctypes:Image"
    }
  },
  "on": "http://example.org/iiif/book1/canvas/p1#xywh=100,150,500,30"
}
```

Alternatively, if the image is available via the IIIF Image API, it may be more convenient to have the server do the rotation of the image.  This uses a custom Selector for the Image API, further described in the [Open Annotation extensions][oa-ext-annex] annex.  For the purposes of rotation, the example below demonstrates the pattern.

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/annotation/anno1",
  "type": "oa:Annotation",
  "motivation": "sc:painting",
  "resource":{
    "id": "http://example.org/iiif/book1-page1/full/full/90/default.jpg",
    "type": "oa:SpecificResource",
    "full": {
      "id": "http://example.org/iiif/book1-page1/full/full/0/default.jpg",
      "type": "dctypes:Image",
      "service": {
        "@context": "http://iiif.io/api/image/2/context.json",
        "id": "http://example.org/iiif/book1-page1",
        "profile": "http://iiif.io/api/image/2/level2.json"
      }
    },
    "selector": {
      "@context": "http://iiif.io/api/annex/openannotation/context.json",
      "type": "iiif:ImageApiSelector",
      "rotation": "90"
    }
  },
  "on": "http://example.org/iiif/book1/canvas/p1#xywh=50,50,320,240"
}
```

###  6.7. Comment Annotations

For annotations which are comments about the canvas, as opposed to painting content resources onto the canvas, there are different types of motivation to make the distinction clear. For annotations about the content (such as comments, notes, descriptions etc.) the `motivation` _SHOULD_ be "oa:commenting", but _MAY_ be any from the list given in the [Open Annotation][openanno] specification.

Unlike painting annotations, comments or annotations with other motivations _SHOULD_ have a URI assigned as their identity and provided in the `id` property.  When dereferencing that URI, the representation of the annotation _SHOULD_ be returned.  This is to allow further annotations to annotate the comment, for example in order to reply to it, or to tag it for organizational or discovery purposes.

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/annotation/anno1",
  "type": "oa:Annotation",
  "motivation": "oa:commenting",
  "resource":{
    "id": "http://example.org/iiif/book1/res/comment1.html",
    "type": "dctypes:Text",
    "format": "text/html"
  },
  "on": "http://example.org/iiif/book1/canvas/p1"
}
```

Other resources may also have comments made about them, including manifests (comments about the object), sequences (comments about that particular ordering), ranges (comments about the section), annotations (replies to the targeted annotation), and so forth.  In order for the client to discover these annotations, they can be included in an AnnotationList referenced from the target resource.  This is accomplished by reusing the `otherContent` pattern.  Any resource may have a list of annotations associated with it in this way.

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id": "http://example.org/iiif/book1/manifest",
  "type": "sc:Manifest",
  // ...

  "otherContent": [
    {
      "id": "http://example.org/iiif/book1/list/book1",
      "type": "sc:AnnotationList"
    }
  ]
}
```

###  6.8. Hotspot Linking

It is also possible to use annotations to create links between resources, both within the manifest or to external content.  This can be used to link to the continuation of an article in a digitized newspaper in a different canvas, or to link to an external web page that describes the diagram in the canvas.

Hotspot linking is accomplished using an annotation with a `motivation` of "oa:linking". The region of the canvas that should trigger the link when clicked is specified in the `on` field in the same way as other annotations. The linked resource is given in the `resource` field.  The linked resource _MAY_ also be another canvas or region of a canvas.  The user experience of whether the linked resource is opened in a new tab, new window or by replacing the current view is up to the implementation.

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "id":"http://www.example.org/iiif/book1/annotation/anno1",
  "type":"oa:Annotation",
  "motivation":"oa:linking",
  "resource": {
    "id":"http://www.example.org/page-to-go-to.html",
    "type":"dctypes:Text",
    "format":"text/html"
  },
  "on":"http://www.example.org/iiif/book1/canvas/p1#xywh=500,500,150,30"
}
```


### E. Versioning

Starting with version 2.0, this specification follows [Semantic Versioning][semver]. See the note [Versioning of APIs][versioning] for details regarding how this is implemented.

### F. Acknowledgements

The production of this document was generously supported by a grant from the [Andrew W. Mellon Foundation][mellon].

Many thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### G. Change Log

| Date       | Description           |
| ---------- | --------------------- |
| 2016-05-12 | Version 2.1 (Hinty McHintface) [View change log][change-log] |


[iiif-discuss]: mailto:iiif-discuss@googlegroups.com "Email Discussion List"
[shared-canvas]: /model/shared-canvas/{{ site.shared_canvas.latest.major}}.{{ site.shared_canvas.latest.minor }} "Shared Canvas Data Model"
[image-api]: /api/image/{{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }}/ "Image API"
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
