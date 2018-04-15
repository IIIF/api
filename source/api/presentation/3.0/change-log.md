---
title: "Presentation API 3.0 Change Log"
title_override: "Changes for IIIF Presentation API Version 3.0"
id: presentation-api-30-change-log
layout: spec
cssversion: 2
tags: [specifications, presentation-api, change-log]
major: 3
minor: 0
patch: 0
pre: final

redirect_from:
  - /api/presentation/3.0/change-log-30.html
---

This document is a companion to the [IIIF Presentation API Specification, Version 3.0][prezi-api]. It describes the changes to the API specification made in this major release, including ones that are backwards incompatible with version 2.1.1, the previous version.


## Table of Contents
{:.no_toc}

* Goes Here
{:toc}


## 1. Breaking Changes

### 1.1. Property Name Changes

#### 1.1.1. Rename `@id` to `id`

#### 1.1.2. Rename `@type` to `type`

#### 1.1.3. Rename `viewingHint` to `behavior`

#### 1.1.4. Rename `within` to `partOf`

#### 1.1.5. Rename `startCanvas` to `start`

#### 1.1.6. Rename `contentLayer` to `supplementary`

#### 1.1.7. Rename structural properties to `items`

And remove class specific structural properties

#### 1.1.8. Rename `attribution` to `requiredStatement`

And see 1.2.1

#### 1.1.9. Rename `license` to `rights`

And see 1.2.2.

#### 1.1.10. Rename `description` to `summary`

And see 1.2.3.

#### 1.1.11. Rename `related` to `homepage`

And see 1.2.4.

### 1.2. Property Value Changes

#### 1.2.1. Allow label and value for `requiredStatement`

#### 1.2.2. Require controlled values for `rights`

#### 1.2.3. Short snippet text for `summary`

And see 1.2.5.

#### 1.2.4. Use `homepage` for only preferred homepage

And put other previously related resources in `metadata`

#### 1.2.5. Allow long texts in `metadata`

#### 1.2.6. Allow non-images in `thumbnail`

#### 1.2.7. Use language map feature for `label`, `value`, `summary`

#### 1.2.8. Always require arrays if property can have multiple values

#### 1.2.9. Canvases always include AnnotationPages, not Annotations directly

#### 1.2.10. Change requirements for `navDate` value

#### 1.2.11. Require JSON Object for all non-enumerable resources


### 1.3. Property Requirements Changes

#### 1.3.1. Establish client requirements per property

#### 1.3.2. Canvas should have `label`

#### 1.3.3. ...


### 1.4. Classes Changes

#### 1.4.1. Remove Sequence in favor of Ranges and `items`

#### 1.4.2. Remove Layer in favor of AnnotationCollection

#### 1.4.3. Remove AnnotationList in favor of AnnotationPage

#### 1.4.4. Remove paging functionality


### 1.5. External Specification Changes

#### 1.5.1. Use Web Annotation Data Model

#### 1.5.2. Move "advanced" Annotation features to cookbook



## 2. Non-Breaking Changes

### 2.1. New Properties

#### 2.1.1. Add `posterCanvas` for associated content

#### 2.1.2. Add `language` on external resources

#### 2.1.3. Add `duration` on Canvas

#### 2.1.4. Add `timeMode` on Annotation

#### 2.1.5. Add explicit definition of `profile`


### 2.2. New Values

#### 2.2.1 Add "auto-advance" for `behavior`

#### 2.2.2. Add "no-nav" for `behavior`

#### 2.2.3. Add "hidden" for `behavior`

#### 2.2.4. Add "repeat" for `behavior`

#### 2.2.5. Add "sequence" for `behavior`

#### 2.2.6. Add "thumbnail-nav" for `behavior`

#### 2.2.7. Add "together" for `behavior`

#### 2.2.8. Add "unordered" for `behavior`

#### 2.2.9. Add "transcribing" for `motivation`


### 2.3. Additional Modeling Features

#### 2.3.1. Allow Canvases to be treated as Content Resources


### 2.4. Protocol Features

#### 2.4.1. Define json-ld profile for media type

#### 2.4.2. Recommend HTTPS

#### 2.4.3. Remove URI pattern recommendations

#### 2.4.4. Allow external Ranges


## 3. Editorial Changes


### 3.1. Clarifications

#### 3.1.1. Clarify "referenced" and "embedded"


### 3.2. Style

#### 3.2.1. Improve icons in requirements tables

#### 3.2.2. Restructure document sections

#### 3.2.3. Use https for all examples

#### 3.2.4. Consistency of Language



## 4. Related Document Changes

### 4.1. Establish Registries for Extensions

### 4.2. Establish Cookbook of Implementation Patterns

### 4.3. Update Design Patterns

### 4.4. Establish new Annotation Selectors

### 4.5. Update JSON-LD Contexts and Frames


[prezi-api]: {{ site.url }}{{ site.baseurl }}/api/presentation/3.0/ "Presentation API 3.0"
[semver]: {{ site.url }}{{ site.baseurl }}/api/annex/notes/semver/ "Note on Semantic Versioning"

{% include acronyms.md %}
