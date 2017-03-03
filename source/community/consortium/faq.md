---
title: IIIF Consortium Frequently Asked Questions (FAQs)
id: consortium
layout: spec
---

## Why IIIF?

 * Challenge: Scholars increasingly rely on digital image repositories for research, as they contain easily accessible images of important artifacts like manuscripts, paintings, 3D objects, sheet music, newspapers, maps, and other fragile, rare, and heavily studied cultural materials.  Libraries, archives, and museums have been increasingly making their collection materials available to the public digitally, but online assets have essentially been locked into repository-based silos, with incompatible systems and varying user interfaces that place a burden on hosting institutions and limitations on functionality for end-users. Working independently, many institutions have found digital image repositories challenging to maintain, with constantly evolving user needs and ever-changing technology systems as digital content is migrated from one bespoke application to another.

 * Solution: Working together in response to these challenges, the International Image Interoperability Framework (IIIF) [specifications][specs] were developed to provide a standard practice for making digital images available online, allowing for the transfer and sharing of image pixels, metadata, and annotations across repositories and systems. Adoption of the IIIF specifications can provide end-users with the ability to compare images from across multiple repositories and interact with them through deep pan and zoom, image manipulation (size, quality, rotation, etc.), the ability to tag and annotate, search within annotations, and easily share work with others. Several choices of [IIIF-compatible image servers and clients][apps-demos] allow institutions to easily mix and match technologies and maintain their repositories. For more details on the benefits of IIIF, see the general [IIIF FAQ][iiif-faq].

## What is the IIIF Consortium?

 * The IIIF Consortium is a group of institutions committed to providing steering and sustainability for the IIIF initiative. The number of IIIF adopters is growing worldwide, and the benefits of interoperability for digital images will continue to increase as more IIIF-compatible content becomes available. The [IIIF Consortium][iiif-c] (IIIF-C) is group of organizations across the globe committed to supporting the growth and adoption of IIIF. With more than 40 Founding Members, IIIF-C provides continued support for adoption, experimentation, outreach, and a thriving community of libraries, museums, software firms, scholars, and technologists working with IIIF.

 * As outlined in the IIIF Consortium [Memorandum of Understanding][mou], the Consortium is comprised of 11 Core Founding Member Institutions, with Additional Founding Members to be added through December 2017. The 11 original Founding Members, plus two additional Founding Members, compose the IIIF-C Executive Committee, which provides high-level direction for the activities of the Consortium, including strategic planning and budgeting, agreements with third parties, growing the membership, and determining by-laws for the operation of the consortium.

 * The IIIF-C provides sustainability and steering for the IIIF initiative. Membership requires a signed Memorandum of Understanding (MOU) and a $10,000 annual fee to support staffing, strategic direction, training and communication infrastructure, and international events, such as the annual IIIF Conference. The IIIF-C is currently accepting additional Founding Members until the close of 2017. Founding Members are the leading organizations that recognize the power and benefits of IIIF and agree to join and help advance the IIIF Consortium and community within the first several years of the founding of the Consortium.

## Why Join the IIIF Consortium?

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
     * Priority attendance at IIIF Working meetings and other [events][iiif-events]
     * See additional details in the [IIIF-C MOU][mou]

## How can my institution join the IIIF Consortium?

 * To join the IIIF-C, please send an email expressing interest to Sheila Rabun, IIIF Community and Communications Officer, at srabun@iiif.io. You will be asked to sign and return the IIIF-C [Memorandum of Understanding][mou]. Once a signed MOU has been received, you will receive an invoice for an initial payment of $10,000.

## What institutions are part of the IIIF Consortium?

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

## What is the difference between the IIIF Consortium and the IIIF community?

 * The IIIF Consortium members have signed a Memorandum of Understanding and are committed to contributing $10,000 per year to support the IIIF initiative. IIIF-C funds and administrative oversight are managed by the Council on Library and Information Resources (CLIR), based in Washington, DC. The wider [IIIF community][community-list] comprises institutions who have adopted IIIF APIs in their collections, software developers and tech firms creating IIIF-compatible software applications, and active participants in community discussions, in addition to Consortium members.

## Can I request a letter of support from the IIIF Consortium for my IIIF-related grant application?

 * Letters of support from the IIIF-C for IIIF-related grant applications may be requested according to the [IIIF Support for Grant Proposals policy][support-policy].

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
[iiif-faq]: /community/faq/
