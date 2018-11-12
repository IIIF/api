---
title: "IIIF Change Discovery API 0.2"
title_override: "IIIF Change Discovery API 0.2"
id: discovery-api
layout: spec
cssversion: 3
tags: [specifications, presentation-api]
major: 0
minor: 2
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

__Previous Version:__ [0.1][discovery01]

**Editors**

  * **[Michael Appleby](https://orcid.org/0000-0002-1266-298X)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-1266-298X), [_Yale University_](http://www.yale.edu/)
  * **[Tom Crane](https://orcid.org/0000-0003-1881-243X)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0003-1881-243X), [_Digirati_](http://digirati.com/)
  * **[Robert Sanderson](https://orcid.org/0000-0003-4441-6852)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0003-4441-6852), [_J. Paul Getty Trust_](http://www.getty.edu/)
  * **[Jon Stroop](https://orcid.org/0000-0002-0367-1243)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-0367-1243), [_Princeton University Library_](https://library.princeton.edu/)
  * **[Simeon Warner](https://orcid.org/0000-0002-7970-7855)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-7970-7855), [_Cornell University_](https://www.cornell.edu/)
  {: .names}

{% include copyright.md %}

__Status Warning__
This is a work in progress and may change without notice. Implementers should be aware that this document is not stable. Implementers are likely to find the specification changing in incompatible ways. Those interested in implementing this document before it reaches beta or release stages should join the IIIF [mailing list][iiif-discuss] and the [Discovery Specification Group][groups-discovery], take part in the discussions, and follow the [emerging issues][github-discovery-issues] on Github.
{: .warning}

----

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Introduction
{: #introduction}

The resources made available via the IIIF (pronounced "Triple-Eye-Eff") [Image][image-api] and [Presentation][prezi-api] APIs are only useful if they can be found. Users cannot interact directly with a distributed, decentralized ecosystem but instead must rely on services that harvest and process the available content, and then provide a user interface enabling navigation to that content via searching, browsing or other paradigms. Once the user has discovered the content, they can then display it in their viewing application of choice. Machine to machine interfaces are also enabled by this pattern, where software agents could interact via APIs to discover the same content and retrieve it for further analysis or processing.

This specification leverages existing techniques, specifications, and tools in order to promote widespread adoption. It enables the collaborative development of global or thematic search engines and portal applications that allow users to easily find and engage with content available via existing IIIF APIs.

### 1.1. Objectives and Scope
{: #objectives-and-scope}

The objective of the IIIF Change Discovery API is to provide the information needed to discover and subsequently make use of IIIF resources.  The intended audience is other IIIF aware systems that can leverage the content and APIs. While this work may benefit others outside of the IIIF community directly or indirectly, the objective of the API is to specify an interoperable solution that best and most easily fulfills the discovery needs within the community of participating organizations.

The discovery of IIIF resources requires a consistent and well understood pattern for content providers to publish lists of links to their available content. This allows a baseline implementation of discovery systems that process the list, looking for resources that have been added or changed.

This process can be optimized by allowing the content providers to publish descriptions of when their content has changed, enabling consuming systems to only retrieve the resources that have been modified since they were last retrieved. These changes might include when content is deleted or otherwise becomes unavailable. Finally, for rapid synchronization, a system of notifications pushed from the publisher to a set of subscribers can reduce the amount of effort required to constantly poll all of the systems to see if anything has changed. 

Work that is out of scope of this API includes the recommendation or creation of any descriptive metadata formats, and the recommendation or creation of metadata search APIs or protocols. The diverse domains represented within the IIIF community already have successful standards fulfilling these use cases, and the results of previous attempts to reconcile these standards across domains have not seen widespread adoption. Also out of scope is optimization of the transmission of content, for example recommendations about transferring any source media or data between systems.


__Notification of Changes__<br>This draft version of the specification does not include the subscription mechanism for enabling change notifications to be pushed to remote systems.  The current specification only enables the polling pattern where the set of changes must be periodically reprocessed. Notifications are likely to be added in a future version before 1.0.
{: .warning}

### 1.2. Terminology
{: #terminology}

The specification uses the following terms:

* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

The terms _array_, _JSON object_, _number_, and _string_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].


## 2. Overview of IIIF Resource Discovery
{: #overview-of-iiif-resource-discovery}

In order to discover IIIF resources, the state of those resources in the systems that publish them needs to be communicated succinctly and easily to a consuming system.  The consumer can then use that information to retrieve and process the resources of interest and provide machine or user interfaces that enable discovery.  This communication takes place via the IIIF Change Discovery API, which uses the W3C [Activity Streams][org-w3c-activitystreams] specification to describe and serialize changes to resources, where the semantics of those changes and the interactions between publishers and consumers are based on those identified by the [ResourceSync][org-openarchives-rsync] framework. 

Activities are used to describe the state of the publishing system by recording each individual change, in the order that they occur. The changes described are the creation, modification and deletion of IIIF Presentation API resources, primarily Collections and Manifests.  If the consuming application is aware of all of the changes that took place in the publishing system, it would have full knowledge of the set of resources available.  The focus on IIIF Collections and Manifests is because these are the main access points to published content and references to descriptive metadata about that content, however Activities describing changes to other resources could also be published in this way.

The Presentation API does not directly include descriptive metadata fields suitable for indexing beyond a simple full text search. The data intentionally lacks the semantics needed to construct indexes that enable advanced or fielded search. Instead, the Presentation API uses the `seeAlso` property to link to external documents that can have richer and domain-specific information about the content being presented. For example, a museum object might have a `seeAlso` reference to a CIDOC-CRM or LIDO description, while a bibliographic resource might reference a Dublin Core or MODS description. These external descriptions should be used when possible to provide interfaces giving access to more precise matching algorithms.

This specification describes three levels of conformance that build upon each other in terms of functionality enabled and precision of the information published. Sets of changes are published in pages, which are then collected together in a collection per publisher. To reduce barriers to implementation, care has been take to allow the implementation of all levels using only static files on a web server, rather than requiring dynamic access to a database.

### 2.1. Listing Resources and their Changes
{: #listing-resources-and-their-changes}

There are three levels of conformance at which changes can be described. Level 0 is simply a list of the resources available.  Level 1 adds timestamps and ordering from earliest change to most recent, allowing the consumer to stop processing once it encounters a change that it has already processed. Level 2 adds information about the types of activities, enabling the explicit creation and deletion of resources.

#### 2.1.1. Level 0: Basic Resource List
{: #level-0-basic-resource-list}

The core information required to provide a minimally effective set of links to IIIF resources is just the URIs of those resources. However, with the addition of some additional JSON structure wrapped around those URIs, we can be on the path towards a robust set of information that clients can use to optimize their processing.  

Starting with the IIIF resource URIs, we add an "Update" Activity wrapper around them.  The order of the resources in the resulting list is unimportant, but each should only appear once. In terms of optimization, this approach provides no additional benefit over any other simpler list format, but is compatible with the following levels which introduce significant benefits.  This is the minimum level for interoperability, while being compatible with the more detailed patterns described below.

If resources are deleted after being referred to in the resource list, the entire list should be republished without the reference to the deleted resource. Clients should also expect to encounter resource URIs that are out of date and no longer resolve to a IIIF Manifest or Collection.

Example Level 0 Activity:

```
{ 
  "type": "Update",
  "object": {
    "id": "https://example.org/iiif/1/manifest",
    "type": "Manifest"  	
  }
}
```

#### 2.1.2. Level 1: Basic Change List
{: #level-1-basic-change-list}

When dealing with large sets of resources, it can be useful to work with only those resources that have changed since the last time the list was processed. This can be facilitated by the addition of a time stamp that indicates when a resource was last modified or initially created. This is included using the `endTime` property, representing the time at which the activity of publishing the resource was finished. Lists with multiple activities are then ordered such that the most recent activities occur last. Consumers will then process the list of Activities in reverse order, from last to first, stopping when they encounter an Activity they have already processed in a previous run.

Example Level 1 Activity:

```
{
  "type": "Update",
  "object": {
    "id": "https://example.org/iiif/1/manifest",
    "type": "Manifest"
  },
  "endTime": "2017-09-20T00:00:00Z"
}
```

#### 2.1.3. Level 2: Complete Change List
{: #level-2-complete-change-list}

At the most detailed level, a log of all of the Activities that have taken place can be recorded, with the likelihood of multiple Activities per IIIF resource.  This allows the additional types of "Create" and "Delete", enabling a synchronization process to remove resources as well as add or update them. 

Example Level 2 Activity:

```
{
  "type": "Create",
  "object": {
    "id": "https://example.org/iiif/1/manifest",
    "type": "Manifest"
  },
  "endTime": "2017-09-20T00:00:00Z"
}
```

### 2.2. Pages of Changes
{: #pages-of-changes}

Activities are collected together into pages that together make up the entire set of changes that the publishing system has made. Pages reference the previous and next pages in that set, and the overall collection of which they are part. The Activities are listed such that the most recent activities occur last.

```
{
  "@context": "http://iiif.io/api/discovery/0/context.json",
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

As the number of Activities is likely too many to usefully be represented in a single Page, they are collected together into a Collection as the initial entry point. The Collection references the URIs of the first and last pages.

```
{
  "@context": "http://iiif.io/api/discovery/0/context.json",
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


## 3. Activity Streams Details
{: #activity-streams-details}

The W3C [Activity Streams][org-w3c-activitystreams] specification defines a "model for representing potential and completed activities", and is compatible with the [design patterns][annex-patterns] established for IIIF APIs. It is defined in terms of [JSON-LD][org-w3c-json-ld] and can be seamlessly integrated with the existing IIIF APIs. The model can be used to represent activities carried out by content publishers of creating, updating, and deleting (or otherwise de-publishing) IIIF resources.

This section is a summary of the properties and types used by this specification, and defined by Activity Streams.  This is intended to ease implementation efforts by collecting the relevant information together.

Properties, beyond those described in this specification, that the consuming application does not have code to process _MUST_ be ignored.  Other properties defined by Activity Streams _MAY_ be used, such as `origin` or `instrument`, but there are no current use cases that would warrant their inclusion in this specification.

### 3.1. Ordered Collection
{: #orderedcollection}

The top-most resource for managing the lists of Activities is an Ordered Collection, broken up into Ordered Collection Pages. This is the same pattern that the Web Annotation model uses for Annotation Collections and Annotation Pages. The Collection does not directly contain any of the Activities, instead it refers to the `first` and `last` pages of the list.  

The overall ordering of the Collection is from the oldest Activity as the first entry in the first page, to the most recent as the last entry in the last page. Consuming applications _SHOULD_ therefore start at the end and walk **backwards** through the list, and stop when they reach a timestamp before the time they last processed the list.

Content providers _MUST_ publish an Ordered Collection at the HTTP(S) URI listed in the `id` property of the Collection.

##### id

The identifier of the Ordered Collection.

Ordered Collections _MUST_ have an `id` property. The value _MUST_ be a string and it _MUST_ be an HTTP(S) URI. The JSON representation of the Ordered Collection _MUST_ be available at the URI.

```
{ "id": "https://example.org/activity/all-changes" }
```

##### type

The class of the Ordered Collection.

Ordered Collections _MUST_ have a `type` property.  The value _MUST_ be `OrderedCollection`.

```
{ "type": "OrderedCollection" }
```

##### first

A link to the first Ordered Collection Page for this Collection.

Ordered Collections _SHOULD_ have a `first` property.  The value _MUST_ be a JSON object, with the `id` and `type` properties.  The value of the `id` property _MUST_ be a string, and it _MUST_ be the HTTP(S) URI of the first page of items in the Collection. The value of the `type` property _MUST_ be a string, and _MUST_ be `OrderedCollectionPage`.

```
{ 
  "first": {
    "id": "https://example.org/activity/page-0",
    "type": "OrderedCollectionPage"
  }
}
```

##### last

A link to the last Ordered Collection Page for this Collection.  As the client processing algorithm works backwards from the most recent to least recent, the inclusion of `last` is _REQUIRED_, but `first` is only _RECOMMENDED_.

Ordered Collections _MUST_ have a `last` property.  The value _MUST_ be a JSON object, with the `id` and `type` properties.  The value of the `id` property _MUST_ be a string, and it _MUST_ be the HTTP(S) URI of the last page of items in the Collection. The value of the `type` property _MUST_ be a string, and _MUST_ be `OrderedCollectionPage`.

```
{ 
  "last": {
    "id": "https://example.org/activity/page-1234",
    "type": "OrderedCollectionPage"
  }
}
```

##### totalItems

The total number of Activities in the entire Ordered Collection.

OrderedCollections _MAY_ have a `totalItems` property.  The value _MUST_ be a non-negative integer.

```
{ "totalItems": 21456 }
```

##### context

This property is used to refer to one or more documents that semantically describe the set of resources that are being acted upon in the Activities within the OrderedCollection. This would allow the OrderedCollection to refer to, for example, a [DCAT][org-w3c-dcat] description of the dataset. For OrderedCollections that aggregate activities and/or objects from multiple sources, the referenced description should describe the complete aggregation rather than an individual source.

OrderedCollections _MAY_ have a `context` property (distinct from the `@context` property).  The value _MUST_ be an array of one or more JSON objects, with the `id` and `type` properties.  The value of the `id` property _MUST_ be a string, and it _MUST_ be the HTTP(S) URI of the description of the dataset. The value of the `type` property _MUST_ be a string, and _MUST_ be `Dataset`. The JSON object _MAY_ have the `mediaType` property, the value of which _MUST_ be a string, and it _MUST_ be the MIME media type of the referenced description document.

```
{
  "context": [
    {
      "id": "https://example.org/dataset/all-dcat.jsonld",
      "type": "Dataset",
      "mediaType": "application/ld+json"
    }
  ]
}
```


##### Complete Ordered Collection Example

```
{
  "@context": "http://iiif.io/api/discovery/0/context.json",
  "id": "https://example.org/activity/all-changes",
  "type": "OrderedCollection",
  "totalItems": 21456,
  "context": [
    {
      "id": "https://example.org/dataset/all-dcat.jsonld",
      "type": "Dataset",
      "mediaType": "application/ld+json"
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

The list of Activities is ordered both from page to page by following `prev` (or `next`) relationships, and internally within the page in the `orderedItems` property. The number of entries in each page is up to the implementer, and cannot be modified at request time by the client.

Content providers _MUST_ publish at least one Ordered Collection Page at the HTTP(S) URI given in the `id` property of the Page.

##### id

The identifier of the Collection Page.

Ordered Collection Pages _MUST_ have an `id` property. The value _MUST_ be a string and it _MUST_ be an HTTP(S) URI. The JSON representation of the Ordered Collection Page _MUST_ be available at the URI.

```
{ "id": "https://example.org/activity/page-0" }
```

##### type

The class of the Ordered Collection Page.

Ordered Collections _MUST_ have a `type` property.  The value _MUST_ be `OrderedCollectionPage`.

```
{ "type": "OrderedCollectionPage" }
```

##### partOf

The Ordered Collection that this Page is part of.

Ordered Collection Pages _SHOULD_ have a `partOf` property. The value _MUST_ be a JSON object, with the `id` and `type` properties.  The value of the `id` property _MUST_ be the a string, and _MUST_ be the HTTP(S) URI of the Ordered Collection that this page is part of.  The value of the `type` property _MUST_ be a string, and _MUST_ be `OrderedCollection`.

```
{
  "partOf": {
    "id": "https://example.org/activity/all-changes",
    "type": "OrderedCollection"
  }
}
```

##### startIndex

The position of the first item in this page's `orderedItems` list, relative to the overall ordering across all pages within the Collection.  The first entry in the overall list has a `startIndex` of 0.  If the first page has 20 entries, the first entry on the second page would therefore be 20.

Ordered Collection Pages _MAY_ have a `startIndex` property.  The value _MUST_ be a non-negative integer.

```
{ "startIndex": 20 }
```

##### next

A reference to the next page in the list of pages.

Ordered Collection Pages _SHOULD_ have a `next` property, unless they are the last Page in the Collection. The value _MUST_ be a JSON object, with the `id` and `type` properties.  The value of the `id` property _MUST_ be the a string, and _MUST_ be the HTTP(S) URI of the following Ordered Collection Page.  The value of the `type` property _MUST_ be a string, and _MUST_ be `OrderedCollectionPage`.

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

Ordered Collection Pages _MUST_ have a `prev` property, unless they are the first page in the Collection. The value _MUST_ be a JSON object, with the `id` and `type` properties.  The value of the `id` property _MUST_ be the a string, and _MUST_ be the HTTP(S) URI of the preceding Ordered Collection Page.  The value of the `type` property _MUST_ be a string, and _MUST_ be `OrderedCollectionPage`.

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

```
{
  "@context": "http://iiif.io/api/discovery/0/context.json",
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

The Activities are the means of describing the changes that have occured in the content provider's system.

Content providers _MAY_ publish Activities separately from Ordered Collection Pages, and if so they _MUST_ be at the HTTP(S) URI given in the `id` property of the Activity.

##### id

An identifier for the Activity.

Activities _MAY_ have an `id` property. The value _MUST_ be a string and it _MUST_ be an HTTP(S) URI. The JSON representation of the Activity _MAY_ be available at the URI.

```
{ "id": "https://example.org/activity/1" }
```

##### type

The type of Activity. 

This specification uses the types described in the table below.

| Type   | Definition |
| ------ | ---------- |
| `Create` | The initial creation of the resource.  Each resource _MUST_ have at most one `Create` Activity in which it is the `object`. |
| `Update` | Any change to the resource.  In a system that does not distinguish creation from modification, then all changes _MAY_ have the `Update` type. |
| `Delete` | The deletion of the resource, or its de-publication from the web. Each resource _MUST_ have at most one Activity in which it is the `object`. |
{: .api-table #table-type-dfn}

Activities _MUST_ have the `type` property. The value _MUST_ be a registered Activity class, and _SHOULD_ be one of `Create`, `Update`, or `Delete`.

```
{ "type": "Update" }
```

##### object

The IIIF resource that was affected by the Activity.  It is an implementation decision whether there are separate lists of Activities, one per object type, or a single list with all of the object types combined.

Activities _MUST_ have the `object` property.  The value _MUST_ be a JSON object, with the `id` and `type` properties.  The `id` _MUST_ be an HTTP(S) URI. The `type` _SHOULD_ be a class defined in the IIIF Presentation API, and _SHOULD_ be one of `Collection`, or `Manifest`. The object _MAY_ have a `context` property, as defined for `OrderedCollection` above, to reference a description document of the object resource. The document referenced in the `context` property _MAY_ also be referenced with the `seeAlso` property via the IIIF Presentation API.

<!-- This can't be on the Activity, as some activities reference more than one resource e.g. Add X to Y, Move X from Y to Z, etc. -->


```
{
  "object": {
    "id": "http://example.org/iiif/1/manifest",
    "type": "Manifest",
    "context": [
      {
        "id": "https://example.org/dataset/single-item.jsonld",
        "type": "Dataset",
        "mediaType": "application/ld+json"
      }
    ] 
  }
}
```

##### endTime

The time at which the Activity was finished. It is up to the implementer to decide whether the Activity includes the publication of the IIIF resource online, or only the internal data modification, but the decision _MUST_ be consistently applied. The changed resource given in `object` _MUST_ be available at its URI at or before the timestamp given in `endTime`. The value of `endTime` _SHOULD_ be before the time that the Activity is published as part of its Ordered Collection.

Activities _SHOULD_ have the `endTime` property.  The value _MUST_ be a datetime expressed in UTC in the [xsd:dateTime][org-w3c-xsd-datetime] format.

```
{ "endTime": "2017-09-21T00:00:00Z" }
```

##### startTime

The time at which the Activity was started.

Activities _MAY_ have the `startTime` property.  The value _MUST_ be a datetime expressed in UTC in the [xsd:dateTime][org-w3c-xsd-datetime] format.

```
{ "startTime": "2017-09-20T23:58:00Z" }
```

##### summary

A short textual description of the Activity. This is intended primarily to be used for debugging purposes or explanatory messages.

Activities _MAY_ have the `summary` property.  The value _MUST_ be a string.

```
{ "summary": "admin updated the manifest, fixing reported bug #15." }
```

##### actor

The organization, person, or software agent that carried out the Activity.

Activities _MAY_ have the `actor` property.  The value _MUST_ be a JSON object, with the `id` and `type` properties. The `id` _SHOULD_ be an HTTP(S) URI. The `type` _MUST_ be one of `Application`, `Organization`, or `Person`.

```
{ 
  "actor": {
    "id": "https://example.org/person/admin1",
    "type": "Person"
  }
}
```

##### Complete Activity Example

A complete example Activity would thus look like the following example. Note that it does not have a `@context` property, as it is always embedded within a `CollectionPage`.

```
{ 
  "id": "https://example.org/activity/1",
  "type": "Update",
  "summary": "admin updated the manifest, fixing reported bug #15.",
  "object": {
    "id": "https://example.org/iiif/1/manifest",
    "type": "Manifest",  	
    "context": [
      {
        "id": "https://example.org/dataset/single-item.jsonld",
        "type": "Dataset",
        "mediaType": "application/ld+json"
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


### 3.4. Activity Streams Processing Algorithm
{: #activity-streams-processing-algorithm}

The aim of the processing algorithm is to inform consuming applications how to make best use of the available information.

#### 3.4.1. Collection Algorithm
{: #collection-algorithm}

Given the URI of an ActivityStreams Collection (`collection`) as input, a conforming processor _SHOULD_:

<!-- This should be nested * markdown... but can't figure it -->

<ol>
  <li>Initialization:
    <ol>
      <li>Let <code class="highlighter-rouge">processedItems</code> be an empty array</li>
      <li>Let <code class="highlighter-rouge">lastCrawl</code> be the timestamp of the previous time the algorithm was executed</li>
    </ol>
  </li>
  <li>Retrieve the representation of <code class="highlighter-rouge">collection</code> via HTTP(S)</li>
  <li>Minimally validate that it conforms to the specification</li>
  <li>Find the URI of the last page at <code class="highlighter-rouge">collection.last.id</code> (<code class="highlighter-rouge">pageN</code>)</li>
<li>Apply the results of the page algorithm to <code class="highlighter-rouge">pageN</code></li>
</ol>

#### 3.4.2. Page Algorithm
{: #page-algorithm}

Given the URI of an ActivityStreams CollectionPage (`page`) and the date of last crawling (`lastCrawl`) as input, a conforming processor _SHOULD_:

<ol class="ordered-list">
  <li>Retrieve the representation of <code class="highlighter-rouge">page</code> via HTTP(S)</li>
  <li>Minimally validate that it conforms to the specification</li>
  <li>Find the set of updates of the page at <code class="highlighter-rouge">page.orderedItems</code> (<code class="highlighter-rouge">items</code>)</li>
  <li>In reverse order, iterate through the activities (<code class="highlighter-rouge">activity</code>) in <code class="highlighter-rouge">items</code>:
    <ol>
      <li>For each <code class="highlighter-rouge">activity</code>, if <code class="highlighter-rouge">activity.endTime</code> is before <code class="highlighter-rouge">lastCrawl</code>, then terminate ;</li>
      <li>If the updated resource's uri at <code class="highlighter-rouge">activity.object.id</code> is in <code class="highlighter-rouge">processedItems</code>, then continue ;</li>
      <li>Otherwise, if <code class="highlighter-rouge">activity.type</code> is <code class="highlighter-rouge">Update</code> or <code class="highlighter-rouge">Create</code>, then find the URI of the updated resource at <code class="highlighter-rouge">activity.object.id</code> (<code class="highlighter-rouge">object</code>) and process the resource ;</li>
      <li>Otherwise, if <code class="highlighter-rouge">activity.type</code> is <code class="highlighter-rouge">Delete</code>, then find the URI of the deleted resource at <code class="highlighter-rouge">activity.object.id</code> and process its removal.</li>
      <li>Add the processed resource's URI to <code class="highlighter-rouge">processedItems</code></li>
    </ol>
  </li>
  <li>Finally, find the URI of the previous page at <code class="highlighter-rouge">collection.prev.id</code> (<code class="highlighter-rouge">pageN1</code>)</li>
 <li>If there is a previous page, apply the results of the page algorithm to <code class="highlighter-rouge">pageN1</code></li>
</ol>

#### 3.4.3. Indexing
{: #indexing}

If the objective of the consuming application is to find descriptive information that might be used to build an index allowing the resources to be discovered, then the application _SHOULD_ use the IIIF Presentation API `seeAlso` property to discover an appropriate, machine-readable description of the resource.  For different types of resource, and for different domains, the external resources will have different formats and semantics. If there are no external descriptions, or none that can be processed, the data in the Manifest and in other IIIF resources might be used as a last resort, despite its presentational intent. 

## Appendices

### A. Acknowledgements
{: #acknowledgements}

Many thanks to the members of the [IIIF community][iiif-community] for their continuous engagement, innovative ideas, and feedback.

Many of the changes in this version are due to the work of the [IIIF Discovery Technical Specification Group][groups-discovery], chaired by Antoine Isaac (Europeana), Matthew McGrattan (Digirati) and Rob Sanderson (J. Paul Getty Trust). The IIIF Community thanks them for their leadership, and the members of the group for their tireless work.

### B. Change Log
{: #change-log}

| Date       | Description           |
| ---------- | --------------------- |
| 2018-11-12 | Version 0.2 (unnamed) |
| 2018-05-04 | Version 0.1 (unnamed) |

{% include links.md %}
 