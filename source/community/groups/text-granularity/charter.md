---
title: "IIIF Text Granularity Technical Specification Group Charter"
layout: spec
tags: []
cssversion: 2
---


## Introduction

Many IIIF images have associated text either from OCR, text transcriptions or annotations. As the development of the [IIIF Search API][search] matures, the desire to make use of the text in specific ways has arisen. The granularity of the text needed, however, varies depending on the use cases.

### Giving access to text as paragraphs, lines and words

**Use case:** I would like to share multiple versions of the same annotation list from a Newspaper page with different specificities, so for example I might have:

* a word level annotation list for harvesting by Europeana where the aggregator would like to offer word level highlighting for search results.
* a line level annotation list for use in Mirador as word level annotation lists can be large for a big newspaper page and reducing the amount of JSON objects can lead to a smoother user experience.
* a paragraph annotation list for OCR correction where the user wants to have a single box to correct rather than a box per line or word.

I would like to be able to link to these options to allow the client to decide which ones they want to use. The source format for the text in the Newspaper page maybe ALTO and creating the serialisations above could be done on the fly.

This group will define the terms and usage of granularity levels using the use cases defined in [IIIF-Stories][stories]. A number of relevant stories are below:

* [Access to illustrations; granularity or motivation?][illustrations]
* [Access the OCR text at a specific granularity][ocr]

Relevant github issues where this has been discussed previously:

* [Granularity search parameter][gran-search]
* [Annotation lists with different specificities][anno]

## Scope

This group will focus on text associated with IIIF images. Text may be OCR, transcription, or other defined text with coordinate information. The group will test static implementations describing the granularity of multiple annotation lists as a proof of concept, then make recommendations and test implementation of granularity selection in the IIIF Search API.

If successful, the work will enable an increased use of text with IIIF, [eliminate the need for an ALTO API][alto], and provide a common vocabulary to refine granularities of text returned.
Relevant use cases will be collected in [IIIF-Stories][stories] using the text-granularity label.

### Anticipated Activities / Deliverables

* Defined granularity parameters
* Develop example annotations lists for different granularities to be used as test fixtures
* Prototype API implementations that provide access to different granularities
* Provide recommendation and testing for API(s)
* Recommendation of where to maintain granularity recommendations and other deliverables, including documentation and examples

## Estimated Timeline

* Q2 2017: Group established, work commences
* Q2 2017: Gather Use Cases;
* Q3 2017: Draft granularity description guidelines and demo implementations
* Q4 2017: Evaluation of dynamic granularity
* Q1 2018: Draft Search API recipe/extension to specify granularity & demo implementations
* Q2 2018: Guidelines ready to be included in relevant specifications

## Communication Channels

* Github Repository: [IIIF-Stories][stories]
* Slack: [# text-granularity][text-slack]
* Email: [IIIF-Discuss][iiif-discuss]; subject line: [granularity]
* Face to face: Annual Conference and Working Group meetings, plus as incidental travel allows
* Calls: Initially bi-weekly, plus standing updates/feedback on Technical Call
    * Online: [https://stanford.zoom.us/j/375412551][zoom]
    * Phone: see [international numbers][international-zoom] - Enter Meeting ID: 375412551, Participant ID: #

## Community Support

### Organizations

* ALTO Board
* Bavarian State Library
* Berlin State Library
* Bibliothèque nationale de France
* Cornell University
* Digirati
* Europeana
* Loyola University Maryland
* National Library of Wales
* Oxford University, Digital Bodleian Library
* Pennsylvania State University Libraries
* Princeton University
* Saint Louis University
* University of Alberta
* University of Toronto
* Yale Center for British Art

### Technical Editors

* Mike Appleby
* Tom Crane
* Rob Sanderson
* Simeon Warner


[text-slack]: https://iiif.slack.com/messages/text-granularity/details/
[iiif-discuss]: https://groups.google.com/forum/#!forum/iiif-discuss
[design-principles]: http://iiif.io/api/annex/notes/design_patterns/
[editorial-process]: http://iiif.io/api/annex/notes/editors/
[av-gist]: https://docs.google.com/document/d/1X7b7zQGDsiEvAfvb1WboDXe360mz7Zmm0o0LT43nozk/edit
[zoom]: https://stanford.zoom.us/j/375412551
[stories]: https://github.com/IIIF/iiif-stories/issues/
[illustrations]: https://github.com/IIIF/iiif-stories/issues/79
[ocr]: https://github.com/IIIF/iiif-stories/issues/77
[gran-search]: https://github.com/IIIF/iiif.io/issues/764
[anno]: https://github.com/IIIF/iiif.io/issues/758
[search]: /api/search/
[alto]: https://github.com/altoxml/schema/issues/33
[international-zoom]: https://zoom.us/zoomconference

{% include acronyms.md %}
