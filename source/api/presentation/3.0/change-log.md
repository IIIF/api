---
title: "Presentation API 3.0 Change Log"
title_override: "Changes for IIIF Presentation API Version 3.0"
id: presentation-api-30-change-log
layout: spec
cssversion: 3
tags: [specifications, presentation-api, change-log]
major: 3
minor: 0
patch: 0
pre: final
redirect_from:
  - /api/presentation/3.0/change-log-30.html
---

This document is a companion to the [IIIF Presentation API Specification, Version 3.0][prezi30]. It describes the changes to the API specification made in this major release, including ones that are backwards incompatible with [version 2.1.1][prezi21], the previous version.

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}


## 1. Breaking Changes

### 1.1. External Specifications

#### 1.1.1. Use JSON-LD 1.1

JSON-LD remains the core serialization of the Presentation API. For version 3.0, some features of the JSON-LD Community Group specification make a significant improvement to the API's structure and consistency. While this specification is not a W3C Technical Recommendation at the time of release, the likelihood of the standardization process being successful is extremely high and the rewards have been judged to be worth the minimal risk of unintended incompatibility. Scoped contexts, language sets, and the ability to use `@none` in language maps make implementation significantly easier. See issue [#1192](https://github.com/IIIF/api/issues/1192).

#### 1.1.2. Use Web Annotation Data Model

