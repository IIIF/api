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
 /presentation/3.0/change-log-30.html
---

This document is a companion to the [IIIF Presentation API Specification, Version 3.0][prezi30]. It describes the changes to the API specification made in this major release, including ones that are backwards incompatible with [version 2.1.1][prezi21], the previous version.


## 1. Breaking Changes

### 1.1. External Specifications

#### 1.1.1. Use JSON-LD 1.1

JSON-LD remains the core serialization of the Presentation API. For version 3.0, some features of the JSON-LD Community Group specification make a significant improvement to the API's structure and consistency. While this specification is not a W3C Technical Recommendation at the time of release, the likelihood of the standardization process being successful is extremely high and the rewards have been judged to be worth the minimal risk of unintended incompatibility. Scoped contexts, language sets, and the ability to use `@none` in language maps make implementation significantly easier. See issue [#1192](https://github.com/IIIF/api/issues/1192).

#### 1.1.2. Use Web Annotation Data Model

Annotations remain a core feature of the Presentation API. Instead of the community specified Open Annotation model, version 3.0 adopts the W3C standard Web Annotation Data Model. The practical effects are limited but real, including changes to property names and classes, and introducing some slight inconsistencies between IIIF properties and Web Annotation Data Model properties. See issue [#496](https://github.com/IIIF/api/issues/496), [#1764](https://github.com/IIIF/api/issues/1764).

### 1.2. Property Naming and Semantics Changes

Several existing properties were renamed for consistency, developer convenience, or to better reflect the intended semantics. Some of the semantics were also clarified based on implementation experience from previous versions.

#### 1.2.1. Rename `@id` to `id`, `@type` to `type`

These properties were renamed to enable Javascript developers to use the "dot notation" (`manifest.id`) instead of the square-brackets-based equivalent needed with the `@` character (`manifest['@id']`). This follows JSON-LD community best practices established by schema.org, the JSON-LD, Web Annotation and Social Web working groups. See issue [#590](https://github.com/IIIF/api/issues/590).

#### 1.2.2. Rename `viewingHint` to `behavior`

The `viewingHint` property was renamed to `behavior` as it was felt this more accurately reflected the intent, and avoids the image specific "viewing" which would be inappropriate for audio only content. As `viewingDirection` is inherently spatial, it was not renamed. The "hint" part was removed as some behaviors are very important to respect. See issue [#1073](https://github.com/IIIF/api/issues/1073).

#### 1.2.3. Rename `attribution` to `requiredStatement`, allow `label`+`value`

The `attribution` property could not specify the label to render with the value, and thus clients typically used "Attribution". This was not able to be internationalized, nor changed in contexts where "Attribution" has specific meaning (such as for artworks, where the attribution is assignment of the creator). The structure was changed to allow both `label` and `value`, following `metadata` entries, to solve this and the property renamed to remove the rights-specific semantics. See issue [#1287](https://github.com/IIIF/api/issues/1287).

#### 1.2.4. Consolidate structural properties to `items` where possible

The Presentation API classes in version 2.1.1 had both `members` to allow for mixed class lists (e.g. a Range can include both Canvases and other Ranges) and properties that were class specific. The `members` properties were renamed to `items` to follow the pattern established in the Web Annotation Data Model and ActivityStreams. The class specific properties were removed completely as insufficient to cover important use cases, and no longer necessary. See issue [#1145](https://github.com/IIIF/api/issues/1145).

#### 1.2.5. Rename `license` to `rights`

The `license` property was renamed to the more general `rights` to accommodate both rights statements and usage licenses. The value was further constrained to allow only `http` Creative Commons URIs, `https` RightsStatements.org URIs, and any URI registered as an extension. This additional constraint is to allow clients to treat the property as an enumeration rather than free text, and implement URI specific behavior. See issues [#644](https://github.com/IIIF/api/issues/644), [#1479](https://github.com/IIIF/api/issues/1479), and [#1874](https://github.com/IIIF/api/issues/1874) which was approved by [trc#32](https://github.com/IIIF/trc/issues/32).

#### 1.2.6. Rename `description` to `summary`

The `description` property was renamed to `summary` and the semantics changed to be a short descriptive text. The new property is a replacement for the content in `metadata`, for situations when a a table of label/value pairs is too much to render. Descriptions that are not short descriptive text are now recorded in `metadata` to allow for appropriate labeling. See issue [#1242](https://github.com/IIIF/api/issues/1242) and entry [1.3.1][prezi30-changelog-long-texts] below.

#### 1.2.7. Rename `related` to `homepage`

Similar to the above changes where non-actionable links and content are put into `metadata`, the `related` property was renamed to `homepage` with more specific semantics of being the home page of the resource. Links to other resources instead go in to `metadata` as HTML. Multiple homepages are allowed per resource, but they should represent different language or format representations of the same content. See issues [#1286](https://github.com/IIIF/api/issues/1286), [#1484](https://github.com/IIIF/api/issues/1484), [#1760](https://github.com/IIIF/api/issues/1760). Approved by [trc#4](https://github.com/IIIF/trc/issues/4).

#### 1.2.8. Rename `contentLayer` to `supplementary`

With the removal of the `Layer` class in favor of the standard `AnnotationCollection`, and the introduction of the `motivation` value `supplementing`, the `contentLayer` property was renamed to `supplementary`. This conveys that the Annotations in the Annotation Collection are those with the `motivation` value `supplementing` while avoiding the use of the defunct class name. See issues [#1480](https://github.com/IIIF/api/issues/1480) and [#1174](https://github.com/IIIF/api/issues/1174).

#### 1.2.9. Rename `startCanvas` to `start`, allow reference to part of a Canvas

Following the pattern of removing class names from property names when unnecessary, combined with the change that the referenced resource might be part of a Canvas rather than the entire Canvas, the property was renamed. The increased scope for parts of Canvases is to allow jumping to a specific time point within a Canvas with a `duration` property. See issues [#1320](https://github.com/IIIF/api/issues/1320) and [#1930](https://github.com/IIIF/api/issues/1930).

#### 1.2.10. Rename `within` to `partOf`

While renaming properties, `within` was renamed to `partOf` to follow the same naming convention in ActivityStreams and the Web Annotation Data Model. See issue [#1482](https://github.com/IIIF/api/issues/1482).

#### 1.2.11. Specify interaction and inheritance model for `behavior` values

The specification now mandates an inheritance model for behaviors across classes, and is clear about which behaviors can be asserted on the same resource. This clarifies the implementation expectations for clients and publishers alike, and prevents different implementers from making very different choices about how to present the same information. See issues [#1612](https://github.com/IIIF/api/issues/1612) and [#1643](https://github.com/IIIF/api/issues/1643). Approved by [trc#13](https://github.com/IIIF/trc/issues/13) and [trc#16](https://github.com/IIIF/trc/issues/16).

#### 1.2.12. Wrap `logo` in a structure with more information, introduce `provider` property

Previously, the APIs allowed for a `logo` property for referencing the logos of institutions that somehow contributed or needed acknowledgement. There was no way, however, to associate a label with the logo and this was magnified by the change from `attribution` to `requiredStatement`. The solution adopted is to introduce a `provider` property that has a full structure to represent information about providing people or organizations, including `logo`, `label`, `seeAlso`, `homepage` and others. See issues [#1639](https://github.com/IIIF/api/issues/1639), [#1698](https://github.com/IIIF/api/issues/1698), [#1759](https://github.com/IIIF/api/issues/1759), [#1777](https://github.com/IIIF/api/issues/1777), [#1924](https://github.com/IIIF/api/issues/1924). Approved by [trc#3](https://github.com/IIIF/trc/issues/3) and [trc#7](https://github.com/IIIF/trc/issues/7).

#### 1.2.13. Remove `otherContent` property, use `annotations` and `items` instead

Previously, the `otherContent` property was used to link from Canvas and Layer resources to Annotation Lists containing transcriptions, video, audio or commentary. Such annotations are now included in Annotation Pages linked via the `annotations` property from Canvas resources, and via `items` from Annotation Collection resources respectively. These annotations may have various non-`painting` motivations, including the `supplementing` motivation for transcriptions. See issue [#1262](https://github.com/IIIF/api/issues/1262).

Guidance is added regarding the order in which Annotation Pages and their items should be processed. See issue [#1763](https://github.com/IIIF/api/issues/1763). Approved by [trc#22](https://github.com/IIIF/trc/issues/22).

#### 1.2.14. Update context for new major version

The URI of the context document was updated for the new major version, and thus the value of the `@context` is either the new value `http://iiif.io/api/presentation/3/context.json`, or includes this as the last item in an array value.


### 1.3. Property Value Changes

#### 1.3.1. Allow long texts in `metadata` values
{: #long-texts}

Several use cases were raised for long texts that were not descriptions, such as bibliography citation lists or provenance histories for artworks. These texts did not have a home in the previous versions, as `metadata` only allowed short values and `description` was a description of the object not information about it. The adopted solution was to allow long texts within `metadata` values, and to replace `description` with `summary`, now more specifically a short textual summary. See issue [#1270](https://github.com/IIIF/api/issues/1270)

#### 1.3.2. Allow non-images in `thumbnail`

The semantics of `thumbnail` were changed to allow for non-image content resources such as short audio or video files. This is important with the addition of time-based media being painted into Canvases. See issue [#1176](https://github.com/IIIF/api/issues/1176).

#### 1.3.3. Use language map pattern for `label`, `value`, `summary`

A new pattern has been adopted for all textual values of a JSON object with the language code as the key (or `none` if the language is not known) and the content as a string within an array as the value. This pattern is much easier to implement and use than the previous `@value` / `@language` tuples pattern. See issues [#755](https://github.com/IIIF/api/issues/755) and [#1739](https://github.com/IIIF/api/issues/1739). Approved by [trc#2](https://github.com/IIIF/trc/issues/2), [trc#5](https://github.com/IIIF/trc/issues/5) and [trc#26](https://github.com/IIIF/trc/issues/26).

#### 1.3.4. Always require arrays if property can have multiple values

Previous versions allowed a property that allowed multiple values to express a single value without an array. From version 3.0, if a property can ever have multiple values, then the value of the property is always an array. This reduces the type checking needed on values by clients as they can always iterate over the array, improving the developer experience. See issue [#1131](https://github.com/IIIF/api/issues/1131).

#### 1.3.5. Require a JSON object for all non-enumerable resources

Similarly, to reduce type checking, all resources where the URIs cannot be enumerated (such as behaviors, viewing directions, rights statements, and so forth) must be expressed as a JSON object with at least the `id` and `type` properties. This further reduces the type checking needed, as previously it could have been just the URI as a string. See issue [#1284](https://github.com/IIIF/api/issues/1284).

#### 1.3.6. Canvases always include AnnotationPages, not Annotations directly

For consistency, and to allow all content to be external to the Manifest, all Annotations are now only included via `AnnotationPage` resources. This is a change from previous versions, where image Annotations were included directly to Canvases using `images`. See issue [#1068](https://github.com/IIIF/api/issues/1068).

#### 1.3.7. Change requirements for `navDate` value

Previously the value of `navDate` was required to be in the UTC timezone. However this meant that the navigation date text generated was sometimes not the same date as the resource due to when midnight occurs in the local timezone versus in UTC. The solution adopted was to allow any timezone to be given in the value. See issue [#1296](https://github.com/IIIF/api/issues/1296).


### 1.4. Classes Changes

#### 1.4.1. Remove Sequence in favor of Ranges, `items`, and `behavior` value `sequence`

There has been a long outstanding question of how the order of Canvases in the `items` of Ranges and the order in the current Sequence interact. With further implementations from outside of the initial library-oriented domain, the need for an explicit order for views is also greatly decreased. The initial use case of multiple orderings for the content remains valid, but an edge case that can be supported using other patterns rather than requiring every Manifest to have an explicitly named Sequence. The replacement is a new `behavior` value or `sequence`. The model is simplified and clarified by this removal. See issues [#1471](https://github.com/IIIF/api/issues/1471), [#1489](https://github.com/IIIF/api/issues/1489) and further issues referenced from those.

#### 1.4.2. Ranges express full extent

In previous versions, it was unclear whether Ranges were intended to capture the extent of the content or simply the hierarchy. This is particularly important with time-based media, as the intent is not to skip between the navigation entry points when rendering the Range, but instead to play continuously. However a Range that captures the discrete sections of newspaper pages that make up an article does not include all of the intervening content. This difference was reconciled by requiring Ranges to include all and only Canvases or segments of Canvases that are strictly part of the Range. At the same time, the structure was made easier to process by embedding child ranges within the parent, rather than referencing within a flat list.
See issue [#1070](https://github.com/IIIF/api/issues/1070) and the referenced documentation.

#### 1.4.3. Remove Layer, AnnotationList in favor of AnnotationCollection, AnnotationPage

With the adoption of the Web Annotation Data Model, we remove the IIIF specific Layer in favor of the standard AnnotationCollection, and AnnotationList in favor of the equivalent AnnotationPage. See issue [#496](https://github.com/IIIF/api/issues/496).

#### 1.4.4. Remove paging functionality

As the Web Annotation Data Model defines the paging model, and Collection paging was neither implemented nor especially different from simply having a hierarchy of Collections, paging functionality was removed from the API. This simplifies the model at no cost. See issue [#1343](https://github.com/IIIF/api/issues/1343).

#### 1.4.5. Move "advanced" Annotation features to cookbook

The number of possible uses of the Web Annotation Data Model within the context of the Presentation API is extremely high. The previous section 6 of version 2.0 and 2.1 was removed in favor of entries in a "cookbook" that could be expanded and adapted over time, rather than as a specification process. This separation makes new use cases easier to accommodate and describe solutions for, without producing new minor versions of the specification.

### 1.5. Requirements Changes

#### 1.5.1. Establish client requirements per property

It was previously unclear which properties clients were required to process, and which could be left unimplemented without severely affecting the user experience of resources that made use of the properties. Requirements have been added per class/property combination. See issues [#1243](https://github.com/IIIF/api/issues/1243) and [#1271](https://github.com/IIIF/api/issues/1271)

#### 1.5.2. Canvas should have `label`

Not every view of an object has a defined label, or can have one automatically generated. As such, in order to conform with the previous requirement that Canvases _MUST_ have labels, implementers were adding empty or invisible labels as a workaround. In version 3.0, `label` on Canvas is only _RECOMMENDED_ rather than _REQUIRED_. See issue [#964](https://github.com/IIIF/api/issues/964)

#### 1.5.3. Resources referenced from Collections should have `thumbnail`

With the clarification that Collections are exclusively for navigation and not discovery, their use in user interfaces was improved by recommending the inclusion of `thumbnail` on referenced resources. See issue [#1502](https://github.com/IIIF/api/issues/1502).

#### 1.5.4. Requirements of `id` and `type`

The `type` property with a single value is now required on all resources, including content resources and services. This serves several purposes, including facilitating object mapping code libraries, clarity about the rendering needs for the resource given the new inclusion of audio and video as core content, and forcing the serialization to generate a JSON object for the resource, not just a string with the resource's URI. The values of `type` were enumerated for content resources. See issues [#1676](https://github.com/IIIF/api/issues/1676), [#1677](https://github.com/IIIF/api/issues/1677) and [#1147](https://github.com/IIIF/api/issues/1147). Approved in part by [trc#27](https://github.com/IIIF/trc/issues/27).

The `id` property is now also required for every class. This brings the specification into alignment with the `id` requirements from the Web Annotation model. See issue [#1607](https://github.com/IIIF/api/issues/1607). Approved by [trc#9](https://github.com/IIIF/trc/issues/9).


## 2. Non-Breaking Changes

### 2.1. Enable Audio and Video Content

#### 2.1.1. Allow Canvases to be treated as Content Resources

Canvases may be treated as content resources for the purposes of annotating on to other Canvases. For example, an excerpt of a Canvas that contains a video resource and annotations representing subtitles may be annotated on to another Canvas; the relative spatial and temporal alignment of the video and subtitles will be maintained. See issue [#1191](https://github.com/IIIF/api/issues/1191), previously [#42](https://github.com/IIIF/api/issues/42).

#### 2.1.2. Add `accompanyingCanvas`, `placeholderCanvas` for associated content

Many time-based media presentations have additional content associated with the object, such as either a poster that is rendered while video is buffering or on a selection user interface (`placeholderCanvas`), or images that might be displayed while an audio-only object is being rendered (`accompanyingCanvas`). The addition of these properties allows the content to be associated with the resource while not being part of the object directly. The rendering requirements for these Canvases are different from Canvases that represent the object, including that they cannot have their own accompanying or placeholder Canvases in a recursive structure. See issues [#1263](https://github.com/IIIF/api/issues/1263), [#1605](https://github.com/IIIF/api/issues/1605) and [#1615](https://github.com/IIIF/api/issues/1615). Approved by [trc#8](https://github.com/IIIF/trc/issues/8).

#### 2.1.3. Add `duration` on Canvas

In order to have time-based media associated with a Canvas, the Canvas needs to have a duration dimension. This was added to allow multiple video and/or audio files to be synchronized in time in the same way that Image (and Video) files can be aligned in the spatial dimensions. See issues [#1069](https://github.com/IIIF/api/issues/1069) and [#1190](https://github.com/IIIF/api/issues/1190).

#### 2.1.4. Add `timeMode` on Annotation

The `timeMode` indicates whether the client should `trim`, `scale`, or `loop` playback of content resources with a time component when those resources are not identical in length to the duration of the portion of the Canvas onto which they are annotated. See issue [#1075](https://github.com/IIIF/api/issues/1075).

#### 2.1.5. Add `auto-advance`, `no-auto-advance` for `behavior`

In some cases it may be desirable to have playback advance automatically from one Canvas, or part thereof, to the next, such as when Canvases represent tracks of an album; the `auto-advance` `behavior` enables this. The `no-auto-advance` behavior would then turn it off, if `auto-advance` has been inherited. See issues [#1583](https://github.com/IIIF/api/issues/1583) and [#1632](https://github.com/IIIF/api/issues/1632). Approved by [trc#17](https://github.com/IIIF/trc/issues/17).

#### 2.1.6. Add `thumbnail-nav` for `behavior`

Ranges may be used to present navigation based on thumbnails, such as video keyframes displayed in a timeline. The`thumbnail-nav` `behavior` on a Range indicates it is not to be displayed in a conventional table of contents. See issue [#1259](https://github.com/IIIF/api/issues/1259).

#### 2.1.7. Add `repeat`, `no-repeat` for `behavior`

The `repeat` `behavior` indicates that the playback order of a Collection or Manifest containing temporal Canvases should return to the first Canvas after reaching the end of the final Canvas of the resource. The `no-repeat` behavior would then turn it off, if `repeat` has been inherited. See issue [#1328](https://github.com/IIIF/api/issues/1328).

#### 2.1.8. Reference external Selectors

New content type specific Selectors for the Web Annotation Data Model are needed in order to refer to points (rather than ranges) within image, audio and video content. Similarly, there is a need to select all Audio or Visual content from within a multi-media resource. These Selectors (`PointSelector`, `AudioContentSelector`, `VideoContentSelector`) are defined in an [annex](https://iiif.io/api/annex/openannotation/), and referenced from the specification. See issue [#1593](https://github.com/IIIF/api/issues/1593).


### 2.2. Additional Features

#### 2.2.1. Add `language` on external resources

External resources referenced by `homepage`, `rendering`, and `partOf` may be associated with a language code, as described under the [languages section][prezi30-languages]. See issues [#1065](https://github.com/IIIF/api/issues/1065) and [#1933](https://github.com/IIIF/api/issues/1933).

#### 2.2.2. Add `no-nav`, `unordered`, `hidden` for `behavior`

A number of behaviors are introduced to accommodate new user interaction requirements. The `no-nav` `behavior` can be used to suppress the display of a Range that is not intended for user navigation. The `hidden` `behavior` is valid on Annotation Collections, Annotation Pages, Annotations, Specific Resources and Choices and indicates that the resource should by default not be rendered. The `unordered` `behavior` indicates that the resource’s Canvases do not have an inherent order. See issues [#1070](https://github.com/IIIF/api/issues/1070), [#1417](https://github.com/IIIF/api/issues/1417) and [#1679](https://github.com/IIIF/api/issues/1679). Approved by [trc#14](https://github.com/IIIF/trc/issues/14).

#### 2.2.3. Add `together` for `behavior`

The `together` `behavior`, valid on Collections, was introduced to indicate to clients that child Manifests, for example those containing a musical score and a related recording, should be presented simultaneously.

#### 2.2.4. Add `supplementing` for `motivation`

The `painting` `motivation` does not permit sufficient flexibility in the display of annotation content derived from the Canvas, such as a transcription of text in an image or the words spoken in an audio representation. Annotations with the `motivation` value `supplementing` may be displayed as part of the Canvas representation or in a separate area of the user interface. See issues [#1258](https://github.com/IIIF/api/issues/1258), [#1480](https://github.com/IIIF/api/issues/1480) and [#1738](https://github.com/IIIF/api/issues/1738).

#### 2.2.5. Allow `paged` behavior on Collections with `multi-part` behavior

Collections with the `multi-part` behavior often represent bound volumes, and thus are now allowed to have the `paged` behavior. See issue [#1680](https://github.com/IIIF/api/issues/1680). Approved by [trc#15](https://github.com/IIIF/trc/issues/15).


#### 2.2.6. Add `services` property for Collections and Manifests

Some services are used multiple times within a single Collection or Manifest, such as [IIIF Authentication][iiif-auth] services. These were difficult to find or overly verbose to repeat for every usage. The `services` property was added to the top level resources that can collect these multiply referenced services in a single, easy-to-find location. See issue [#1873](https://github.com/IIIF/api/issues/1873). Approved by [trc#31](https://github.com/IIIF/trc/issues/31).

### 2.3. Protocol Features

#### 2.3.1. Define JSON-LD profile for media type

A specific media-type, to be used with the HTTP headers `Accept` and `Content-Type` was defined. This media type is the JSON-LD media type, with the context in the `profile` parameter, following established conventions. See issue [#1066](https://github.com/IIIF/api/issues/1066).

#### 2.3.2. Remove per-class URI patterns, instead make general recommendations

The URI patterns given in earlier versions were removed as unhelpful. They were replaced with section 6.1. that makes general best practice recommendations about the form of URIs, including the use of the HTTPS scheme and protocol. See issue [#1214](https://github.com/IIIF/api/issues/1214).

#### 2.3.3. Allow external Ranges

In previous versions, Ranges were required to be embedded within the Manifest. With the removal of Sequences, this means that Ranges must be allowed to be referenced resources from the Manifest and thus separately requested. An additional use case comes from the AV work, where a Range could give a large set of thumbnails for every keyframe of a video to be presented on a scrubbing bar (see the `thumbnail-nav` value for `behavior`). It would be overwhelming to include this in the Manifest directly. See issue [#1218](https://github.com/IIIF/api/issues/1218).

#### 2.3.4. Recommend HEAD functionality

Implementation of the HTTP HEAD method is now recommended for Presentation API resources. See issue [#1609](https://github.com/IIIF/api/issues/1609). Approved by [trc#11](https://github.com/IIIF/trc/issues/11).

#### 2.3.5. Clarify content negotiation expectations

Expectations around the implementation of content negotiation were added. See issue [#1685](https://github.com/IIIF/api/issues/1685).


## 3. Editorial Changes

### 3.1. Clarifications

#### 3.1.1. Add explicit definition of `profile`

In previous versions, `profile` was mentioned but never formally defined. This has now been defined explicitly. See issue [#1276](https://github.com/IIIF/api/issues/1276).

#### 3.1.2. Clarify "referenced" and "embedded"

The terms "referenced" and "embedded" were never defined, but used in dozens of places. These are now defined explicitly. See issue [#1396](https://github.com/IIIF/api/issues/1396).

#### 3.1.3. Clarify patterns for cross-version references

With significant breaking changes, it was necessary to clarify that the representations of resources that are in divergent versions retain the features of the version they were defined in, even when referenced from the diverging version's resources. See issue [#1064](https://github.com/IIIF/api/issues/1064).

#### 3.1.4. Clarify `@graph` is just not allowed

Previously it had been noted in an implementation note that clients might encounter the `@graph` key in the JSON-LD, but that publishers had to strip it out. This has been clarified that `@graph` is simply not allowed in the IIIF Presentation API. See issue [#920](https://github.com/IIIF/api/issues/920).

#### 3.1.5. Clarify no interstitial pages for `rendering`

Some organizations had a desire to include a web page between the manifest and the `rendering` resource, such as a terms and conditions for download agreement. It was clarified that this is not allowed, and instead the IIIF Authentication API would serve this use case. See issue [#1155](https://github.com/IIIF/api/issues/1155).

#### 3.1.6. Clarify `multi-part` collections can have sub-collections

The text was not clear as to whether Collections can be members of a Collection that has the behavior value `multi-part`, or if only Manifests are valid. It was clarified that both Manifests and Collections can be present. See issue [#1633](https://github.com/IIIF/api/issues/1633). Approved by [trc#10](https://github.com/IIIF/trc/issues/10).

#### 3.1.7. Clarify case-sensitivity of terms

It was clarified that all terms in the JSON are case sensitive, and must be represented exactly as given in the specification. See issue [#1703](https://github.com/IIIF/api/issues/1703)


### 3.2. Style

#### 3.2.1. Restructure document

The document was again fundamentally restructured for clarity, and to remove non-core content that simply described how to make use of external specifications, and especially Web Annotations, to a [cookbook][annex-cookbook]. This enables additional use cases and patterns to be documented without requiring a new version of the specification to describe something that is already possible. It can be managed by the community, rather than via the more rigorous specification process.

#### 3.2.2. Consistency

The use of `code` font and capitalization was made consistent for class names, property names and values when used in prose. References to them in lists, especially for implementation requirements, were made consistent.

#### 3.2.3. Visual Appearance

The CSS and icons used in the requirements tables were improved, and the information updated.

#### 3.2.4. Examples Improved

The examples were improved to be more intuitive, and cover more of the features available.


[prezi30-changelog-long-texts]: #long-texts

{% include acronyms.md %}
{% include links.md %}
