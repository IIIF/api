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

{% include copyright2015.md %}

----

## Contents
{:.no_toc}
* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Overview


See [Community Process][process].




## 2. Design Principles Adopted

### Scope Design Through Shared Use Cases

IIIF specifications are scoped through documented and well understood, shared use cases.  This process governs the method by which decisions are made as to which features should be included or prioritized.  

This decision was made in order to keep the resulting specifications practical and to solve real problems.  Implementers will invest time in solutions that solve their problems, and not speculative or abstract ones.  If the use case is shared by multiple organizations, then there is a need for interoperability.

### Select Solutions That Are as Simple as Possible and No Simpler

IIIF specifications should be designed to reduce the complexity to the lowest possible point at which the use cases that feed them can be met.  They should make simple things easy and complex things possible.  They should allow implementers to build up from a minimum viable product in stages and incrementally enable more complex use cases.

This decision was made to ensure the adoption of the specifications is as high as possible.

### Intelligently Manage Ramping Up

IIIF specifications should allow basic implementation with static on-disk files, often called "level 0", when possible. They should not require costly or complicated libraries or tooling to get started, nor computationally expensive runtime processing. A useful implementation should require only a way of hosting files that are accessible via a web server.  

This decision was made to support simple and quick implementations as a way to encourage adoption.

### Avoid Dependency on Specific Technologies

IIIF specifications should avoid placing undue value on one technology or format over another, unless there is a clear benefit and the choice does not pose a significant barrier to entry.  While the APIs must make choices for the sake of interoperability, these choices must be weighed as to how closely tied they are to specific products or formats. For example, the JPEG format has extremely widespread adoption across multiple programming languages and environments. The JPEG2000 format, although technically superior, is not able to be rendered by most web browsers natively.  The first is an acceptable dependency, the second is not.

This decision was made in order to ensure that the specifications can be implemented in a variety of languages and styles.  It results from the combination of the previous two principles.

### Use Resource Oriented Design

IIIF specifications follow resource-centric design principles and use [REST][rest] interfaces, rather than service or operation-centric design patterns. This carries on from the previous design principles, and serves to provide a consistent and coherent pattern across many different functional areas.

This decision was made to ensure that the specifications are cacheable and performant, at the same time as being easy to understand and implement. 

### Don't Break Web Caches

IIIF specifications are designed to work seamlessly with modern web caching infrastructure.  The specifications will ensure that representations can be trivially cached by intermediate systems without loss of fidelity or function.  

This decision was made for performance and simplicity of implementation, and results from the previous principles.

### Follow Linked Data Principles

IIIF specifications conform to [Linked Data][lod], and relevant [web architecture][webarch] standards as defined by the W3C and IETF. They should not require an RDF based development stack to implement, but it must be possible to implement using one.  It should be possible to transform representations back and forth between triples and the JSON-LD serialiation without loss, but not necessarily without the use of custom code.  

This decision was made to ensure that the data published via IIIF specifications can be part of the Web, not just on the Web. The semantics of the properties and classes used in the APIs are therefore self-documenting and able to be shared.

### Design for JSON-LD First

IIIF specifications that involve the description of resources, rather than the transfer of bitstreams, are designed for JSON-LD as the primary serialization. This is comprised of publishing and maintaining a JSON-LD context document, and providing JSON-LD Frames.

This decision was made to ensure that the representation of the Linked Data is as easy to use as possible without the need for a full RDF development suite.  Developers must be able to treat the representation as plain JSON, with a predictable structure.  This ease of understanding increases the likelihood of wide spread adoption.

### Use Existing Standards Where Possible

IIIF specifications should be consistent with and use existing open standards when possible.  This is tempered by the need for ease of understanding, implementation and the timing of standards evolution and updates.

This decision was made to ensure the continued integration of IIIF specifications with the wider web environment, and existing implementations.
 
### Follow Existing Best Practices

IIIF specifications follow existing best practices for the standards that it adopts, including [JSON-LD best practices][jsonbp], [Linked Open Data best practices][lodbp], and [Data on the Web best practices][dwbp], where possible and appropriate.  Exceptions are made when the cost of following the best practice would prove to be a significant barrier to understanding or implementation, and hence adoption.

This decision, as above, was made to ensure the continued integration of IIIF specifications with the wider web environment. The design of IIIF specifications should be informed by existing and ongoing work, but evaluated as to the appropriateness of the application to the IIIF context.

### Separate Concerns, Loosely Couple APIs

In the well established pattern of doing one thing well, IIIF specifications should address their own area of concern and be loosely coupled rather than tightly bound together.  This allows for independent implementation and tooling, and simplifies the process for deployment by adopters and API updates by the community.  For example, it is possible to implement the Image API without the Presentation API and vice versa.  A counter example is that the Search API is more tightly linked to the Presentation API.
  
This decision was made to ensure that the on-ramp for adopters was as easy and multi-entrant as possible.  The Presentation API can be a starting point for any of the other APIs, the Image API can be a starting point for the Presentation or Authentication APIs.  It also ensures the simplicity and scope of the APIs individually, as the complexity must be managed entirely within the API's specification.

### Define Success, Not Failure

IIIF specifications define the functionality that can be expected to work and how to request it in an open manner, and do not limit the interpretation of requests that are beyond the scope or current definition of the specification.  Any pattern outside of those defined by the APIs is able to be used by implementers, keeping in mind that future official API extensions might make it inconsistent.  For example, an implementation of the Image API can recognize its own specific parameter values for quality or size, it just cannot change the interpretation of the parameter values specified.

This decision was made to enable experimentation by implementers, thereby encouraging the early adoption and validation of new (minor) versions.   

### Follow the IIIF Community Process



## 4. Appendices

### A. Change Log

 | Date       | Description                                                         |
 | ---------- | ------------------------------------------------------------------- |
 | 2017-02-01 | Initial draft version |

[change-log]: #change-log "Change Log"
[iiif-announce]: https://groups.google.com/forum/#!forum/iiif-announce "IIIF Email Announcement List"
[iiif-discuss]: https://groups.google.com/forum/#!forum/iiif-discuss "IIIF Email Discussion List"
[iiif-semver]: /api/annex/notes/semver/ "Versioning of APIs"
[rfc-2119]: https://www.ietf.org/rfc/rfc2119.txt "RFC 2119"
[spec-disclaimer]: /api/annex/notes/disclaimer/ "Specification Disclaimer"

[process]: /api/annex/notes/editors/#community-process
[services]: /api/annex/services/

[rest]: https://en.wikipedia.org/wiki/Representational_state_transfer
[lod]:
[webarch]: 
[jsonbp]: http://json-ld.org/spec/latest/json-ld-api-best-practices/
[lodbp]: https://www.w3.org/TR/ld-bp/
[databp]: https://www.w3.org/TR/dwbp/


{% include acronyms.md %}
