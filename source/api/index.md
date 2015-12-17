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
| Presentation API   | [{{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }}.{{ site.image_api.latest.patch }}][prezi{{ site.image_api.latest.major }}{{ site.image_api.latest.minor }}] |
{: .api-table}

## Draft Specifications

| API                | Draft Version (Status)     |
| ------------------ | ---------------------------- |
| Image API          | [2.1.0][image21] *(Beta draft)* |
| Presentation API   | [2.1.0][prezi21] *(Beta draft)* |
| Authentication API | [0.9.1][auth09] *(Beta draft)* |
| Search API         | [0.9.1][search09] *(Beta draft)* |
{: .api-table}

__Feedback Requested__
We welcome feedback on all IIIF Specifications. In particular, we are actively seeking implementations and feedback on beta draft specifications. Please send any feedback to [iiif-discuss@googlegroups.com][iiif-discuss].
{: .alert}

## Old Versions

Current IIIF specifications _SHOULD_ be used for all new work. Old versions are retained for reference and are listed below.

| Old API Version            | Notes |
| -------------------------- | ----- |
| [Image API 1.1][image11]   | Published 2013-09-17 |
| [Image API 1.0][image10]   | Published 2012-08-10 |
| [Metadata API 1.0][meta10] | "Metadata API" was replaced with the Presentation API, published 2013-09-16 |
| [Metadata API 0.9][meta09] | Draft of the "Metadata API", published 2013-06-11 |
{: .api-table}

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
[search09]: /api/search/0.9/ "Search API v0.9"

{% include acronyms.md %}
