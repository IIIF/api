---
title: IIIF Image and Presentation API Second Drafts Released
author: Robert Sanderson, Jon Stroop, Simeon Warner
date: 2014-07-01
tags: [specifications, image-api, presentation-api, announcements]
layout: post
---

After a month of public testing and feedback, the IIIF Editors are pleased to announce second draft revisions of the International Image Interoperability Framework Image and Presentation (formerly 'Metadata') API specifications.

 * [IIIF Image API 2.0.0-draft2](/api/image/2.0/)
 * [IIIF Presentation API 2.0.0-draft2](/api/presentation/2.0/)

Since the release of the first drafts. a few significant changes have been made:

### Image API

 * Added `services` to info.json [ [Changes](https://github.com/IIIF/iiif.io/commit/801e9e1628f34c77001d2b151df8efb88e1c688a) \| [Discussion](https://groups.google.com/d/msg/iiif-discuss/4rp3OvK0jtI/Gow0pF45bMIJ) ]
 * Added mirroring option to rotation syntax [ [Changes](https://github.com/IIIF/iiif.io/commit/93869af7e4fee290c044392e0858d1805cf26e80) \| [Discussion](https://groups.google.com/forum/#!topic/iiif-discuss/J7u9cyKZKU4) ]
 * Added clarification of `default` quality [ [Changes](https://github.com/IIIF/iiif.io/commit/dd54d7dfaf4bd2b5ade8b1ab16b8ada8687eb7bb) ] and rotation/background [ [Changes](https://github.com/IIIF/iiif.io/commit/b2d6bfe59bd3fdbe3147c88333d2c922f4caf1d6) \| [Discussion](https://groups.google.com/forum/#!topic/iiif-discuss/AnXBvw_gVI0) ]
 * Expanded `info.json` descriptions [ [Changes](https://github.com/IIIF/iiif.io/commit/044da46a2eea17374f2604036bd4c066788cf95b) ]
 * Clarified and cleanly separated information about support for tiles vs. support for preferred sizes in `info.json` [ [Changes](https://github.com/IIIF/iiif.io/commit/15c8445403d8ed72f300f8a3da6de2ce05cc8475) \| [Discussion](https://groups.google.com/forum/#!topic/iiif-discuss/YOAAcALqoAE) ]


### Presentation API

* Added server side rotation option with iiif:ImageApiSelector [ [Changes](https://github.com/IIIF/iiif.io/commit/f94fda233731b4140a922ee673f09fd2f04dc053) \| [Discussion](https://groups.google.com/forum/#!topic/iiif-discuss/k2Lu6INn5KM) ]
* Improved JSON to RDF mapping [ [Changes](https://github.com/IIIF/iiif.io/commit/522f1664f244d3a6f35b05db4d66a7833b9b6bd2) ]
* Minor Clarifications:
  * Cannot reference locations outside of a Canvas
  * Reduced focus on presenting digitized physical objects
  * Explicit definition of physical scale algorithm

As always, we welcome your feedback, questions, and use cases, and encourage you to submit them to the [IIIF Discussion Listserv](mailto:{{ site.data.organization.email }}). Drafts will be kept open for comment until the beginning of August, with the goal of final release in September. However, we would appreciate feedback early in order to work on and gain consensus for any necessary changes.

Sincerely,

The IIIF Image and Presentation API Editors
Benjamin Albritton
Michael Appleby
Robert Sanderson
Stuart Snydman
Jon Stroop
Simeon Warner

cc:
code4lib@listserv.nd.edu
dlf-announce@lists.clir.org
iiif-announce@googlegroups.com
iiif-discuss@googlegroups.com
libdevconx@mailman.stanford.edu
lod-lam@googlegroups.com
