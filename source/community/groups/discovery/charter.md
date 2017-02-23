---
title: "IIIF Discovery Technical Specification Group Charter"
layout: spec
tags: []
cssversion: 2
---


## Introduction

Interoperable resources are only useful if they can be found. This has been well-recognized since the early days of the IIIF community, and more recently it has become clear that a concerted effort to standardize patterns that will facilitate discovery, harvesting and synchronization, indexing, and importing of IIIF resources is required.

This group will create specifications that improve the discovery process for IIIF resources, with a focus on leveraging existing techniques and tools, and promoting widespread adoption within the community. It will assist with and steer the implementation of community infrastructure, such as a registry of adopters, validators for the implementations, and transformation tools to generate the required data from existing systems and APIs.

If successful, the work will enable the collaborative development of global or thematic registries, search engines and portal applications that allow developers and end users to easily find and use content available via existing IIIF APIs.

## Scope

The scope of the group's efforts is divided into four separate but interlinked areas.  Each area is important to make progress on for the overall effort to be successful and sustainable. This Technical Specifications Group expands the scope of the IIIF community into these areas, as agreed by the community and according to the community roadmap.

Work that is out of scope for this group includes the selection or creation of any descriptive metadata formats, and the selection or creation of metadata search APIs or protocols. These are out of scope as the diverse domains represented within the IIIF community already have different standards in these spaces, and previous attempts to reconcile these specifications across domains have not been successful.

The group commits to following the requirements for the specification process, including the production of two independent implementations of each feature specified, and to reach out to other communities aligned with IIIF for feedback and to encourage adoption.


### 1. Crawling and Harvesting

The first, necessary step for enabling the discovery of IIIF resources, is to have a consistent and well understood pattern for lists of the available resources to be published by the content providers, and for consuming systems to be able to find and process those lists.  The work does not include transmission optimization for the content itself, for example transferring any source image content between systems, only for the discovery of the existing content on the web.

The anticipated deliverables:

  * Specification of how content providers publish lists of their resources
  * Recommendations for how consuming applications process those lists
  * Validation service that checks the lists are correctly generated
  * Registry of institutions' lists
  * Reference implementations for list generators and consumers

__Background work:__

  * Sitemap Protocol
  * ResourceSync
  * IIIF Collections

### 2. Content Indexing

The IIIF Presentation API does not include any information about the objects being presented that would allow for a fielded or advanced search, however it does have the facilities for linking to external non-IIIF descriptions of the objects.  For example, the Presentation API's manifest for a book contains a description of the book intended for humans, and might link to a description of the book intended for machines.

In order to facilitate advanced search and thematic portals where a subset of the available resources are indexed in more detail, work will be carried out to identify the common formats used in the various communities that have adopted IIIF, and provide best practices for how to reference those descriptions.  The work will not include further best practices on how institutions should use those formats, but might include outreach to the maintainers of the formats to establish how to include the reverse link from the format to the IIIF resources.

The anticipated deliverables:

  * Recommendations for profile identifiers and formats, following existing practice.

__Background work:__

  * Newspaper Group work on METS/ALTO
  * EDM / IIIF Alignment work

### 3. Change Notification

Once a system has crawled the list of resources available, there are several benefits to being updated with the changes, rather than requiring the list be re-crawled every time. In particular, it is easier to stay up to date in a timely fashion, it is easier on the providing organization to not have their content constantly crawled by robots, and it is more efficient to index only known changes rather than detect if a resource has changed.  The work will include analysis and prototyping of notification systems, built on top of existing standards, to promote this efficiency.

The anticipated deliverables:

  * Specification for notification interactions
  * Reference implementations for notification generators and consumers
  * Validation service for notifications
  * If necessary, a central hub for distribution of notifications

__Background work:__

* ResourceSync
* WebMention
* Linked Data Notifications
* PubSub


### 4. Import to Viewers

IIIF resources are intended to be used in different contexts, with different viewing applications, as appropriate to the needs of the user.  In order to enable users to work with the content once it has been discovered, the fourth part of the work is to establish a specification of how content providers and discovery applications can allow the user to import the IIIF content into externally hosted viewers.  

The anticipated deliverables:

  * Specification of viewer import
  * Recommendations around consistent UI/UX patterns
  * Validation service for the import process
  * Reference implementations for generators and consumers

__Background work:__

  * IIIF Drag and Drop implementations


## Estimated Timeline

* Q4 2016: Group established, work commences
* Q1 2017: Gather Use Cases; Publish Import draft, with implementations
* Q2 2017: Publish Crawling draft
* Q3 2017: Publish Indexing and Notification drafts
* Q4 2017: Revisions to Import; Implementations of Crawling
* Q1 2018: Implementations of Indexing and Notification
* Q2 2018: Revisions to specifications and implementations
* Q3 2018: Revisions to specifications and implementations
* Q4 2018: Version 1.0, with implementations

## Communication Channels

* Github Repository:  http://github.com/IIIF/discovery
* Slack:  [#discovery][discovery-slack]
* Email:  [IIIF-Discuss list][iiif-discuss] ; subject line: \[discovery\]
* Face to Face: Annual [IIIF events][events] such as Conferences and Working Group meetings, plus as incidental travel allows
* Calls: Initially bi-weekly, plus standing updates/feedback on Technical Call


## Community Support

### Organizations

* Bavarian State Library
* Biblissima - Campus Condorcet
* Brumfield Labs
* Carnegie Museum of Art
* Cornell University
* Digirati
* Europeana
* Harvard University
* J. Paul Getty Trust
* Los Alamos National Laboratory
* National Gallery of Art
* National Library of Israel
* National Library of Wales
* North Carolina State University Libraries
* Loyola University Maryland
* Oxford University
* Princeton University
* Stanford University
* University of Edinburgh
* University of Michigan
* University of Toronto
* Yale Center for British Art

### Technical Editors

* Michael Appleby
* Tom Crane
* Rob Sanderson
* Jon Stroop
* Simeon Warner

[discovery-slack]: https://iiif.slack.com/messages/discovery/details/
[iiif-discuss]: https://groups.google.com/forum/#!forum/iiif-discuss
[events]: /event

{% include acronyms.md %}
