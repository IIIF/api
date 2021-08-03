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
| Image API          | [{{ site.image_api.stable.major }}.{{ site.image_api.stable.minor }}.{{ site.image_api.stable.patch}}][image{{ site.image_api.stable.major }}{{ site.image_api.stable.minor }}] (2020-06-03)|
| Presentation API   | [{{ site.presentation_api.stable.major }}.{{ site.presentation_api.stable.minor }}.{{ site.presentation_api.stable.patch }}][prezi{{ site.presentation_api.stable.major }}{{ site.presentation_api.stable.minor }}] (2020-06-03)|
| Authentication API | [{{ site.auth_api.stable.major }}.{{ site.auth_api.stable.minor }}.{{ site.auth_api.stable.patch}}][auth{{ site.auth_api.stable.major }}{{ site.auth_api.stable.minor }}] (2017-01-19)|
| Change Discovery API | [{{ site.discovery_api.stable.major }}.{{ site.discovery_api.stable.minor }}.{{ site.discovery_api.stable.patch }}][discovery{{ site.discovery_api.stable.major }}{{ site.discovery_api.stable.minor }}] (2021-06-22)|
| Content Search API | [{{ site.search_api.stable.major }}.{{ site.search_api.stable.minor }}.{{ site.search_api.stable.patch }}][search{{ site.search_api.stable.major }}{{ site.search_api.stable.minor }}] (2016-05-12)|
{: .api-table}


## Draft Specifications

| API                  | Draft Version (Status) |
| -------------------- | ---------------------- |
| Content State API    | [0.9.0][contentstate09]|
{: .api-table}

__Feedback Requested__<br/>
We welcome feedback on all IIIF Specifications. Please send any feedback to [iiif-discuss@googlegroups.com][iiif-discuss].
{: .alert}

## Community Translations

| API                | Version | Translation           |
| ------------------ | ------- | --------------------- |
| Image API          | [3.0][image3-jp], [2.1][image-jp] | Japanese |
| Presentation API   | [2.1][prezi-jp] | Japanese |
| Search API         | [1.0][search-jp] | Japanese |
| Authentication API | [1.0][auth-jp] | Japanese |
{: .api-table}

__Translation Note__<br/>
Please note that the IIIF community does not guarantee the accuracy of any translation. They are linked to for information purposes only, and any discrepancies with the specifications are unintentional. The English versions of the specifications linked above are the definitive versions.
{: .alert}

## Community Cookbook

The [Cookbook][annex-cookbook] gathers together examples of how to create IIIF Presentation API assets, in order to:

 * Provide many more examples than the specification alone can do, for reference and learning;
 * Encourage publishers to adopt common patterns in modeling classes of complex objects;
 * Enable client software developers to support these patterns, for consistency of user experience (when desirable); and
 * Demonstrate the applicability of IIIF to a broad range of use cases.

The [Cookbook][annex-cookbook] webpages are under constant development and the list of recipes include links to completed recipes and place holders for future recipes. The community welcomes additions to the [Cookbook][annex-cookbook]. To get started, review the [Cookbook process][recipe-process] and say hello on the Cookbook [Slack][slack] channel. 

## Older Versions

Current IIIF specifications _SHOULD_ be used for all new work. Old versions are retained for reference and are listed below. Technical resources and reference implementations of older versions are _NOT_ guaranteed to be maintained across new major versions.

| Old API Version            | Notes |
| -------------------------- | ----- |
| [Authentication API 0.9.4][auth094] | Published 2016-10-05 |
| [Change Discovery API 0.9.2][discovery09] | Published 2021-04-28 |
| [Image API 2.1][image21]   | Published 2016-05-12, updated 2017-06-09 |
| [Image API 2.0][image20]   | Published 2014-09-11 |
| [Image API 1.1][image11]   | Published 2013-09-17 |
| [Image API 1.0][image10]   | Published 2012-08-10 |
| [Presentation API 2.1][prezi21] | Published 2016-05-12, updated 2017-06-09 |
| [Presentation API 2.0][prezi20] | Published 2014-08-12 |
| [Metadata API 1.0][meta10] | "Metadata API" was replaced with the Presentation API, published 2013-09-16 |
| [Metadata API 0.9][meta09] | Draft of the "Metadata API", published 2013-06-11 |
| [Search API 0.9][search09] | Draft published 2016-04-11 |
{: .api-table}

## Notes

IIIF also has a series of [Implementation Notes][annex-notes] which are not subject to the same process as formal APIs but may be useful to implementers.

## Process

IIIF Specifications are created and published following the [IIIF Editorial Process][editorial-process].

[image3-jp]: http://www.asahi-net.or.jp/~ax2s-kmtn/ref/iiif/apiimage3.0.html
[image-jp]: http://www.asahi-net.or.jp/~ax2s-kmtn/ref/iiif/apiimage2.1.html
[prezi-jp]: http://www.asahi-net.or.jp/~ax2s-kmtn/ref/iiif/apipresentation2.1.html
[search-jp]: http://www.asahi-net.or.jp/~ax2s-kmtn/ref/iiif/searchapi1.0.html
[auth-jp]: http://www.asahi-net.or.jp/~ax2s-kmtn/ref/iiif/apiauthentication1.0.html

{% include acronyms.md %}
{% include links.md %}
