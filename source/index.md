---
title: "API Specifications - International Image Interoperability Framework™"
layout: spec
hero:
  image: ''
api_current_table:
  headers:
    - API
    - Current Version
    - Description
  version: latest
  apis:
    - image
    - presentation
    - auth
    - discovery
    - search
    - content-state
---

## Current specifications

{% include api/api-listing-table.html table=page.api_current_table %}

<!--
## Draft specifications

| API                  | Draft Version (Status) |
| -------------------- | ---------------------- |
{: .api-table}
-->

### Feedback requested
{: #feedback}

We welcome feedback on all IIIF Specifications. Please send any feedback to [iiif-discuss@googlegroups.com][iiif-discuss].
{: .alert}

## Approved extensions

Please see the [Registry of Extensions][registry] for full details on how extensions work and the process for creating them.

Currently, there are two formally published extensions available for use with the Presentation API.

| Presentation API Extensions    | Description |
| ------------------------------ | ----------- |
| [navPlace Extension][navPlace] | This IIIF Presentation 3 API extension defines a new property, navPlace, which is defined by earthbound geographic coordinates in the form of GeoJSON-LD. |
| [Text Granularity Extension][text-granularity] | This extension recommends a pattern for indicating the level of text granularity for an annotation related to optical character recognition (OCR) software, manual transcription, and existing digitized text. |
{: .api-table style="max-width: 780px;"}




## Community translations

| API                | Version | Translation           |
| ------------------ | ------- | --------------------- |
| Image API          | 3.0   | [Japanese][image3-jp], [Chinese][image3-chinese]|
| Image API          | 2.1   | [Japanese][image-jp] |
| Presentation API   | 3.0   | [Chinese] [prezi3-chinese] |
| Presentation API   | 2.1   | [Japanese][prezi-jp] |
| Content Search API | 1.0   | [Japanese][search-jp], [Chinese][contentsearch1-chinese]|
| Authentication API | 1.0   | [Japanese][auth-jp], [Chinese][auth1-chinese] |
| Discovery API      | 1.0   | [Chinese][discovery1-chinese] |
| Content State API  | 0.9   | [Chinese][contentstate-09-chinese] |
|NavPlace Extension  |       | [Chinese][Navplace-chinese]
{: .api-table}

__Translation note__<br/>
Please note that the IIIF community does not guarantee the accuracy of any translation. They are linked to for information purposes only, and any discrepancies with the specifications are unintentional. The English versions of the specifications linked above are the definitive versions.
{: .alert}

## Community cookbook

The [Cookbook][annex-cookbook] gathers together examples of how to create IIIF Presentation API assets, in order to:

* Provide many more examples than the specification alone can do, for reference and learning;
* Encourage publishers to adopt common patterns in modeling classes of complex objects;
* Enable client software developers to support these patterns, for consistency of user experience (when desirable); and
* Demonstrate the applicability of IIIF to a broad range of use cases.

The [Cookbook][annex-cookbook] webpages are under constant development and the list of recipes include links to completed recipes and place holders for future recipes. The community welcomes additions to the [Cookbook][annex-cookbook]. To get started, review the [Cookbook process][recipe-process] and say hello on the Cookbook [Slack][slack] channel.

## Validators


- [Image API validator]({{ site.api_url | absolute_url }}/image/validator/) - A service to validate a IIIF Image API resource against the specification.
- [Presentation API validator]({{ site.api_url | absolute_url }}/presentation/validator/service/) - A service to validate a IIIF Presentation API resource against the specification.

## Older versions

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
| [Search API 1.0][search10] | Published 2016-05-12 |
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
[image3-chinese]: https://www.yuque.com/iiifchina/df4qfk/fwybkl
[prezi3-chinese]: https://www.yuque.com/iiifchina/df4qfk/gpf6od
[auth1-chinese]: https://www.yuque.com/iiifchina/df4qfk/vkxifz
[contentsearch1-chinese]: https://www.yuque.com/iiifchina/df4qfk/ygbnck
[discovery1-chinese]: https://www.yuque.com/iiifchina/df4qfk/hdb26g
[contentstate-09-chinese]: https://www.yuque.com/iiifchina/df4qfk/wysy7i
[navplace-chinese]: https://www.yuque.com/iiifchina/df4qfk/xh0bna

{% include acronyms.md %}
{% include links.md %}
