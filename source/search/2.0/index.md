---
title: "IIIF Content Search API 2.0"
title_override: "IIIF Content Search API 2.0"
id: content-search-api
layout: spec
tags: [specifications, content-search-api]
major: 2
minor: 0
patch: 0
pre: final
cssversion: 2
redirect_from:
  - /search/index.html
  - /api/search/2/index.html
editors:
  - name: Michael Appleby
    ORCID: https://orcid.org/0000-0002-1266-298X
    institution: Yale University
  - name: Dawn Childress  
    ORCID: https://orcid.org/0000-0003-2602-2788
    institution: UCLA
  - name: Tom Crane
    ORCID: https://orcid.org/0000-0003-1881-243X
    institution: Digirati
  - name: Jeff Mixter
    ORCID: https://orcid.org/0000-0002-8411-2952
    institution: OCLC
  - name: Robert Sanderson
    ORCID: https://orcid.org/0000-0003-4441-6852
    institution: Yale University
  - name: Simeon Warner
    ORCID: https://orcid.org/0000-0002-7970-7855
    institution: Cornell University

---

## Status of this Document
{:.no_toc}
__This Version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest Stable Version:__ [{{ site.search_api.stable.major }}.{{ site.search_api.stable.minor }}.{{ site.search_api.stable.patch }}][search-stable-version]

__Previous Version:__ [1.0.0][search1]

**Editors**

{% include api/editors.md editors=page.editors %}

{% include copyright.md %}

----

