---
title: "API Specifications - International Image Interoperability Framework™"
id: apis
layout: spec
tags: [specifications ]
cssversion: 2
---

## Current Specifications

| API                | Current Version |
| ------------------ | --------------- |
| Authentication API | [{{ site.auth_api.stable.major }}.{{ site.auth_api.stable.minor }}.{{ site.auth_api.stable.patch}}][auth{{ site.auth_api.stable.major }}{{ site.auth_api.stable.minor }}] |
| Image API          | [{{ site.image_api.stable.major }}.{{ site.image_api.stable.minor }}.{{ site.image_api.stable.patch}}][image{{ site.image_api.stable.major }}{{ site.image_api.stable.minor }}] |
| Presentation API   | [{{ site.presentation_api.stable.major }}.{{ site.presentation_api.stable.minor }}.{{ site.presentation_api.stable.patch }}][prezi{{ site.presentation_api.stable.major }}{{ site.presentation_api.stable.minor }}] |
| Search API   | [{{ site.search_api.stable.major }}.{{ site.search_api.stable.minor }}.{{ site.search_api.stable.patch }}][search{{ site.search_api.stable.major }}{{ site.search_api.stable.minor }}] |
{: .api-table}

## Draft Specifications

| API                | Draft Version (Status) |
| ------------------ | ---------------------- |
| Image API          | [3.0.0 ALPHA][image30] |
| Presentation API   | [3.0.0 ALPHA][prezi30] |
| Change Discovery API | [0.2.0][discovery02] |
{: .api-table}

__Feedback Requested__<br/>
We welcome feedback on all IIIF Specifications. In particular, we are actively seeking feedback on the Image API and Presentation API version 3.0 draft specifications. Please send any feedback to [iiif-discuss@googlegroups.com][iiif-discuss].
{: .alert}

## Community Translations

| API                | Version | Translation           |
| ------------------ | ------- | --------------------- |
| Image API          | 2.1     | [Japanese][image-jp]  |
| Presentation API   | 2.1     | [Japanese][prezi-jp]  |
| Search API         | 1.0     | [Japanese][search-jp] |
| Authentication API | 1.0     | [Japanese][auth-jp]   |
{: .api-table}

__Translation Note__<br/>
Please note that the IIIF community does not guarantee the accuracy of any translation. They are linked to for information purposes only, and any discrepancies with the specifications are unintentional. The English versions of the specifications linked above are the definitive versions.
{: .alert}

## Older Versions

Current IIIF specifications _SHOULD_ be used for all new work. Old versions are retained for reference and are listed below. Technical resources and reference implementations of older versions are _NOT_ guaranteed to be maintained across new major versions.

| Old API Version            | Notes |
| -------------------------- | ----- |
| [Authentication API 0.9.4][auth094] | Published 2016-10-05 |
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

IIIF Specifications are created and published following the [IIIF Editorial Process][editorial-process].

[image-jp]: http://www.asahi-net.or.jp/~ax2s-kmtn/ref/iiif/apiimage2.1.html
[prezi-jp]: http://www.asahi-net.or.jp/~ax2s-kmtn/ref/iiif/apipresentation2.1.html
[search-jp]: http://www.asahi-net.or.jp/~ax2s-kmtn/ref/iiif/searchapi1.0.html
[auth-jp]: http://www.asahi-net.or.jp/~ax2s-kmtn/ref/iiif/apiauthentication1.0.html


[iiif-discuss]: mailto:iiif-discuss@googlegroups.com "Email Discussion List"
[image30]: {{ site.url }}{{ site.baseurl }}/api/image/3.0/ "Image API v3.0 ALPHA"
[image21]: {{ site.url }}{{ site.baseurl }}/api/image/2.1/ "Image API v2.1"
[image20]: {{ site.url }}{{ site.baseurl }}/api/image/2.0/ "Image API v2.0"
[image11]: {{ site.url }}{{ site.baseurl }}/api/image/1.1/ "Image API v1.1"
[image10]: {{ site.url }}{{ site.baseurl }}/api/image/1.0/ "Image API v1.0"
[prezi30]: {{ site.url }}{{ site.baseurl }}/api/presentation/3.0/ "Presentation API v3.0 ALPHA" 
[prezi21]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/ "Presentation API v2.1"
[prezi20]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.0/ "Presentation API v2.0"
[meta10]: {{ site.url }}{{ site.baseurl }}/api/metadata/1.0/ "Metadata API v1.0"
[meta09]: {{ site.url }}{{ site.baseurl }}/api/metadata/0.9/ "Metadata API v0.9"
[auth10]: {{ site.url }}{{ site.baseurl }}/api/auth/1.0/ "Authentication API v1.0"
[auth094]: {{ site.url }}{{ site.baseurl }}/api/auth/0.9/ "Authentication API v0.9.4"
[search10]: {{ site.url }}{{ site.baseurl }}/api/search/1.0/ "Search API v1.0"
[search09]: {{ site.url }}{{ site.baseurl }}/api/search/0.9/ "Search API v0.9"
[discovery02]: {{ site.url }}{{ site.baseurl }}/api/discovery/0.2/ "IIIF Change Discovery API"
[notes]: {{ site.url }}{{ site.baseurl }}/api/annex/ "Implementation Notes"
[editorial-process]: {{ page.webprefix }}/community/policy/editorial/ "IIIF Editorial Process"

{% include acronyms.md %}
