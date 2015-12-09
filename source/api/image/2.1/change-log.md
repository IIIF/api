---
title: "Image API 2.1 Change Log"
title_override: "Changes for IIIF Image API Version 2.1"
id: image-api-21-change-log
layout: spec
tags: [specifications, image-api, change-log]
major: 2
minor: 1
# no patch
pre: final
---

This document is a companion to the [IIIF Image API Specification, Version 2.1][api-21]. It describes the significant changes to the API since [Version 2.0][api-20]. The changes are broken into two groups: [Non-breaking Changes][non-breaking-changes], i.e. those that are backwards compatible from client or server perspectives; and [Deferred Changes][deferred-changes], i.e. those that will be made in a future iteration of the Image API.

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## Non-breaking Changes

### Add Rights, Logo and Attribution Information

### Add `square` region

### Tie to Authentication Specification

## Deferred Changes

### Add Compression 

A recommendation was made to allow compression to be specified in the image URL in order to obtain a compressed representation of the image.  The motivation was bandwidth management, such as for mobile or rural areas where access is limited.  The change was deferred until a future version of the API to allow extra time to gather use cases and requirements, as no consensus was reached as to how this could be accomplished.  No proposal introduced a backwards incompatibility, and hence this feature can be introduced without a new major version.

[api-21]: /api/image/2.1/ "Image API 2.1"
[api-compliance]: /api/image/2.0/#compliance-levels "Image API 6. Compliance Levels"
[api-20]: /api/image/2.0/ "Image API 2.0"
[non-breaking-changes]: #non-breaking-changes "Image API 2.0 Non-reaking Changes"
[deferred-changes]: #deferred-changes "Deferred Changes"

{% include acronyms.md %}
