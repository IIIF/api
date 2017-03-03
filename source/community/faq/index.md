---
title: IIIF Frequently Asked Questions (FAQs)
id: consortium
layout: spec
---

## What is IIIF?

* The International Image Interoperability Framework (IIIF) is a set of shared application programming interface (API) specifications for interoperable functionality in digital image repositories. The IIIF is comprised of and driven by a community of libraries, museums, archives, software companies, and other organizations working together to create, test, refine, implement and promote the IIIF specifications. Using JSON-LD, linked data, and standard W3C web protocols such as Web Annotation, IIIF makes it easy to parse and share digital image data, migrate across technology systems, and provide enhanced image access for scholars and researchers. In short, IIIF enables better, faster and cheaper image delivery. It lets you leverage interoperability and the fabric of the Web to access new possibilities and new users for your image-based resources, while reducing long term maintenance and technological lock in. IIIF gives users a rich set of baseline functionality for viewing, zooming, and assembling the best mix of resources and tools to view, compare, manipulate and work with images on the Web, an experience made portable--shareable, citable, and embeddable.

## What are the benefits of IIIF?

IIIF allows for:

 * Advanced, interactive functionality for end users
    * Fast, rich, zoom and pan delivery of images
    * Manipulation of size, scale, region of interest, rotation, quality and format.
    * Annotation - IIIF has native compatibility with the W3C annotation working group’s [Web Annotation Data Model][wadm], which supports annotating content on the Web. Users can comment on, transcribe, and draw on image-based resources using the Web’s inherent architecture.
    * Assemble and use image-based resources from across the Web, regardless of source. Compare pages, build an exhibit, or view a virtual collection of items served from different sites.
    * Cite and Share - IIIF APIs provide motivation for persistence, providing portable views of images and/or regions of images. Cite an image with confidence in stable image URIs, or share it for reference by others--or yourself in a different environment.
 * Support for institutional authentication
    * IIIF is designed to support access control and can leverage existing SSO systems, via the [IIIF Authentication API][auth]
 * System flexibility
   * Use any IIIF-compatible software for viewing, comparing and manipulating images, regardless of the back-end server. Swap parts of the stack at any time, or run multiple components in parallel at once.
 * Easy data transfer and sharing
    * IIIF is standards-based, uses RESTful API construction, JSON-LD, and follows Web patterns, simplifying processes for data migration and sharing
 * Avoidance of vendor lock-in, complicated migrations, and system overhauls
    * IIIF provides the ability to separate image delivery user interfaces from back end data stores, allowing repositories the ability to update image servers and databases without changing front end delivery, or vice versa, avoiding the need to re-architect the entire stack. With an active and growing community of organizations developing and supporting IIIF-compatible technologies, there are plenty of software options to choose from.
 * Reduction of long term total costs
    * A rich ecosystem of interoperable software, including many high quality, open source options, keeps licensing and operational costs low and predictable over time.
 * Combining content from across repositories
    * Unify presentation of content from many different stores (within or outside your institution) without complex or expensive system or data migrations. Bring together content from your institutional DAM, library digital collections, and external sources.
 * Publish once, re-use often
    * Deliver images from your own site for manifold uses; host a single copy and embed in other sites. No need to transfer images to others for them to locally load for one off analysis or republishing.  
 * A thriving global network
    * Join a global network of image suppliers making content available in a common , interoperable framework. Tap a growing suite of software tools and platforms. Maximize the use of your images on the Web. Unlock new potential with interoperability.

## Who else is part of the IIIF community?

* The IIIF Community encompasses a large and growing group of interested and active individuals and organizations dedicated to leading and sustaining the IIIF. As a community-driven initiative, IIIF thrives on active discussion, input, and feedback from a wide array of diverse individuals from libraries, museums, cultural heritage institutions, software firms, and other organizations working with digital images and audio/visual materials. We welcome any organization or individual interested in adopting the IIIF, developing software to support it, or giving feedback on the effort to get involved. Participants in all IIIF activities are expected to follow the IIIF [code of conduct][conduct]. The [list of known IIIF community participants][community-list] is always growing. Additionally, the IIIF Consortium (IIIF-C) provides sustainability and steering for the initiative. For more information about the IIIF-C, see the [Consortium page][iiif-c] and [IIIF-C FAQ][iiifc-faq].

## What are the current IIIF specifications?

 * [Image API][image]
 * [Presentation API][presentation]
 * [Content Search API][search]
 * [Authentication API][auth]
 * In Progress: [IIIF for Audio/Visual materials][av]

[search]: /api/search/
[presentation]: /api/presentation/
[image]: /api/image/
[apps-demos]: /apps-demos
[iiifc-faq]: /community/consortium/faq
[iiif-c]: /community/consortium
[community-list]: /community/
[auth]: /api/auth/
[wadm]: https://www.w3.org/TR/2017/REC-annotation-model-20170223/
[conduct]: /event/conduct/
