---
title: Presentation API Use Cases
layout: spec
tags: [presentation-api, use-cases]
redirect_from:
  - /api/presentation/usecases.html
---

## Status of this Document
{:.no_toc}

This document is not subject to [semantic versioning][semver].
Changes will be tracked within the document.

_Copyright © 2012-2014 Editors and contributors. Published by the IIIF under the [CC-BY][cc-by] license._

**Editors**

  * Benjamin Albritton, _Stanford University_
  * Michael Appleby, _Yale University_
  * Robert Sanderson, _Stanford University_
  * Jon Stroop, _Princeton University_
  * Simeon Warner, _Cornell University_
  {: .names}

## Abstract
{:.no_toc}
This document describes use cases that were motivating with respect to the definition of the [IIIF Presentation API][prezi-api].

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Introduction

In order to ensure that the IIIF APIs solved real issues, rather than hypothetical ones that never actually come up in reality, there has been a great deal of discussion focusing on use cases and examples.  This document lists the use cases, and provides a reference document for additional information about them.

## 2. Use Case List

* A medieval manuscript that has had each page digitized, and the user should be able to step from the first page through to the end to view the images
* An early printed book that has had each page digitized and the transcribed text associated with each page.
* A large map where the image depicting it can be zoomed and panned for ease of inspection.
* A digitized newspaper with the text extracted automatically by Optical Character Recognition and linked to the individual line in its depiction
* A photograph, digitized front and back.
* A manuscript that has been disbound and is now separated across different institutions, some of which have digitized their leaves.
* An important diary that has had multiple digitizations over time as technology improves, any of which should be available to the user to compare
* A painting that has been re-used by erasing the original and painting over top of it, where the original artwork can be recovered using modern techniques of multi-spectral imaging.
* A manuscript where different, multi-spectral images of a single page, taken for the text reconstruction, are available to be displayed.
* A letter where pages are known to have existed, but have been lost or still exist but are too fragile to digitize without destroying them.
* Objects that are not basically rectangular.
* A page where only fragments of it remain, and they are not rectangular. These fragments are often digitized together, regardless of the page that they originally came from, and must be able to be associated with the correct pages separately.
* The same fragment, where the text is known from other witnesses, or can be otherwise inferred, which should be associated in the display of the object even though the physical content no longer exists.
* Older projects which only digitized the "interesting" sections of an object, such as the interesting or famous parts. Equivalently, they may have digitized those sections in more detail, and the rest to a lower quality.
* Disagreement between scholars as to the correct reconstruction of an object.
* A score where the music has been transcribed into modern notation, which should be associated with the page in the same way as transcribed text.
* The same score, where the music has been performed and recorded, which should be associated with the page so that the performance can be played to the user.
* Transcription of diagrams, formulae, charts or tables into individual images, or other digitally accessible resources.
* Structured texts, including chapters, sections, verses, books, articles, texts, where the structure is important for navigation around the document.
* Manuscripts that have been re-ordered, intentionally or otherwise, over time and the different sequences of pages are known.
* Books that have had additional fly-leaves or other artifacts added to them over time which are now historically important, but the user should be able to display the object as it was before they were added.
* Pages with foldouts, curtains or other additions that can be dynamically interacted with by the user to experience the different states that the object can be in.
* Multiple transcriptions, editions, translations or other sets of information that should be associated with the digitized object in a coherent and consistent fashion.


## Appendices

### A. Acknowledgements

The production of this document was generously supported by a grant from the [Andrew W. Mellon Foundation][mellon].

Thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### B. Change Log

| Date       | Description                                        |
| ---------- | -------------------------------------------------- |
| 2014-06-01 | Version 1.0 RFC                                    |

   [semver]: {{ site.url }}{{ site.baseurl }}/api/annex/notes/semver/ "Versioning of APIs"
   [cc-by]: http://creativecommons.org/licenses/by/4.0/ "Creative Commons &mdash; Attribution 4.0 International"
   [iiif-discuss]: mailto:iiif-discuss@googlegroups.com "Email Discussion List"
   [prezi-api]: {{ site.url }}{{ site.baseurl }}/api/presentation/{{ site.presentation_api.stable.major }}.{{ site.presentation_api.stable.minor }}/ "Presentation API"
   [iiif-community]: {{page.webprefix}}/community/ "IIIF Community"
   [mellon]: http://www.mellon.org/ "The Andrew W. Mellon Foundation"
[icon-req]: /img/metadata-api/required.png "Required"
[icon-rec]: /img/metadata-api/recommended.png "Recommended"
[icon-opt]: /img/metadata-api/optional.png "Optional"
[icon-na]: /img/metadata-api/not_allowed.png "Not allowed"

{% include acronyms.md %}