## 1. Introduction
{: #introduction}

In the IIIF (pronounced "Triple-Eye-Eff") [Presentation API][prezi-api], content is brought together from distributed systems via annotations. That content might include images, audio, video, rich or plain text, or anything else. In a vibrant and dynamic system, that content can come from many sources and be rich, varied and abundant. Of that list of content types, textual resources lend themselves to being searched, either as the transcription, translation or edition of the intellectual content, or commentary, description, tagging or other annotations about the object.  

This specification lays out the interoperability mechanism for performing these searches within the IIIF context. The scope of the specification is searching annotation content within a single IIIF resource, such as a Manifest, Canvas, Range or Collection. Every effort is made to keep the interaction as consistent with existing IIIF patterns as possible. Searching for metadata or other descriptive properties is __not__ in scope for this work.

In order to make searches easier against unknown content, a related service for the automatic completion of search terms is also specified.

We welcome [feedback][feedback] on all IIIF Specifications.

### 1.1. Use Cases
{: #use-cases}

Use cases for being able to search the annotations within the Presentation API include:

 * Searching OCR generated text to find words or phrases within a book, newspaper or other primarily textual content.
 * Searching transcribed content, provided by crowd-sourcing or transformation of scholarly output.
 * Searching multiple streams of content, such as the translation or edition, rather than the raw transcription of the content, to jump to the appropriate part of an object.
 * Searching on sections of text, such as defined chapters or articles.
 * Searching for user provided commentary about the resource, either as a discovery mechanism for the resource or for the discussion.
 * Discovering similar sections of text to compare either the content or the object.
 * Searching for non-textual annotations, such as tags or highlights.
 * Searching within captions, subtitles or transcriptions of audio/visual material.

User interfaces that could be built using the search response include highlighting matching words in the display, providing a heatmap of where the matches occur within the object, and providing a mechanism to jump between points within the object.

### 1.2. Terminology
{: #terminology}

This specification uses the following terms:

* __embedded__: When a resource (A) is embedded within an embedding resource (B), the complete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will not result in additional information. Example: Canvas A is embedded in Manifest B.
* __referenced__: When a resource (A) is referenced from a referencing resource (B), an incomplete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will result in additional information. Example:  Manifest A is referenced from Collection B.

The terms _array_, _JSON object_, _number_, _string_, and _boolean_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].

### 1.3. Common Specification Features
{: #common}

All IIIF specifications share common features to ensure consistency across the IIIF ecosystem. These features are documented in the [Presentation API][prezi3-considerations] and are foundational to this specification. Common principles for the design of the specifications are documented in the [IIIF Design Principles][annex-patterns].

## 2. Overview
{: #overview}

The IIIF [Presentation API][prezi-api] provides just enough information to a viewer so that it can present the images and other content to the user in a rich and understandable way. Those content resources may have textual annotations associated with them. Annotations may also be associated with the structural components of the Presentation API, such as a Collection, Manifest, or Range. Further, annotations can be replied to by annotating them to form a threaded discussion about the commentary, transcription, edition or translation.

Annotations are made available in IIIF via Annotation Pages, where typically the included Annotations target the same resource or part of it. Where known, these Annotation Pages can be directly referenced from the Manifest to allow clients to simply follow the link to retrieve them.
This specification uses Annotation Pages to deliver search results, in which the Annotations in one Annotation Page can target multiple Canvases or other resources, and the Annotation Pages are likely to be generated dynamically.

Beyond the ability to search for words or phrases, users find it helpful to have suggestions for what terms they should be searching for. This facility is often called autocomplete or type-ahead, and within the context of a single object can provide insight into the language and content.

This specification defines two services to be associated with IIIF resources: the Content Search service and the Autocomplete service.

## 3. Declaring Services
{: content-search-autocomplete-services}

The Content Search and the Autocomplete services are associated with IIIF resources using the `service` property, defined by the [Presentation API][prezi3-service] as an array of JSON objects. These objects _MUST_ have the `id` and `type` properties. The value of the `id` property _MUST_ be the URI used to interact with the service.

Any resource in the [Presentation API][prezi3] _MAY_ have a Content Search service associated with it. The resource determines the scope of the content that will be searched. A service associated with a Manifest will search all of the annotations on Canvases or other resources below the Manifest, a service associated with a particular Range will only search the Canvases within the Range, or a service on a Canvas will search only Annotations on that particular Canvas.  

An example service description block:

{% include api/code_header.html %}
``` json-doc
{
  // ... the resource that the search service is associated with ...
  "service": [
    {
      "id": "https://example.org/services/identifier/search",
      "type": "SearchService2"
    }
  ]
}
```

Any Content Search service _MAY_ have a nested Autocomplete service which provides term completion functionality specific to the Content Search service. This structure allows multiple Content Search services to be referenced, each with their own Autocomplete service.

The above service description block would become:

{% include api/code_header.html %}
``` json-doc
{
  // Resource that the services are associated with ...
  "service": [
    {
      "id": "https://example.org/services/identifier/search",
      "type": "SearchService2",
      "service": [
        {
          "id": "https://example.org/services/identifier/autocomplete",
          "type": "AutoCompleteService2"
        }
      ]
    }
  ]
}
```

## 4. Content Search
{: #search}

The Content Search service takes a query, typically including a search term or URI. Results may be constrained by other properties, such as the date the annotation was created or last modified, the motivation for the annotation, or the user that created the annotation.

### 4.1. Request
{: #request-1}

A search request is made to a service that is associated with a particular Presentation API resource. The URIs for services associated with different resources _MUST_ be different to allow the client to use the correct one for the desired scope of the search. To perform a search, the client _MUST_ use the HTTP GET method to make the request to the service, with query parameters to specify the search terms.

#### 4.1.1. Query Parameters
{: #query-parameters}

The following query parameters are defined:

| Parameter  | Definition |
| ---------  | ---------- |
| `q`          | A space separated list of search terms. For example, the search terms might be words (to search for within textual bodies) or URIs (to search identities of annotation body resources). The semantics of multiple, space separated terms is server implementation dependent.|
| `motivation` | A space separated list of motivation terms. If multiple motivations are supplied, an annotation matches the search if any of the motivations are present. Common values for the motivation parameter can be found in the [IIIF Registry of Motivations][registry-motivations], including the two Content Search motivations `contextualizing` and `highlighting` defined in sections [4.3.1][search20-match-context] and [4.3.2][search20-match-highlighting] below. |
| `date`       | A space separated list of date ranges. An annotation matches if the date on which it was created falls within any of the supplied date ranges. The dates _MUST_ be supplied in the ISO8601 format: `YYYY-MM-DDThh:mm:ssZ/YYYY-MM-DDThh:mm:ssZ`. The dates _MUST_ be expressed in UTC and _MUST_ be given in the `Z` based format. |
| `user`       | A space separated list of URIs that are the identities of users. If multiple users are supplied, an annotation matches the search if any of the supplied users created the annotation. |
{: .api-table}

Other than `q`, which is _RECOMMENDED_, all other parameters are _OPTIONAL_ in the request. The default, if a parameter is empty or not supplied, is to not restrict the annotations that match the search by that parameter. If the value is supplied but the field is not present in an annotation, then the search does not match that annotation. For example if an annotation does not have a creator, and the query specifies a `user` parameter, then the annotation does not match the query.

Servers _SHOULD_ implement the `q` and `motivation` parameters and _MAY_ implement the other parameters. Parameters defined by this specification that are received in a request but not implemented _MUST_ be ignored, and _MUST_ be included in the `ignored` property in the response, described [below](#ignored-parameters).

#### 4.1.2. Example Request
{: #example-request}

Consider the example request:

`https://example.org/service/manifest/search?q=bird&motivation=painting`

This request would search for annotations with the word "bird" in their textual content, and have the motivation of `painting`. It would search annotations within the resource with which the service was associated.

### 4.2. Responses
{: #responses}

The response from the server _MUST_ be an [Annotation Page][prezi30-annopage], following the format from the Presentation API with some additional features. This allows clients that already implement the Annotation Page format to avoid further implementation work to support search results.

#### 4.2.1. Simple Lists
{: #simple-lists}

The simplest response is a normal Annotation Page, where all of the matching Annotations are returned in a single response.

The total number of matching Annotations is the length of the `items` array, as all matching Annotations have been returned in the response. Every Annotation _MUST_ be fully embedded in the response.

Consider the example request:

`https://example.org/service/manifest/search?q=bird&motivation=painting`

This request might result in:

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/search/2/context.json",
  "id": "https://example.org/service/manifest/search?q=bird&motivation=painting",
  "type": "AnnotationPage",

  "items": [
    {
      "id": "https://example.org/identifier/annotation/anno-line",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "A bird in the hand is worth two in the bush",
        "format": "text/plain"
      },
      "target": "https://example.org/identifier/canvas1#xywh=100,100,250,20"
    }
    // Further matching annotations here ...
  ]
}
```

#### 4.2.2. Paging Results
{: #paging-results}

For long lists of Annotations, the server _MAY_ divide the response into multiple Annotation Pages within one Annotation Collection. The initial response is the first Annotation Page, which includes an embedded Annotation Collection and references subsequent pages to be retrieved.

The URI of the Annotation Page reported in the `id` property _MAY_ be different from the one used by the client to request the search. This would allow, for example, a `page` query parameter to be appended to the URI to allow the server to track which Annotation Page is being requested.

When results are paged, the Annotation Pages have several additional properties:

* `partOf` - The Annotation Page _MUST_ have a `partOf` property. The value is a JSON object, which is the embedded Annotation Collection resource, following the structure defined below.
* `next` - The Annotation Page _MUST_ have a `next` property if there is a subsequent page. The value is a JSON object with an `id` of the URI of the subsequent page, and `type` with a value of `AnnotationPage`.
* `prev` - The Annotation Page _SHOULD_ have a `prev` property if there is a previous page. The value is a JSON object with `id` containing the URI of the previous page, and `type` with a value of `AnnotationPage`.
* `startIndex` - The Annotation Page _MAY_ have a `startIndex` property, which is the position of the first Annotation in this page’s `items` list, relative to the overall ordering of Annotations across all pages within the Annotation Collection. The value is a zero-based integer.

The embedded Annotation Collection has the following properties:

* `first` - The Annotation Collection _MUST_ have a `first` property. The value is a JSON object, with an `id` of the URI of the first page, and `type` with a value of `AnnotationPage`.
* `last` - The Annotation Collection _MAY_ have a `last` property. The value is a JSON object, with an `id` of the URI of the last page, and `type` with a value of `AnnotationPage`.
* `total` - The Annotation Collection _MAY_ have a `total` property. The value is an integer, which is the total number of Annotations in the Collection, across all Annotation Pages.

Consider the example request:

`https://example.org/service/manifest/search?q=bird`

This request might result in the following response:

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/search/2/context.json",
  "id": "https://example.org/service/manifest/search?q=bird&page=1",
  "type": "AnnotationPage",

  "partOf": {
    "id": "https://example.org/service/manifest/search?q=bird",
    "type": "AnnotationCollection",
    "total": 125,
    "first": {
      "id": "https://example.org/service/identifier/search?q=bird&page=1",
      "type": "AnnotationPage"
    },
    "last": {
      "id": "https://example.org/service/identifier/search?q=bird&page=13",
      "type": "AnnotationPage"
    }
  },
  "next": {
    "id": "https://example.org/service/identifier/search?q=bird&page=2",
    "type": "AnnotationPage"
  },
  "startIndex": 0,

  "items": [
    {
      "id": "https://example.org/identifier/annotation/anno-line",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "A bird in the hand is worth two in the bush",
        "format": "text/plain"
      },
      "target": "https://example.org/identifier/canvas1#xywh=100,100,250,20"
    }
    // Further annotations from the first page here ...
  ]
}  
```

#### 4.2.3. References to Containing Resources
{: #references-containing-resources}

It is possible that Canvases referenced by the Annotations in the results are contained in Manifests that the client has not loaded, for example when searching in a Collection. In this and similar cases, it is important to have a reference to the containing resource so that a client can retrieve and render it.

This reference to the containing resource is included in the `target` structure of the Annotation, in a `partOf` property, with a JSON object as its value. The `id` and `type` of the containing resource _MUST_ be given, and a `label` _SHOULD_ be included.

Consider the example request:

`https://example.org/service/collection/search?q=bird&motivation=painting`

This request might result in:

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/search/2/context.json",
  "id": "https://example.org/service/collection/search?q=bird&motivation=painting",
  "type": "AnnotationPage",

  "items": [
    {
      "id": "https://example.org/identifier/annotation/anno-line",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "A bird in the hand is worth two in the bush",
        "format": "text/plain"
      },
      "target": {
        "id": "https://example.org/identifier/canvas1#xywh=100,100,250,20",
        "partOf": {
          "id": "https://example.org/manifest1868",
          "type": "Manifest",
          "label": {
            "en": [ "Example Manifest" ]
          }
        }
      }
    }
    // Further annotations here ...
  ]
}
```

#### 4.2.4. Ignored Parameters
{: #ignored-parameters}

If the server has ignored any of the parameters in the request, then an `ignored` property _MUST_ be present, and _MUST_ contain a list of the ignored parameters. Servers _MAY_ omit ignored query parameters from the `id` of the Annotation Page.

Consider the example request:

`http://example.org/service/manifest/search?q=bird&user=https%3A%2F%2Fexample.com%2Fusers%2Fwigglesworth`

If the `user` parameter was ignored when processing this request, the response could be:

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/search/2/context.json",
  "id": "http://example.org/service/manifest/search?q=bird&page=1",
  "type": "AnnotationPage",

  "ignored": [ "user" ],

  "items": [
    // Annotations ...
  ]
}
```

### 4.3. Extended Responses
{: #extended-responses}

Clients may require additional information about the matches in order to generate a rich user experience for search. This additional information about matches in search results is provided by further Annotations in a property called `annotations`. This structure maintains the distinction in the [Presentation API][prezi3], where the main content annotations are listed in `items` and additional annotations such as comments are listed in `annotations`. The value of `annotations` is an array containing a single Annotation Page, in which all of the Annotations reference Annotations in the `items` property.

The structure of extended responses is:

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/search/2/context.json",
  "id": "https://example.org/service/manifest/search?q=bird",
  "type": "AnnotationPage",

  "items": [
    // Matching Annotations here ...
  ],

  "annotations": [
    {
      "type": "AnnotationPage",
      "items": [
        // Annotations with additional information about matching Annotations here ...
      ]
    }
  ]
}
```

#### 4.3.1. Match Context
{: #match-context}

Search interfaces often display text before and after the matching text in a search result, as a snippet which shows the match in the context of the surrounding content. This is most useful when the service has word-level boundaries of the text on the Canvas, such as when OCR has been used to generate the text positions.

To meet this requirement, the Annotations have a `motivation` of `contextualizing`, and a [Web Annotation Data Model][org-w3c-webanno-TextQuoteSelector] `TextQuoteSelector` with `prefix` and `suffix` of the text immediately before and after the matching content in the annotation. The matching content is conveyed in the `exact` property. The selector has the URI of the annotation it refers to in the `source` property, to be matched against the `id` property of the annotations in `items`.

Consider a search request for the query term "bird":

`https://example.org/service/manifest/search?q=bird`

This request might match the plural "birds":

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/search/2/context.json",
  "id": "https://example.org/service/manifest/search?q=bird",
  "type": "AnnotationPage",

  "items": [
    {
      "id": "https://example.org/identifier/annotation/anno-bird",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "birds",
        "format": "text/plain"
      },
      "target": "https://example.org/identifier/canvas1#xywh=200,100,40,20"
    }
    // Further 'bird' annotations here ...
  ],

  "annotations": [
    {
      "type": "AnnotationPage",
      "items": [
        {
          "id": "https://example.org/identifier/annotation/match-1",
          "type": "Annotation",
          "motivation": "contextualizing",
          "target": {
            "type": "SpecificResource",
            "source": "https://example.org/identifier/annotation/anno-bird",
            "selector": [
              {
                "type": "TextQuoteSelector",
                "prefix": "There are two ",
                "exact": "birds",
                "suffix": " in the bush"
              }
            ]
          }
        }
      ]
    }
  ]
}
```

#### 4.3.2. Match Highlighting
{: #match-highlighting}

Many systems do not have full word-level coordinate information, and are restricted to line or paragraph level boundaries. In these cases the client may display the entire annotation and highlight the matches within it. This is similar, but different, to the match context use case. Here, the match is somewhere within the `body` property of the annotation and the client needs to make it more prominent.

The client needs to know the text that matched and enough information about where it occurs in the content to reliably highlight it and not highlight non-matching content. To do this, the service can use the `selector` pattern to supply the text before and after the matching term _within the content of the annotation_, again via a `TextQuoteSelector` object. The value of the `motivation` property is `highlighting` in this case, to distinguish from the match context use case. Non-textual content, such as audio or video resources, would use other selectors instead, but the pattern would otherwise remain the same.  

Consider the example request:

`https://example.org/service/manifest/search?q=bird`

This request might have the response:

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/search/2/context.json",
  "id": "https://example.org/service/manifest/search?q=bird",
  "type": "AnnotationPage",

  "items": [
    {
      "id": "https://example.org/identifier/annotation/anno-bird",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "There are two birds in the bush",
        "format": "text/plain"
      },
      "target": "https://example.org/identifier/canvas1#xywh=200,100,200,20"
    }
    // Further 'bird' annotations here ...
  ],

  "annotations": [
    {
      "type": "AnnotationPage",
      "items": [
        {
          "id": "https://example.org/identifier/annotation/match-1",
          "type": "Annotation",
          "motivation": "highlighting",
          "target": {
            "type": "SpecificResource",
            "source": "https://example.org/identifier/annotation/anno-bird",
            "selector": [
              {
                "type": "TextQuoteSelector",
                "prefix": "There are two ",
                "exact": "birds",
                "suffix": " in the bush"
              }
            ]
          }
        }
      ]
    }
  ]
}
```

#### 4.3.3. Multi-Match Annotations
{: #multi-match-annotations}

A query might result in multiple matches within a single annotation, especially if wildcards or stemming are enabled or the content of the annotation is long. This is handled by including the matching Annotation once in `items`, and the multiple entries that refer to it in the `annotations` list. Each entry then uses a different `TextQuoteSelector` on the same matching Annotation to describe where the matching content can be found. A client can process each entry in turn to highlight each match in the Annotation.

The Annotation Page in `annotations` _MAY_ embed an Annotation Collection allowing the response to include the total number of additional information Annotations. This Annotation Collection _MUST_ be different from the Annotation Collection embedded within the Annotation Page at the top level of the response. In this and similar scenarios, the values of the `total` properties of the two Annotation Collections may not be the same: the total number of matching annotations is determined by the division of the content, whereas the total number of additional annotations is determined by the query.

Consider the request for words beginning with "b":

`https://example.org/service/manifest/search?q=b*`

The request might have the response:

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/search/2/context.json",
  "id": "https://example.org/service/manifest/search?q=b*&page=1",
  "type": "AnnotationPage",

  "partOf": {
    "id": "https://example.org/service/manifest/search?q=b*",
    "type": "AnnotationCollection",
    "total": 129
  },

  "items": [
    {
      "id": "https://example.org/identifier/annotation/anno-bird",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "There are two birds in the bush",
        "format": "text/plain"
      },
      "target": "https://example.org/identifier/canvas1#xywh=200,100,200,20"
    }
    // Further 'b' annotations here ...
  ],

  "annotations": [
    {
      "id": "https://example.org/service/additional/search?q=b*&page=1",
      "type": "AnnotationPage",
      "partOf": {
        "id": "https://example.org/service/additional/search?q=b*",
        "type": "AnnotationCollection",
        "total": 521
      },
      "items": [
        {
          "id": "https://example.org/additional/annotation/match-1",
          "type": "Annotation",
          "motivation": "highlighting",
          "target": {
            "type": "SpecificResource",
            "source": "https://example.org/identifier/annotation/anno-bird",
            "selector": [
              {
                "type": "TextQuoteSelector",
                "prefix": "There are two ",
                "exact": "birds",
                "suffix": " in the bush"
              }
            ]
          }
        },
        {
          "id": "https://example.org/additional/annotation/match-2",
          "type": "Annotation",
          "motivation": "highlighting",
          "target": {
            "type": "SpecificResource",
            "source": "https://example.org/identifier/annotation/anno-bird",
            "selector": [
              {
                "type": "TextQuoteSelector",
                "prefix": "birds in the ",
                "exact": "bush"
              }
            ]
          }
        }
      ]
    }
  ]
}
```

#### 4.3.4. Multi-Annotation Matches
{: #multi-annotation-matches}

For some queries, matching result text may be spread across multiple annotations that encode the sections of the source text. This means that multiple matching annotations may be required to match a single search.

For example, imagine a set of manual transcription annotations which are divided up line by line, and that there are two lines of text. In this example the first line is "A bird in the hand", the second line is "is worth two in the bush", and the search is for the phrase "hand is". Therefore the match comprises parts of both line-based annotations.

In cases like this there are more annotations in the `items` list than in the `annotations` list as two or more annotations will be needed to make a match. This is handled by referencing all of the required matching annotations as multiple targets in a single annotation with the `highlighting` motivation in the `annotations` list.

Consider the example request:

`http://example.org/service/manifest/search?q=hand+is`

