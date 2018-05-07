---
title: "IIIF Content Search API 0.9.3"
title_override: "IIIF Content Search API 0.9.3"
id: content-search-api
layout: spec
tags: [specifications, content-search-api]
major: 0
minor: 9
patch: 3
pre: draft
cssversion: 2
sitemap: false
---

## Status of this Document
{:.no_toc}
__This Version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest Stable Version:__ [{{ site.search_api.stable.major }}.{{ site.search_api.stable.minor }}.{{ site.search_api.stable.patch }}][stable-version]

{% include beta.md %}

**Editors**

  * **[Michael Appleby](https://orcid.org/0000-0002-1266-298X)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-1266-298X), [_Yale University_](http://www.yale.edu/)
  * **[Tom Crane](https://orcid.org/0000-0003-1881-243X)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0003-1881-243X), [_Digirati_](http://digirati.com/)
  * **[Robert Sanderson](https://orcid.org/0000-0003-4441-6852)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0003-4441-6852), [_Stanford University_](http://www.stanford.edu/)
  * **[Jon Stroop](https://orcid.org/0000-0002-0367-1243)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-0367-1243), [_Princeton University Library_](https://library.princeton.edu/)
  * **[Simeon Warner](https://orcid.org/0000-0002-7970-7855)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-7970-7855), [_Cornell University_](https://www.cornell.edu/)
  {: .names}

{% include copyright2015.md %}

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Introduction

In the IIIF (pronounced "Triple-Eye-Eff") [Presentation API][prezi-api], content is brought together from distributed systems via annotations.  That content might include images, often with a IIIF [Image API][image-api] service to access them, audio, video, rich or plain text, or anything else.  In a vibrant and dynamic system, that content can come from many sources and be rich, varied and abundant.  Of that list of content types, textual resources lend themselves to being searched, either as the transcription, translation or edition of the intellectual content, or commentary, description, tagging or other annotations about the object.  

This specification lays out the interoperability mechanism for performing these searches within the IIIF context.  The scope of the specification is searching annotation content within a single IIIF resource, such as a Manifest, Range or Collection.  Every effort is made to keep the interaction as consistent with existing IIIF patterns as possible.  Searching for metadata or other descriptive properties is __not__ in scope for this work.

In order to make searches easier against unknown content, a related service for the auto-completion of search terms is also specified. The auto-complete service is specific to a search service to ensure that the retrieved terms can simply be copied to the query of the search.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]

### 1.1. Use Cases

Use cases for being able to search the annotations within the Presentation API include:

 * Searching OCR generated text to find words or phrases within a book, newspaper or other primarily textual content.
 * Searching transcribed content, provided by crowd-sourcing or transformation of scholarly output.
 * Searching multiple streams of content, such as the translation or edition, rather than the raw transcription of the content, to jump to the appropriate part of an object.
 * Searching on sections of text, such as defined chapters or articles.
 * Searching for user provided commentary about the resource, either as a discovery mechanism for the resource or for the discussion.
 * Discovering similar sections of text to compare either the content or the object.

User interfaces that could be built using the search response include highlighting matching words in the display, providing a heatmap of where the matches occur within the object, and providing a mechanism to jump between points within the object.  The auto-complete service assists users in identifying terms that exist within the selected scope.

### 1.2. Terminology

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][rfc-2119].

## 2. Overview

The IIIF [Presentation API][prezi-api] provides just enough information to a viewer so that it can present the images and other content to the user in a rich and understandable way.  Those content resources may have textual annotations associated with them.  Annotations may also be associated with the structural components of the Presentation API, such as the manifest itself, sequences, ranges, and layers.  Further, annotations can be replied to by annotating them to form a threaded discussion about the commentary, transcription, edition or translation.

Annotations are typically made available to viewing applications in an annotation list, where all of the annotations in the list target the same resource, or part of it.  Where known, these lists can be directly referenced from the manifest document to allow clients to simply follow the link to retrieve them.  For fixed, curated content, this is an appropriate method to discover them, as the annotations do not frequently change, nor are they potentially distributed amongst multiple servers. Annotation lists can be included in layers to group them together, such as by the source of the annotations, to allow the user to manipulate that grouping as a whole.

However this is less useful for comment-style annotations, crowd-sourced or distributed transcriptions, corrections to automated OCR transcription, and similar, as the annotations may be in constant flux.  Further, being able to quickly discover individual annotations without stepping through all of the views of an object is essential for a reasonable user experience.  This specification adds this capability to the IIIF suite of specifications.  

Beyond the ability to search for words or phrases, users find it helpful to have suggestions for what terms they should be searching for.  This facility is often called auto-complete or type-ahead, and within the context of a single object can provide insight into the language and content.  The auto-complete service is associated with a search service into which the terms can be fed as part of a query.

## 3. Search

The search service takes a query, including typically a search term or URI, and potentially filtering further by other properties including the date the annotation was created or last modified, the motivation for the annotation, or the user that created the annotation.

### 3.1. Service Description

Any resource in the Presentation API may have a search service associated with it.  The resource determines the scope of the content that will be searched.  A service associated with a manifest will search all of the annotations on canvases or other objects below the manifest, a service associated with a particular range will only search the canvases within the range, or a service on a canvas will search only annotations on that particular canvas.  

The description of the service follows the pattern established in the [Linking to Services][service-annex] specification.  The description block _MUST_ have the `@context` property with the value "http://iiif.io/api/search/{{ page.major }}/context.json", the  `profile` property with the value "http://iiif.io/api/search/{{ page.major }}/search", and the `@id` property that contains the URI where the search can be performed.  

An example service description block:

``` json-doc
{
  // ... the resource that the search service is associated with ...
  "service": {
    "@context": "http://iiif.io/api/search/{{ page.major }}/context.json",
    "@id": "http://example.org/services/identifier/search",
    "profile": "http://iiif.io/api/search/{{ page.major }}/search"
  }
}
```

### 3.2. Request

The search request is made to a service that is related to a particular Presentation API resource.  The URIs for services associated with different resources must be different to allow the client to use the correct one for the desired scope of the search.  To perform a search, the client _MUST_ use HTTP GET (rather than POST) to make the request to the service, with query parameters to specify the search terms.

#### 3.2.1. Query Parameters

Other than `q`, which is _RECOMMENDED_, all other parameters are _OPTIONAL_ in the request.  The default, if a parameter is empty or not supplied, is to not restrict the annotations that match the search by that parameter.  If the value is supplied but the field is not present in an annotation, then the search does not match that annotation. For example if an annotation does not have a creator, and the query specifies a `user` parameter, then the annotation does not match the query.

Servers _SHOULD_ implement the `q` and `motivation` parameters and _MAY_ implement the other parameters. Parameters that are received in a request but not implemented _MUST_ be ignored, and _SHOULD_ be included in the `ignored` property of the Layer in the response, described [below][ignored-parameters].

| Parameter  | Definition |
| ---------  | ---------- |
| `q`          | A space separated list of search terms. The search terms _MAY_ be either words (to search for within textual bodies) or URIs (to search identities of annotation body resources).  The semantics of multiple, space separated terms is server implementation dependent.|
| `motivation` | A space separated list of motivation terms. If multiple motivations are supplied, an annotation matches the search if any of the motivations are present. Expected values are given below. |
| `date`       | A space separated list of date ranges.  An annotation matches if the date on which it was created falls within any of the supplied date ranges. The dates _MUST_ be supplied in the ISO8601 format: `YYYY-MM-DDThh:mm:ssZ/YYYY-MM-DDThh:mm:ssZ`. The dates _MUST_ be expressed in UTC and _MUST_ be given in the `Z` based format. |
| `user`       | A space separated list of URIs that are the identities of users. If multiple users are supplied, an annotation matches the search if any of the users created the annotation. |
{: .api-table}

Common values for the motivation parameter are:

| Motivation | Definition |
| ---------- | ---------- |
| `painting`     | Only annotations with the `sc:painting` motivation |
| `non-painting` | Annotations with any motivation other than `sc:painting` |
| `commenting`   | Annotations with the `oa:commenting` motivation |
| `describing`   | Annotations with the `oa:describing` motivation |
| `tagging`      | Annotations with the `oa:tagging` motivation |
| `linking`      | Annotations with the `oa:linking` motivation |
{: .api-table}

Other motivations are possible, and the full list from the [Open Annotation][openanno] specification _SHOULD_ be available by dropping the "oa:" prefix.  Other, community specific motivations _SHOULD_ include a prefix or use their full URI.

#### 3.2.2. Example Request

This example request:

``` none
http://example.org/services/manifest/search?q=bird&motivation=painting
```
{: .urltemplate}

Would search for annotations with the word "bird" in their textual content, and have the motivation of `painting`.  It would search annotations within the resource the service was associated with.

### 3.3. Presentation API Compatible Responses

The response from the server is an [annotation list][prezi-annolist], following the format from the Presentation API with a few additional features.  This allows clients that already implement the AnnotationList format to avoid further implementation work to support search results.

The search results are returned as annotations in the regular IIIF syntax. Note that the annotations can come from multiple canvases, rather than the default situation from the Presentation API where all of the annotations target a single canvas.

#### 3.3.1. Simple Lists

The simplest response looks exactly like a regular annotation list, where all of the matching annotations are returned in a single response. The value of `@id` will be the same as the URI used in the query, however servers _MAY_ drop query parameters that are ignored so long as they are reported in the `ignored` property.

Clients wishing to know the total number of annotations that match may count the number of annotations in the `resources` property, as all matches have been returned.  The full annotation description _MUST_ be included in the response, even if the annotations are separately dereferencable via their URIs.

``` json-doc
{
  "@context":"http://iiif.io/api/presentation/2/context.json",
  "@id":"http://example.org/service/manifest/search?q=bird&motivation=painting",
  "@type":"sc:AnnotationList",

  "resources": [
    {
      "@id": "http://example.org/identifier/annotation/anno-line",
      "@type": "oa:Annotation",
      "motivation": "sc:painting",
      "resource": {
        "@type": "cnt:ContentAsText",
        "chars": "A bird in the hand is worth two in the bush"
      },
      "on": "http://example.org/identifier/canvas1#xywh=100,100,250,20"
    }
    // Further matching annotations here ...
  ]
}
```

#### 3.3.2. Paging Results

For long lists of annnotations, the server may choose to divide the response into multiple sections, often called pages.  Each page is an annotation list and can refer to other pages to allow the client to traverse the entire set.  This uses the [paging features][paging] introduced in version 2.1 of the Presentation API, but is backwards compatible with version 2.0.  The next page of results that follows the current response _MUST_ be referenced in a `next` property of the annotation list, and the previous page _SHOULD_ be referenced in a `prev` property.  

The URI of the first annotation list reported in the `@id` property _MAY_ be different from the one used by the client to request the search.  Each page _SHOULD_ also have a `startIndex` property with an integer value that reports the position of the first result within the entire result set, where the first annotation has an index of 0.  For example, if the client has requested the first page which has 10 hits, then the `startIndex` will be 0, and the `startIndex` of second page will be 10, being the 11th hit.

All of the pages are within a [layer][prezi-layer] that represents the entire resultset of matched annotations.  The layer is the value of a `within` property on each of the page annotation lists, and is recorded as an object with properties.

The layer _MUST_ have the `@type` property, with the value of "sc:Layer".  It _SHOULD_ refer to the URIs of the first and last annotation list pages with `first` and `last` properties, respectively. The layer _SHOULD_ have a `total` property which is the total number of hits generated by the query, and it _MAY_ have a URI given as the value of the `@id` property.

An example request:

``` none
http://example.org/service/manifest/search?q=bird
```
{: .urltemplate}

And the response for the first page of annotations from a total of 125 matches:

``` json-doc
{
  "@context":"http://iiif.io/api/presentation/2/context.json",
  "@id":"http://example.org/service/manifest/search?q=bird&page=1",
  "@type":"sc:AnnotationList",

  "within": {
    "@type": "sc:Layer",
    "total": 125,
    "first": "http://example.org/service/manifest/search?q=bird&page=1",
    "last": "http://example.org/service/identifier/search?q=bird&page=13"
  },
  "next": "http://example.org/service/identifier/search?q=bird&page=2",
  "startIndex": 0,

  "resources": [
    {
      "@id": "http://example.org/identifier/annotation/anno-line",
      "@type": "oa:Annotation",
      "motivation": "sc:painting",
      "resource": {
        "@type": "cnt:ContentAsText",
        "chars": "A bird in the hand is worth two in the bush"
      },
      "on": "http://example.org/identifier/canvas1#xywh=100,100,250,20"
    }
    // Further annotations from the first page here ...
  ]
}
```

#### 3.3.3. Target Resource Structure

The annotations may also include references to the structure or structures that the target (the resource in the `on` property) is found within.  The URI and type of the including resource _MUST_ be given, and a `label` _SHOULD_ be included.

This structure is called out explicitly as although it uses only properties from the Presentation API, it is not a common pattern and thus clients may not be expecting it.

``` json-doc
{
  "@context":"http://iiif.io/api/search/{{ page.major }}/context.json",
  "@id":"http://example.org/service/manifest/search?q=bird&motivation=painting",
  "@type":"sc:AnnotationList",

  "resources": [
    {
      "@id": "http://example.org/identifier/annotation/anno-line",
      "@type": "oa:Annotation",
      "motivation": "sc:painting",
      "resource": {
        "@type": "cnt:ContentAsText",
        "chars": "A bird in the hand is worth two in the bush"
      },
      "on": {
        "@id": "http://example.org/identifier/canvas1#xywh=100,100,250,20",
        "within": {
          "@id": "http://example.org/identifier/manifest",
          "type": "sc:Manifest",
          "label": "Example Manifest"
        }
      }
    }
    // Further annotations here ...
  ]
}
```

### 3.4 Search API Specific Responses

There may be properties that are specific to the search result, and not features of the annotation in general, that are valuable to return to the client.  Examples include the text before and after the matched content to allow a result snippet to be presented, the matched text in case stemming or wildcards have been applied, or to link annotations that together fulfill the search query for a phrase, such as when the phrase spans across lines of text.

As these responses include Search specific information, the value of `@context` _MUST_ be an array with both the Presentation API and the Search API context URIs included, in that order.  This allows the two APIs to develop separately and yet remain as synchronized as possible.

To incrementally build upon existing solutions and provide graceful degradation for clients that do not support these features and retain compatibility with the Presentation API, the search API specific information is included in a second list within the annotation list called `hits`, other than the `ignored` property on the layer.  Annotation lists _MAY_ have this property, and servers _MAY_ support these features.

If supported, each entry in the `hits` list is a `search:Hit` object.  This type must be included as the value of the `@type` property. Hit objects reference one or more annotations that they provide additional information for, in a list as the value of the hit's `annotations` property.  The reference is made to the value of the `@id` property of the annotation, and thus annotations _MUST_ have a URI to enable this further information.

The basic structure is:

``` json-doc
{
  "@context":[
      "http://iiif.io/api/presentation/2/context.json",
      "http://iiif.io/api/search/{{ page.major }}/context.json"
  ],
  "@id":"http://example.org/service/manifest/search?q=bird&page=1",
  "@type":"sc:AnnotationList",

  "within": {
    "@type": "sc:Layer"
    // Result set information here ...
  },

  "resources": [
    {
      "@id": "http://example.org/identifier/annotation/anno1",
      "@type": "oa:Annotation"
      // More regular annotation information here ...
    }
    // Further annotations from the first page here ...
  ],

  "hits": [
    {
      "@type": "search:Hit",
      "annotations": [
        "http://example.org/identifier/annotation/anno1"
      ]
      // More search specific information for anno1 here ...
    }
    // Further hits for the first page here ...
  ]
}
```

#### 3.4.1. Ignored Parameters
{: #ignored-parameters}

If the server has ignored any of the parameters in the request, then the layer _MUST_ be present and _MUST_ have an `ignored` property where the value is a list of the ignored parameters.

If the request from previous examples had been:

``` none
http://example.org/service/manifest/search?q=bird&user=azaroth42
```
{: .urltemplate}

And the user parameter was ignored when processing the request, the response would be:

``` json-doc
{
  "@context":[
      "http://iiif.io/api/presentation/2/context.json",
      "http://iiif.io/api/search/{{ page.major }}/context.json"
  ],
  "@id":"http://example.org/service/manifest/search?q=bird&page=1",
  "@type":"sc:AnnotationList",

  "within": {
    "@type": "sc:Layer",
    "total": 125,
    "ignored": ["user"]
  },
  "next": "http://example.org/service/identifier/search?q=bird&page=2",
  "startIndex": 0,

  "resources": [
    // Annotations ...
  ]
}
```


#### 3.4.2. Search Term Snippets

The simplest addition to the hit object is to add text that appears before and after the matching text in the annotation.  This allows the client to construct a snippet where the matching text is provided in the context of surrounding content, rather than simply by itself.  This is most useful when the service has word-level boundaries of the text on the canvas, such as available when OCR has been used to generate the text positions.

The service _MAY_ add a `before` property to the hit with some amount of text that appears before the content of the annotation (given in `chars`), and _MAY_ also add an `after` property with some amount of text that appears after the content of the annotation.

For example, in a search for the query term "bird" in our example sentence, when the server has full word level coordinates:

``` none
http://example.org/service/manifest/search?q=bird
```
{: .urltemplate}

That the server matches against the plural "birds":

``` json-doc
{
  "@context":[
      "http://iiif.io/api/presentation/2/context.json",
      "http://iiif.io/api/search/{{ page.major }}/context.json"
  ],
  "@id":"http://example.org/service/manifest/search?q=bird",
  "@type":"sc:AnnotationList",

  "resources": [
    {
      "@id": "http://example.org/identifier/annotation/anno-bird",
      "@type": "oa:Annotation",
      "motivation": "sc:painting",
      "resource": {
        "@type": "cnt:ContentAsText",
        "chars": "birds"
      },
      "on": "http://example.org/identifier/canvas1#xywh=200,100,40,20"
    }
    // Further annotations here ...
  ],

  "hits": [
    {
      "@type": "search:Hit",
      "annotations": [
        "http://example.org/identifier/annotation/anno-bird"
      ],
      "before": "There are two ",
      "after": " in the bush"
    }
    // Further hits for the first page here ...
  ]
}
```

#### 3.4.3. Search Term Highlighting

Many systems do not have full word-level coordinate information, and are restricted to line or paragraph level boundaries.  In this case the most useful thing that the client can do is to display the entire annotation and highlight the hits within it.  This is similar, but different, to the previous use case.  Here the word will appear somewhere within the `chars` property of the annotation, and the client needs to make it more prominent.  In the previous situation, the word was the entire content of the annotation, and the information was convenient for presenting it in a list.

The client in this case needs to know the text that caused the service to create the hit, and enough information about where it occurs in the content to reliably highlight it and not highlight non-matches.  To do this, the service can supply text before and after the matching term within the content of the annotation, via an [Open Annotation][oa-textquotesel] `TextQuoteSelector` object.  TextQuoteSelectors have three properties: `exact` to record the exact text to look for, `prefix` with some text before the match, and `suffix` with some text after the match.

This would look like:

``` json-doc
{
  "@type": "oa:TextQuoteSelector",
  "exact": "birds",
  "prefix": "There are two ",
  "suffix": " in the bush"
}
```

As multiple words might match the query within the same annotation, multiple selectors may be given in the hit as objects within a `selectors` property.  For example, if the search used a wildcard to search for all words starting with "b" it would match the same annotation twice:

``` none
http://example.org/service/manifest/search?q=b*
```
{: .urltemplate}

The result might be:

``` json-doc
{
  "@context":[
      "http://iiif.io/api/presentation/2/context.json",
      "http://iiif.io/api/search/{{ page.major }}/context.json"
  ],
  "@id":"http://example.org/service/manifest/search?q=b*&page=1",
  "@type":"sc:AnnotationList",

  "resources": [
    {
      "@id": "http://example.org/identifier/annotation/anno-line",
      "@type": "oa:Annotation",
      "motivation": "sc:painting",
      "resource": {
        "@type": "cnt:ContentAsText",
        "chars": "There are two birds in the bush."
      },
      "on": "http://example.org/identifier/canvas1#xywh=200,100,40,20"
    }
    // Further annotations here ...
  ],

  "hits": [
    {
      "@type": "search:Hit",
      "annotations": [
        "http://example.org/identifier/annotation/anno-line"
      ],
      "selectors": [
        {
          "@type": "oa:TextQuoteSelector",
          "exact": "birds",
          "prefix": "There are two ",
          "suffix": " in the bush"
        },
        {
          "@type": "oa:TextQuoteSelector",
          "exact": "bush",
          "prefix": "two birds in the ",
          "suffix": "."
        }        
      ]
    }
    // Further hits for the first page here ...
  ]
}
```

#### 3.4.4. Multi-Annotations Hits

Given the flexibility of alignment between the sections of the text (such as word, line, paragraph, page, or arbitrary sections) and the annotations that expose that text to the client, there may be multiple annotations that match a single multi-term search. These differences will depend primarily on the method by which the text and annotations were generated and will likely be very different for manually transcribed texts and text that it is generated by Optical Character Recognition (OCR).

For example, imagine that the annotations are divided up line by line as they were manually transcribed that way and there are two lines of text. The first line is "A bird in the hand", the second line was "is worth two in the bush", and then the search is for the phrase "hand is", the match would span both of the line based annotations.  If the annotations were instead at word level, then phrases will always require multiple annotations.

In cases like this there are more annotations than hits as two or more annotations are needed to make up one hit.  The `match` property of the hit captures the text across the annotations.


``` json-doc
{
  "@context":[
      "http://iiif.io/api/presentation/2/context.json",
      "http://iiif.io/api/search/{{ page.major }}/context.json"
  ],
  "@id":"http://example.org/service/manifest/search?q=hand+is",
  "@type":"sc:AnnotationList",

  "resources": [
    {
      "@id": "http://example.org/identifier/annotation/anno-bird",
      "@type": "oa:Annotation",
      "motivation": "sc:painting",
      "resource": {
        "@type": "cnt:ContentAsText",
        "chars": "A bird in the hand"
      },
      "on": "http://example.org/identifier/canvas1#xywh=200,100,150,30"
    },
    {
      "@id": "http://example.org/identifier/annotation/anno-are",
      "@type": "oa:Annotation",
      "motivation": "sc:painting",
      "resource": {
        "@type": "cnt:ContentAsText",
        "chars": "is worth two in the bush"
      },
      "on": "http://example.org/identifier/canvas1#xywh=200,140,170,30"
    }
    // Further annotations here ...
  ],

  "hits": [
    {
      "@type": "search:Hit",
      "annotations": [
        "http://example.org/identifier/annotation/anno-bush",
        "http://example.org/identifier/annotation/anno-are"
      ],
      "match": "hand is",
      "before": "A bird in the ",
      "after": " worth two in the bush"
    }
    // Further hits for the first page here ...
  ]
}
```


## 4. Autocomplete

The autocomplete service returns terms that can be added into the `q` parameter of the related search service, given the first characters of the term.

### 4.1. Service Description

The autocomplete service is nested within the search service that it provides term completion for.  This is to allow multiple search services, each with their own autocomplete service.

The autocomplete service _MUST_ have an `@id` property with the value of the URI where the service can be interacted with, and _MUST_ have a `profile` property with the value "http://iiif.io/api/search/{{ page.major }}/autocomplete" to distinguish it from other types of service.

``` json-doc
{
  // Resource that the services are associated with ...
  "service": {
    "@context": "http://iiif.io/api/search/{{ page.major}}/context.json",
    "@id": "http://example.org/services/identifier/search",
    "profile": "http://iiif.io/api/search/{{ page.major }}/search",
    "service": {
      "@id": "http://example.org/services/identifier/autocomplete",
      "profile": "http://iiif.io/api/search/{{ page.major }}/autocomplete"
    }
  }
}
```

### 4.2. Request

The request is very similar to the search request, with one additional parameter to allow the number of occurrences of the term within the object to be constrained.  The value of the `q` parameter, which is _REQUIRED_ for the autocomplete service, is the beginning characters from the term to be completed by the service.  For example, the query term of 'bir' might complete to 'bird', 'biro', 'birth', and 'birthday'.

The term should be parsed as a complete string, regardless of whether there is whitespace included in it. For example, the query term of "green bir" should not autocomplete on fields that match "green" and also include something that starts with "bir", but instead look for terms that start with the string "green bir".

The other parameters (`motivation`, `date` and `user`), if supported, refine the set of terms in the response to only ones from the annotations that match those filters.  For example, if the motivation is given as "painting", then only text from painting transcriptions will contribute to the list of terms in the response.


#### 4.2.1. Query Parameters

| Parameter | Definition |
| --------- | ---------- |
| `min`       | The minimum number of occurrences for a term in the index in order for it to appear within the response ; default is 1 if not present.  Support for this parameter is _OPTIONAL_ |
{: .api-table}

#### 4.2.2. Example Request

An example request

``` none
http://example.org/service/identifier/autocomplete?q=bir&motivation=painting&user=azaroth42
```
{: .urltemplate}

### 4.2. Response

The response is a list (a "search:TermList") of simple objects that include the term, a link to the search for that term, and the number of matches that search will have.  The number of terms provided in the list is determined by the server.  

Parameters that were not processed by the service _MUST_ be returned in the `ignored` property of the main "TermList" object.  The value _MUST_ be an array of strings.

The objects in the list of terms are all of `@type` "search:Term", and this _MAY_ be included explicitly but is not necessary.  The Term object has a number of possible properties:

  * The matching term is given as the value of the `match` property, and _MUST_ be present.
  * The link to the search to perform is the value of the `url` property, and this _MUST_ be present.
  * The number of matches for the term is the integer value of the `count` property, and _SHOULD_ be present.
  * A label to display instead of the match can be given as the value of the `label` property, and _MAY_ be present.  There may be more than one label given, to allow for internationaliation.


The terms _SHOULD_ be provided in ascending alphabetically sorted order, but other orders are allowed, such as by the term's count descending to put the most common matches first.

The example request above might generate the following response:

``` json-doc
{
  "@context": "http://iiif.io/api/search/{{ page.major }}/context.json",
  "@id": "http://example.org/service/identifier/autocomplete?q=bir&motivation=painting",
  "@type": "search:TermList",
  "ignored": ["user"],
  "terms": [
    {
      "match": "bird",
      "url": "http://example.org/service/identifier/search?motivation=painting&q=bird",
      "count": 15
    },
    {
      "match": "biro",
      "url": "http://example.org/service/identifier/search?motivation=painting&q=biro",
      "count": 3
    },
    {
      "match": "birth",
      "url": "http://example.org/service/identifier/search?motivation=painting&q=birth",
      "count": 9
    },
    {
      "match": "birthday",
      "url": "http://example.org/service/identifier/search?motivation=painting&q=birthday",
      "count": 21
    }
  ]
}
```

It is also possible to associate one or more `label`s to display to the user with URIs or other data that are searchable via the `q` parameter, rather than using the exact string that matched.  This can also be useful if stemming or other term normalization has occured, in order to display the original rather than the processed term.

``` json-doc
{
  "@context": "http://iiif.io/api/search/{{ page.major }}/context.json",
  "@id": "http://example.org/service/identifier/autocomplete?q=http://semtag.example.org/tag/b&motivation=tagging",
  "ignored": ["user"],
  "terms": [
    {
      "match": "http://semtag.example.org/tag/bird",
      "url": "http://example.org/service/identifier/autocomplete?motivation=tagging&q=http://semtag.example.org/tag/bird",
      "count": 15,
      "label": "bird"
    },
    {
      "match": "http://semtag.example.org/tag/biro",
      "url": "http://example.org/service/identifier/autocomplete?motivation=tagging&q=http://semtag.example.org/tag/biro",
      "count": 3,
      "label": "biro"
    }
  ]
}
```


## 5. Property Definitions

after
:   The segment of text that occurs after the text that triggered the search to match the particular anotation.  The value _MUST_ be a single string.

    * A Hit _MAY_ have the `after` property.

before
:   The segment of text that occurs before the text that triggered the search to match the particular anotation.  The value _MUST_ be a single string.

    * A Hit _MAY_ have the `before` property.

count
:   The number of times that the term appears.  The value _MUST_ be an positive integer.

    * A Term _SHOULD_ have the `count` property.

ignored
:   The set of parameters that were received by the server but not taken into account when processing the query. The value _MUST_ be an array of strings.

    * A TermList or a Layer _MAY_ have an ignored property, and _MUST_ have it if the server ignored any query parameter.

match
:   The text that triggered the search to match the particular anotation.  The value _MUST_ be a single string.

    * A Hit _MAY_ have the `match` property.
    * A Term _MUST_ have the `match` property.


## Appendices

### A. Request Parameter Requirements

| Parameter | Required in Request | Required in Search | Required in Autocomplete |
| --------- | ------------------- | ------------------ | ------------------------ |
| `q`       | recommended | recommended | mandatory |
| `motivation` | optional | recommended | optional |
| `date`    | optional | optional | optional |
| `uri`     | optional | optional | optional |
| `min`     | optional | n/a | optional |
{: .api-table}


### B. Versioning

This specification follows [Semantic Versioning][semver]. See the note [Versioning of APIs][versioning] for details regarding how this is implemented.

### C. Acknowledgements

The production of this document was generously supported by a grant from the [Andrew W. Mellon Foundation][mellon].

Many thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### D. Change Log

| Date       | Description                                        |
| ---------- | -------------------------------------------------- |
| 2016-04-11 | Version 0.9.3 (Lost Summer) draft                  |
| 2016-02-08 | Version 0.9.2 (Trip Life) draft                    |
| 2015-12-05 | Version 0.9.1 (Trip Life) draft                    |
| 2015-07-20 | Version 0.9 (Trip Life) draft                      |
{: .api-table}


[cc-by]: http://creativecommons.org/licenses/by/4.0/ "Creative Commons &mdash; Attribution 4.0 International"
[iiif-discuss]: mailto:iiif-discuss@googlegroups.com "Email Discussion List"
[versioning]: {{ site.url }}{{ site.baseurl }}/api/annex/notes/semver/ "Versioning of APIs"
[mellon]: http://www.mellon.org/ "The Andrew W. Mellon Foundation"
[semver]: http://semver.org/spec/v2.0.0.html "Semantic Versioning 2.0.0"
[iiif-community]: {{page.webprefix}}/community/ "IIIF Community"
[stable-version]: {{ site.url }}{{ site.baseurl }}/api/search/{{ site.search_api.stable.major }}.{{ site.search_api.stable.minor }}/ "Stable Version"
[paging]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.0/

[image-api]: {{ site.url }}{{ site.baseurl }}/api/image/2.0/ "Image API"
[openanno]: http://www.openannotation.org/spec/core/ "Open Annotation"
[prezi-api]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.0/ "Presentation API"
[rfc-2119]: http://tools.ietf.org/html/rfc2119
[service-annex]: {{ site.url }}{{ site.baseurl }}/api/annex/services/
[prezi-annolist]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.0/#other-content-resources
[prezi-layer]: {{ site.url }}{{ site.baseurl }}/api/presentation/2.0/#Layers
[ignored-parameters]: #ignored-parameters
[oa-textquotesel]: http://www.openannotation.org/spec/core/

[icon-req]: {{ site.url }}{{ site.baseurl }}/img/metadata-api/required.png "Required"
[icon-rec]: {{ site.url }}{{ site.baseurl }}/img/metadata-api/recommended.png "Recommended"
[icon-opt]: {{ site.url }}{{ site.baseurl }}/img/metadata-api/optional.png "Optional"
[icon-na]: {{ site.url }}{{ site.baseurl }}/img/metadata-api/not_allowed.png "Not allowed"

{% include acronyms.md %}
