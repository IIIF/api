---
title: "IIIF Content Search API 2.0"
title_override: "IIIF Content Search API 2.0"
id: content-search-api
layout: spec
tags: [specifications, content-search-api]
major: 2
minor: 0
patch: 0
pre: alpha
cssversion: 2
redirect_from:
  - /api/search/2/index.html
editors:
  - name: Michael Appleby
    ORCID: https://orcid.org/0000-0002-1266-298X
    institution: Yale University
  - name: Dawn Childress  
    orcid: https://orcid.org/0000-0003-2602-2788
    institution: UCLA
  - name: Tom Crane
    ORCID: https://orcid.org/0000-0003-1881-243X
    institution: Digirati
  - name: Jeff Mixter
    orcid: https://orcid.org/0000-0002-8411-2952
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

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Introduction
{: #introduction}

In the IIIF (pronounced "Triple-Eye-Eff") [Presentation API][prezi-api], content is brought together from distributed systems via annotations.  That content might include images, often with a IIIF [Image API][image-api] service to access them, audio, video, rich or plain text, or anything else.  In a vibrant and dynamic system, that content can come from many sources and be rich, varied and abundant.  Of that list of content types, textual resources lend themselves to being searched, either as the transcription, translation or edition of the intellectual content, or commentary, description, tagging or other annotations about the object.  

This specification lays out the interoperability mechanism for performing these searches within the IIIF context.  The scope of the specification is searching annotation content within a single IIIF resource, such as a Manifest, Range or Collection.  Every effort is made to keep the interaction as consistent with existing IIIF patterns as possible.  Searching for metadata or other descriptive properties is __not__ in scope for this work.

In order to make searches easier against unknown content, a related service for the auto-completion of search terms is also specified. The auto-complete service is specific to a search service to ensure that the retrieved terms can simply be copied to the query of the search.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]

