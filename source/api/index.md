---
title: "IIIF API Specifications"
id: apis
layout: spec
tags: [specifications ]
cssversion: 2
---

## Current Specifications

| API                | Current Version |
| ------------------ | --------------- |
| Image API          | [{{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }}.{{ site.image_api.latest.patch}}][image{{ site.image_api.latest.major }}{{ site.image_api.latest.minor }}] |
| Presentation API   | [{{ site.presentation_api.latest.major }}.{{ site.presentation_api.latest.minor }}.{{ site.presentation_api.latest.patch }}][prezi{{ site.presentation_api.latest.major }}{{ site.presentation_api.latest.minor }}] |
| Search API   | [{{ site.search_api.latest.major }}.{{ site.search_api.latest.minor }}.{{ site.search_api.latest.patch }}][search{{ site.search_api.latest.major }}{{ site.search_api.latest.minor }}] |
{: .api-table}

## Draft Specifications

| API                | Draft Version (Status)     |
| ------------------ | ---------------------------- |
| Authentication API | [0.9.1][auth09] *(Beta draft)* |
{: .api-table}


__Feedback Requested__<br/>
We welcome feedback on all IIIF Specifications. In particular, we are actively seeking implementations and feedback on the Authentication API draft specification. Please send any feedback to [iiif-discuss@googlegroups.com][iiif-discuss].
{: .alert}

## Community Translations

| API              | Version | Translation           |
| ---------------- | ------- | --------------------- |
| Image API        | 2.1     | [Japanese][image-jp]  |
| Presentation API | 2.1     | [Japanese][prezi-jp]  |
| Search API       | 1.0     | [Japanese][search-jp] |
{: .api-table}

__Translation Note__<br/>
Please note that the IIIF community does not guarantee the accuracy of any translation. They are linked to for information purposes only, and any discrepancies with the specifications are unintentional. The English versions of the specifications linked above are the definitive versions.
{: .alert}

## Older Versions

Current IIIF specifications _SHOULD_ be used for all new work. Old versions are retained for reference and are listed below.

| Old API Version            | Notes |
| -------------------------- | ----- |
| [Image API 2.0][image20]   | Published 2014-09-11 |
| [Image API 1.1][image11]   | Published 2013-09-17 |
| [Image API 1.0][image10]   | Published 2012-08-10 |
| [Presentation API 2.0][prezi20] | Published 2014-08-12 |
| [Metadata API 1.0][meta10] | "Metadata API" was replaced with the Presentation API, published 2013-09-16 |
| [Metadata API 0.9][meta09] | Draft of the "Metadata API", published 2013-06-11 |
| [Search API 0.9][search09] | Draft published 2016-04-11 |
{: .api-table}

## Notes

IIIF also has a series of [Implementation Notes][notes] which are not subject to the same process as formal APIs but may be useful to implementers.

## Process

IIIF Specifications are created and published following the [IIIF Editorial Process][editors].

[image-jp]: http://www.asahi-net.or.jp/~ax2s-kmtn/ref/iiif/apiimage2.1.html
[prezi-jp]: http://www.asahi-net.or.jp/~ax2s-kmtn/ref/iiif/apipresentation2.1.html
[search-jp]: http://www.asahi-net.or.jp/~ax2s-kmtn/ref/iiif/searchapi1.0.html

[iiif-discuss]: mailto:iiif-discuss@googlegroups.com "Email Discussion List"
[image21]: /api/image/2.1/ "Image API v2.1"
[image20]: /api/image/2.0/ "Image API v2.0"
[image11]: /api/image/1.1/ "Image API v1.1"
[image10]: /api/image/1.0/ "Image API v1.0"
[prezi21]: /api/presentation/2.1/ "Presentation API v2.1"
[prezi20]: /api/presentation/2.0/ "Presentation API v2.0"
[meta10]: /api/metadata/1.0/ "Metadata API v1.0"
[meta09]: /api/metadata/0.9/ "Metadata API v0.9"
[auth09]: /api/auth/0.9/ "Authentication API v0.9"
[search10]: /api/search/1.0/ "Search API v1.0"
[search09]: /api/search/0.9/ "Search API v0.9"
[notes]: /api/annex/ "Implementation Notes"
[editors]: /api/annex/notes/editors/ "IIIF Editorial Process"

{% include acronyms.md %}
