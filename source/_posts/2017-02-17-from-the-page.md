---
title: Full IIIF Support for Collaborative Digital Editions in FromThePage
author: Ben Brumfield and Sara Carlstead Brumfield, Brumfield Labs
date: 2017-02-17
tags: [announcements ]
layout: post
---

Thanks to a commissioned implementation grant, Brumfield Labs has implemented full client-side and server-side support for IIIF in the collaborative digital edition tool FromThePage. IIIF support allows editors to focus on textual issues instead of image format challenges, whether they run public-facing crowdsourced transcription projects or scholarly translation projects within small research groups.

Using FromThePage’s IIIF client functionality, editorial projects can build transcription, translation, and indexing projects on documents from any IIIF repository, importing manifests directly into the collaborative platform. This eliminates the need for editors to upload zip files or PDFs, valuable not only because it reduces tedium, but also because it allows editors to work with material that cannot be released in high-resolution images but can be served as tiles through the [IIIF Image API][iiif-image].

For projects whose images have been uploaded directly to FromThePage, whether bulk uploads of zip files or images uploaded directly from mobile devices in the field, IIIF server functionality allows reuse within the ecosystem of IIIF scholarly tools. Both the Image API and the [IIIF Presentation API][iiif-prezi] allow other clients like the Universal Viewer or Mirador to display FromThePage documents for presentation and annotation. Transcriptions, translations, and comments created within FromThePage are exposed as AnnotationLists and Layers, so there is no need for additional exports for scholarly reuse.

FromThePage is an open source tool supported by Brumfield Labs, and can be downloaded at [https://github.com/benwbrum/fromthepage][fromthepage]. Hosted FromThePage accounts are available at [FromThePage.com][fromthepage.com]. A demo video is available at [https://www.youtube.com/watch?v=92Blut3l2ds][demo]

[iiif-image]: /api/image/
[iiif-prezi]: /api/presentation/
[fromthepage]: https://github.com/benwbrum/fromthepage
[fromthepage.com]: http://fromthepage.com/
[demo]: https://www.youtube.com/watch?v=92Blut3l2ds
