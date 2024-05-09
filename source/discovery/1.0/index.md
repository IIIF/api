---
title: "IIIF Change Discovery API 1.0"
title_override: "IIIF Change Discovery API 1.0"
id: discovery-api
layout: spec
cssversion: 3
tags: [specifications, discovery-api]
major: 1
minor: 0
patch: 0
pre: final
redirect_from:
  - /discovery/
  - /discovery/index.html
  - /discovery/1/index.html
editors:
  - name: Michael Appleby
    ORCID: https://orcid.org/0000-0002-1266-298X
    institution: Yale University
  - name: Tom Crane
    ORCID: https://orcid.org/0000-0003-1881-243X
    institution: Digirati
  - name: Robert Sanderson
    ORCID: https://orcid.org/0000-0003-4441-6852
    institution: J. Paul Getty Trust
  - name: Jon Stroop
    ORCID: https://orcid.org/0000-0002-0367-1243
    institution: Princeton University Library
  - name: Simeon Warner
    ORCID: https://orcid.org/0000-0002-7970-7855
    institution: Cornell University
hero:
  image: ''

---

## Status of this Document
{:.no_toc}
__This Version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest Stable Version:__ [{{ site.data.apis.discovery.stable.major }}.{{ site.data.apis.discovery.stable.minor }}.{{ site.data.apis.discovery.stable.patch }}][discovery-stable-version]

__Previous Version:__ [0.9.2][discovery09]

**Editors**

{% include api/editors.md editors=page.editors %}

{% include copyright.md %}

----

