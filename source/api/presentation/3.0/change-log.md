---
title: "Presentation API 2.1.1 Change Log"
title_override: "Changes for IIIF Presentation API Version 2.1.1"
id: presentation-api-211-change-log
layout: spec
tags: [specifications, presentation-api, change-log]
major: 2
minor: 1
patch: 1
pre: final
redirect_from:
  - /api/presentation/2.1/change-log-211.html
---

This document is a companion to the [IIIF Presentation API Specification, Version 2.1.1][prezi-api]. It describes the editorial changes to the API specification made in this patch release, such as clarifications and typo corrections. It also describes corrections to related documents that are not [semantically versioned][semver], such as example resources and resources to manage transformation to and from the JSON-LD serialization.

For the significant changes between 2.0 and 2.1, please see the [2.1 Change Log][changelog-21].

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## 1. Editorial Changes

### 1.1. Clarify use of `viewingHint`

Not all of the `viewingHint` values were clearly described as to which resources they could be used with. The validity was clarified and the descriptions improved.
See issue [#878](https://github.com/IIIF/iiif.io/issues/878)

### 1.2. Clarify if Canvas id should be dereferencable

The text of the document said that the id MAY be able to be dereferenced, whereas the summary table said SHOULD. The summary table was updated to reflect the normative text. This issue does not set a precedent for changing to SHOULD or even MUST in future major versions.
See issue [#884](https://github.com/IIIF/iiif.io/issues/884)

### 1.3. Use better URIs for example rights/licenses

The URIs were not helpful in giving realistic examples. The examples were updated to use Creative Commons and Rights Statements URIs to promote the use of shared agreements.
See issue [#960](https://github.com/IIIF/iiif.io/issues/960)

### 1.4. Clarify use of non-rectangular region annotations

The description of non-rectangular regions confusingly talked about rectangular regions at the same time.  The description was improved, including better links.
See issue [#941](https://github.com/IIIF/iiif.io/issues/941)

### 1.5. Update references to other specifications

The introduction referred to a "future specification", meaning the Search API. The reference was updated now that API is available.
See issue [#1003](https://github.com/IIIF/iiif.io/issues/1003)

### 1.6. Clarify ranges without children are permitted

The specification was clear that empty Collections are possible but was not obvious whether the same was true of Ranges (a Range with no child Ranges or Canvases).  This was clarified as possible, with the same proviso that this is discouraged without careful thought. 
See issue [#1016](https://github.com/IIIF/iiif.io/issues/1016)

### 1.7. Expand thumbnail examples to promote good practice

The examples that included thumbnails did not include information about the thumbnail representation, which would be valuable to viewing applications.  The examples were updated to promote better practice.
See issue [#1098](https://github.com/IIIF/iiif.io/issues/1098)

### 1.8. Update deprecation warning for Ranges

The discussions about Ranges in the Audio-Visual work has led to a proposal for a significantly more consistent and functional representation in a future version of the Presentation API.  The deprecation warning for `canvases` and `ranges` was made less specific to not assume any particular conclusion from those discussions.
See issue [#1118](https://github.com/IIIF/iiif.io/issues/1118)

### 1.9. Typos for `ContentAsText`

There were several typos for `ContentAsText` in the example JSON documents. These were corrected.
See issue [#1139](https://github.com/IIIF/iiif.io/issues/1139)

### 1.10. Typos for Image Profile URI

There were two typos for the Image Profile URI that included an extra `profiles` path component. These were corrected.  See issue [#1170](https://github.com/IIIF/iiif.io/issues/1170)


## 2. Changes to Non-Semantically-Versioned Documents

These changes were scheduled to coincide with the release of 2.1.1 to benefit from a shared deadline, but are not managed in the same way as the main specification documents with respect to versioning.

### 2.1. Context

#### 2.1.1. Missing Search API terms

The terms for `exact`, `prefix` and `suffix` were missing from both the Search and Presentation context documents. They were added to the Presentation context to ensure availability.
See issue [#952](https://github.com/IIIF/iiif.io/issues/952)

#### 2.1.2. Unnecessary types prevent compaction

The intended-to-be-helpful types provided in the context such as `ViewingHint` and `ViewingDirection` instead just prevented the values from being compacted correctly when these types were not asserted. The types were removed to make this easier.
See issue [#946](https://github.com/IIIF/iiif.io/issues/946)

#### 2.1.3. Choice options should always be a set

The specifications were not clear as to how to represent a single option other than the default, whether it should be a list with a single item, or just the item. This is clarified that it should always be a list, and the context updated to add `@container: @set` to the definition.
See issue [#1120](https://github.com/IIIF/iiif.io/issues/946)

### 2.2. Frames should use `@explicit` to ensure correct summaries

The frame documents used `@embed: false` for referenced resources such as an external AnnotationList.  This meant that only the URI was included, but not `@type` or `label`. The solution was to use `@explicit` to list the set of terms that should be included.
See issue [#959](https://github.com/IIIF/iiif.io/issues/959)

### 2.3. Fixtures

#### 2.3.1. Fixture 6 did not have multiple descriptions

The fixture example for multiple descriptions did not actually have multiple descriptions.  The bug in the generation software was fixed that was stripping the second description.
See issue [#1122](https://github.com/IIIF/iiif.io/issues/1122)

#### 2.3.2. Fixture 64 had unnecessary array

The fixture object had an array around a single description, which made it incompatible with the JSON-LD framing algorithm. 
See issue [#1123](https://github.com/IIIF/iiif.io/issues/1123)

#### 2.3.3. Fixture 65 had typo for startCanvas

The fixture for `startCanvas` instead had the pre-2.0 use of `start_canvas` before snake and camel case were reconciled.  This was corrected.
See issue [#1125](https://github.com/IIIF/iiif.io/issues/1125)
 
[prezi-api]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/ "Presentation API 2.1"
[prezi-api-20]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.0/ "Presentation API 2.0"
[changelog-21]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.1/change-log.html "Presentation API 2.1 Change Log"
[semver]: {{ site.url }}{{ site.baseurl }}/api/annex/notes/semver/ "Note on Semantic Versioning"

{% include acronyms.md %}