Annotations remain a core feature of the Presentation API. Instead of the community specified Open Annotation model, version 3.0 adopts the W3C standard Web Annotation Data Model. The practical effects are limited but real, including changes to property names and classes. See issue [#496](https://github.com/IIIF/api/issues/496).


### 1.2. Property Naming and Semantics Changes

Several existing properties were renamed for consistency, developer convenience, or to better reflect the intended semantics. Some of the semantics were also clarified based on implementation experience during previous versions.

#### 1.2.1. Rename `@id` to `id`, `@type` to `type`

These properties were renamed to enable javascript developers to use the "dot notation" (`manifest.id`) instead of the square brackets based equivalent needed with the `@` character (`manifest['@id']`). This follows JSON-LD community best practices established by schema.org, the JSON-LD, Web Annotation and Social Web working groups. See issue [#590](https://github.com/IIIF/api/issues/590).

#### 1.2.2. Rename `viewingHint` to `behavior`

The `viewingHint` property was renamed to `behavior` as it was felt this more accurately reflected the intent, and avoids the image specific "viewing" which would be inappropriate for audio only content. As `viewingDirection` is inherently spatial, it was not renamed. The "hint" part was removed as some behaviors are very important to respect. See issue [#1073](https://github.com/IIIF/api/issues/1073).

#### 1.2.3. Rename `attribution` to `requiredStatement`, allow `label`+`value`

The `attribution` property could not specify the label to render with the value, and thus clients typically used "Attribution". This was not able to be internationalized, nor changed in contexts where "Attribution" has specific meaning (such as for artworks, where the attribution is assignment of the creator). The structure was changed to allow both `label` and `value`, following `metadata` entries, to solve this and the property renamed to remove the rights-specific semantics. See issue [#1287](https://github.com/IIIF/api/issues/1287).

#### 1.2.4. Consolidate structural properties to `items` where possible

The Presentation API classes in version 2.1.1 had both `members` to allow for mixed class lists (e.g. a Range can include both Canvases and other Ranges) and properties that were class specific. The `members` properties were renamed to `items` to follow the pattern established in the Web Annotation Data Model and ActivityStreams. The class specific properties were removed completely as insufficient to cover important use cases, and no longer necessary. See issue [#1145](https://github.com/IIIF/api/issues/1145).

#### 1.2.5. Rename `license` to `rights`

The `license` property was renamed to the more general `rights` to accomodate both rights statements and usage licenses. The value was further constrained to allow only Creative Commons URIs, RightsStatements.org URIs and URIs registered as extensions. This additional constraint is to allow clients to treat the property as an enumeration rather than free text, and implement URI specific behavior.  See issues [#644](https://github.com/IIIF/api/issues/644) and [#1479](https://github.com/IIIF/api/issues/1479)

#### 1.2.6. Rename `description` to `summary`

The `description` property was renamed to `summary` and the semantics changed to be a short descriptive text. The new property is a replacement for the content in `metadata`, for situations when a a table of label/value pairs is too much to render. Descriptions that are not short descriptive text are now recorded in `metadata` to allow for appropriate labeling. See issue [#1242](https://github.com/IIIF/api/issues/1242) and entry [1.3.1][prezi30-changelog-long-texts] below.

#### 1.2.7. Rename `related` to `homepage`

Similar to the above changes where non-actionable links and content are put into `metadata`, the `related` property was renamed to `homepage` with more specific semantics of being the home page of the resource. Links to other resources instead go in to `metadata` as HTML. As the intent is to be able to allow `homepage` specific UI affordances, such as an icon, the cardinality was reduced to zero or one. See issues [#1286](https://github.com/IIIF/api/issues/1286) and [#1484](https://github.com/IIIF/api/issues/1484).

#### 1.2.8. Rename `contentLayer` to `supplementary`

With the removal of the `Layer` class in favor of the standard `AnnotationCollection`, and the introduction of the `motivation` value `supplementing`, the `contentLayer` property was renamed to `supplementary`. This conveys that the Annotations in the Annot ation Collection are those with the `motivation` value `supplementing` while avoiding the use of the defunct class name. See issues [#1480](https://github.com/IIIF/api/issues/1480) and [#1174](https://github.com/IIIF/api/issues/1174). 

#### 1.2.9. Rename `startCanvas` to `start`, allow reference to part of a Canvas

Following the pattern of removing class names from property names when unnecessary, combined with the change that the referenced resource might be part of a Canvas rather than the entire Canvas, the property was renamed. The increased scope for parts of Canvases is to allow jumping to a specific time point within a Canvas with a `duration` property. See [#1320](https://github.com/IIIF/api/issues/1320).

#### 1.2.10. Rename `within` to `partOf`

While renaming properties, `within` was renamed to `partOf` to follow the same naming convention in ActivityStreams and the Web Annotation Data Model. See issue [#1482](https://github.com/IIIF/api/issues/1482).

### 1.3. Property Value Changes

#### 1.3.1. Allow long texts in `metadata` values
{: #long-texts}

Several use cases were raised for long texts that were not descriptions, such as bibliography citation lists or provenance histories for artworks. These texts did not have a home in the previous versions, as `metadata` only allowed short values and `description` was a description of the object not information about it. The adopted solution was to allow long texts within `metadata` values, also allowing `description` to be made more specifically a short textual summary. See issue [#1270](https://github.com/IIIF/api/issues/1270)

#### 1.3.2. Allow non-images in `thumbnail`

The semantics of `thumbnail` were changed to allow for non-image content resources such as short audio or video files. This is important with the addition of time-based media being painted into Canvases. See issue [#1176](https://github.com/IIIF/api/issues/1176).

#### 1.3.3. Use language map pattern for `label`, `value`, `summary`

A new pattern has been adopted for all textual values of a JSON object with the language code as the key (or `@none` if the language is not known) and the content as a string within an array as the value.  This pattern is much easier to implement and use than the previous `@value` / `@language` tuples pattern. The pattern relies on features that have been introduced by the JSON-LD Community Group, and are not yet standardized. See issue [#755](https://github.com/IIIF/api/issues/755).

#### 1.3.4. Always require arrays if property can have multiple values

Previous versions allowed a property that allowed multiple values to express a single value without an array. From version 3.0, if a property can ever have multiple values, then the value of the property is always an array. This reduces the type checking needed on values by clients as they can always iterate over the array, improving the developer experience. See issue [#1131](https://github.com/IIIF/api/issues/1131).

#### 1.3.5. Require JSON object for all non-enumerable resources

Similarly, to reduce type checking, all resources where the URIs cannot be enumerated (such as behaviors, viewing directions, rights statements and so forth) must be expressed as a JSON object with at least the `id` and `type` properties. This further reduces the type checking needed, as previously it could have been just the URI as a string.  See issue [#1284](https://github.com/IIIF/api/issues/1284).

#### 1.3.6. Canvases always include AnnotationPages, not Annotations directly

For consistency, and to allow all content to be external to the Manifest, all Annotations are now only included via `AnnotationPage` resources. This is a change from previous versions, where image Annotations were included directly to Canvases using `images`. See issue [#1068](https://github.com/IIIF/api/issues/1068).

#### 1.3.7. Change requirements for `navDate` value

Previous, the value of `navDate` was required to be in the UTC timezone. However this meant that the navigation date text generated was sometimes not the same date as the resource due to when midnight occurs in the local timezone versus in UTC. The solution adopted was to allow any timezone to be given in the value. See issue [#1296](https://github.com/IIIF/api/issues/1296). 

### 1.4. Classes Changes

#### 1.4.1. Remove Sequence in favor of Ranges and `items`

There has been a long outstanding question of how the order of Canvases in the `items` of Ranges and the order in the current Sequence interact. With further implementations from outside of the initial library-oriented domain, the need for an explicit order for views is also greatly decreased. The initial use case of multiple orderings for the content remains valid, but an edge case that can be supported using other patterns rather than requiring every Manifest to have an explicitly named Sequence. The model is simplified and clarified by this removal. See issues [#1471](https://github.com/IIIF/api/issues/1471), [#1489](https://github.com/IIIF/api/issues/1489) and further issues referenced from those.

#### 1.4.2. Ranges 

In previous versions, it was unclear whether Ranges were intended to capture the extent of the content or simply the hierarchy. This is particularly important with time-based media, as the intent is not to skip between the navigation entry points when rendering the Range, but instead to play continuously. However a Range that captures the discrete sections of newspaper pages that make up an article does not include all of the intervening content.  This difference was reconciled by requiring Ranges to include all and only Canvases or segments of Canvases that are strictly part of the Range. At the same time, the structure was made easier to process by embedding child ranges within the parent, rather than referencing within a flat list.
See issue [#1070](https://github.com/IIIF/api/issues/1070) and the referenced documentation.

#### 1.4.3. Remove Layer, AnnotationList in favor of AnnotationCollection, AnnotationPage

With the adoption of the Web Annotation Data Model, we remove the IIIF specific Layer in favor of the standard AnnotationCollection and AnnotationList in favor of the equivalent AnnotationPage. See issue [#496](https://github.com/IIIF/api/issues/496).

#### 1.4.4. Remove paging functionality

As the Web Annotation Data Model defines the paging model, and Collection paging was neither implemented nor especially different from simply having a hierarchy of Collections, paging functionality was removed from the API. This simplifies the model at no cost. See issue [#1343](https://github.com/IIIF/api/issues/1343).

#### 1.4.5. Move "advanced" Annotation features to cookbook

The number of possible uses of the Web Annotation Data Model within the context of the Presentation API is extremely high.  The previous section 6 of version 2.0 and 2.1 was removed in favor of entries in a "cookbook" that could be expanded and adapted over time, rather than as a specification process. This separation makes new use cases easier to accomodate and describe solutions for, without producing new minor versions of the specification.

### 1.5. Requirements Changes

#### 1.5.1. Establish client requirements per property

It was previously unclear which properties clients were required to process, and which could be left unimplemented without severely affecting the user experience of resources that made use of the properties. Requirements have been added per class/property combination. See issues [#1243](https://github.com/IIIF/api/issues/1243) and [#1271](https://github.com/IIIF/api/issues/1271)

#### 1.5.2. Canvas should have `label`

Not every view of an object has a defined label, or can have one automatically generated. As such, in order to conform with the previous requirement that Canvases _MUST_ have labels, implementers were adding empty or invisible labels as a workaround. In version 3.0, `label` on Canvas is only _RECOMMENDED_ rather than _REQUIRED_. See issue [#964](https://github.com/IIIF/api/issues/964)

#### 1.5.3. ...

There

Must 

Be

More 

Changes

Like

This?


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



[prezi30-changelog-long-texts]: #long-texts

{% include acronyms.md %}
{% include links.md %}