## 1. Introduction
{: #introduction}

The resources made available via the IIIF (pronounced "Triple-Eye-Eff") [Image][image-api] and [Presentation][prezi-api] APIs are useful only if they can be found. Users cannot interact directly with a distributed, decentralized ecosystem but instead must rely on services that harvest and process the available content, and then provide a user interface enabling navigation to that content via searching, browsing or other paradigms. Once the user has discovered the content, they can then display it in their viewing application of choice. Machine to machine interfaces are also enabled by this approach, where software agents can interact via APIs to discover the same content and retrieve it for further analysis or processing.

This specification leverages existing techniques, specifications, and tools in order to promote widespread adoption of an easy-to-implement service. The service describes changes to IIIF content resources and the location of those resources to harvest. Content providers can implement this API to enable the collaborative development of global or thematic search engines and portal applications that ultimately allow users to easily find and engage with content available via existing IIIF APIs.

### 1.1. Objectives and Scope
{: #objectives-and-scope}

The objective of the IIIF Change Discovery API is to provide a machine to machine API that provides the information needed to discover and subsequently make use of IIIF resources. The intended audience is other IIIF-aware systems that can leverage the content and APIs. While this work may benefit others outside of the IIIF community directly or indirectly, the objective of the API is to specify an interoperable solution that best and most easily fulfills the discovery needs within the community of participating organizations.

The discovery of IIIF resources requires a consistent and well understood pattern for content providers to publish lists of links to their available content. This allows a baseline implementation of discovery systems that process the list, looking for resources that have been added or changed.

This process can be optimized by allowing the content providers to publish descriptions of how their content has changed, enabling consuming systems to retrieve only the resources that have been modified since they were last retrieved. These changes might include when content is deleted or otherwise becomes unavailable. Finally, for rapid synchronization, a system of notifications pushed from the publisher to a set of subscribers can reduce the amount of effort required to constantly poll multiple sources to see if anything has changed.

Work that is out of scope of this API includes the recommendation or creation of any descriptive metadata formats, and the recommendation or creation of metadata search APIs or protocols. The diverse domains represented within the IIIF community already have successful standards fulfilling these use cases. Also out of scope is optimization of the transmission of content, for example recommendations about transferring any source media or data between systems.

__Change Notifications__<br>This specification does not include a subscription mechanism for enabling change notifications to be pushed to remote systems. Only periodic polling for the set of changes that must be processed is supported. A subscription/notification pattern may be added in a future version after implementation experience with the polling pattern has demonstrated that it would be valuable.
{: .warning}

### 1.2. Terminology
{: #terminology}

The specification uses the following terms:

* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

The terms _array_, _JSON object_, _number_, and _string_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].


## 2. Overview of IIIF Resource Discovery
{: #overview-of-iiif-resource-discovery}

In order to discover IIIF resources, the state of those resources in the systems that publish them needs to be communicated succinctly and easily to a consuming system. The consuming system can then use that information to retrieve and process the resources of interest and provide platforms that enable discovery and use. This communication takes place via the IIIF Change Discovery API, which uses the W3C [Activity Streams][org-w3c-activitystreams] specification to describe and serialize changes to resources. The conceptual model for those changes and the interactions between publishers and consumers are based on those identified by the [ResourceSync][org-openarchives-rsync] framework. It is not necessary to understand either of these standards in order to use or implement the IIIF Change Discovery API, which is fully specified in this document.

Activities are used to describe the state of the publishing system by recording each individual change, in the order that they occur. The changes described are the creation, modification and deletion of IIIF Presentation API resources. A consuming application that is aware of all of the changes that took place in the publishing system has full knowledge of the set of resources available. IIIF [Collections][prezi30-collection] and [Manifests][prezi30-manifest] are the main access points to published content and references to descriptive metadata about that content, however, Activities describing changes to other resources, such as the IIIF Image API endpoints or the descriptive metadata about the object represented, could also be published in this way. As the intended use is to inform a consuming system, rather than to display information, the Change Discovery API does not include any content intended to be rendered to end users.

The Presentation API does not include descriptive metadata fields, and intentionally lacks the semantics needed to implement advanced or fielded search. Instead, the Presentation API uses the [`seeAlso`][prezi30-seealso] property to link to external documents that can have richer and domain-specific information about the content being presented. For example, a museum object might have a `seeAlso` reference to a CIDOC-CRM or LIDO description, while a bibliographic resource might reference a Dublin Core or MODS description. These external descriptions should be used when possible to provide interfaces giving access to more precise matching algorithms.

This specification describes three levels of conformance that build upon each other in terms of functionality and precision of the information published. Sets of changes are published in pages, which are then aggregated into a collection per publisher. To reduce barriers to entry, care has been taken to allow for the possibility of implementing all levels using only static files on a web server, rather than requiring dynamic access to a database. 

### 2.1. IIIF Resources and their Changes
{: #resources-and-their-changes}

There are three levels of conformance at which changes to IIIF resources can be described. Level 0 is simply a list of the resources available. Level 1 adds timestamps and ordering from earliest change to most recent, allowing a consuming application to work backwards through the list and stop processing once it encounters a change that it has already seen from a previous run. Level 2 adds information about the types of activities, enabling the explicit description of the creation and deletion of resources.

The subsections below describe first how to construct the description of the changes for each level, and then in the next section how to embed them into ordered lists.

#### 2.1.1. Level 0: Resource References
{: #level-0-basic-resource-list}

The core information required to provide a minimally effective set of links to IIIF resources is the URIs of those resources. The order of the resources in the resulting list is unimportant, but each _SHOULD_ only appear once. This is the minimum level for any effective interoperability.

This minimal level 0 API approach is compatible with the levels 1 and 2 which introduce significant benefits that allow clients to better optimize their interactions.

If resources are deleted after being referred to in the resource list, the entire list should be republished without the reference to the deleted resource. Clients should also expect to encounter resource URIs that are out of date and no longer resolve to a IIIF Manifest or Collection, as well as activities which do not refer to IIIF resource types at all.

Example Level 0 Activity:

```json-doc
{
  "type": "Update",
  "object": {
    "id": "https://example.org/iiif/1/manifest",
    "type": "Manifest"
  }
}
```

#### 2.1.2. Level 1: Resource Changes
{: #level-1-basic-change-list}

When dealing with large lists of resources, it can be useful to work with only those resources that have changed since the last time the list was processed. This is managed by the addition of a time stamp in the `endTime` property, that indicates the time at which the resource was last modified or initially created. Lists _MUST_ be ordered such that the most recent activities occur last. Consumers will then process the list of Activities in reverse order, from last to first, stopping when they encounter an Activity they have already processed.

Example Level 1 Activity:

```json-doc
{
  "type": "Update",
  "object": {
    "id": "https://example.org/iiif/1/manifest",
    "type": "Manifest"
  },
  "endTime": "2017-09-20T00:00:00Z"
}
```

#### 2.1.3. Level 2: Resource Creation, Change, Deletion and Moving
{: #level-2-complete-change-list}

At the most detailed level, a log of all Activities that have taken place can be recorded, with the likelihood of multiple Activities per IIIF resource. Use of the additional types of "Create", "Delete" and "Move" allows explicit description of creations, deletions and moves, enabling a synchronization process to remove resources as well as add or update them.

A complete change history is not required, and sometimes not even desirable. If there are many or frequent changes to a resource, an implementation _MAY_ omit any number of individual changes, but _SHOULD_ always  have the most recent change included in the list. Changes that are deemed to be insignificant to the publisher of the list _MAY_ also be omitted, such as changes that do not affect the content visible to users.

Example Level 2 Activity:

```json-doc
{
  "type": "Create",
  "object": {
    "id": "https://example.org/iiif/1/manifest",
    "type": "Manifest"
  },
  "endTime": "2017-09-20T00:00:00Z"
}
```

#### 2.1.4. Aggregating Activities
{: #aggregated-activity-streams}

Activities can be added to or removed at times other than when the resources they refer to are created, modified, deleted or moved. There are several use cases for this pattern, however they are all outside of the normal publication of a stream by the content owners and thus are unlikely to affect most publishing implementations. They do affect consuming applications, and the implications are documented in [3.5. Activity Streams Processing Algorithm][discovery-processing-streams].

The first use case is when third-party aggregators add activities harvested from different institutions, filter those activities or objects, and aggregate them into a composite stream. For example, a dinosaur aggregator might filter several natural history museum streams for only those manifests that are about dinosaurs.

Secondly, resources might become available or unavailable without being created or deleted. This could happen because of changes to their permissions, such as an embargo period after creation, or when resources are temporarily removed in order to be edited as part of some data cleaning or migration process.

Whenever an "Add" Activity is encountered, it is semantically similar to a "Create" Activity in that it is the first time that resource is mentioned in the stream. It is, therefore, expected that if there is an "Add", then there may not be a "Create" for the same resource occurring before it. Similarly, there will be no more references to the resource after a "Remove" or "Delete".

Example Add Activity:

```json-doc
{
  "type": "Add",
  "summary": "Added newly discovered manifest to stream",
  "object": {
    "id": "https://example.org/iiif/1/manifest",
    "type": "Manifest"
  },
  "target": {
    "id": "https://example.org/activity/aggregated-changes",
    "type": "OrderedCollection"
  },
  "endTime": "2019-11-22T00:00:00Z"
}
```

Example Remove Activity:

```json-doc
{
  "type": "Remove",
  "summary": "Removed manifest from stream due to being out of scope",
  "object": {
    "id": "https://example.org/iiif/1/manifest",
    "type": "Manifest"
  },
  "origin": {
    "id": "https://example.org/activity/aggregated-changes",
    "type": "OrderedCollection"
  },
  "endTime": "2017-11-23T00:00:00Z"
}
```

#### 2.1.5. State Refresh Activities
{: #state-refresh-activities}

Sometimes a publishing system will do a complete refresh of its records and re-issue an activity for every resource.  When this happens, it is a good practice to include a `Refresh` activity immediately before the `Update` activities for the resources. This allows a consuming application to stop looking for new resources beyond this point, as all of the available ones will already have been encountered. Note that the `Refresh` uses `startTime` rather than `endTime` as the datetime when it occurs, in order to ensure that it is positioned before the resource activities in the sorted stream. 

Consuming applications that have processed the stream previously should continue to read backwards beyond this point, in order to process any Delete activities, but do not need to process other activity types.  Applications that have not processed the stream previously can simply stop when the `Refresh` activity is encountered. 

```json-doc
{
  "type": "Refresh",
  "summary": "System refresh initiated",
  "startTime": "2020-06-21T00:00:00Z"
}
```

### 2.2. Pages of Changes
{: #pages-of-changes}

The Activities are collected together into pages that together make up the entire set of changes that the publishing system is aware of. Pages reference the previous and next pages in that set, and the overall collection of which they are part. The Activities within the page are listed such that the most recent activities occur last.

Pages are subsequently collected together in ordered collections, described in the following section.

```json-doc
{
  "@context": "http://iiif.io/api/discovery/1/context.json",
  "id": "https://example.org/activity/page-1",
  "type": "OrderedCollectionPage",
  "partOf": {
    "id": "https://example.org/activity/all-changes",
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
      "type": "Update",
      "object": {
        "id": "https://example.org/iiif/9/manifest",
        "type": "Manifest"
      },
      "endTime": "2018-03-10T10:00:00Z"
    },
    {
      "type": "Update",
      "object": {
        "id": "https://example.org/iiif/2/manifest",
        "type": "Manifest"
      },
      "endTime": "2018-03-11T16:30:00Z"
    }
  ]
}
```

### 2.3. Collections of Pages
{: #collections-of-pages}

As the number of Activities is likely too many to usefully be represented in a single Page, they are collected together into a Collection as the initial entry point. The Collection references the URIs of the first and last pages, where the first page contains the earliest activities and the last page contains the most recent.

```json-doc
{
  "@context": "http://iiif.io/api/discovery/1/context.json",
  "id": "https://example.org/activity/all-changes",
  "type": "OrderedCollection",
  "totalItems": 21456,
  "first": {
    "id": "https://example.org/activity/page-0",
    "type": "OrderedCollectionPage"
  },
  "last": {
    "id": "https://example.org/activity/page-214",
    "type": "OrderedCollectionPage"
  }
}
```

### 2.4. Registries of Collections
{: # registries-of-collections}

In order to discover the URIs for Collections, and through them the URIs of the IIIF resources, the IIIF Consortium manages a [Registry of Collections][discovery-registry]. This registry is itself an implementation of the Change Discovery API, however the IIIF resources are not Presentation API resources, but other Change Discovery API resources. This might include both Collections of Manifests, or other registries of Collections. The registry describes how it is managed and how to retrieve or submit content. The registry may also reference other methods of discovering IIIF content.


## 3. Activity Streams Details
{: #activity-streams-details}

The W3C [Activity Streams][org-w3c-activitystreams] specification defines a "model for representing potential and completed activities", and is compatible with the [design patterns][annex-patterns] established for IIIF APIs. It is defined in terms of [JSON-LD][org-w3c-json-ld] and can be seamlessly integrated with the existing IIIF APIs. The model can be used to represent activities carried out by content publishers of creating, updating, and deleting (or otherwise de-publishing) IIIF resources.

This section is a summary of the properties and types used by this specification, and defined by Activity Streams. This is intended to ease implementation efforts by collecting the relevant information together.

Properties, beyond those described in this specification, that the consuming application does not have code to process _MUST_ be ignored. Other properties defined by Activity Streams _MAY_ be used, such as `origin` or `instrument`, but there are no current use cases that would warrant their inclusion in this specification.


### 3.1. Ordered Collection
{: #orderedcollection}

The top-most resource for managing the lists of Activities is an Ordered Collection, broken up into Ordered Collection Pages. The Collection does not directly contain any of the Activities, instead it refers to the `first` and `last` pages of the list.

The overall ordering of the Collection is from the oldest Activity as the first entry in the first page, to the most recent as the last entry in the last page. Consuming applications _SHOULD_ therefore start at the end and walk **backwards** through the list, and stop when they reach a timestamp before the time they last processed the list.

Content providers _MUST_ publish an Ordered Collection at the HTTP(S) URI listed in the `id` property of the Collection.

##### id

The identifier of the Ordered Collection.

Ordered Collections _MUST_ have an `id` property. The value _MUST_ be a string and it _MUST_ be an HTTP(S) URI. The JSON representation of the Ordered Collection _MUST_ be available at the URI.

```json-doc
{ "id": "https://example.org/activity/all-changes" }
```

##### type
{: #type-ordered-collection}

The class of the Ordered Collection.

Ordered Collections _MUST_ have a `type` property. The value _MUST_ be `OrderedCollection`.

```json-doc
{ "type": "OrderedCollection" }
```

##### first

A link to the first Ordered Collection Page for this Collection.

Ordered Collections _SHOULD_ have a `first` property. The value _MUST_ be a JSON object, with the `id` and `type` properties. The value of the `id` property _MUST_ be a string, and it _MUST_ be the HTTP(S) URI of the first page of items in the Collection. The value of the `type` property _MUST_ be the string `OrderedCollectionPage`.

```json-doc
{
  "first": {
    "id": "https://example.org/activity/page-0",
    "type": "OrderedCollectionPage"
  }
}
```

##### last

A link to the last Ordered Collection Page for this Collection. As the client processing algorithm works backwards from the most recent to least recent, the inclusion of `last` is _REQUIRED_, but `first` is only _RECOMMENDED_.

Ordered Collections _MUST_ have a `last` property. The value _MUST_ be a JSON object, with the `id` and `type` properties. The value of the `id` property _MUST_ be a string, and it _MUST_ be the HTTP(S) URI of the last page of items in the Collection. The value of the `type` property _MUST_ be the string `OrderedCollectionPage`.

```json-doc
{
  "last": {
    "id": "https://example.org/activity/page-1234",
    "type": "OrderedCollectionPage"
  }
}
```

##### totalItems

The total number of Activities in the entire Ordered Collection.

Ordered Collections _MAY_ have a `totalItems` property. The value _MUST_ be a non-negative integer.

```json-doc
{ "totalItems": 21456 }
```

##### seeAlso

This property is used to refer to one or more documents that semantically describe **the set of resources** that are being acted upon in the Activities within the Ordered Collection, rather than any particular resource referenced from within the collection. This would allow the Ordered Collection to refer to, for example, a [DCAT][org-w3c-dcat] description of the dataset. For Ordered Collections that aggregate activities and/or objects from multiple sources, the referenced description should describe the complete aggregation rather than an individual source.

Ordered Collections _MAY_ have a `seeAlso` property. The value _MUST_ be an array of one or more JSON objects, with the `id` and `type` properties. The value of the `id` property _MUST_ be a string, and it _MUST_ be the HTTP(S) URI of the description of the dataset. The value of the `type` property _MUST_ be the string `Dataset`. Please note that any resource that is intended to be used by software is tagged as `Dataset`, including single files. The JSON object has the same structure as in the Presentation API, and thus _SHOULD_ have the following properties:

* `format`, the value of which _MUST_ be a string, and it _MUST_ be the MIME media type of the referenced description document
* `label`, the value of which _MUST_ be a JSON object, following the pattern for language maps described in the [Presentation API][prezi30-languages]
* `profile`, the value of which _MUST_ be a string containing either a value from the [profiles registry][registry-profiles] or a URI


```json-doc
{
  "seeAlso": [
    {
      "id": "https://example.org/dataset/all-dcat.jsonld",
      "type": "Dataset",
      "label": { "en": [ "DCAT description of Collection" ] },
      "format": "application/ld+json",
      "profile": "http://www.w3.org/ns/dcat#"
    }
  ]
}
```

##### partOf

This property is used to refer to a larger Ordered Collection, of which this Ordered Collection is part. This would allow a publisher to have thematic or temporal sets of activities, for example to have different collections of activities for their paintings from their sculptures, or their modern content from their archival content.

Ordered Collections _MAY_ have a `partOf` property. The value _MUST_ be an array of one or more JSON objects, with the `id` and `type` properties. The value of the `id` property _MUST_ be a string, and it _MUST_ be the HTTP(S) URI of the larger collection. The value of the `type` property _MUST_ be the string `OrderedCollection`.

```json-doc
{
  "partOf": [
    {
      "id": "https://example.org/aggregated-changes",
      "type": "OrderedCollection"
    }
  ]
}

```

##### rights

A string that identifies a license or rights statement that applies to the usage of the Ordered Collection. The value _MUST_ be drawn from the set of [Creative Commons][org-cc-licenses] license URIs, the [RightsStatements.org][org-rs-terms] rights statement URIs, or those added via the [extension][prezi30-ldce] mechanism. The inclusion of this property is informative, and for example could be used to display an icon representing the rights assertions.

The value _MUST_ be a string. If the value is drawn from Creative Commons or RightsStatements.org, then the string _MUST_ be a URI defined by that specification.

``` json-doc
{ "rights": "http://creativecommons.org/licenses/by/4.0/" }
```


##### Complete Ordered Collection Example

```json-doc
{
  "@context": "http://iiif.io/api/discovery/1/context.json",
  "id": "https://example.org/activity/all-changes",
  "type": "OrderedCollection",
  "totalItems": 21456,
  "rights": "http://creativecommons.org/licenses/by/4.0/",
  "seeAlso": [
    {
      "id": "https://example.org/dataset/all-dcat.jsonld",
      "type": "Dataset",
      "label": { "en": [ "DCAT description of Collection" ] },
      "format": "application/ld+json",
      "profile": "http://www.w3.org/ns/dcat#"
    }
  ],
  "partOf": [
    {
      "id": "https://example.org/aggregated-changes",
      "type": "OrderedCollection"
    }
  ],
  "first": {
    "id": "https://example.org/activity/page-0",
    "type": "OrderedCollectionPage"
  },
  "last": {
    "id": "https://example.org/activity/page-214",
    "type": "OrderedCollectionPage"
  }
}
```

### 3.2. Ordered Collection Page
{: #ordered-collection-page}

The list of Activities is ordered both from page to page by following `prev` (or `next`) relationships, and internally within the page in the `orderedItems` property. The number of entries in each page is up to the implementer, and cannot be modified at request time by the client. Pages are not required to have the same number of entries as any other page.

Content providers _MUST_ publish at least one Ordered Collection Page at the HTTP(S) URI given in the `id` property of the Page.

##### id

The identifier of the Collection Page.

Ordered Collection Pages _MUST_ have an `id` property. The value _MUST_ be a string and it _MUST_ be an HTTP(S) URI. The JSON representation of the Ordered Collection Page _MUST_ be available at the URI.

```json-doc
{ "id": "https://example.org/activity/page-0" }
```

##### type
{: #type-ordered-collection-page}

The class of the Ordered Collection Page.

Ordered Collections _MUST_ have a `type` property. The value _MUST_ be `OrderedCollectionPage`.

```json-doc
{ "type": "OrderedCollectionPage" }
```

##### partOf

The Ordered Collection of which this Page is a part.

Ordered Collection Pages _SHOULD_ have a `partOf` property. The value _MUST_ be a JSON object, with the `id` and `type` properties. The value of the `id` property _MUST_ be a string, and _MUST_ be the HTTP(S) URI of the Ordered Collection that this page is part of. The value of the `type` property _MUST_ be the string `OrderedCollection`.

```json-doc
{
  "partOf": {
    "id": "https://example.org/activity/all-changes",
    "type": "OrderedCollection"
  }
}
```

##### startIndex

The position of the first item in this page's `orderedItems` list, relative to the overall ordering across all pages within the Collection. The first entry in the overall list has a `startIndex` of 0. If the first page has 20 entries, the first entry on the second page would therefore be 20.

Ordered Collection Pages _MAY_ have a `startIndex` property. The value _MUST_ be a non-negative integer.

```json-doc
{ "startIndex": 20 }
```

##### next

A reference to the next page in the list of pages.

Ordered Collection Pages _SHOULD_ have a `next` property, unless they are the last page in the Collection. The value _MUST_ be a JSON object, with the `id` and `type` properties. The value of the `id` property _MUST_ be a string, and _MUST_ be the HTTP(S) URI of the following Ordered Collection Page. The value of the `type` property _MUST_ be the string `OrderedCollectionPage`.

```json-doc
{
  "next": {
    "id": "https://example.org/activity/page-2",
    "type": "OrderedCollectionPage"
  }
}
```

##### prev

A reference to the previous page in the list of pages.

Ordered Collection Pages _MUST_ have a `prev` property, unless they are the first page in the Collection. The value _MUST_ be a JSON object, with the `id` and `type` properties. The value of the `id` property _MUST_ be a string, and _MUST_ be the HTTP(S) URI of the preceding Ordered Collection Page. The value of the `type` property _MUST_ be the string `OrderedCollectionPage`.

```json-doc
{
  "prev": {
    "id": "https://example.org/activity/page-1",
    "type": "OrderedCollectionPage"
  }
}
```

##### orderedItems

The Activities that are listed as part of this page. If the Activities have an `endTime` property, then they _MUST_ be ordered within the array from the earliest datetime to the most recent datetime, in the same way as the pages are ordered within the Ordered Collection. 

Ordered Collection Pages _MUST_ have an `orderedItems` property. The value _MUST_ be an array, with at least one item. Each item _MUST_ be a JSON object, conforming to the requirements of an Activity.

```json-doc
{
  "orderedItems": [
     {
     	"type": "Update",
     	"object": {
     		"id": "https://example.org/iiif/1/manifest",
     		"type": "Manifest"
     	},
     	"endTime": "2018-03-10T10:00:00Z"
     }
  ]
}
```


##### Complete Ordered Collection Page Example

```json-doc
{
  "@context": "http://iiif.io/api/discovery/1/context.json",
  "id": "https://example.org/activity/page-1",
  "type": "OrderedCollectionPage",
  "startIndex": 20,
  "partOf": {
    "id": "https://example.org/activity/all-changes",
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
      "type": "Update",
      "object": {
        "id": "https://example.org/iiif/1/manifest",
        "type": "Manifest"
      },
      "endTime": "2018-03-10T10:00:00Z"
    }
  ]
}
```

### 3.3. Activities
{: #activities}

The Activities are the means of describing the changes that have occurred in the content provider's system.

Content providers _MAY_ publish Activities separately from Ordered Collection Pages, and if so they _MUST_ be at the HTTP(S) URI given in the `id` property of the Activity.

##### id

An identifier for the Activity.

Activities _MAY_ have an `id` property. The value _MUST_ be a string and it _MUST_ be an HTTP(S) URI. The JSON representation of the Activity _MAY_ be available at the URI.

```json-doc
{ "id": "https://example.org/activity/1" }
```

##### type
{: #type-activity}

The type of Activity.

This specification uses the types described in the table below.

| Type   | Definition |
| ------ | ---------- |
| `Create` | The initial creation of the resource. Each resource _SHOULD_ have at most one `Create` Activity in which it is the `object`, but if the URI of the resource is re-used after a `Delete` activity, then there _MAY_ be more than one. |
| `Update` | Any change to the resource. In a system that does not distinguish creation from modification, then all changes _MAY_ have the `Update` type. |
| `Delete` | The deletion of the resource, or its de-publication from the web. Each resource _SHOULD_ have at most one `Delete` Activity in which it is the `object`, but _MAY_ have more than one if it is subsequently republished and then deleted again. |
| `Move`   | The re-publishing of the resource at a new URI, with the same content. Each resource _MAY_ have zero or more `Move` activities in which it is the `object` or `target`.|
| `Add`    | The addition of an object to a stream, outside of any of the above types of activity, such as a third party aggregator adding resources from a newly discovered stream. Each resource _SHOULD_ have at most one `Add` Activity in which it is the object, but if the resource is re-added after a `Remove` activity, then there _MAY_ be more than one. The `Add` Activity _SHOULD NOT_ be present if a `Create` or `Update` Activity is present at the same time. |
| `Remove` | The removal of an object from a stream, outside of any of the above types of activity, such as a third party aggregator removing resources from a stream that are no longer considered to be in scope. Each resource _SHOULD_ have at most one `Remove` activity, but if the resource is re-added and then re-removed, then there _MAY_ be more than one. The `Remove` Activity _SHOULD NOT_ be present if a `Delete` Activity is present at the same time.|
| `Refresh` | The beginning of an activity to refresh the stream with the state of all of the resources. It does not have an `object` or `target`. |
{: .api-table #table-type-dfn}

Activities _MUST_ have the `type` property. The value _MUST_ be a registered Activity type, and _SHOULD_ be one of `Create`, `Update`, or `Delete`.

```json-doc
{ "type": "Update" }
```

##### object

The IIIF resource that was affected by the Activity. It is an implementation decision whether there are separate lists of Activities, one per object type, or a single list with all of the object types combined.

In the case of the `Move` activity, the `object` property contains the `id` and `type` of the source from whence it was moved. The new location will be in the `target` property, described below.

Activities _MUST_ have the `object` property. The value _MUST_ be a JSON object, with the `id` and `type` properties. The `id` _MUST_ be an HTTP(S) URI. The `type` _SHOULD_ be a class defined in the IIIF Presentation API, and _SHOULD_ be one of `Collection`, or `Manifest`.  The `type`, therefore, _MAY_ be any class, including those not defined by the IIIF Presentation API, and consuming applications _SHOULD_ validate the `type` as being one that is appropriate for their usage.

The object _MAY_ have a `seeAlso` property, as defined for `OrderedCollection` above, to reference a document that describes the object resource. The document referenced in the `seeAlso` property _MAY_ also be referenced with the `seeAlso` property in an instance of the IIIF Presentation API. The `type` of the document referenced in the `seeAlso` property should be given as `Dataset`, meaning that it is data rather than a human-readable document.

The object _MAY_ have a `canonical` property, the value of which _MUST_ be a string that contains a URI.  This URI identifies the resource, regardless of the URI given in the `id` property of the object, which might be specific to a format, API version or publishing platform. The use of this property allows changes to be aligned across representations without relying on `seeAlso` links or only having a single representation.

The object _MAY_ have a `provider` property, as defined by the [IIIF Presentation API](https://iiif.io/api/presentation/3.0/#provider). In particular, the value of the property _MUST_ be an array of JSON objects, each of which _MUST_ have the `id`, `type` and `label` attributes, carrying the URI of the provider, the string "Agent", and the name of the provider in a language map object, respectively. 

```json-doc
{
  "object": {
    "id": "http://example.org/iiif/v3/1/manifest",
    "type": "Manifest",
    "canonical": "https://example.org/iiif/1",
    "seeAlso": [
      {
        "id": "https://example.org/dataset/single-item.jsonld",
        "type": "Dataset",
        "label": { "en": [ "Object Description in Schema.Org" ] },
        "format": "application/ld+json",
        "profile": "https://schema.org/"
      }
    ],
    "provider": [
      {
        "id": "https://example.org/about",
        "type": "Agent",
        "label": { "en": [ "Example Organization" ] }
      }
    ]
  }
}
```

##### target

The new location of the IIIF resource, after it was affected by a `Move` activity.

`Move` activities _MUST_ have the `target` property. The value _MUST_ be a JSON object, with the `id` and `type` properties. The `id` _MUST_ be an HTTP(S) URI, and _MUST_ be different from the URI given in the `object` property's `id`. The `type` _SHOULD_ be a class defined in the IIIF Presentation API, and _SHOULD_ be the same as the `object` property's `type`. Other properties that are usable for the description of `object`, such as `seeAlso` and `canonical` are also available for use in describing the `target`.

```json-doc
{
  "target": {
    "id": "http://example.org/a/manifest",
    "type": "Manifest",
    "seeAlso": [
      {
        "id": "https://example.org/single-item-a.jsonld",
        "type": "Dataset",
        "format": "application/ld+json"
      }
    ]
  }
}
```

##### endTime

The time at which the Activity was finished. It is up to the implementer to decide whether the value of `endTime` is the timestamp for the publication of the IIIF resource online or is the timestamp of the modification to the data in the managing system if these are different, but the decision _MUST_ be consistently applied. The changed resource given in `object` _MUST_ be available at its URI at or before the timestamp given in `endTime`. The value of `endTime` _SHOULD_ be before the time that the Activity is published as part of its Ordered Collection.

Activities _SHOULD_ have the `endTime` property. The value _MUST_ be a datetime expressed in UTC in the [xsd:dateTime][org-w3c-xsd-datetime] format.

```json-doc
{ "endTime": "2017-09-21T00:00:00Z" }
```

##### startTime

The time at which the Activity was started.

Activities _MAY_ have the `startTime` property. The value _MUST_ be a datetime expressed in UTC in the [xsd:dateTime][org-w3c-xsd-datetime] format.

```json-doc
{ "startTime": "2017-09-20T23:58:00Z" }
```

##### summary

A short textual description of the Activity. This is intended primarily to be used for debugging purposes or explanatory messages, and thus does not have the requirement for internationalization of the content. The intended audience of this field is a human who manages an aggregation service and is looking at the data, not an end user of the IIIF resource. It is not recommended that this field be present as in most situations it will never be seen.

Activities _MAY_ have the `summary` property. The value _MUST_ be a string.

```json-doc
{ "summary": "admin updated the manifest, fixing reported bug #15." }
```

##### actor

The organization, person, or software agent that carried out the Activity.

Activities _MAY_ have the `actor` property. The value _MUST_ be a JSON object, with the `id` and `type` properties. The `id` _SHOULD_ be an HTTP(S) URI. The `type` _MUST_ be one of `Application`, `Organization`, or `Person`.

```json-doc
{
  "actor": {
    "id": "https://example.org/person/admin1",
    "type": "Person"
  }
}
```

##### Complete Activity Example

A complete example Activity would thus look like the following example. Note that it does not have a `@context` property, as it is always embedded within a `CollectionPage`. Please note also that this is a complete example with all possible fields; most implementations will not need nor expose this level of data.

```json-doc
{
  "@context": "http://iiif.io/api/discovery/1/context.json",
  "id": "https://example.org/activity/1",
  "type": "Update",
  "summary": "admin updated the manifest, fixing reported bug #15.",
  "object": {
    "id": "https://example.org/iiif/1/manifest",
    "type": "Manifest",
    "canonical": "https://example.org/iiif/1",
    "seeAlso": [
      {
        "id": "https://example.org/dataset/single-item.jsonld",
        "type": "Dataset",
        "format": "application/ld+json"
      }
    ]
  },
  "endTime": "2017-09-21T00:00:00Z",
  "startTime": "2017-09-20T23:58:00Z",
  "actor": {
    "id": "https://example.org/person/admin1",
    "type": "Person"
  }
}
```


### 3.4. Linked Data Context and Extensions

#### 3.4.1. @context

The top level resource in the response _MUST_ have the `@context` property, and it _SHOULD_ appear as the very first key/value pair of the JSON representation. This property lets Linked Data processors interpret the document as a graph. The value of the property _MUST_ be either the URI of the IIIF Discovery context document, `http://iiif.io/api/discovery/1/context.json`, or an array of strings, where the URI of the IIIF Discovery context document is the last item in the array.

```json-doc
{
  "@context": "http://iiif.io/api/discovery/1/context.json"
}
```

#### 3.4.2. Extensions

If any additional types or properties are desired beyond the ones defined in this specification or the ActivityStreams specification, then those types or properties _SHOULD_ be mapped to RDF terms in one or more additional context documents. These extension contexts _SHOULD_ be added to the top level `@context` property, and _MUST_ be before the URI of the Discovery context. The JSON-LD 1.1 functionality of defining terms only within a specific property, known as [scoped contexts][org-w3c-json-ld-scoped-contexts], _MUST_ be used to minimize cross-extension collisions. Extensions intended for broad use _SHOULD_ be registered in the [extensions registry][registry].

```json-doc
{
  "@context": [
    "http://example.org/extension/context.json",
    "http://iiif.io/api/discovery/1/context.json"
  ]
}
```


### 3.5. Activity Streams Processing Algorithm
{: #activity-streams-processing-algorithm}

The aim of the processing algorithm is to inform developers implementing consuming applications how to make best use of the available information. The specification does not require any particular processing of the information by the consuming application, but considers indexing of the resource as a common use case in [section 3.5.3](#indexing).

Any other algorithm that arrives at the same results as an implementation of the algorithms specified below would also be considered to be conforming. The algorithms are provided as recommendations (_SHOULD_) rather than strict requirements in order to not overly constrain the usage or inhibit novel ideas and experimentation.

For processing multiple streams concurrently, there is additional processing work to be done to ensure the correct results, as the same activity might be represented in multiple streams. This is described in [section 3.5.4](#processing-multiple).


#### 3.5.1. Collection Algorithm
{: #collection-algorithm}

Given the URI of an ActivityStreams Collection (`collection`) as input, a conforming processor _SHOULD_:

<!-- This should be nested * markdown... but can't figure it -->

<ol>
  <li>Initialization:
    <ol>
      <li>Let <code class="highlighter-rouge">processedItems</code> be an empty array</li>
      <li>Let <code class="highlighter-rouge">lastCrawl</code> be the timestamp of the previous time the algorithm was executed or null if this is the first time the stream has been processed</li>
      <li>Let <code class="highlighter-rouge">onlyDelete</code> be <code class="highlighter-route">False</code></li>
    </ol>
  </li>
  <li>Retrieve the representation of <code class="highlighter-rouge">collection</code> via HTTP(S)</li>
  <li>Validate that the retrieved representation contains at least the features required for processing</li>
  <li>Find the URI of the last page at <code class="highlighter-rouge">collection.last.id</code> (<code class="highlighter-rouge">pageN</code>)</li>
<li>Apply the results of the page algorithm to <code class="highlighter-rouge">pageN</code></li>
</ol>

#### 3.5.2. Page Algorithm
{: #page-algorithm}

Given the URI of an ActivityStreams CollectionPage (`page`), a list of processed items (`processedItems`), the date of last crawling (`lastCrawl`), and a processing function (`process()`) as input, a conforming processor _SHOULD_:

<ol class="ordered-list">
  <li>Retrieve the representation of <code class="highlighter-rouge">page</code> via HTTP(S)</li>
  <li>Validate that the retrieved representation contains at least the features required for processing</li>
  <li>Find the set of updates of the page at <code class="highlighter-rouge">page.orderedItems</code> (<code class="highlighter-rouge">items</code>)</li>
  <li>In <b>reverse order</b>, iterate through the activities (<code class="highlighter-rouge">activity</code>) in <code class="highlighter-rouge">items</code>:
    <ol>
      <li>If <code class="highlighter-rouge">activity.endTime</code> is before <code class="highlighter-rouge">lastCrawl</code>, then terminate ;</li>
      <li>If <code class="highlighter-rouge">activity.type</code> is <code class="highlighter-rouge">Refresh</code>, then if <code class="highlighter-rouge">lastCrawl</code> is not null, then set <code class="highlighter-rouge">onlyDelete</code> to <code class="highlighter-rouge">True</code>, else if <code class="highlighter-rouge">lastCrawl</code> is null, then terminate;</li> 
      <li>If the updated resource's URI at <code class="highlighter-rouge">activity.object.id</code> is in <code class="highlighter-rouge">processedItems</code>, then continue ;</li>
      <li>If the updated resource's class at <code class="highlighter-rouge">activity.object.type</code> is not one that is known to the processor, then continue ;</li>
      <li>Otherwise, if <code class="highlighter-rouge">activity.type</code> is <code class="highlighter-rouge">Delete</code>, or it is <code class="highlighter-rouge">Remove</code> and <code class="highlighter-rouge">activity.origin.id</code> is the URI of the current stream, then find the URI of the resource at <code class="highlighter-rouge">activity.object.id</code> and process its removal ;</li>
      <li>Otherwise, if <code class="highligher-rouge">onlyDelete</code> is <code class="highlighter-rouge">True</code>, then continue ;</li>
      <li>Otherwise, if <code class="highlighter-rouge">activity.type</code> is <code class="highlighter-rouge">Update</code> or <code class="highlighter-rouge">Create</code>, or it is <code class="highlighter-rouge">Add</code> and <code class="highlighter-rouge">activity.target.id</code> is the URI of the current stream, then find the URI of the resource at <code class="highlighter-rouge">activity.object.id</code> (<code class="highlighter-rouge">object</code>) and process its inclusion ;</li>
      <li>Otherwise, if <code class="highlighter-rouge">activity.type</code> is <code class="highlighter-rouge">Move</code>, then find the original URI of the moved resource at <code class="highlighter-rouge">activity.object</code> and process its removal, and find the new URI of the moved resource at <code class="highlighter-rouge">activity.target</code> and process its inclusion.</li>
      <li>Add the processed resource's URI to <code class="highlighter-rouge">processedItems</code></li>
    </ol>
  </li>
  <li>Finally, find the URI of the previous page at <code class="highlighter-rouge">collection.prev.id</code> (<code class="highlighter-rouge">pageN1</code>)</li>
 <li>If there is a previous page, apply the results of the page algorithm to <code class="highlighter-rouge">pageN1</code></li>
</ol>

#### 3.5.3. Resource Processing: Indexing
{: #indexing}

While there are many possible algorithms to process the discovered resources and activities, a core use case for the Change Discovery API is to maintain an up-to-date index of the resources.

In this case, the objective of the consuming application is to find accurate, machine-readable descriptive information that might be used to build an index, and thus the application _SHOULD_ use the IIIF Presentation API `seeAlso` property to retrieve such a description if available. For different types of resources, and for different domains, the referenced descriptive resources will have different formats and semantics. If there are no such descriptions, or none that can be processed, the data in the Manifest and in other IIIF resources might be used as a last resort, despite its presentational intent.

#### 3.5.4. Processing Multiple Streams
{: #processing-multiple}

In order to process multiple streams simultaneously, the steps for processing a page should be followed, but applied to the set of changes across all of the streams, sorted by the timestamp of the activity. One motivating factor for this is that the same activity might appear in multiple streams, when the activities have been broadly aggregated. For example, the same update might occur in three streams out of ten that are being processed together, and should only be processed once.

Implementations that process activities beyond the most recent per resource should consider two activities with the same `type`, `object.id` and `endTime` to be the same activity regardless of any other properties. In this way, duplicate activities can be detected even if different streams maintain different degrees of description and information, or some implementations have activities available at their URIs and some do not.

The algorithm below does not take into account any optimizations or constraints around memory or processing. A more sophisticated algorithm might process pages, relying on each being sorted, to keep an interleaved buffer of activities full, rather than retrieving and processing everything before starting to process the activities. It is not described in as much detail as the processing algorithms above for this reason.

Given an array (`collections`) of collection URIs as input,

<ol class="ordered-list">
  <li>Initialize global values <code class="highlighter-rouge">processedItems</code> and  <code class="highlighter-rouge">lastCrawl</code> as above.</li>
  <li>Let  <code class="highlighter-rouge">allActivities</code> be an empty array.</li>
  <li>For each <code class="highlighter-rouge">collection</code> in <code class="highlighter-rouge">collections</code>:
    <ol>
      <li>Retrieve and validate the representation of <code class="highlighter-rouge">collection</code>.</li>
      <li>While there are pages with activities that have a timestamp after <code class="highlighter-rouge">lastCrawl</code>:
        <ol>
          <li>Retrieve and validate the representation of the page, and add the matching activities to <code class="highlighter-rouge">allActivities</code></li>
        </ol>
      </li>
    </ol>
  </li>
  <li>Sort <code class="highlighter-rouge">allActivities</code> by <code class="highlighter-rouge">activity.endTime</code>, descending, removing any duplicates as described above.</li>
  <li>For each activity in <code class="highlighter-rouge">allActivities</code>, apply the page algorithm's handling of an activity.</li>
</ol>

## 4. Network Considerations

### 4.1. Media Type

The base format for all responses of this API is JSON, as described above. 

If the server receives a request with an `Accept` header, it _SHOULD_ respond following the rules of [content negotiation][org-rfc-7231-conneg]. Note that content types provided in the `Accept` header of the request _MAY_ include parameters, for example `profile` or `charset`.

If the request does not include an `Accept` header, the HTTP `Content-Type` header of the response _SHOULD_ have the value `application/ld+json` (JSON-LD) with the `profile` parameter given as the context document: `http://iiif.io/api/discovery/1/context.json`.

``` none
Content-Type: application/ld+json;profile="http://iiif.io/api/discovery/1/context.json"
```
{: .urltemplate}

If the above `Content-Type` header value cannot be generated, then the value _SHOULD_ instead be `application/json` (regular JSON), without a `profile` parameter.

``` none
Content-Type: application/json
```
{: .urltemplate}

The HTTP server _SHOULD_ follow the [CORS requirements][org-w3c-cors] to enable browser-based clients to retrieve the responses. Recipes for enabling CORS and conditional Content-Type headers are provided in the [Apache HTTP Server Implementation Notes][notes-apache]. Responses _SHOULD_ be compressed by the server as there are significant performance gains to be made for very repetitive data structures.

### 4.2. Activities for Access-Restricted Content

Activities _MAY_ be published about content that has access restrictions. Clients _MUST NOT_ assume that they will be able to access every resource that is the object of an Activity, and _MUST NOT_ assume that it has been deleted if it is inaccessible. For example, the content might be protected by an authentication system that is denying access (an end user might be able to provide the right credentials to gain access) or there may be a temporary network outage preventing the content from being retrieved (the network will eventually be restored).

Content may also change from being available to being protected by access restrictions, or become available having previously been protected. There are no more specific activity types for these situations, and the publisher _SHOULD_ issue the regular `Update` or `Delete` activities accordingly.

### 4.3. Negotiable Resources

Some HTTP(S) URIs are able to respond with different representations of the same content in response to requests with different headers, such as the same URI being able to return both version 2 and version 3 of the IIIF Presentation API based on the Accept header. This is known as "content negotiation", and such resources are known as "negotiable resources". The representations that can be negotiated for are known as "variants".

Negotiable resources are not supported by the Discovery API, only variants. This means that there would be one Activity entry for each of the representations that are available, and that each representation _MUST_ have its own URI, even if it can also be reached via the negotiable resource. In the case of negotiating for different versions of the IIIF Presentation API, the `format` property can be used to include the full media type of the resource, where the version-specific context document is given in the `profile` parameter. If there are additional descriptive resources available, each such resource would describe all of the variants, and thus the `seeAlso` property of each Activity would refer to the same descriptions, allowing the variants to be connected together.

Two variants of the same negotiable resource can be represented as follows.

```json-doc
{
  "orderedItems": [
    {
      "type": "Update",
      "object": {
        "id": "https://example.org/iiif/1/manifest/v2",
        "type": "Manifest",
        "seeAlso": "https://example.org/iiif/1/metadata.xml",
        "format": "application/ld+json;profile=\"https://iiif.io/api/presentation/2/context.json\""
      },
      "endTime": "2018-03-10T10:00:00Z"
    },
    {
      "type": "Update",
      "object": {
        "id": "https://example.org/iiif/1/manifest/v3",
        "type": "Manifest",
        "seeAlso": "https://example.org/iiif/1/metadata.xml",
        "format": "application/ld+json;profile=\"https://iiif.io/api/presentation/3/context.json\""
      },
      "endTime": "2018-03-10T10:00:00Z"
    }
  ]
}
```


## Appendices

### A. Acknowledgements
{: #acknowledgements}

Many thanks to the members of the [IIIF community][iiif-community] for their continuous engagement, innovative ideas, and feedback.

This specification is due primarily to the work of the [IIIF Discovery Technical Specification Group][groups-discovery], chaired by Antoine Isaac (Europeana), Matthew McGrattan (Digirati) and Robert Sanderson (Yale University). The IIIF Community thanks them for their leadership, and the members of the group for their tireless work.

### B. Change Log
{: #change-log}

| Date       | Description           |
| ---------- | --------------------- |
| 2021-06-22 | Version 1.0 (Zooming Heatwave) |
| 2021-04-28 | Version 0.9.2 (unnamed) |
| 2020-09-29 | Version 0.9.1 (unnamed) |
| 2020-06-04 | Version 0.9 (unnamed) |
| 2019-11-01 | Version 0.4 (unnamed) |
| 2019-03-20 | Version 0.3 (unnamed) |
| 2018-11-12 | Version 0.2 (unnamed) |
| 2018-05-04 | Version 0.1 (unnamed) |

{% include links.md %}
