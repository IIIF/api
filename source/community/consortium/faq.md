---
title: IIIF Consortium Value and Benefits
id: consortium
layout: spec
---

## Why IIIF?

Scholars increasingly rely on digital image repositories for research, as they contain easily accessible images of important artifacts like manuscripts, paintings, 3D objects, sheet music, newspapers, maps, and other fragile, rare, and heavily studied cultural materials.  Libraries, archives, and museums have been increasingly making their collection materials available to the public digitally, but online assets have essentially been locked into repository-based silos, with incompatible systems and varying user interfaces that place a burden on hosting institutions and limitations on functionality for end-users. Working independently, many institutions have found digital image repositories challenging to maintain, with constantly evolving user needs and ever-changing technology systems as digital content is migrated from one bespoke application to another.

Working together in response to these challenges, the International Image Interoperability Framework (IIIF) [specifications][specs] were developed to provide a standard practice for making digital images available online, allowing for the transfer and sharing of image pixels, metadata, and annotations across repositories and systems. Adoption of the IIIF specifications can provide end-users with the ability to compare images from across multiple repositories and interact with them through deep pan and zoom, image manipulation (size, quality, rotation, etc.), the ability to tag and annotate, search within annotations, and easily share work with others. Several choices of [IIIF-compatible image servers and clients][apps-demos] allow institutions to easily mix and match technologies and maintain their repositories.

## IIIF Consortium and Community

The number of IIIF adopters is growing worldwide, and the benefits of interoperability for digital images will continue to increase as more IIIF-compatible content becomes available. The [IIIF Consortium][iiif-c] (IIIF-C) is group of organizations across the globe committed to supporting the growth and adoption of IIIF. With more than 40 Founding Members, IIIF-C provides continued support for adoption, experimentation, outreach, and a thriving community of libraries, museums, software firms, scholars, and technologists working with IIIF.

The IIIF-C provides sustainability and steering for the IIIF initiative. Membership requires a signed Memorandum of Understanding (MOU) and a $10,000 annual fee to support staffing, strategic direction, training and communication infrastructure, and international events, such as the annual IIIF Conference. As outlined in the IIIF Consortium [MOU][mou], the IIIF-C Executive Committee sets the high-level direction of the IIIF-C.

The IIIF-C is currently accepting additional Founding Members until the close of 2017. Founding Members are the leading organizations that recognize the power and benefits of IIIF and agree to join and help advance the IIIF Consortium and community within the first several years of the founding of the Consortium. Benefits of joining the IIIF-C as a Founding Member include:

* The ability to influence and drive local and community benefits via interoperability by formally supporting and implementing IIIF in its successive versions
* Recognition globally as a leader and Founding Member of IIIF
* Increased visibility among growing global community of IIIF adopters
* Opportunity to shape the IIIF Agenda and Roadmap for future development
* Provide advice and consent on the IIIF Budget & Expense plan
* Special rates for IIIF Conference registration
* Priority attendance at IIIF Working meetings and other [events][iiif-events]
* See additional details in the [IIIF-C MOU][mou]

## Current Members

<ul>
{% for i in site.data.institutions %}
    {% if i.iiifc %}
  <li>
      {% if i.uri %}<a href="{{ i.uri }}">{% endif %}
        {{ i.name }}
      {% if i.uri %}</a>{% endif %}
  </li>
    {% endif %}
{% endfor %}
</ul>

## IIIF Consortium Frequently Asked Questions (FAQs)

### What is IIIF?

* The International Image Interoperability Framework (IIIF) is a set of shared application programming interface (API) specifications for interoperable functionality in digital image repositories. The IIIF is comprised of and driven by a community of libraries, museums, archives, software companies, and other organizations working together to create, test, refine, implement and promote the IIIF specifications. Using JSON-LD, linked data, and standard W3C web protocols such as Web Annotation, IIIF makes it easy to parse and share digital image data, migrate across technology systems, and provide enhanced image access for scholars and researchers. In short, IIIF enables better, faster and cheaper image delivery. It lets you leverage interoperability and the fabric of the Web to access new possibilities and new users for your image-based resources, while reducing long term maintenance and technological lock in. IIIF gives users a rich set of baseline functionality for viewing, zooming, and assembling the best mix of resources and tools to view, compare, manipulate and work with images on the Web, an experience made portable--shareable, citable, and embeddable.

### What are the benefits of IIIF?

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

