---
title: "Image API 3.0 Change Log"
title_override: "Changes for IIIF Image API Version 3.0"
id: image-api-30-change-log
layout: spec
cssversion: 3
tags: [specifications, image-api, change-log]
major: 3
minor: 0
patch: 0
pre: beta
redirect_from:
  - /api/image/3.0/change-log-30.html
---

This document is a companion to the [IIIF Image API Specification, Version 3.0][image30]. It describes the changes to the API specification made in this major release, including ones that are backwards incompatible with version 2.1.1, the previous version.

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}


## 1. Breaking Changes

The following changes are backwards incompatible with version 2.1.1 of the Image API.

### 1.1. Image Request Changes

#### 1.1.1. Remove size `full` in favor of `max`

Per the [deprecation warning][image21-full-dep] in the previous version, the value `full` is no longer allowed for the size parameter, `max` must be used instead. See issues [#678](https://github.com/IIIF/api/issues/678) and [#1369](https://github.com/IIIF/api/issues/1369).

#### 1.1.2. Change canonical form of size parameter to _`w,h`_

Per the [deprecation warning][image21-full-dep] and the [inconsistency warning][image21-size-inconsistency] about the size parameter in the previous version, the canonical form of the size parameter is now _`w,h`_ unless `max` is requested. This resolves the inconsistency between the server-preferred values in the `sizes` object, and the canonical form of the size parameter. In order to request preferred sizes, a client should use the `width` and `height` values from `sizes` unmodified to build the _`w,h`_ size to request. See issues [#544](https://github.com/IIIF/api/issues/544) and [#678](https://github.com/IIIF/api/issues/678).

#### 1.1.3. Size parameter value must not scale image to larger than the extracted region

The value of the size parameter must not result in an image larger than the extracted region. Attempts to do so must generate an error response. Previous versions allowed implementations to [optionally support scaling up][image21-size]. The `sizeAboveFull` feature name was also removed. See issues [#693](https://github.com/IIIF/api/issues/693) and [#1370](https://github.com/IIIF/api/issues/1370).

### 1.2. Image Information Changes

Several existing properties were renamed for consistency with the Presentation API, developer convenience, or to better reflect the intended semantics. Some of the semantics were also clarified based on implementation experience during previous versions.

#### 1.2.1. Rename `@id` to `id`, `@type` to `type`

These properties were renamed to enable Javascript developers to use the "dot notation" (`image.id`) instead of the square-brackets based equivalent needed with the `@` character (`image['@id']`). This follows JSON-LD community best practices established by schema.org, the JSON-LD, Web Annotation and Social Web working groups. See issue [#590](https://github.com/IIIF/api/issues/590).

#### 1.2.2. Rename `attribution` to `requiredStatement`, allow `label`+`value`
{: requiredStatement}

The `attribution` property could not specify the label to render with the value, and thus clients typically used "Attribution". This was not able to be internationalized, nor changed in contexts where "Attribution" has specific meaning (such as for artworks, where the attribution is assignment of the creator). The property was renamed to `requiredStatement` to remove the rights-specific semantics, and the structure was changed to allow both `label` and `value` to allow for appropriate labeling with internationalization. See issues [#1287](https://github.com/IIIF/api/issues/1287) and [#1415](https://github.com/IIIF/api/issues/1415).

Additionally, in the [Presentation API][prezi3] and here, a new pattern has been adopted for all textual values of a JSON object with the language code as the key (or `@none` if the language is not known) and the content as a string within an array as the value. This applies only to the `requiredStatement` property in the Image API. The pattern relies on features that have been introduced by the JSON-LD Community Group, and are not yet standardized. See issue [#755](https://github.com/IIIF/api/issues/755).

#### 1.2.3. Rename `license` to `rights`, allow only a single value

The `license` property was renamed to `rights` to accommodate both rights statements and usage licenses. The value is constrained to be a single URI, an array is no longer permitted. The value is further constrained to allow only Creative Commons URIs, RightsStatements.org URIs and URIs registered as extensions. This additional constraint is to allow clients to treat the property as an enumeration rather than free text, and implement URI specific behavior. See issues [#644](https://github.com/IIIF/api/issues/644) and [#1479](https://github.com/IIIF/api/issues/1479).

#### 1.2.4. Require an array of JSON objects for the `logo` property

Previous versions of the specification allowed the `logo` property have a single value or an array value, each with either string or JSON object contents. The value of the `logo` property must now always be an array of JSON objects, even if there is only one object. This reduces the type checking needed on values by clients as they can always iterate over the array, improving the developer experience. See issue [#1131](https://github.com/IIIF/api/issues/1131).

#### 1.2.5. Require the `type` property on all resources, with new values

The `type` property with a single value is now required on all resources, including content resources and services. This serves several purposes, including facilitating object mapping code libraries, and forcing the serialization to generate a JSON object for the resource, not just a string with the resource's URI. The values for `type` have been changed to version-specific strings that avoid the namespace structure, for example from `iiif:Image` in 2.1 to `ImageService3` in 3.0. Note that the `@type` property is used only when referring to object from older specifications such as the Authentication API 1.0.

#### 1.2.6. Change the `profile` property to take one compliance level

The `profile` property must have a single value that is a compliance level string. The property value must not be an array as in previous versions, and features supported beyond those specified are instead described in the new `extraFeatures` property. See issues [#1275](https://github.com/IIIF/api/issues/1275), [#1373](https://github.com/IIIF/api/issues/1373), [#1554](https://github.com/IIIF/api/issues/1554), and [#1013](https://github.com/IIIF/api/issues/1013).

#### 1.2.7. Change the `service` property value to an array of objects

In version 2.1 the value of the `service` property could be a single value or an array of objects, the value must now be an array of objects. See issue [#1131](https://github.com/IIIF/api/issues/1131).

#### 1.2.8. Remove feature names `sizeByWhListed` and `sizeByForcedWh`

Per the [deprecation warning][image21-dep-sizes] in the previous version, the feature names `sizeByWhListed` and `sizeByForcedWh` have been removed. See PR [#727](https://github.com/IIIF/api/pull/727).

#### 1.2.9. Remove feature name `sizeByDistortedWh`

The feature `sizeByWhDistorted` has no useful meaning separate from `sizeByWh` and was thus removed. See issue [#879](https://github.com/IIIF/api/issues/879).

### 1.3. Compliance Requirements

#### 1.3.1. Require support for region `square` at `level1` and `level2` compliance

Support for the region parameter value `square`, introduced in [version 2.1][image21], is now required at `level1` and `level2` [compliance][image30-compliance]. See issue [#501](https://github.com/IIIF/api/issues/501).

#### 1.3.2. No longer require support for `pct:x` size at `level1` compliance

Support for the `pct:x` size form is no longer required at `level1` compliance. This is consistent with the `pct:x,y,w,h` for region as both are now `level2` features. See issue [#478](https://github.com/IIIF/api/issues/478).

### 1.4. External Specifications

#### 1.4.1. Use JSON-LD 1.1

JSON-LD remains the serialization format of the Image API, as it is for the Presentation API. Some features of the JSON-LD Community Group specification make significant improvements to the Presentation API's structure and consistency and are also adopted by the Image API although the impact is much less. While this specification is not a W3C Technical Recommendation at the time of release, the likelihood of the standardization process for JSON-LD 1.1 being successful is extremely high and the advantages have been judged to be worth the risk of unintended incompatibility. See issue [#1192](https://github.com/IIIF/api/issues/1192).


## 2. Non-Breaking Changes

The following changes are backwards compatible with version 2.1.1 of the Image API.

### 2.1. Add notes on extension mechanisms and registry

A new [Extensions][image30-extensions] section describes mechanisms for extension of image requests and the new [Extra Functionality][image30-extra-functionality] section describes how extensions are described in the image information response. The `extraQualities` and `extraFormats` properties have been added to allow description of additional functionality. See issues [#1374](https://github.com/IIIF/api/issues/1374), [#1373](https://github.com/IIIF/api/issues/1373), and [#1435](https://github.com/IIIF/api/issues/1435).

There is now a [registry of known extensions][registry-extensions] to the IIIF specifications, which includes a [registry of Image API extensions][registry-image-extensions]. Extensions intended for community use should be registered in the extensions registry, but registration is not mandatory.

### 2.2. Add `partOf` and `seeAlso` linking properties

Two linking properties also present in the Presentation API were added to the image information. The `seeAlso` property addresses the use case of providing a link to technical metadata, and the `partOf` property supports discovery of a containing Manifest. See issue [#1507](https://github.com/IIIF/api/issues/1507) and [#600](https://github.com/IIIF/api/issues/600).

### 2.3. Define JSON-LD profile for media type

A specific media-type, to be used with the HTTP headers `Accept` and `Content-Type` was defined. This media type is the JSON-LD media type, with the context in the `profile` parameter, following established conventions. See issue [#1066](https://github.com/IIIF/api/issues/1066).


## 3. Editorial Changes

The following changes do not change the Image API behavior from version 2.1.1.

### 3.1. Clarify distinctions between underlying image content, full image, extracted region, and image returned

The [Terminology][image30-terminology] section now explicitly defines **underlying image content** and **full image**. These terms, along with "extracted region" and "image returned" are used to describe the image manipulations more consistently than in previous versions. See issue [#1425](https://github.com/IIIF/api/issues/1425).

### 3.2. Clarify description of the _`!w,h`_ form for the size parameter

Description of the _`!w,h`_ form for the size parameter has been clarified to point out that the returned image must be as large as possible to fit within the _`w,h`_ box subject to constraints of extracted region size and server-imposed limits. See issue [#1372](https://github.com/IIIF/api/issues/1372).

### 3.3. Clarify that the `color` format value might still yield a non-color image

Description of the `color` value of the format parameter has been clarified to make it clear that it is a request for the image with all of its color information. If the underlying image content has no color information then the resulting image will not have any either, even with the `color` format value. See issue [#1375](https://github.com/IIIF/api/issues/1375) and [#1435](https://github.com/IIIF/api/issues/1435).

### 3.4. Change examples to use `https` URIs

All examples now use `https` URIs in order to reflect best practices for interoperable implementations. See issue [#1421](https://github.com/IIIF/api/issues/1421).

### 3.5. Clarify and move discussion of floating point representation

Discussion of floating point representation has been moved from the image requests introduction to the [Canonical URI Syntax][image30-canonical-uri-syntax] section, and has been expanded for clarity. The advice on using at most 10 decimal digits has been removed. Description of `pct` values clarifies these may be either floating point or integer. See issues [#1468](https://github.com/IIIF/api/issues/1468) and [#1240](https://github.com/IIIF/api/issues/1240).

### 3.6. Clarify support for CORS

Discussion of CORS has be moved to a new [CORS][image30-cors-response] section and the wording clarified to make it clear that not only the `Access-Control-Allow-Origin` header but also the preflight request pattern (ie. including the `OPTIONS` header) should be supported. See issue [#1274](https://github.com/IIIF/api/issues/1274).

### 3.7. Clarify that the `@context` value may be a single URI or an array of URIs

The previous version mentioned only the Image API JSON-LD context. The description has been changed to make it clear that the value of `@context` may be either a single URI, or an array with extension context URIs followed by the Image API context URI. See issue [#1472](https://github.com/IIIF/api/issues/1472).

### 3.8. Clarify that a compliance `Link` header may be returned with both Image and Image Information responses

The [description of compliance][image30-compliance-levels] has been changed to note that the compliance level may be given in a HTTP `Link` header on both Image and Image Information responses. See issue [#1365](https://github.com/IIIF/api/issues/1365).

### 3.9. Move implementation notes to a separate document

A new [Image API 3.0 Implementation Notes][image30-implementation-notes] document was created by extracting notes from the appendices of the previous version. An algorithm for handling implementation constraints on maximum sizes with `maxWidth`, `maxHeight` and/or `maxArea` was added. Care has been taken to avoid [RFC 2119][org-rfc-2119] keywords as the implementation notes are not normative. See issues [#928](https://github.com/IIIF/api/issues/928) and [#1427](https://github.com/IIIF/api/issues/1427).

### 3.10. Describe implementation with static web resources

Explicit mention of support for `level0` implementation with pre-generated files was added. The Image API Compliance document has [additional guidance][image30-compliance-level0] on interpretation of `scaleFactors`, `tiles` and `sizes` information at `level0`. See issues [#1231](https://github.com/IIIF/api/issues/1231) and [#1274](https://github.com/IIIF/api/issues/1254).

### 3.11. Add note encouraging adoption of HTTP/2

A new [HTTP Versions][image30-http-versions] section was added to describe issues with many concurrent requests and recommends support for HTTP/2. See issue [#957](https://github.com/IIIF/api/issues/957).

### 3.12. Improve font and style consistency

The use of `code` font and capitalization was made consistent for class names, property names and values when used in prose.


{% include links.md %}
{% include acronyms.md %}
