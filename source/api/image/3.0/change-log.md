---
title: "Image API 3.0 Change Log"
title_override: "Changes for IIIF Image API Version 3.0"
id: image-api-30-change-log
layout: spec
cssversion: 2
tags: [specifications, image-api, change-log]
major: 3
minor: 0
patch: 0
pre: beta
redirect_from:
  - /api/image/3.0/change-log-30.html
---

This document is a companion to the [IIIF Image API Specification, Version 3.0][image-api]. It describes the editorial changes to the API specification made in this major release, including ones that are backwards incompatible with version 2.1.1, the previous version. 

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}


## 1. Breaking Changes

### 1.1. External Specifications

#### 1.1.1. Use JSON-LD 1.1

JSON-LD remains the serialization format of the Image API, as it is for the Presentation API. Some features of the JSON-LD Community Group specification make a significant improvements to the Presentation API's structure and consistency and are also adopted by the Image API although the impact is much less. While this specification is not a W3C Technical Recommendation at the time of release, the likelihood of the standardization process for JSON-LD 1.1 being successful is extremely high and the rewards have been judged to be worth the risk of unintended incompatibility. See issue [#1192](https://github.com/IIIF/api/issues/1192).

### 1.2. Property Naming, Value, and Semantics Changes

Several existing properties were renamed for consistency with the Presentation API, developer convenience, or to better reflect the intended semantics. Some of the semantics were also clarified based on implementation experience during previous versions.

#### 1.2.1. Rename `@id` to `id`, `@type` to `type`

These properties were renamed to enable javascript developers to use the "dot notation" (`manifest.id`) instead of the square brackets based equivalent needed with the `@` character (`manifest['@id']`). This follows JSON-LD community best practices established by schema.org, the JSON-LD, Web Annotation and Social Web working groups. See issue [#590](https://github.com/IIIF/api/issues/590).

#### 1.2.2. Rename `attribution` to `requiredStatement`, allow `label`+`value`
{: requiredStatement}

The `attribution` property could not specify the label to render with the value, and thus clients typically used "Attribution". This was not able to be internationalized, nor changed in contexts where "Attribution" has specific meaning (such as for artworks, where the attribution is assignment of the creator). The structure was changed to allow both `label` and `value`, following `metadata` entries, to solve this and the property renamed to remove the rights-specific semantics. See issue [#1287](https://github.com/IIIF/api/issues/1287).

Additionally, in the [Presentation API][prezi3-api] a new pattern has been adopted for all textual values of a JSON object with the language code as the key (or `@none` if the language is not known) and the content as a string within an array as the value. This applies only to the `requiredStatement` propery in the Image API. The pattern relies on features that have been introduced by the JSON-LD Community Group, and are not yet standardized. See issue [#755](https://github.com/IIIF/api/issues/755).

#### 1.2.5. Rename `license` to `rights`, allow only a single value

The `license` property was renamed to the more general `rights` to accomodate both rights statements and usage licenses. The value was constrained to be a single URI, an array is no longer permitterd. The value was further constrained to allow only Creative Commons URIs, RightsStatements.org URIs and URIs registered as extensions. This additional constraint is to allow clients to treat the property as an enumeration rather than free text, and implement URI specific behavior. See issues [#644](https://github.com/IIIF/api/issues/644) and [#1479](https://github.com/IIIF/api/issues/1479).

#### 1.2.6. Always require an array of JSON objects for the `logo` property

Previous versions of the specification allowed the `logo` property have a single value or an array value, each with either string or JSON object contents. The value of the `logo` property must now always be an array of JSON objects, even if there is only one object. This reduces the type checking needed on values by clients as they can always iterate over the array, improving the developer experience. See issue [#1131](https://github.com/IIIF/api/issues/1131).

#### 1.2.7. Requirements for `type`

The `type` (or `@type`) property with a single value is now required on all resources, including content resources and services. This serves several purposes, including facilitating object mapping code libraries, and forcing the serialization to generate a JSON object for the resource, not just a string with the resource's URI. The `@type` property is used only when referring to object from older specifications such as the Authentication API 1.0.


## 2. Non-Breaking Changes

#### 2.3.1. Define JSON-LD profile for media type

A specific media-type, to be used with the HTTP headers `Accept` and `Content-Type` was defined. This media type is the JSON-LD media type, with the context in the `profile` parameter, following established conventions. See issue [#1066](https://github.com/IIIF/api/issues/1066).


## 3. Editorial Changes

### 3.1. Clarifications

#### 3.1.1 Add explicit definition of `profile` -- FIXME -- DOES THIS APPLY?

In previous versions, `profile` was mentioned but never formally defined. This has now been defined explicitly. See issue [#1276](https://github.com/IIIF/api/issues/1276).

### 3.2. Style

#### 3.2.2. Consistency

The use of `code` font and capitalization was made consistent for class names, property names and values when used in prose.

#### 3.2.3. Visual Appearance

The CSS and icons used in the requirements tables were improved.


## 4. Related Document Changes

### 4.1. Establish Registries for Extensions

### 4.2. Establish Cookbook of Implementation Patterns

### 4.3. Update Design Patterns

### 4.4. Establish new Annotation Selectors

### 4.5. Update JSON-LD Contexts and Frames

[image-api]: {{ site.url }}{{ site.baseurl }}/api/image/3.0/ "Image API 3.0"
[semver]: {{ site.url }}{{ site.baseurl }}/api/annex/notes/semver/ "Note on Semantic Versioning"
     
{% include acronyms.md %}
