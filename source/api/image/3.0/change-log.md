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

#### 1.1.1. Size `full` has been removed in favor of `max`

Per the [deprecation warning][image21-full-dep] in the previous version, the value `full` is no longer allowed for the size parameter, `max` must be used instead. See issue [#678](https://github.com/IIIF/api/issues/678).

#### 1.1.2. Canonical form of size parameter changed to _`w,h`_

Per the [deprecation warning][image21-full-dep] and the [inconsistency warning][image21-size-inconsistency] about the size parameter in the previous version, the canonical form of the size parameter is now _`w,h`_ unless `max` is requested. This resolves the inconsistency between the server-preferred values in the `sizes` object, and the canonical form of the size parameter. In order to request preferred sizes, a client simply uses `width` and `height` values from `sizes` to build the _`w,h`_ size to request. See issues [#544](https://github.com/IIIF/api/issues/544) and [#678](https://github.com/IIIF/api/issues/678).

#### 1.1.3. Size parameter value must not scale image to larger than the extracted region

The value of the size parameter must not result in an image larger than the extracted region. Attempts to do so must generate an error response. Previous versions allowed implementations to [optionally support scaling up][image21-size]. The `sizeAboveFull` feature name was also removed. See issue [#693](https://github.com/IIIF/api/issues/693).

### 1.2. Image Information Changes

Several existing properties were renamed for consistency with the Presentation API, developer convenience, or to better reflect the intended semantics. Some of the semantics were also clarified based on implementation experience during previous versions.

#### 1.2.1. Rename `@id` to `id`, `@type` to `type`

These properties were renamed to enable javascript developers to use the "dot notation" (`manifest.id`) instead of the square brackets based equivalent needed with the `@` character (`manifest['@id']`). This follows JSON-LD community best practices established by schema.org, the JSON-LD, Web Annotation and Social Web working groups. See issue [#590](https://github.com/IIIF/api/issues/590).

#### 1.2.2. Rename `attribution` to `requiredStatement`, allow `label`+`value`
{: requiredStatement}

The `attribution` property could not specify the label to render with the value, and thus clients typically used "Attribution". This was not able to be internationalized, nor changed in contexts where "Attribution" has specific meaning (such as for artworks, where the attribution is assignment of the creator). The property was renamed to `requiredStatement` to remove the rights-specific semantics, and the structure was changed to allow both `label` and `value` to allow for appropriate labeling with internationlization. See issue [#1287](https://github.com/IIIF/api/issues/1287).

Additionally, in the [Presentation API][prezi3] and here, a new pattern has been adopted for all textual values of a JSON object with the language code as the key (or `@none` if the language is not known) and the content as a string within an array as the value. This applies only to the `requiredStatement` propery in the Image API. The pattern relies on features that have been introduced by the JSON-LD Community Group, and are not yet standardized. See issue [#755](https://github.com/IIIF/api/issues/755).

#### 1.2.3. Rename `license` to `rights`, allow only a single value

The `license` property was renamed to `rights` to accomodate both rights statements and usage licenses. The value is constrained to be a single URI, an array is no longer permitterd. The value is further constrained to allow only Creative Commons URIs, RightsStatements.org URIs and URIs registered as extensions. This additional constraint is to allow clients to treat the property as an enumeration rather than free text, and implement URI specific behavior. See issues [#644](https://github.com/IIIF/api/issues/644) and [#1479](https://github.com/IIIF/api/issues/1479).

#### 1.2.4. Require an array of JSON objects for the `logo` property

Previous versions of the specification allowed the `logo` property have a single value or an array value, each with either string or JSON object contents. The value of the `logo` property must now always be an array of JSON objects, even if there is only one object. This reduces the type checking needed on values by clients as they can always iterate over the array, improving the developer experience. See issue [#1131](https://github.com/IIIF/api/issues/1131).

#### 1.2.5. The `type` property is required on all resources, with new values

The `type` property with a single value is now required on all resources, including content resources and services. This serves several purposes, including facilitating object mapping code libraries, and forcing the serialization to generate a JSON object for the resource, not just a string with the resource's URI. The values for `type` have been changed to version-specific strings that avoid the namespace structure, for example from `iiif:Image` in 2.1 to `ImageService3` in 3.0. Note that the `@type` property is used only when referring to object from older specifications such as the Authentication API 1.0.

#### 1.2.6. The `profile` property takes one compliance level

The `profile` property must have a single value that is a compliance level string. The property value must not be an array as in previous versions, and features supported beyond those specified are instead described in the new `extraFeatures` property. See issues [#1373](https://github.com/IIIF/api/issues/1373) and [#1554](https://github.com/IIIF/api/issues/1554).

#### 1.2.7. The `service` property value is now an array of objects

In version 2.1 the value of the `service` property could be a single value or an array of objects, the value must now be an array of objects. See issue [#1131](https://github.com/IIIF/api/issues/1131).

#### 1.2.8. Feature names `sizeByWhListed` and `sizeByForcedWh` removed

Per the [deprecation warning][image21-full-dep] in the previous version, the feature names `sizeByWhListed` and `sizeByForcedWh` have been removed. See PR [#727](https://github.com/IIIF/api/pull/727).

#### 1.2.9. Feature name `sizeByDistortedWh` removed

The features `sizeByWhDistorted` hasd no useful meaning separate from `sizeByWh` and was thus removed. See issue [#879](https://github.com/IIIF/api/issues/879).

### 1.3. External Specifications

#### 1.3.1. Use JSON-LD 1.1

JSON-LD remains the serialization format of the Image API, as it is for the Presentation API. Some features of the JSON-LD Community Group specification make significant improvements to the Presentation API's structure and consistency and are also adopted by the Image API although the impact is much less. While this specification is not a W3C Technical Recommendation at the time of release, the likelihood of the standardization process for JSON-LD 1.1 being successful is extremely high and the rewards have been judged to be worth the risk of unintended incompatibility. See issue [#1192](https://github.com/IIIF/api/issues/1192).


## 2. Non-Breaking Changes

The following changes are backwards compatible with version 2.1.1 of the Image API.

### 2.1. Added notes on extension mechanisms and registry

A new [Extensions][image30-extensions] section describes mechanisms for extension of image requests and the new [Extra Functionality][image30-extra-functionality] section describes how extensions are described in the image information response. The `extraQualities` and `extraFormats` properties have been added to allow description of additional functionality. See issues [#1374](https://github.com/IIIF/api/issues/1374), [#1373](https://github.com/IIIF/api/issues/1373), and [#1435](https://github.com/IIIF/api/issues/1435).

There is now a [registry of known extensions][registry-extensions] to the IIIF specifications, which includes a [registry of Image API extensions][registry-image-extensions]. Extensions intended for community use should be registered in the extensions registry, but registration is not mandatory.

### 2.2. Added `partOf` and `seeAlso` linking properties

Two linking properties also present in the Presentation API were added to the image information. The `seeAlso` property addresses the use case of providing a link to technical metadata, and the `partOf` property supports discovery of a containing Manifest. See issue [#1507](https://github.com/IIIF/api/issues/1507) and [#600](https://github.com/IIIF/api/issues/600).

### 2.3. Define JSON-LD profile for media type

A specific media-type, to be used with the HTTP headers `Accept` and `Content-Type` was defined. This media type is the JSON-LD media type, with the context in the `profile` parameter, following established conventions. See issue [#1066](https://github.com/IIIF/api/issues/1066).


## 3. Editorial Changes

The following changes do not change the Image API behavior from version 2.1.1.

#### 3.1. Clarify distinctions between underlying image content, full image, extracted region, and image returned

The [Terminology][image30-terminology] section now explicitly defines **underlying image content** and **full image**. These terms, along with extracted region and image returned are used to describe the image manipulations more consistently than in previous versions. See issue [#1425](https://github.com/IIIF/api/issues/1425).

#### 3.2. Clarify description of the _`!w,h`_ form for the size parameter

Description of the _`!w,h`_ form for the size parameter has been clarified to point out that the returned image must be as large as possible to fit within the _`w,h`_ box subject to constraints of extracted region size and server-imposed limits. See issue [#1372](https://github.com/IIIF/api/issues/1372).

#### 3.3. Clarify that the `color` format value might still yield a non-color image

Description of the `color` value of the format parameter has been clarified to make it clear that it is a request for the image with all of its color information. If the underlying image content has no color information then the resulting image will not have any either, even with the `color` format value. See issue [#1375](https://github.com/IIIF/api/issues/1375) and [#1435](https://github.com/IIIF/api/issues/1435).

#### 3.4. Changed examples to use `https` URIs

All examples now use `https` URIs in order to reflect best practices for interoperable implementations. See issue [#1421](https://github.com/IIIF/api/issues/1421).

#### 3.5. Clarify and move discussion of floating point representation

Discussion of floating point representation has been moved from the image requests introduction to the [Canonical URI Syntax][image30-canonical-uri-syntax] section, and has been expanded for clarity. The advice on using at most 10 decimal digits has been removed. See issue [#1468](https://github.com/IIIF/api/issues/1468).

#### 3.6. Clarify support for CORS

Discussion of CORS has be moved to a new [CORS][image30-cors-response] section and the wording clarified to make it clear that not only the `Access-Control-Allow-Origin` header but also the preflight request pattern (ie. including the `OPTIONS` header) should be supported. See issue [#1274](https://github.com/IIIF/api/issues/1274).

#### 3.7. Implementation with static web resources

Add explicit mention of support for implementation with pre-generated static files.

#### 3.8. Font consistency

The use of `code` font and capitalization was made consistent for class names, property names and values when used in prose.


{% include links.md %}
{% include acronyms.md %}
