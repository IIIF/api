---
title: "Presentation API 2.1 Change Log"
title_override: "Changes for IIIF Presentation API Version 2.1"
id: presentation-api-21-change-log
layout: spec
tags: [specifications, presentation-api, change-log]
major: 2
minor: 1
# no patch
pre: final
---

This document is a companion to the [IIIF Presentation API Specification, Version 2.1][prezi-api]. It describes the significant changes to the API since [Version 2.0][prezi-api-20]. The changes are all backwards compatible. A second section, [Deferred Proposals][deferred-proposals], lists proposals that have been discussed but did not make it into this version of the specification.


## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## Non-Breaking Changes

### Link to alternate representations of Resources

Added the `rendering` property.

### Allow date-based user interfaces for navigation

Added the `navDate` property.

### Annotations of non-Canvas Resources

AnnotationLists may be referenced from any resource, when the annotations in the list are comments.

### Facing Pages Viewing Hint

Add a "facingPages" `viewingHint` value to capture the situation when a single canvas represents both sides of an open spread.  This is common in older digitization projects and also with Eastern works.

### Multi-Part Collections Viewing Hint

Add a "multi-part" `viewingHint` value for the situation when a collection has manifests that are part of a logical whole.


## Clarifications

Several clarifications were made:

* Clarify the intended usage of the "continuous" `viewingHint` ; technically this is a breaking change, but the original specification was unable to be implemented (the semantics were identical to those of the "individuals" `viewingHint`), it was impossible for any implementations to be affected.
* Add a table specifying whether a resource should be dereferenceable or not

### Editorial

Several editorial changes were made:

* Ensure that examples follow the recommendations (e.g. `seeAlso`)


## Deferred Proposals

### Zones

Zones continue to be deferred, awaiting strong, shared use cases.



[deferred-proposals]: #deferred-proposals "Presentation API 2.1 Deferred Proposals"
[other-changes]: #other-changes "Presentation API 2.1 Non-Breaking Changes"
[prezi-api]: /api/presentation/2.1/ "Presentation API 2.1"
[prezi-api-20]: /api/presentation/2.0/ "Presentation API 2.0"
[prezi-api-10]: /api/metadata/1.0/ "Metadata API 1.0"


{% include acronyms.md %}