This request might have the response:

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/search/2/context.json",
  "id": "https://example.org/service/manifest/search?q=hand+is",
  "type": "AnnotationPage",

  "items": [
    {
      "id": "https://example.org/identifier/annotation/anno-hand",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "A bird in the hand",
        "format": "text/plain"
      },
      "target": "https://example.org/identifier/canvas1#xywh=200,100,150,30"
    },
    {
      "id": "https://example.org/identifier/annotation/anno-is",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "is worth two in the bush.",
        "format": "text/plain"
      },
      "target": "https://example.org/identifier/canvas1#xywh=200,140,170,30"
    }
  ],

  "annotations": [
    {
      "id": "https://example.org/service/additional/search?q=hand+is&page=1",
      "type": "AnnotationPage",
      "partOf": {
        "id": "https://example.org/service/additional/search?q=hand+is",
        "type": "AnnotationCollection",
        "total": 1
      },
      "items": [
        {
          "id": "https://example.org/additional/annotation/match-1",
          "type": "Annotation",
          "motivation": "highlighting",
          "target": [
            {
              "type": "SpecificResource",
              "source": "https://example.org/identifier/annotation/anno-hand",
              "selector": [
                {
                  "type": "TextQuoteSelector",
                  "prefix": "bird in the ",
                  "exact": "hand"
                }
              ]
            },
            {
              "type": "SpecificResource",
              "source": "https://example.org/identifier/annotation/anno-is",
              "selector": [
                {
                  "type": "TextQuoteSelector",
                  "exact": "is",
                  "suffix": " worth two in the"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## 5. Autocomplete
{: #autocomplete}

An Autocomplete service returns terms that can be used to perform a search using the related search service, given some characters.

### 5.1. Autocomplete Request
{: #request}

An Autocomplete request takes the same parameters as a Content Search request, with one addition:

| Parameter | Definition |
| --------- | ---------- |
| `min`     | The minimum number of occurrences for a term in the index in order for it to appear within the response; default is 1 if not present. Support for this parameter is _OPTIONAL_ |
{: .api-table}

The `q` parameter _MUST_ be present. Its value is interpreted as a single character string to match within terms in the index, often beginning characters. For example, the query term of 'bir' might complete to 'bird', 'biro', 'birth', and 'birthday'.

The other parameters (`motivation`, `date` and `user`), if supported, refine the set of terms in the response to only ones from the annotations that match those filters. For example, if the motivation is given as `painting`, then only text from painting transcriptions will contribute to the list of terms in the response.

An example request would be:

`https://example.org/service/identifier/autocomplete?q=bir&motivation=painting&user=https%3A%2F%2Fexample.com%2Fusers%2Fwigglesworth`

{: .urltemplate}

### 5.2. Autocomplete Response
{: #autocomplete-response}

Most auto-complete scenarios can be fulfilled by a simple list of terms. These terms can be converted into a search by using them as the value of the `q` parameter of the related Content Search service.

In order to accommodate this use case, a new class `TermPage` is introduced for the response, and a class `Term` to describe the values.

The `TermPage` has the following properties:

* `id` - The `TermPage` _MUST_ have an `id` property. The value is a URI and _MAY_ be different from the one requested.
* `type` - The `TermPage` _MUST_ have a `type` property. The value _MUST_ be `TermPage`.
* `ignored` - The `TermPage` _MAY_ have an `ignored` property. The value _MUST_ be an array of strings, each of which is the name of a query parameter which was ignored by the server.
* `items` - The `TermPage` _MUST_ have an `items` property. The value _MUST_ be an array of zero or more items. Each item _MUST_ be a JSON object, each of which is a `Term`.

In this simple case, `Term` resources have a single property `value` which contains the term string. The number of terms provided in the list is determined by the server.

Consider the example request:

`https://example.org/service/identifier/autocomplete?q=bir`

This request might have the response:

{% include api/code_header.html %}
```json-doc
{
  "@context": "http://iiif.io/api/search/2/context.json",
  "id": "https://example.org/service/identifier/autocomplete?q=bir",
  "type": "TermPage",  
  "items": [
    {
      "value": "bird"
    },
    {
      "value": "biro"
    },
    {
      "value": "birthday"
    }
  ]
}
```

### 5.3. Extended Autocomplete Responses
{: #extended-autocomplete-response}

There are cases where a simple list of terms is not sufficient to support use of the Autocomplete service. These include when a label is required to allow a user to select an appropriate term, when the term cannot be used as a query parameter directly, and when it is useful to know the total number of occurences of a term within the index.

The use cases are fulfilled by extending the properties of the `Term` resources to include further information.

`Term` resources have the following properties:

* `type` - The `Term` _MAY_ have a `type` property. If present, the value _MUST_ be `Term`. The use of the property is _NOT RECOMMENDED_ to keep the response shorter.
* `value` - The `Term` _MUST_ have a `value` property. The value is a the string form of the term.
* `total` - The `Term` _MAY_ have a `total` property. The value is an integer, which is the number of times the term occurs in the index.
* `label` - The `Term` _MAY_ have a `label` property. The value is a JSON object which follows the definition of a [language map][prezi30-languages]. This label should be displayed to the user instead of the `value`, for example when the `value` is a URI or a string that has been manipulated with stemming or other normalization.
* `language` - The `Term` _MAY_ have a `language` property. The value is a string conforming to the [BCP 47][org-bcp-47] language code specification, and gives the language of the term string in the `value` property.
* `service` - The `Term` _MAY_ have a `service` property. The value is an array of JSON objects, where each object is a Service. The `Term` _MUST_ include an entry for the full link to the related `SearchService2`, when the `value` cannot be used directly in the `q` parameter. In this case, the `id` of the service is the full link including the `q` and other parameters.

The usage of the properties in terms need not be consistent within a single response, and properties should only be included when needed.

The terms _SHOULD_ be provided in ascending alphabetically sorted order, but other orders are allowed, such as by the term's `total` count descending to put the most common matches first, or to alphabetize on the `label` rather than the `value`.

Consider the example request:

`https://example.org/service/identifier/autocomplete?q=bir&user=https%3A%2F%2Fexample.com%2Fusers%2Fwigglesworth`

This request might generate the response:

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/search/2/context.json",
  "id": "https://example.org/service/identifier/autocomplete?q=bir",
  "type": "TermPage",
  "ignored": [ "user" ],
  "items": [
    {
      "value": "bird",
      "language": "en",
      "total": 15
      },
    {
      "type": "Term",
      "value": "https://semtag.example.org/tag/biro",
      "total": 3,
      "label": {
        "en": [ "biro" ]
      },
      "service": [
        {
          "id": "https://example.org/service/identifier/search?motivation=tagging&q=semtag:biro",
          "type": "SearchService2"
        }
      ],      
    },
    {
      "value": "birth",
      "total": 9,
      "label": {
        "en": [ "birth" ],
        "fr": [ "naissance" ]
      }
    }
  ]
}
```


## Appendices


### A. Versioning

This specification follows [Semantic Versioning][org-semver]. See the note [Versioning of APIs][notes-versioning] for details regarding how this is implemented.

### B. Acknowledgements

Many thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

This specification is due primarily to the work of the [IIIF Content Search Technical Specification Group](https://iiif.io/community/groups/content-search-tsg/), chaired by Mike Bennett, Dawn Childress (UCLA), Tom Crane (Digirati), and the IIIF Editors, including Maria Whitaker (Indiana University, Editor 2020-2021). The IIIF Community thanks them for their leadership, and the members of the group for their tireless work.

### C. Change Log

| Date       | Description               |
| ---------- | ------------------------- |
| 2022-11-15 | Version 2.0 (Mr. Wigglesworth) [View change log][search20-change-log]|
| 2016-05-12 | Version 1.0 (Lost Summer) |
| 2015-07-20 | Version 0.9 (Trip Life)   |
{: .api-table}

{% include acronyms.md %}
{% include links.md %}
