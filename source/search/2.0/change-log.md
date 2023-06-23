---
title: "Content Search API 2.0 Change Log"
title_override: "Changes for IIIF Content Search API Version 2.0"
id: content-search-api-20-change-log
layout: spec
cssversion: 3
tags: [specifications, content-search-api, change-log]
major: 2
minor: 0
patch: 0
pre: final
redirect_from:
 - /search/2.0/change-log-20.html
---

This document is a companion to the [IIIF Content Search API Specification, Version 2.0][search20]. It describes the changes to the API specification made in this major release, including ones that are backwards incompatible with [version 1.0][search10], the previous version.


## 1. Breaking Changes

### 1.1. External Specifications

#### 1.1.1. Use JSON-LD 1.1 and the Web Annotation Data Model

The Content Search 2.0 API adopts JSON-LD 1.1 and the Web Annotation Data Model in order to align with the IIIF Presentation 3.0 API. See the [IIIF Presentation 3.0 API Change Log, Section 1.1](https://iiif.io/api/presentation/3.0/change-log/#11-external-specifications) for details.

### 1.2. Property Naming and Semantics Changes

Several existing properties were renamed for consistency, developer convenience, or to better reflect the intended semantics. Some of the semantics were also clarified based on implementation experience from previous versions.

#### 1.2.1. Rename `@id` to `id`, `@type` to `type`

These properties were renamed to enable Javascript developers to use the "dot notation" (`manifest.id`) instead of the square-brackets-based equivalent needed with the @ character (`manifest['@id']`). This follows JSON-LD community best practices established by schema.org, the JSON-LD, Web Annotation and Social Web working groups. See issue [#590](https://github.com/IIIF/api/issues/590).

#### 1.2.2. Rename `within` to `partOf`

While renaming properties, `within` was renamed to `partOf` to follow the same naming convention in ActivityStreams and the Web Annotation Data Model. See issue [#1482](https://github.com/IIIF/api/issues/1482).

#### 1.2.3. Rework the semantics of Responses

With adoption of the Web Annotation Data Model, the Content Search 1.0 API `hits` structure was deprecated in favor of presenting Responses as `items` within an AnnotationPage which provides the set of content annotations that contain the match values. Extended information about the matches (for example when one match requires multiple annotations to display, or when one annotation contains multiple matches) is now presented in the `annotations` structure of the AnnotationPage. See issue [#534](https://github.com/IIIF/api/issues/534).

#### 1.2.4. Update context for new major version

The URI of the context document was updated for the new major version, and thus the value of the `@context` is either the new value http://iiif.io/api/search/2/context.json, or includes this as the last item in an array value. See issue [#2055](https://github.com/IIIF/api/issues/2055).

### 1.3. Property Value Changes

#### 1.3.1. Use language map pattern for label and value

Where the `label` property is used, we have adopted the language map pattern from Prezi3 where the value is a dictionary of language codes, each having an array of string values.

### 1.4. Classes Changes

#### 1.4.1. Rename `TermList` to `TermPage`

In keeping with the patterns of other IIIF Specifications and the Web Annotation Data Model, we rename the Autocomplete `TermList` structure to `TermPage` and the `terms` property to `items`.

#### 1.4.2. Remove `Layer`, `AnnotationList` in favor of `AnnotationCollection`, `AnnotationPage`

With the adoption of the Web Annotation Data Model, we remove the IIIF specific `Layer` in favor of the standard `AnnotationCollection`, and `AnnotationList` in favor of the equivalent `AnnotationPage`. See issue [#2126](https://github.com/IIIF/api/issues/2126).


## 2. Non-Breaking Changes

### 2.1. Additional Features

#### 2.1.1. Add `contextualizing` motivation

A new Annotations motivation `contextualizing` was created to support returning match results within their context, such as when search interfaces display text before and after the matching text in search results. See issue [#2120](https://github.com/IIIF/api/issues/2120).

#### 2.1.2. Include `highlighting` motivation

The Annotations motivation `highlighting` is included in the API to support returning match results as highlighted text, such as when a client may display the entire annotation and highlight the matches within. See issue [#2120](https://github.com/IIIF/api/issues/2120).


## 3. Editorial Changes

### 3.1. Clarifications

#### 3.1.1. Terminology

Added definitions for the terms “embedded” and “referenced” in the IIIF Content Search context. 

#### 3.1.2. Search and Autocomplete Services

The section “Declaring Services” was added to clarify and highlight that the Content Search API comprises two distinct Services, the Search Service and the Autocomplete Service, and how to declare each of these Services.

### 3.2. Style

#### 3.2.1. Restructure document

The document was restructured for clarity, and to remove non-core content that simply described how to make use of external specifications, and especially Web Annotations, to a [cookbook][annex-cookbook] and to the IIIF Registry. This enables additional use cases and patterns to be documented without requiring a new version of the specification to describe something that is already possible. It can be managed by the community, rather than via the more rigorous specification process. See issue [#2053](https://github.com/IIIF/api/issues/2053).

#### 3.2.2. Consistency

The use of code font and capitalization was made consistent for class names, property names and values when used in prose. References to them in lists, especially for implementation requirements, were made consistent.

#### 3.2.3. Examples Improved

The examples were improved to be more intuitive, and cover more of the features available.


{% include acronyms.md %}
{% include links.md %}
