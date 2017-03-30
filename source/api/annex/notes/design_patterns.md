---
title: "IIIF Design Patterns"
layout: spec
tags: [annex, presentation-api, image-api]
cssversion: 2
---

## Status of this Document
{:.no_toc}

This document is not subject to [IIIF's versioning semantics][iiif-semver]. Changes will be tracked within the document and its [internal change log][change-log]

**Authors:**

  * **[Michael Appleby](https://orcid.org/0000-0002-1266-298X)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0002-1266-298X), [_Yale University_](http://www.yale.edu/)
  * **[Tom Crane](https://orcid.org/0000-0003-1881-243X)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0003-1881-243X), [_Digirati_](http://digirati.com/)
  * **[Robert Sanderson](https://orcid.org/0000-0003-4441-6852)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0003-4441-6852), [_J Paul Getty Trust_](http://www.getty.edu/)
  * **[Jon Stroop](https://orcid.org/0000-0002-0367-1243)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0002-0367-1243), [_Princeton University Library_](https://library.princeton.edu/)
  * **[Simeon Warner](https://orcid.org/0000-0002-7970-7855)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0002-7970-7855), [_Cornell University_](https://www.cornell.edu/)
  {: .names}

{% include copyright2017.md %}

----

## Contents
{:.no_toc}
* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Overview

This document aims to describe, rationalize, and document the design patterns that have evolved around the creation of the IIIF specifications to date. These patterns should be used as a guide for ongoing and future work in order to promote consistency across the growing number of IIIF specifications.

The patterns do not speak to the process by which the specifications are written and managed over time.  For notes on the adopted approaches for these, please see:

  * [Editorial Process][process]: The community process of discussion, and the editorial process of writing, the specifications.
  * [Semantic Versioning][iiif-semver]: The interpretation of the semantic versioning pattern for managing change of APIs in a responsible and responsive manner.


## 2. Design Patterns

### 2.1. Scope Design Through Shared Use Cases

IIIF specifications are shaped by shared, documented, and well-understood use cases. Shared understanding promotes interoperability, and the specifications are more likely to be implemented if the results solve real, not speculative, problems. Assessment of use cases is a key factor in the process of determining which features should be included or prioritized.

The intent of adopting this pattern is to keep the resulting specifications practical and to solve real problems.  Implementers will invest time in solutions that solve their problems, and not speculative or abstract ones.  If the use case is shared by multiple organizations, then there is a need for interoperability.

### 2.2. Select Solutions That Are as Simple as Possible and No Simpler

IIIF specifications should be designed to reduce the complexity to the lowest possible point at which the use cases that feed them can be met.  They should make simple things easy and complex things possible.  They should allow implementers to build up from a minimum viable product in stages and incrementally enable more complex use cases.

The intent of adopting this pattern is to ensure the adoption of the specifications is as high as possible. Simplicity is often a trade-off between parties, and must take into account the generation and publishing of the data on the server side, and the consumption and processing of the data on the client side.

### 2.3. Intelligently Manage Ramping Up

IIIF specifications should allow basic implementation with static on-disk files, often called "level 0", when possible. They should not require costly or complicated libraries or tooling to get started, nor computationally expensive runtime processing. A useful implementation should require only a way of hosting files that are accessible via a web server.

The intent of adopting this pattern is to support simple and quick implementations as a way to encourage adoption.

### 2.4. Avoid Dependency on Specific Technologies

IIIF specifications should avoid placing undue value on one technology or format over another, unless there is a clear benefit and the choice does not pose a significant barrier to entry.  While the APIs must make choices for the sake of interoperability, these choices must be weighed as to how closely tied they are to specific products or formats. For example, the JPEG format has extremely widespread adoption across multiple programming languages and environments. The JPEG2000 format, although technically superior, is not able to be rendered by most web browsers natively.  The first is an acceptable dependency, the second is not.

The intent of adopting this pattern is to ensure that the specifications can be implemented in a variety of languages and styles.  It results from the combination of the previous two patterns.

### 2.5. Use Resource Oriented Design

IIIF specifications follow resource-centric design patterns, for example by using [REST][rest] interfaces rather than service or operation-centric design patterns. This carries on from the previous design patterns, and serves to provide a consistent and coherent pattern across many different functional areas.

The intent of adopting this pattern is to ensure that the specifications are cacheable and performant, at the same time as being easy to understand and implement.

### 2.6. Don't Break Web Caches

IIIF specifications are designed to work seamlessly with modern web caching infrastructure.  The specifications will ensure that representations can be trivially cached by intermediate systems without loss of fidelity or function.

The intent of adopting this pattern is ensure performance and simplicity of implementation, and results from the previous patterns.

### 2.7. Follow Linked Data Principles

IIIF specifications conform to [Linked Data][lod], and relevant [web architecture][webarch] standards as defined by the W3C and IETF. They should not require an RDF based development stack to implement, but it must be possible to implement using one.  It should be possible to transform representations back and forth between triples and the [JSON-LD][json-ld] serialization without loss, but not necessarily without the use of custom code.

The intent of adopting this pattern is to ensure that the data published via IIIF specifications can be part of the Web, not just on the Web. The semantics of the properties and classes used in the APIs are therefore self-documenting and able to be shared.

### 2.8. Design for JSON-LD First

IIIF specifications that involve the description of resources, rather than the transfer of bitstreams, are designed for [JSON-LD][json-ld] as the primary serialization. This is comprised of publishing and maintaining a JSON-LD context document, and providing JSON-LD Frames.

The intent of adopting this pattern is to ensure that the representation of the Linked Data is as easy to use as possible without the need for a full RDF development suite.  Developers must be able to treat the representation as plain JSON, with a predictable structure.  This ease of understanding increases the likelihood of wide spread adoption.

### 2.9. Use Existing Standards Where Possible

IIIF specifications should be consistent with and use existing open standards when possible.  This is tempered by the need for ease of understanding, implementation and the timing of standards evolution and updates.

The intent of adopting this pattern is to ensure the continued integration of IIIF specifications with the wider web environment, and existing implementations.

### 2.10. Follow Existing Best Practices

IIIF specifications follow existing best practices for the standards that it adopts, including [JSON-LD best practices][jsonbp], [Linked Open Data best practices][lodbp], and [Data on the Web best practices][dwbp], where possible and appropriate.  Exceptions are made when the cost of following the best practice would prove to be a significant barrier to understanding or implementation, and hence adoption.

The intent of adopting this pattern is to ensure the continued integration of IIIF specifications with the wider web environment. The design of IIIF specifications should be informed by existing and ongoing work, but evaluated as to the appropriateness of the application to the IIIF context.

### 2.11. Separate Concerns, Loosely Couple APIs

In the well established pattern of doing one thing well, IIIF specifications should address their own area of concern and be loosely coupled rather than tightly bound together.  This allows for independent implementation and tooling, and simplifies the process for deployment by adopters and API updates by the community.  For example, it is possible to implement the [Image API][image-api] without the [Presentation API][presentation-api] and vice versa.  A counter example is that the [Search API][search-api] is necessarily more tightly linked to the Presentation API.

The intent of adopting this pattern is to ensure that the on-ramp for adopters was as easy and multi-entrant as possible.  The Presentation API can be a starting point for any of the other APIs, the Image API can be a starting point for the Presentation or [Authentication API][auth-api]s.  It also ensures the simplicity and scope of the APIs individually, as the complexity must be managed entirely within the API's specification.

### 2.12. Define Success, Not Failure

IIIF specifications define the functionality that can be expected to work and how to request it, and do not limit the interpretation of requests that are beyond the scope or current definition of the specification.  Any pattern outside of those defined by the APIs is able to be used by implementers, keeping in mind that future official API extensions might make it inconsistent.  For example, an implementation of the [Image API][image-api] can legitimately recognize its own specific parameter values for `quality` or `size`, but it should not change the interpretation of parameter values that are specified.

The intent of adopting this pattern is to enable experimentation by implementers, thereby encouraging the early adoption and validation of new (minor) versions.


## 3. Change Log

 | Date       | Description                                                         |
 | ---------- | ------------------------------------------------------------------- |
 | 2017-03-15 | First published version after community review |
 | 2017-02-06 | Initial draft version |

[change-log]: #3-change-log "Change Log"
[iiif-announce]: https://groups.google.com/forum/#!forum/iiif-announce "IIIF Email Announcement List"
[iiif-discuss]: https://groups.google.com/forum/#!forum/iiif-discuss "IIIF Email Discussion List"
[iiif-semver]: /api/annex/notes/semver/ "Versioning of APIs"
[rfc-2119]: https://www.ietf.org/rfc/rfc2119.txt "RFC 2119"
[spec-disclaimer]: /api/annex/notes/disclaimer/ "Specification Disclaimer"

[process]: /api/annex/notes/editors/#2-community-process
[services]: /api/annex/services/
[image-api]: /api/image
[presentation-api]: /api/presentation
[search-api]: /api/search
[auth-api]: /api/auth

[rest]: https://en.wikipedia.org/wiki/Representational_state_transfer
[lod]: https://en.wikipedia.org/wiki/Linked_data
[webarch]: https://www.w3.org/TR/webarch/
[json-ld]: https://www.w3.org/TR/json-ld/
[jsonbp]: http://json-ld.org/spec/latest/json-ld-api-best-practices/
[lodbp]: https://www.w3.org/TR/ld-bp/
[dwbp]: https://www.w3.org/TR/dwbp/

{% include acronyms.md %}
