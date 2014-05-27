---
title: "Presentation API 2.0 Change Log"
title_override: "Changes for IIIF Presentation API Version 2.0"
id: presentation-api-20-change-log
layout: spec
tags: [specifications, presentation-api, change-log]
major: 2
minor: 0
# no patch
pre: draft
---

This document is a companion to the [IIIF Presentation API Specification, Version 2.0][prezi-api]. It describes the significant changes to the API since [Version 1.0][prezi-api-10]. The changes are broken into three groups: [Breaking Changes][breaking-changes], i.e. those that are not backwards compatible from either a client or server perspective (or both); [Other Changes][other-changes], i.e. those that are backwards compatible; and [Deferred Changes][deferred-changes], i.e. those that have been discussed but did not make it into this version of the specification.

In addition to the changes described above:

  * The use of [RFC 2119 keywords][rfc-2119] has been made more consistent.
  * Language has been adjusted to make the document less focused on paged objects.
  * [Semantic Versioning][semver] will be used to enumerate releases.

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## Breaking Changes

### Name and URIs Changed

The name for the API used to be the "Metadata API", and this was changed to "Presentation API" with version 2.0.  This was to avoid the implication that the description was semantic, bibliographic information which is not, and has never been, the intent.  This resulted in the documentation moving to a different place, along with all of the auxilliary technical files like JSON-LD context and frames.

### Underscores rather than Camel Case

For consistency with the Image API, the property names which used camelCase were changed to use snake_case. The properties affected are: `viewingHint` to `viewing_hint`; `viewingDirection` to `viewing_direction`; `seeAlso` to `see_also`; and `otherContent` to `other_content`.  Changing the Image API would have been significantly more work, and resulting in more breaking changes. 

### Ranges Easier to Implement

Ranges were changed to follow the top-down pattern of a list of included ranges and canvases, rather than bottom-up where they would assert which parent range they were within.  This makes it significantly easier to implement, and follows the rest of the API's patterns of listed containership.

### Use of HTML Clarified

The use of HTML in the values of fields was permitted but inadequately specified in 1.0.  This version makes it much clearer and easier to determine the content of the value, and provides solid guidance as to which HTML features are allowed.

### Page-Turning Requirements

In order to allow page turning modalities, additional requirements were added to manifests that claim to be 'paged'.  Notably the first canvas is to be shown by itself, and then subsequent canvases can be assumed to be left/right pairs (depending on the viewingDirection).
An additional value of 'non-paged' was added to the viewingHint enumeration to assert that a particular Canvas is not part of the paging sequence.


## Other Changes

### Collections

Section 7.6 was added to describe collections of manifests, and sub-collections.  This allows discovery in a pragmatic and simple way, that is easy to understand and follows the same structure and approach as the rest of the Presentation API.

### Additional Fields

Several new fields were added:

* logo
* thumbnail
* related (although was used in practice in 1.0)

### Services Clarified and Extended

In order to manage requests for features that are not universally applicable, but still useful, the service construction that was previously under-specified has been extended to allow additional external specifications to be embedded or referenced.  Services are now listed in an annex document, and include the oft-discussed geo-tagging and physical dimensions features.

### Start Canvas

An additional value of 'start' was added to the viewingHint value enumeration, to be used on a canvas to assert that it's the one to be rendered to the user first, regardless of its position in the Sequence.

### Top-most Range

An additional value of 'top' was added to the viewingHint value enumeration, to be used on a range which is the top-most level in a table of contents or other structure.

### Restrictions Lifted

In 1.0 it was not possible to add most of the fields to content resources.  This was not for any good reason, and the restrictions were lifted.

## Deferred Changes

### Zones

The underlying Shared Canvas data model has an additional construction called a Zone.  At least one institution has implemented this construction and would like to use IIIF, but can't until it is in the API.  At least one further institution recognizes that they have requirements that are solved by zones. The issue was deferred until 2.1 as the solution is not easy to implement, and can be overlaid without adding backwards incompatibility.

### Dynamic Annotation List Services

An outstanding issue is the ability to associate either AnnotationLists or lists of AnnotationLists with canvases.  The requirements were decided to be not clearly enough defined at this stage, and may be simply AnnotationLists that are generated dynamically.  The major use cases also involved Authentication and Authorization, which have been deferred as well.  With the change to services, it is expected that this request can be experimented with and either blessed as a service or promoted to a full feature in the future without backwards incompatibility.

### Annotations on non-Canvas Resources

Only canvases may list their annotations, and thus it is impossible to refer to annotations on the placeholder for the physical object (the manifest).  It is not impossible to annotate manifests, it is just that there isn't a link from the manifest to its annotations.  Without a set of use cases to justify the addition of the feature, it was decided to defer this and experiment with services in the same manner as for Dynamic Annotation Lists.

### Target Audience

Particularly useful in the teaching and learning domain, the intended audience of resources is useful.  For commentary annotations this is important, and not covered in the base Open Annotation specification.  It was decided to defer this until the Open Annotation community can determine a resolution to be adopted, but to promote use cases and existing solutions such as the IDPF use of schema.org's Audience classes.  Also, not backwards incompatible and no clients are ready to use it yet.

### Compliance

The Image API has a very well formed set of compliance requirements.  The Presentation API, conversely, does not have any.  This was not seen as a requirement that needed to be solved for 2.0, and was deferred for future work.

### Explicit Protocol

The Image API in 2.0 has a protocol field that makes the assertion that the info.json document is part of the IIIF Image API protocol.  The Presentation API does not have this field.  There were no features or implementations identified that would make use of the field, and as backwards compatible it was deferred until a requirement was expressed.



[api-11]: /api/image/1.1/ "Image API 1.1"
[api-compliance]: /api/image/2.0/#compliance-levels "Image API 6. Compliance Levels"
[api]: /api/image/2.0/ "Image API 2.0"
[breaking-changes]: #breaking-changes "Presentation API 2.0 Breaking Changes"
[canonical-uris]: /api/image/2.0/#canonical-uri-syntax "Image API 4.7. Canonical URI Syntax"
[deferred-changes]: #deferred-changes "Presentation API 2.0 Deferred Changes"
[info-request]: /api/image/2.0/#information-request "Image API Section 5. Information Request"
[compliance-doc]: /api/image/2.0/compliance.html "Image API 2.0 Compliance Document"
[context]: /api/image/2/context.json  "Image API 2.0 JSON-LD Context"
[extensions]: /api/image/2.0/#extensions "Image API 4.7. Canonical URI Syntax"
[http-features]: /api/image/2.0/compliance.html#http-features "Image API Compliance: HTTP Features"
[imagemagick-output]: http://www.imagemagick.org/script/command-line-processing.php#output "ImageMagick: Command-line Processing: Output Filename"
[kdu-usage]: http://www.kakadusoftware.com/documents/Usage_Examples.txt "Usage Examples for the Demonstration Applications Supplied with Kakadu V7.0"
[pillow]: http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html#image-file-formats "Pillow: Image file formats"
[other-changes]: #other-changes "Presentation API 2.0 Other Changes"
[prezi-api]: /api/presentation/2.0/ "Presentation API 2.0"
[prezi-api-10]: /api/metadata/1.0/ "Metadata API 1.0"
[rfc-2119]: http://tools.ietf.org/html/rfc2119 "Key words for use in RFCs to Indicate Requirement Levels"
[semver]: http://semver.org/ "Semantic Versioning Specification"
[versioning]: /api/image/2.0/#b-versioning "Image API Appendix B: Versioning"

{% include acronyms.md %}
