---
title: "IIIF Discovery API 0.1"
title_override: "IIIF Discovery API 0.1"
id: discovery-api
layout: spec
cssversion: 2
tags: [specifications, presentation-api]
major: 0
minor: 1
patch: 0
pre: final
redirect_from:
  - /api/discovery/index.html
  - /api/discovery/0/index.html
---

## Status of this Document
{:.no_toc}
__This Version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest Stable Version:__ None

__Previous Version:__ None

**Editors**

  * **[Michael Appleby](https://orcid.org/0000-0002-1266-298X)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-1266-298X), [_Yale University_](http://www.yale.edu/)
  * **[Tom Crane](https://orcid.org/0000-0003-1881-243X)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0003-1881-243X), [_Digirati_](http://digirati.com/)
  * **[Robert Sanderson](https://orcid.org/0000-0003-4441-6852)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0003-4441-6852), [_J. Paul Getty Trust_](http://www.getty.edu/)
  * **[Jon Stroop](https://orcid.org/0000-0002-0367-1243)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-0367-1243), [_Princeton University Library_](https://library.princeton.edu/)
  * **[Simeon Warner](https://orcid.org/0000-0002-7970-7855)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-7970-7855), [_Cornell University_](https://www.cornell.edu/)
  {: .names}

{% include copyright.md %}

__Status Warning__
This is a work in progress and may change without any notices. Implementers should be aware that this document is not stable. Implementers are likely to find the specification changing in incompatible ways. Those interested in implementing this document before it reaches beta or release stages should join the [mailing list][iiif-discuss] and take part in the discussions, and follow the [emerging issues][] on Github.
{: .warning}

----

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Introduction

The resources made available via the IIIF Image and Presentation APIs are only useful if they can be found by an end user. Users cannot interact directly with a distributed, decentralized system but instead must rely on services that harvest and process the content, and then provide a user interface enabling navigation to that content via searching, browsing or other paradigms. Once the user has discovered the content, they can then display it in their viewing application of choice. Machine to machine interfaces are also enabled by this pattern, where software agents could interact via APIs to discovery the same content and retrieve it for further analysis or processing.

This specification leverages existing techniques, specifications, and tools, in order to promote widespread adoption. It enables the collaborative development of global or thematic search engines and portal applications that allow users to easily find and engage with content available via existing IIIF APIs.

### 1.1. Objectives and Scope

The objective of the IIIF Discovery API is to provide the information needed to discover and subsequently make use of existing IIIF resources.  The intended audience is other IIIF aware systems that can proactively work with the content and APIs. While this work may benefit others outside of the IIIF community directly or indirectly, the objective of the API is to specify an interoperable solution that best and most easily fulfills the discovery needs within the community of participating organizations.

The first step towards enabling the discovery of IIIF resources is to have a consistent and well understood pattern for content providers to publish lists of links to their available content. This does not include transmission optimization for the content itself, for example transferring any source image content between systems, only for the discovery of the content.  This allows a baseline implementation of discovery systems that process and reprocess the list, looking for resources that have changed.

This process can be optimized by allowing the content providers to publish descriptions of when their content has changed, enabling consuming systems to only retrieve the resources that have changed. These changes might include when content is deleted or otherwise becomes no longer available. Finally, for rapid synchronization, a system of notifications between systems can reduce the amount of effort required to constantly poll all of the systems to see if anything has changed. 

Work that is out of scope includes the selection or creation of any descriptive metadata formats, and the selection or creation of metadata search APIs or protocols. These are out of scope as the diverse domains represented within the IIIF community already have different standards in these spaces, and previous attempts to reconcile these specifications across domains have not been successful.

### 1.2. Terminology

The terms "array", "JSON object", "number", "string", "true", "false", "boolean" and "null" in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][...] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][rfc-2119].

The specification uses the following terms:

* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.


## 2. Activities

The W3C [Activity Streams](https://www.w3.org/TR/activitystreams-core/) (AS2) specification defines a "model for representing potential and completed activities", and is compatible with the [design patterns][patterns] established for IIIF APIs. It is defined in terms of [JSON-LD][json-ld], and can be seamlessly integrated with the existing IIIF APIs. The model can be used to represent activities of creating, updating and deleting (or otherwise de-publishing) IIIF resources, carried out by content publishers.

This section is a summary of the properties and types used by this specification, and defined by Activity Streams.  This is intended to ease implementation efforts by collecting the relevant information together.

### 2.1. Activity Properties

Properties that the consuming application does not understand _MUST_ be ignored.  Other properties defined by Activity Streams _MAY_ be used, such as `origin` or `instrument`, but there are no current use cases that would warrant their inclusion in this specification.

##### id

An identifier for the Activity.

Activities _MAY_ have an `id` property. The value _MUST_ be a string and it _MUST_ be an HTTP(S) URI. 

```
{ "id": "https://example.org/activity/1" }
```

##### type

The type of Activity. 

This specification uses the types described in the table below.

| Type   | Definition |
| ------ | ---------- |
| Create | The initial creation of the resource.  Each resource _MUST_ have at most one `Create` Activity in which it is the `object`. |
| Update | Any change to the resource.  In a system that does not distinguish creation from modification, then all changes _MAY_ have the `Update` type. |
| Delete | The deletion of the resource, or its de-publication from the web. Each resource _MUST_ have at most one Activity in which it is the `object`. |
{: .api-table #table-type-dfn}

Activities _MUST_ have the `type` property. The value _MUST_ be a registered Activity class, and _SHOULD_ be one of `Create`, `Update`, or `Delete`.

```
{ "type": "Update" }
```

##### object

The IIIF resource that was affected by the Activity.

Activities _MUST_ have the `object` property.  The value _MUST_ be a JSON object, with the `id` and `type` properties.  The `id` _MUST_ be an HTTP(S) URI. The `type` _MUST_ be a class defined in the IIIF Presentation API, and _SHOULD_ be one of `Collection`, or `Manifest`.

```
{
  "object": {
  	"id": "http://example.org/iiif/manifest/1",
  	"type": "Manifest"
  }
}
```

##### endTime

The time at which the Activity was finished.

Activities _SHOULD_ have the `endTime` property.  The value _MUST_ be a datetime expressed in UTC in the ISO8601 format.

```
{ "endTime": "2017-09-21T00:00:00Z" }
```

##### startTime

The time at which the Activity was started.

Activities _MAY_ have the `startTime` property.  The value _MUST_ be a datetime expressed in UTC in the ISO8601 format.

```
{ "startTime": "2017-09-20T23:58:00Z" }
```

##### actor

The organization, person, or software agent that carried out the Activity.

Activities _MAY_ have the `actor` property.  The value _MUST_ be a JSON object, with the `id` and `type` properties. The `id` _SHOULD_ be an HTTP(S) URI. The `type` _MUST_ be one of `Application`, `Organization`, or `Person`.

```
{ 
  "actor": {
    "id": "https://example.org/person/admin",
    "type": "Person"
  }
}
```

##### Complete Example

A complete example Activity would thus look like the following example.

```
{ 
  "id": "https://example.org/activity/1",
  "type": "Update",
  "object": {
  	"id": "https://example.org/iiif/manifest/1"
  	"type": "Manifest"  	
  },
  "endTime": "2017-09-21T00:00:00Z",
  "startTime": "2017-09-20T23:58:00Z",
  "actor": {
    "id": "https://example.org/person/admin",
    "type": "Person"
  }
}
```

### 2.2. Resource Discovery via Activities

#### 2.2.1. Level 0: Basic Resource List

The basic information required, in order to provide a minimally effective set of links to IIIF resources to harvest is just the URIs of those resources. However, with the addition of a little boilerplate in the JSON, we can be on the path towards a robust set of information that clients can use to optimize their harvesting.  

Starting with the Manifest URIs, we add an "Update" Activity wrapper around them.  The order of the Manifests is unimportant, but each should only appear once in the list. In terms of optimization, it provides no additional benefit over any other simpler list format, but is compatible with the following levels.  This is the minimum level for interoperability, but further levels are significant improvements in terms of efficiency.

Example level 0 Activity:

```
{ 
  "type": "Update",
  "object": {
  	"id": "https://example.org/iiif/manifest/1"
  	"type": "Manifest"  	
  }
}
```

#### 2.2.2. Level 1: Basic Change List

The most effective information to add beyond the basic resource list is the datestamp at which the resource was last modified (including the initial modification that created it).  If we know these dates, we can add them to the Activities and order the list such that the most recent activities occur last. The timestamp is given in the `endTime` property -- the time at which the document update process finished. It is up to the implementer to decide whether the update process includes the publication online, or only the internal data modification, but the decision _MUST_ be consistently applied.  

Consumers will then process the list of Activities in reverse order, from last to first. The rationale for processing backwards is that the first parts of the list, once finished, can become static resources.  Note that resources _MAY_ appear multiple times in the list, or only the most recent change might be present, depending on the implementation.

Additional information, using the properties described above, can be added without affecting the way consumers would process the list.

```
{
  "type": "Update",
  "object": {
    "id": "https://example.org/iiif/manifest/1",
    "type": "Manifest"
  },
  "endTime": "2017-09-20T00:00:00Z"
}
```

#### 2.2.3. Level 2: Complete Change List

At the most detailed level, a log of all of the Activities that have taken place can be recorded, with the likeihood of multiple Activities per object resource.  This allows the additional types of Create and Delete, enabling a synchronization process to remove resources as well as add them. This would also allow for the complete history of a resource to be reconstructed, if each version has an archived representation.  The list might end up very long if there are many changes to resources, however this is not a typical situation, and the cost is still reasonable as each entry is short and can be compressed both on disk and at the HTTP(S) transport layer.

A consuming application at this level would process the `type` property of the Activity description.

```
{
  "type": "Create",
  "object": {
    "id": "https://example.org/iiif/manifest/1",
    "type": "Manifest"
  },
  "endTime": "2017-09-20T00:00:00Z"
}
```

## 3. Activity Streams

### 3.1. Collection

The top-most resource for managing the lists of Activities is an Ordered Collection, broken up into Ordered Collection Pages. This is the same pattern that the Web Annotation model uses for Annotation Collections and Annotation Pages. The Collection does not directly contain any of the Activities, instead it refers to the `first` page of the overall list.  The pages are ordered both from page to page by following `next` relationships, and internally within the page in the `orderedItems` property. The number of entries in each page is up to the implementer, and cannot be modified by the client.

#### 3.1.1 Ordered Collection Properties

##### @context


##### id

The identifier of the Ordered Collection.

Ordered Collections _MUST_ have an `id` property. The value _MUST_ be a string and it _MUST_ be an HTTP(S) URI. The JSON representation of the Ordered Collection _MUST_ be available at the URI.

```
{ "id": "https://example.org/activity/collection" }
```

##### type

The class of the Ordered Collection.

Ordered Collections _MUST_ have a `type` property.  The value _MUST_ be "OrderedCollection".

```
{ "type": "OrderedCollection" }
```

##### first

A link to the first Ordered Collection Page for this Collection.

Ordered Collections _SHOULD_ have a `first` property.  The value _MUST_ be a JSON object, with the `id` and `type` properties.  The value of the `id` property _MUST_ be a string, and it _MUST_ be the HTTP(S) URI of the first page of items in the Collection. The value of the `type` property _MUST_ be a string, and _MUST_ be "OrderedCollectionPage".

```
{ 
  "first": {
    "id": "https://example.org/activity/page-0",
    "type": "OrderedCollectionPage"
  }
}
```

##### last

A link to the last Ordered Collection Page for this Collection.  As the client processing algorithm works backwards from the most recent to least recent, the inclusino of `last` is _REQUIRED_, but `first` is only _RECOMMENDED_.  This might seem odd to implementers, without the context of the processing.

Ordered Collections _SHOULD_ have a `last` property.  The value _MUST_ be a JSON object, with the `id` and `type` properties.  The value of the `id` property _MUST_ be a string, and it _MUST_ be the HTTP(S) URI of the last page of items in the Collection. The value of the `type` property _MUST_ be a string, and _MUST_ be "OrderedCollectionPage".

```
{ 
  "last": {
    "id": "https://example.org/activity/page-1234",
    "type": "OrderedCollectionPage"
  }
}
```

##### totalItems

The total number of Activities in the Ordered Collection.

OrderedCollections _MAY_ have a `totalItems` property.  The value _MUST_ be a non-negative integer.

```
{ "totalItems": 21456 }
```

##### Complete Example

```
{
  "@context": "",
  "id": "https://example.org/activity/collection",
  "type": "OrderedCollection",
  "totalItems": 21456,
  "first": {
  	"id": "https://example.org/activity/page-0",
  	"type": "OrderedCollectionPage"
  },
  "last": {
  	"id": "https://example.org/activity/page-1234",
  	"type": "OrderedCollectionPage"
  }
}
```

### 3.2. Ordered Collection Page

#### 3.2.1 Collection Page Properties

##### id

The identifier of the Collection Page.

Ordered Collection Pages _MUST_ have an `id` property. The value _MUST_ be a string and it _MUST_ be an HTTP(S) URI. The JSON representation of the Ordered Collection Page _MUST_ be available at the URI.

```
{ "id": "https://example.org/activity/page-0" }
```

##### type

The class of the Ordered Collection Page.

Ordered Collections _MUST_ have a `type` property.  The value _MUST_ be "OrderedCollectionPage".

```
{ "type": "OrderedCollectionPage" }
```

##### partOf

The Ordered Collection that this Page is part of.

Ordered Collection Pages _SHOULD_ have a `partOf` property. The value _MUST_ be a JSON object, with the `id` and `type` properties.  The value of the `id` property _MUST_ be the a string, and _MUST_ be the HTTP(S) URI of the Ordered Collection that this page is part of.  The value of the `type` property _MUST_ be a string, and _MUST_ be "OrderedCollection".

```
{
  "partOf": {
    "id": "https://example.org/activity/collection",
    "type": "OrderedCollection"
  }
}
```


##### startIndex

The position of the first item in this page's `orderedItems` list, relative to the overall ordering across all pages within the Collection.  The first entry in the list has a `startIndex` of 0.  If the first page has 20 entries, the first entry on the second page would therefore be 20.

Ordered Collection Pages _MAY_ have a `startIndex` property.  The value _MUST_ be a non-negative integer.

```
{ "startIndex": 20 }
```

##### next

A reference to the next page in the list of pages.

Ordered Collection Pages _SHOULD_ have a `next` property. The value _MUST_ be a JSON object, with the `id` and `type` properties.  The value of the `id` property _MUST_ be the a string, and _MUST_ be the HTTP(S) URI of the following Ordered Collection Page.  The value of the `type` property _MUST_ be a string, and _MUST_ be "OrderedCollectionPage".

```
{
  "next": {
    "id": "https://example.org/activity/page-2",
    "type": "OrderedCollectionPage"
  }
}
```


##### prev

A reference to the previous page in the list of pages.

Ordered Collection Pages _MUST_ have a `prev` property. The value _MUST_ be a JSON object, with the `id` and `type` properties.  The value of the `id` property _MUST_ be the a string, and _MUST_ be the HTTP(S) URI of the preceding Ordered Collection Page.  The value of the `type` property _MUST_ be a string, and _MUST_ be "OrderedCollectionPage".

```
{
  "prev": {
    "id": "https://example.org/activity/page-1",
    "type": "OrderedCollectionPage"
  }
}
```

##### orderedItems

The Activities that are listed as part of this page.

Ordered Collection Pages _MUST_ have a `orderedItems` property.  The value _MUST_ be an array, with at least one item.  Each item _MUST_ be a JSON object, conforming to the requirements of an Activity.

```
{
  "orderedItems": [
     {
     	"type": "Activity",
     	"object": {
     		"id": "https://example.org/iiif/manifest/1",
     		"type": "Manifest"
     	},
     	"endTime": "2018-03-10T10:00:00Z"
     }
  ]
}
```

##### Complete Ordered Collection Page Example

```
{
  "@context": "",
  "id": "https://example.org/activity/page-1",
  "type": "OrderedCollectionPage",
  "startIndex": 20,
  "partOf": {
  	"id": "https://example.org/activity/collection",
  	"type": "OrderedCollection"
  },
  "prev": {
  	"id": "https://example.org/activity/page-0",
  	"type": "OrderedCollectionPage"
  },
  "next": {
  	"id": "https://example.org/activity/page-2",
  	"type": "OrderedCollectionPage"
  },
  "orderedItems": [
     {
     	"type": "Activity",
     	"object": {
     		"id": "https://example.org/iiif/manifest/1",
     		"type": "Manifest"
     	},
     	"endTime": "2018-03-10T10:00:00Z"
     }
  ]
}
```

## 3.3. Activity Streams Processing Algorithm

The aim of the processing algorithm is to inform harvesters how to make best use of the available information, with an aim of finding "indexable content" -- the descriptive information that might be used to build an index of the resources to allow them to be discovered.  For different types of resource, and for different domains, the "indexable content" will have different formats and semantics. At worst, the data in the Manifest and other IIIF resources might be used, despite its presentational intent. 

__Collection Algorithm__

Given the URI of an ActivityStreams Collection (`collection`) as input, a conforming processor SHOULD:

1. Initialization:
  1.1. Let `processedItems` be an empty array
  1.2. Let `lastCrawl` be the timestamp of the previous time the algorithm was executed
2. Retrieve the representation of `collection` via HTTP(S)
3. Minimally validate that it conforms to the specification
4. Find the URI of the last page at `collection.last.id` (`pageN`)
5. Apply the results of the page algorithm to `pageN`


__Page Algorithm__

Given the URI of an ActivityStreams CollectionPage (`page`) and the date of last crawling (`lastCrawl`) as input, a conforming processor SHOULD:

1. Retrieve the representation of `page` via HTTP(S)
2. Minimally validate that it conforms to the specification
3. Find the set of updates of the page at `page.orderedItems` (`items`)
4. In reverse order, iterate through the activities (`activity`) in `items`
  4.1. For each `activity`, if `activity.endTime` is before `lastCrawl`, then terminate ;
  4.2. If the updated resource's uri at `activity.target.id` is in `processedItems`, then continue ;
  4.3. Otherwise, if `activity.type` is `Update` or `Create`, then find the URI of the updated resource at `activity.target.id` (`target`) and apply the target resource algorithm ;
  4.4. Otherwise, if `activity.type` is `Delete`, then find the URI of the deleted resource at `activity.target.id` and remove it from the index.
  4.5. Add the processed resource's URI to `processedItems`
5. Finally, find the URI of the previous page at `collection.prev.id` (`pageN1`)
6. If there is a previous page, apply the results of the page algorithm to `pageN1`

__Target Resource Algorithm__

Given the URI of a target resource (`target`), a conforming processor SHOULD:

1. Retrieve the representation of `target` via HTTP(S)
2. Minimally validate that it conforms to the appropriate specification
3. Find the URI of the resource at `target.id` (`targetId`)
4. If the resource has the `seeAlso` property, then for each resource referenced ('extref')
  4.1. If the `format` and/or `profile` of `extref` is understood by the processor, then it should retrieve any representations that it can process to extract Indexable Content.
5. Otherwise, extract any indexable content from the resource's representation, using resource type specific functionality.
6. Index the content against `targetId`


## 4. Notifications

__Coming soon__

## Appendices

### A. Acknowledgements

### B. Change Log


includes/links is only in prezi3. Links here are placeholders.
{: .warning}

[iiif-discuss]: mailto:iiif-discuss@googlegroups.com "Email Discussion List"
[patterns]: http://iiif.io/api/
[json-ld]: http://w3.org/
[rfc-2119]: http://ietf.org/