### 1.1. Use Cases
{: #use-cases}

Use cases for being able to search the annotations within the Presentation API include:

 * Searching OCR generated text to find words or phrases within a book, newspaper or other primarily textual content.
 * Searching transcribed content, provided by crowd-sourcing or transformation of scholarly output.
 * Searching multiple streams of content, such as the translation or edition, rather than the raw transcription of the content, to jump to the appropriate part of an object.
 * Searching on sections of text, such as defined chapters or articles.
 * Searching for user provided commentary about the resource, either as a discovery mechanism for the resource or for the discussion.
 * Discovering similar sections of text to compare either the content or the object.

User interfaces that could be built using the search response include highlighting matching words in the display, providing a heatmap of where the matches occur within the object, and providing a mechanism to jump between points within the object.  The auto-complete service assists users in identifying terms that exist within the selected scope.

### 1.2. Terminology
{: #terminology}

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].

## 2. Overview
{: #overview}

The IIIF [Presentation API][prezi-api] provides just enough information to a viewer so that it can present the images and other content to the user in a rich and understandable way.  Those content resources may have textual annotations associated with them.  Annotations may also be associated with the structural components of the Presentation API, such as the manifest itself, sequences, ranges, and layers.  Further, annotations can be replied to by annotating them to form a threaded discussion about the commentary, transcription, edition or translation.

Annotations are typically made available to viewing applications in an annotation list, where all of the annotations in the list target the same resource, or part of it.  Where known, these lists can be directly referenced from the manifest document to allow clients to simply follow the link to retrieve them.  For fixed, curated content, this is an appropriate method to discover them, as the annotations do not frequently change, nor are they potentially distributed amongst multiple servers. Annotation lists can be included in layers to group them together, such as by the source of the annotations, to allow the user to manipulate that grouping as a whole.

However this is less useful for comment-style annotations, crowd-sourced or distributed transcriptions, corrections to automated OCR transcription, and similar, as the annotations may be in constant flux.  Further, being able to quickly discover individual annotations without stepping through all of the views of an object is essential for a reasonable user experience.  This specification adds this capability to the IIIF suite of specifications.  

Beyond the ability to search for words or phrases, users find it helpful to have suggestions for what terms they should be searching for.  This facility is often called auto-complete or type-ahead, and within the context of a single object can provide insight into the language and content.  The auto-complete service is associated with a search service into which the terms can be fed as part of a query.

## 3. Search
{: #search}

The search service takes a query, including typically a search term or URI, and potentially filtering further by other properties including the date the annotation was created or last modified, the motivation for the annotation, or the user that created the annotation.

### 3.1. Service Description
{: #service-description}

Any resource in the Presentation API may have a search service associated with it.  The resource determines the scope of the content that will be searched.  A service associated with a manifest will search all of the annotations on canvases or other objects below the manifest, a service associated with a particular range will only search the canvases within the range, or a service on a canvas will search only annotations on that particular canvas.  

The description of the service follows the pattern established in the [Linking to Services][annex-services] specification.  The description block _MUST_ have the `@context` property with the value "http://iiif.io/api/search/{{ page.major }}/context.json", the  `profile` property with the value "http://iiif.io/api/search/{{ page.major }}/search", and the `id` property that contains the URI where the search can be performed.  

An example service description block:

``` json-doc
{
  // ... the resource that the search service is associated with ...
  "service": {
    "id": "http://example.org/services/identifier/search",
    "type": "SearchService2",
    "profile": "http://iiif.io/api/search/{{ page.major }}/search"
  }
}
```

### 3.2. Request
{: #request-1}

The search request is made to a service that is related to a particular Presentation API resource.  The URIs for services associated with different resources must be different to allow the client to use the correct one for the desired scope of the search.  To perform a search, the client _MUST_ use HTTP GET (rather than POST) to make the request to the service, with query parameters to specify the search terms.

#### 3.2.1. Query Parameters
{: #query-parameters}

Other than `q`, which is _RECOMMENDED_, all other parameters are _OPTIONAL_ in the request.  The default, if a parameter is empty or not supplied, is to not restrict the annotations that match the search by that parameter.  If the value is supplied but the field is not present in an annotation, then the search does not match that annotation. For example if an annotation does not have a creator, and the query specifies a `user` parameter, then the annotation does not match the query.

Servers _SHOULD_ implement the `q` and `motivation` parameters and _MAY_ implement the other parameters. Parameters that are received in a request but not implemented _MUST_ be ignored, and _SHOULD_ be included in the `ignored` property of the Layer in the response, described [below][ignored-parameters].

| Parameter  | Definition |
| ---------  | ---------- |
| `q`          | A space separated list of search terms. The search terms _MAY_ be either words (to search for within textual bodies) or URIs (to search identities of annotation body resources).  The semantics of multiple, space separated terms is server implementation dependent.|
| `motivation` | A space separated list of motivation terms. If multiple motivations are supplied, an annotation matches the search if any of the motivations are present. Expected values are given below. |
| `date`       | A space separated list of date ranges.  An annotation matches if the date on which it was created falls within any of the supplied date ranges. The dates _MUST_ be supplied in the ISO8601 format: `YYYY-MM-DDThh:mm:ssZ/YYYY-MM-DDThh:mm:ssZ`. The dates _MUST_ be expressed in UTC and _MUST_ be given in the `Z` based format. |
| `user`       | A space separated list of URIs that are the identities of users. If multiple users are supplied, an annotation matches the search if any of the users created the annotation. |
{: .api-table}

Common values for the motivation parameter can be found in the [IIIF Registry of Motivations][registry-motivations], including the two Content Search motivations `contextualizing` and `highlighting` defined in sections [3.4.2][search20-search-term-snippets] and [3.4.3][search20-search-term-highlighting] below.


#### 3.2.2. Example Request
{: #example-request}

This example request:

``` none
http://example.org/services/manifest/search?q=bird&motivation=painting
```
{: .urltemplate}

Would search for annotations with the word "bird" in their textual content, and have the motivation of `painting`.  It would search annotations within the resource the service was associated with.

### 3.3. Presentation API Compatible Responses
{: #presentation-api-compatible-responses}

The response from the server is an [annotation page][prezi30-annopage], following the format from the Presentation API with a few additional features.  This allows clients that already implement the AnnotationPage format to avoid further implementation work to support search results.

The search results are returned as annotations in the regular IIIF syntax. Note that the annotations can come from multiple canvases, rather than the default situation from the Presentation API where all of the annotations target a single canvas.

#### 3.3.1. Simple Lists
{: #simple-lists}

The simplest response looks exactly like a regular annotation page, where all of the matching annotations are returned in a single response. The value of `id` will be the same as the URI used in the query, however servers _MAY_ drop query parameters that are ignored so long as they are reported in the `ignored` property.

Clients wishing to know the total number of annotations that match may count the number of annotations in the `items` property, as all matches have been returned.  The full annotation description _MUST_ be included in the response, even if the annotations are separately dereferenceable via their URIs.

``` json-doc
{
  "@context":"http://iiif.io/api/presentation/{{ site.presentation_api.stable.major }}/context.json",
  "id":"http://example.org/service/manifest/search?q=bird&motivation=painting",
  "type":"AnnotationPage",

  "items": [
    {
      "id": "http://example.org/identifier/annotation/anno-line",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "A bird in the hand is worth two in the bush",
        "format": "text/plain"
      },
      "target": "http://example.org/identifier/canvas1#xywh=100,100,250,20"
    }
    // Further matching annotations here ...
  ]
}
```

#### 3.3.2. Paging Results
{: #paging-results}

For long lists of annotations, the server may choose to divide the response into multiple sections using an Annotation Collection. Each section is an Annotation Page and links to adjacent pages to allow the client to traverse the entire set. The Annotation Collection _MUST_ link to the first Annotation Page using the `first` property and _SHOULD_ link to the last Annotation Page using the `last` property.

The URI of the first Annotation Page reported in the `id` property _MAY_ be different from the one used by the client to request the search.  

Each Annotation Page _MUST_ have the `type` property, with the value of "AnnotationPage".  The next page of results that follows the current response _MUST_ be referenced in a `next` property, and the previous page _SHOULD_ be referenced in a `prev` property.  Each Annotation Page _SHOULD_ also have a `partOf` property with the value being the URI of the Annotation Collection.

An example request:

``` none
http://example.org/service/manifest/search?q=bird
```
{: .urltemplate}

And the responses for the Annotation Collection and the first page of annotations from a total of 125 matches:

``` json-doc
{
  "@context":"http://iiif.io/api/presentation/{{ site.presentation_api.stable.major }}/context.json",
  "id":"http://example.org/service/manifest/search?q=bird",
  "type":"AnnotationCollection",

  "total": 125,
  "first": {
    "id": "http://example.org/service/identifier/search?q=bird&page=1",
    "type": "AnnotationPage"
  },
  "last": {
    "id": "http://example.org/service/identifier/search?q=bird&page=13",
    "type": "AnnotationPage"
  },
}
```



``` json-doc
{
  "@context":"http://iiif.io/api/presentation/{{ site.presentation_api.stable.major }}/context.json",
  "id":"http://example.org/service/manifest/search?q=bird&page=1",
  "type":"AnnotationPage",

  "partOf": {
    "id": "http://example.org/service/manifest/search?q=bird",
    "type": "AnnotationCollection"
  },
  "next": {
    "id": "http://example.org/service/identifier/search?q=bird&page=2",
    "type": "AnnotationPage"
  },

  "items": [
    {
      "id": "http://example.org/identifier/annotation/anno-line",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "A bird in the hand is worth two in the bush",
        "format": "text/plain"
      },
      "target": "http://example.org/identifier/canvas1#xywh=100,100,250,20"
    }
    // Further annotations from the first page here ...
  ]
}  
```

#### 3.3.3. Target Resource Structure
{: #target-resource-structure}

The annotations may also include references to the structure or structures that the target (the resource in the `target` property) is found within.  The URI and type of the including resource _MUST_ be given, and a `label` _SHOULD_ be included.

This structure is called out explicitly as although it uses only properties from the Presentation API, it is not a common pattern and thus clients may not be expecting it.

``` json-doc
{
  "@context":"http://iiif.io/api/presentation/{{ site.presentation_api.stable.major }}/context.json",
  "id":"http://example.org/service/manifest/search?q=bird&motivation=painting",
  "type":"AnnotationPage",

  "items": [
    {
      "id": "http://example.org/identifier/annotation/anno-line",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "A bird in the hand is worth two in the bush",
        "format": "text/plain"
      },
      "target": {
        "id": "http://example.org/identifier/canvas1#xywh=100,100,250,20",
        "partOf": {
          "id": "http://example.org/identifier/manifest",
          "type": "Manifest",
          "label": {
            "en": "Example Manifest"
          }
        }
      }
    }
    // Further annotations here ...
  ]
}
```

### 3.4 Search API Specific Responses
{: #search-api-specific-responses}

There may be properties that are specific to the search result, and not features of the annotation in general, that are valuable to return to the client.  Examples of such properties include the text before and after the matched content (to allow a result snippet to be presented), the matched text itself (when case normalization, stemming or wildcards have been applied), and a reference to the set of annotations that together fulfill the search query (when a phrase spans across multiple annotations).

As these responses include Search specific information, the value of `@context` _MUST_ be an array with both the Presentation API and the Search API context URIs included, in that order.  This allows the two APIs to develop separately and yet remain as synchronized as possible.

To incrementally build upon existing solutions and provide graceful degradation for clients that do not support these features and retain compatibility with the Presentation API, the search API specific information is included in a second list of annotations called `annotations`, other than the `ignored` property. This structure mirrors the distinction in the [Presentation API][prezi3], where the main content annotations are listed in `items` and additional annotations such as comments are listed in `annotations`.

The extended structure is:

``` json-doc
{
  "@context":[
      "http://iiif.io/api/presentation/{{ site.presentation_api.stable.major }}/context.json",
      "http://iiif.io/api/search/{{ page.major }}/context.json"
  ],
  "id":"http://example.org/service/manifest/search?q=bird&page=1",
  "type":"AnnotationPage",

  "partOf": {
    "id": "http://example.org/service/manifest/search?q=bird",
    "type": "AnnotationCollection"
  },
  "next": {
    "id": "http://example.org/service/identifier/search?q=bird&page=2",
    "type": "AnnotationPage"
  },

  "ignored": [ "parameter" ], // Ignored parameters here ...

  "items": [
      // Regular content annotations here ...
  ],

  "annotations": [
    {
      "type": "AnnotationPage",
      "partOf": {
        "http://example.org/service/manifest/search?q=bird",
        "type": "AnnotationCollection",
        "total": 129
      }
      "items": [
        // Additional information in annotations here ...
      ]
    }
  ]
}
```

#### 3.4.1. Ignored Parameters
{: #ignored-parameters}

If the server has ignored any of the parameters in the request, then an `ignored` property _MUST_ be present, and _MUST_ contain a list of the ignored parameters.

If the request from previous examples had been:

``` none
http://example.org/service/manifest/search?q=bird&user=myusername
```
{: .urltemplate}

And the `user` parameter was ignored when processing the request, the response would be:

``` json-doc
{
  "@context":[
      "http://iiif.io/api/presentation/{{ site.presentation_api.stable.major }}/context.json",
      "http://iiif.io/api/search/{{ page.major }}/context.json"
  ],
  "id":"http://example.org/service/manifest/search?q=bird&page=1",
  "type":"AnnotationPage",

  "partOf": {
    "id": "http://example.org/service/manifest/search?q=bird",
    "type": "AnnotationCollection"
  },
  "next": {
    "id": "http://example.org/service/identifier/search?q=bird&page=2",
    "type": "AnnotationPage"
  },

  "ignored": ["user"],

  "items": [
    // Annotations ...
  ]
}
```


#### 3.4.2. Search Term Context
{: #search-term-snippets}


The simplest addition to the hit object is to add text that appears before and after the matching text in the annotation.  This allows the client to construct a snippet where the matching text is provided in the context of surrounding content, rather than simply by itself.  This is most useful when the service has word-level boundaries of the text on the canvas, such as are available when Optical Character Recognition (OCR) has been used to generate the text positions.

This is done by adding an entry to the `annotations` list with a `motivation` of "contextualizing", and a TextQuoteSelector with `prefix` and `suffix` of the text immediately before and after the matching content in the annotation. The matching content is conveyed in the `exact` property. The selector has the URI of the annotation it refers to in the `source` property, to be matched against the `id` property of the annotations in `items`.

For example, in a search for the query term "bird" in our example sentence, when the server has full word level coordinates:

``` none
http://example.org/service/manifest/search?q=bird
```
{: .urltemplate}

That the server matches against the plural "birds":

``` json-doc
{
  "@context":[
      "http://iiif.io/api/presentation/{{ site.presentation_api.stable.major }}/context.json",
      "http://iiif.io/api/search/{{ page.major }}/context.json"
  ],
  "id":"http://example.org/service/manifest/search?q=bird",
  "type":"AnnotationPage",

  "items": [
    {
      "id": "http://example.org/identifier/annotation/anno-bird",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "birds",
        "format": "text/plain"
      },
      "target": "http://example.org/identifier/canvas1#xywh=200,100,40,20"
    }
    // Further 'bird' annotations here ...
  ],

  "annotations": [
    {
      "type": "AnnotationPage",
      "partOf": {
        "id": "http://example.org/service/manifest/search?q=bird",
        "type": "AnnotationCollection",
        "total": 129
      }
      "items": [
        {
          "id": "http://example.org/identifier/annotation/match-1",
          "type": "Annotation",
          "motivation": "contextualizing",
          "target": {
            "type": "SpecificResource",
            "source": "http://example.org/identifier/annotation/anno-bird",
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

#### 3.4.3. Search Term Highlighting
{: #search-term-highlighting}

Many systems do not have full word-level coordinate information, and are restricted to line or paragraph level boundaries.  In this case the most useful thing that the client can do is to display the entire annotation and highlight the hits within it.  This is similar, but different, to the previous use case.  Here the word will appear somewhere within the `body` property of the annotation, and the client needs to make it more prominent.  In the previous situation, the word was the entire content of the annotation, and the information was convenient for presenting it in a list.

The client in this case needs to know the text that caused the service to create the hit, and enough information about where it occurs in the content to reliably highlight it and not highlight non-matching content of the annotation.  To do this, the service can use the `selector` pattern to supply the text before and after the matching term **within the content of the annotation**, again via a [Web Annotation Data Model][org-w3c-webanno-TextQuoteSelector] `TextQuoteSelector` object. The value of the `motivation` property is "highlighting" in this case, to distinguish from the search snippet in the previous section. Non-textual content, such as audio or video resources, would use other selectors instead, but the pattern would otherwise remain the same.  

``` none
http://example.org/service/manifest/search?q=bird
```
{: .urltemplate}

The result might be:

``` json-doc
{
  "@context":[
      "http://iiif.io/api/presentation/{{ site.presentation_api.stable.major }}/context.json",
      "http://iiif.io/api/search/{{ page.major }}/context.json"
  ],
  "id":"http://example.org/service/manifest/search?q=bird",
  "type":"AnnotationPage",

  "items": [
    {
      "id": "http://example.org/identifier/annotation/anno-bird",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "There are two birds in the bush",
        "format": "text/plain"
      },
      "target": "http://example.org/identifier/canvas1#xywh=200,100,200,20"
    }
    // Further 'bird' annotations here ...
  ],

  "annotations": [
    {
      "type": "AnnotationPage",
      "partOf": {
        "id": "http://example.org/service/manifest/search?q=bird",
        "type": "AnnotationCollection",
        "total": 129
      }
      "items": [
        {
          "id": "http://example.org/identifier/annotation/match-1",
          "type": "Annotation",
          "motivation": "highlighting",
          "target": {
            "type": "SpecificResource",
            "source": "http://example.org/identifier/annotation/anno-bird",
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

#### 3.4.4. Multi-Match Annotations
{: #multi-match-annotations}

The same annotation might generate multiple matches against a single query, especially if wildcards or stemming are enabled or the content of the annotation is long.

This is handled by having the content annotation only once, but to have two entries for it in the `annotations` list. Each entry then uses a different TextQuoteSelector on the same source Annotation to describe where the matching content can be found. A client could then process each in turn to highlight each match in the annotation.

For example, if the search was for words beginning with "b":

``` none
http://example.org/service/manifest/search?q=b*
```
{: .urltemplate}

The result might be:

``` json-doc
{
  "@context":[
      "http://iiif.io/api/presentation/{{ site.presentation_api.stable.major }}/context.json",
      "http://iiif.io/api/search/{{ page.major }}/context.json"
  ],
  "id":"http://example.org/service/manifest/search?q=b*",
  "type":"AnnotationPage",

  "items": [
    {
      "id": "http://example.org/identifier/annotation/anno-bird",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "There are two birds in the bush",
        "format": "text/plain"
      },
      "target": "http://example.org/identifier/canvas1#xywh=200,100,200,20"
    }
    // Further 'b' annotations here ...
  ],

  "annotations": [
    {
      "type": "AnnotationPage",
      "partOf": {
        "id": "http://example.org/service/manifest/search?q=bird",
        "type": "AnnotationCollection",
        "total": 521
      }
      "items": [
        {
          "id": "http://example.org/identifier/annotation/match-1",
          "type": "Annotation",
          "motivation": "highlighting",
          "target": {
            "type": "SpecificResource",
            "source": "http://example.org/identifier/annotation/anno-bird",
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
          "id": "http://example.org/identifier/annotation/match-2",
          "type": "Annotation",
          "motivation": "highlighting",
          "target": {
            "type": "SpecificResource",
            "source": "http://example.org/identifier/annotation/anno-bird",
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

#### 3.4.5. Multi-Annotation Matches
{: #multi-annotation-matches}

Given the flexibility of alignment between the sections of the text (such as word, line, paragraph, page, or arbitrary sections) and the annotations that expose that text to the client, there may be multiple annotations that are required to match a single multi-term search.

For example, imagine that the annotations are divided up line by line as they were manually transcribed that way, and that there are two lines of text. In this example the first line is "A bird in the hand", the second line is "is worth two in the bush", and the search is for the phrase "hand is". Therefore the match spans both of the line-based annotations.

In cases like this there are more annotations in the `items` list than in the `annotations` list as two or more annotations will be needed to make a match. This is handled by referencing all of the required annotations as multiple targets in a single highlighting annotation.

``` none
http://example.org/service/manifest/search?q=hand+is
```
{: .urltemplate}

``` json-doc
{
  "@context":[
      "http://iiif.io/api/presentation/{{ site.presentation_api.stable.major }}/context.json",
      "http://iiif.io/api/search/{{ page.major }}/context.json"
  ],
  "id":"http://example.org/service/manifest/search?q=hand+is",
  "type":"AnnotationPage",

  "items": [
    {
      "id": "http://example.org/identifier/annotation/anno-hand",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "A bird in the hand",
        "format": "text/plain"
      },
      "target": "http://example.org/identifier/canvas1#xywh=200,100,150,30"
    },
    {
      "id": "http://example.org/identifier/annotation/anno-is",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
        "type": "TextualBody",
        "value": "is worth two in the bush.",
        "format": "text/plain"
      },
      "target": "http://example.org/identifier/canvas1#xywh=200,140,170,30"
    }
    // Further annotations here ...
  ],

  "annotations": [
    {
      "type": "AnnotationPage",
      "partOf": {
        "id": "http://example.org/service/manifest/search?q=hand+is",
        "type": "AnnotationCollection",
        "total": 7
      }
      "items": [
        {
          "id": "http://example.org/identifier/annotation/match-1",
          "type": "Annotation",
          "motivation": "highlighting",
          "target": [
            {
              "type": "SpecificResource",
              "source": "http://example.org/identifier/annotation/anno-hand",
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
              "source": "http://example.org/identifier/annotation/anno-is",
              "selector": [
                {
                  "type": "TextQuoteSelector",
                  "exact": "is",
                  "suffix": " worth two in the"
                }
              ]
            },
          ]
        }
      ]
    }
  ]
}
```

## 4. Autocomplete
{: #autocomplete}

The autocomplete service returns terms that can be added into the `q` parameter of the related search service, given the first characters of the term.

### 4.1. Service Description
{: #service-description-1}

The autocomplete service is nested within the search service that it provides term completion for.  This is to allow multiple search services, each with their own autocomplete service.

The autocomplete service _MUST_ have an `id` property with the value of the URI where the service can be interacted with, and _MUST_ have a `profile` property with the value "http://iiif.io/api/search/{{ page.major }}/autocomplete" to distinguish it from other types of service.

``` json-doc
{
  // Resource that the services are associated with ...
  "service": {
    "@context": "http://iiif.io/api/search/{{ page.major}}/context.json",
    "id": "http://example.org/services/identifier/search",
    "profile": "http://iiif.io/api/search/{{ page.major }}/search",
    "service": {
      "id": "http://example.org/services/identifier/autocomplete",
      "profile": "http://iiif.io/api/search/{{ page.major }}/autocomplete"
    }
  }
}
```

### 4.2. Request
{: #request}

The request is very similar to the search request, with one additional parameter to allow the number of occurrences of the term within the object to be constrained.  The value of the `q` parameter, which is _REQUIRED_ for the autocomplete service, is the beginning characters from the term to be completed by the service.  For example, the query term of 'bir' might complete to 'bird', 'biro', 'birth', and 'birthday'.

The term should be parsed as a complete string, regardless of whether there is whitespace included in it. For example, the query term of "green bir" should not autocomplete on fields that match "green" and also include something that starts with "bir", but instead look for terms that start with the string "green bir".

The other parameters (`motivation`, `date` and `user`), if supported, refine the set of terms in the response to only ones from the annotations that match those filters.  For example, if the motivation is given as "painting", then only text from painting transcriptions will contribute to the list of terms in the response.


#### 4.2.1. Query Parameters
{: #query-parameters-1}

| Parameter | Definition |
| --------- | ---------- |
| `min`       | The minimum number of occurrences for a term in the index in order for it to appear within the response ; default is 1 if not present.  Support for this parameter is _OPTIONAL_ |
{: .api-table}

#### 4.2.2. Example Request
{: #example-request-1}

An example request

``` none
http://example.org/service/identifier/autocomplete?q=bir&motivation=painting&user=http%3A%2F%2Fexample.com%2Fusers%2Fazaroth42
```
{: .urltemplate}

### 4.3. Response
{: #response}

The response is a list (a "TermList") of simple objects that include the term, a link to the search for that term, and the number of matches that search will have.  The number of terms provided in the list is determined by the server.  

Parameters that were not processed by the service _MUST_ be returned in the `ignored` property of the main "TermList" object.  The value _MUST_ be an array of strings.

The objects in the list of terms are all of `type` "Term", and this _MAY_ be included explicitly but is not necessary.  The Term object has a number of possible properties:

  * The matching term is given as the value of the `match` property, and _MUST_ be present.
  * The link to the search to perform is the value of the `url` property, and this _MUST_ be present.
  * The number of matches for the term is the integer value of the `count` property, and _SHOULD_ be present.
  * A label to display instead of the match can be given as the value of the `label` property, and _MAY_ be present.  There may be more than one label given, to allow for internationalization.


The terms _SHOULD_ be provided in ascending alphabetically sorted order, but other orders are allowed, such as by the term's count descending to put the most common matches first.

The example request above might generate the following response:

``` json-doc
{
  "@context": "http://iiif.io/api/search/{{ page.major }}/context.json",
  "id": "http://example.org/service/identifier/autocomplete?q=bir&motivation=painting",
  "type": "TermList",
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

It is also possible to associate one or more `label`s to display to the user with URIs or other data that are searchable via the `q` parameter, rather than using the exact string that matched.  This can also be useful if stemming or other term normalization has occurred, in order to display the original rather than the processed term.

``` json-doc
{
  "@context": "http://iiif.io/api/search/{{ page.major }}/context.json",
  "id": "http://example.org/service/identifier/autocomplete?q=http%3A%2F%2Fsemtag.example.org%2Ftag%2Fb&motivation=tagging",
  "ignored": ["user"],
  "terms": [
    {
      "match": "http://semtag.example.org/tag/bird",
      "url": "http://example.org/service/identifier/autocomplete?motivation=tagging&q=http%3A%2F%2Fsemtag.example.org%2Ftag%2Fbird",
      "count": 15,
      "label": {
        "none": "bird"
        }
    },
    {
      "match": "http://semtag.example.org/tag/biro",
      "url": "http://example.org/service/identifier/autocomplete?motivation=tagging&q=http%3A%2F%2Fsemtag.example.org%2Ftag%2Fbiro",
      "count": 3,
      "label": {
        "none": "biro"
        }
    }
  ]
}
```


## 5. Property Definitions
{: #property-definitions}

after
:   The segment of text that occurs after the text that triggered the search to match the particular annotation.  The value _MUST_ be a single string.

    * A Hit _MAY_ have the `after` property.

before
:   The segment of text that occurs before the text that triggered the search to match the particular annotation.  The value _MUST_ be a single string.

    * A Hit _MAY_ have the `before` property.

count
:   The number of times that the term appears.  The value _MUST_ be an positive integer.

    * A Term _SHOULD_ have the `count` property.

ignored
:   The set of parameters that were received by the server but not taken into account when processing the query. The value _MUST_ be an array of strings.

    * A TermList or a Layer _MAY_ have an ignored property, and _MUST_ have it if the server ignored any query parameter.

match
:   The text that triggered the search to match the particular annotation.  The value _MUST_ be a single string.

    * A Hit _MAY_ have the `match` property.
    * A Term _MUST_ have the `match` property.


## Appendices

### A. Request Parameter Requirements

| Parameter | Required in Request | Required in Search | Required in Autocomplete |
| --------- | ------------------- | ------------------ | ------------------------ |
| `q`       | recommended | recommended | mandatory |
| `motivation` | optional | recommended | optional |
| `date`    | optional | optional | optional |
| `user`    | optional | optional | optional |
| `min`     | optional | n/a | optional |
{: .api-table}


### B. Versioning

This specification follows [Semantic Versioning][org-semver]. See the note [Versioning of APIs][notes-versioning] for details regarding how this is implemented.

### C. Acknowledgements

The production of this document was generously supported by a grant from the [Andrew W. Mellon Foundation][org-mellon].

Many thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### D. Change Log

| Date       | Description               |
| ---------- | ------------------------- |
| 2016-05-12 | Version 1.0 (Lost Summer) |
| 2015-07-20 | Version 0.9 (Trip Life)   |
{: .api-table}


[ignored-parameters]: #ignored-parameters

{% include acronyms.md %}
{% include links.md %}
