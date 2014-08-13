---
title: IIIF Image and Presentation API Final Drafts Released
author: Robert Sanderson, Jon Stroop, Simeon Warner
date: 2014-08-12
tags: [specifications, image-api, presentation-api, announcements]
layout: post
---

After an additional month of public testing and feedback, the IIIF Editors are pleased to announce final draft revisions of the International Image Interoperability Framework Image and Presentation (formerly 'Metadata') API specifications.

 * [IIIF Image API 2.0.0-final-draft](/api/image/2.0/)
 * [IIIF Presentation API 2.0.0-final-draft](/api/presentation/2.0/)

Since the release of the previous drafts only a small number of changes have been made:

### Image API

 * Added Google's webp as an optional format [ [Changes](https://github.com/IIIF/iiif.io/pull/297) \| [Discussion](https://github.com/IIIF/iiif.io/issues/295) ]
 * Changed the canonical URI syntax to use `w,` for images that are scaled maintaining their aspect ratio.
 * Clarified the repeatability of scale_factor and width/height for tiles in info.json


### Presentation API

 * Viewing Hints:
   * Changed viewing hints to be URIs, and thus extensions must also be URIs, following the features in the Image API (and just good practice).
   * Changed the `start` viewing hint to a relationship from the Sequence to the first Canvas to be displayed to avoid issues with  multiple Sequences with different start Canvases. 
   * Clarified the `non-paged` viewing hint's usage to be ignored when encountered within a Sequence or Manifest that is _not_ `paged`.
 * Clarified the expectations for http and non-http URIs.
 * Defined the representation for a Layer if it is dereferenced.


### Tools and Infrastructure Support

In addition, tools to aid in the creation and testing of conforming applications and systems are being implemented and added to the iiif.io website.  These include validators for the Image and Presentation APIs:

 * [Image API Validator](http://iiif.io/api/image/validator/)
 * [Presentation API Validator](http://iiif.io/api/presentation/validator/)

Reference implementations of the Image API and collections of fixture Manifests for the Presentation API:

 * [2.0 Reference Implementation](http://iiif.io/api/image/2.0/example/reference/67352ccc-d1b0-11e1-89ae-279075081939/)
 * [Valid Manifest Collection](http://iiif.io/api/presentation/2.0/example/fixtures/collection.json)
 * [Invalid Manifest Collection](http://iiif.io/api/presentation/2.0/example/fixtures/collection.json)

These will continue to be developed, but are ready for testing and comment before the release of the final versions of the specifications.


As always, we welcome your feedback, questions, and use cases, and encourage you to submit them to the [IIIF Discussion Listserv](mailto:{{ site.data.organization.email }}). Comments on the current drafts are still welcomed for the next two weeks, with a view to releasing the final version of the specifications at the beginning of September.


Sincerely,

The IIIF Image and Presentation API Editors
Benjamin Albritton
Michael Appleby
Robert Sanderson
Stuart Snydman
Jon Stroop
Simeon Warner