### What is the IIIF Consortium (IIIF-C)?

 * The IIIF Consortium is a group of institutions committed to providing steering and sustainability for the IIIF initiative. As outlined in the IIIF Consortium [Memorandum of Understanding][mou], the Consortium is comprised of 11 Core Founding Member Institutions, with Additional Founding Members to be added through December 2017. The 11 original Founding Members, plus two additional Founding Members, compose the IIIF-C Executive Committee, which provides high-level direction for the activities of the Consortium, including strategic planning and budgeting, agreements with third parties, growing the membership, and determining by-laws for the operation of the consortium.

### How can my institution join the IIIF Consortium?

 * To join the IIIF-C please send an email expressing interest to Sheila Rabun, IIIF Community and Communications Officer, at srabun@iiif.io. You will be asked to sign and return the IIIF-C [Memorandum of Understanding][mou]. Once a signed MOU has been received, you will receive an invoice for an initial payment of $10,000.

### Why Join the IIIF Consortium?

 * IIIF is a grassroots, community-driven effort that values collaboration and working together to make digital image delivery more effective and sustainable for both institutions and end users. We rely on IIIF-C members to provide leadership and sustainability in support of our shared goals:
    * To give scholars an unprecedented level of uniform and rich access to image-based resources hosted around the world.
    * To define and adopt a set of common application programming interfaces that support interoperability between image repositories.
    * To develop, cultivate and document shared technologies, such as image servers and web clients, that provide a world-class user experience in viewing, comparing, manipulating and annotating images.
 * IIIF-C Membership contributions provide direct funding for supporting staff, training and communications infrastructure, outreach, growth, and adoption of the IIIF initiative.
 * The potential for the use of IIIF and growth of the IIIF community is endless - wherever digital images are present, there is an opportunity for interoperability via IIIF. Lead the effort to expand the benefits of interoperability for all as part of the IIIF-C.
 * Benefits of joining the IIIF-C as a Founding Member include:
    * The ability to influence and drive local and community benefits via interoperability by formally supporting and implementing IIIF in its successive versions
    * Recognition globally as a leader and Founding Member of IIIF
    * Increased visibility among growing global community of IIIF adopters
    * Opportunity to shape the IIIF Agenda and Roadmap for future development
    * Provide advice and consent on the IIIF Budget & Expense plan
    * Special rates for IIIF Conference registration
    * Priority attendance at IIIF Working meetings and other events
    * See additional details in the IIIF-C MOU

### What institutions are part of the IIIF Consortium?

 * See list of IIIF-C institutions above, and on the [IIIF Consortium page][iiif-c].

### Who else is part of the IIIF community?

* The IIIF Community encompasses a large and growing group of interested and active individuals and organizations dedicated to leading and sustaining the IIIF. As a community-driven initiative, IIIF thrives on active discussion, input, and feedback from a wide array of diverse individuals from libraries, museums, cultural heritage institutions, software firms, and other organizations working with digital images and audio/visual materials. We welcome any organization or individual interested in adopting the IIIF, developing software to support it, or giving feedback on the effort to get involved. Participants in all IIIF activities are expected to follow the IIIF [code of conduct][conduct]. The [list of known IIIF community participants][community-list] is always growing.


### What is the difference between the IIIF Consortium and the IIIF community?

 * The IIIF Consortium members have signed a Memorandum of Understanding and are committed to contributing $10,000 per year to support the IIIF initiative. IIIF-C funds and administrative oversight are managed by the Council on Library and Information Resources (CLIR), based in Washington, DC. The wider IIIF community comprises institutions who have implemented IIIF APIs in their collections, software developers and tech firms creating IIIF-compatible software applications, and active participants in community discussions and decision-making.

### Can I request a letter of support from the IIIF Consortium for my IIIF-related grant application?

 * Letters of support from the IIIF-C for IIIF-related grant applications may be requested according to the [IIIF Support for Grant Proposals policy][support-policy].

### What are the current IIIF specifications?

 * [Image API][image]
 * [Presentation API][presentation]
 * [Content Search API][search]
 * [Authentication API][auth]
 * In Progress: [IIIF for Audio/Visual materials][av]

[search]: /api/search/
[presentation]: /api/presentation/
[image]: /api/image/
[support-policy]: /community/policy/support/
[vatican]: /event/2017/vatican/
[apps-demos]: /apps-demos
[specs]: /technical-details/
[mou]: /community/consortium/mou/
[news]: /news/2015/06/17/iiif-consortium/
[iiifc-faq]: /community/consortium/faq
[iiif-c]: /community/consortium
[community-list]: /community/
[auth]: /api/auth/
[av]: /community/groups/av/
[iiif-events]: /event/
[wadm]: https://www.w3.org/TR/2017/REC-annotation-model-20170223/
[conduct]: /event/conduct/
