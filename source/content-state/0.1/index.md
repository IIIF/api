---
title: "IIIF Import to Viewers API 0.1"
title_override: "IIIF Import to Viewers API 0.1"
id: discovery-api-import
layout: spec
cssversion: 3
tags: [specifications, presentation-api]
major: 0
minor: 1
patch: 0
pre: final
editors:
  - name: Michael Appleby
    orchid: https://orcid.org/0000-0002-1266-298X
    institution: Yale University
  - name: Tom Crane
    orchid: https://orcid.org/0000-0003-1881-243X
    institution: Digirati
  - name: Robert Sanderson
    orchid: https://orcid.org/0000-0003-4441-6852
    institution: J. Paul Getty Trust
  - name: Jon Stroop
    orchid: https://orcid.org/0000-0002-0367-1243
    institution: Princeton University Library
  - name: Simeon Warner
    orchid: https://orcid.org/0000-0002-7970-7855
    institution: Cornell University
hero:
  image: ''
---


## Status of this Document
{:.no_toc}
__This Version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest Stable Version:__ None

__Previous Version:__ None

**Editors:**

{% include api/editors.md editors=page.editors %}

{% include copyright.md %}

__Status Warning__
This is a work in progress and may change without notice. Implementers should be aware that this document is not stable. Implementers are likely to find the specification changing in incompatible ways. Those interested in implementing this document before it reaches beta or release stages should join the IIIF [mailing list][iiif-discuss] and the [Discovery Specification Group][groups-discovery], take part in the discussions, and follow the [emerging issues][github-discovery-issues] on Github.
{: .warning}

----


## 1. Introduction
{: #introduction}

The resources made available via the [IIIF Presentation API][prezi-api] are only useful if they can be found. While the [Change Discovery API][discovery01] specifies systems that allow these resources to be found, this document specifies a mechanism that allows a user to then open the found resource in a compatible environment, such as a viewer, annotation tool or other IIIF-compatible software.

This specification makes use of existing techniques and specifications in order to promote widespread adoption. It provides a way of describing a resource, or a part of a resource, in a compact format that can be used to initialise the view of that resource in any client that implements this specification. Linking from a search result to a viewer showing the relevant part of a found resource is one application of this specification. More generally, it provides a description of a _content state_, allowing such states to be shared between applications regardless of their different user interfaces and capabilities.

### 1.1. Objectives and Scope
{: #objectives-and-scope}

The objective of the IIIF Import to Viewers API is to enable the sharing of a standardised description of a view of one or more IIIF Presentation API resources, typically Manifests or Collections. The intended audience is developers of other IIIF-aware systems that can display the resources. While this work may benefit others outside of the IIIF community directly or indirectly, the objective of the API is to specify an interoperable solution that best and most easily fulfills these needs within the community of participating organizations.

The standardised view is a JSON-LD data structure that uses the models described by the [IIIF Presentation API][prezi-api] and [W3C Web Annotation Data Model][org-w3c-webanno] specifications. Viewers built to those specifications will already understand at least some of the model. This specification allows a content state to be passed to the viewer from outside, so that a viewer can show the intended part of the resource (or resources) to the user. The same model can be used by a viewer to _export_ a state, for example to enable a user to share a particular view with another user or publish it as a reference.

The specification describes the model for a content state, but does not mandate a particular mechanism for a viewer accepting the state for initialisation. Different IIIF clients have different user interfaces and audiences. The specification discusses several mechanisms, and more detailed examples may be found in the [IIIF Cookbook][annex-cookbook].


### 1.2. Terminology
{: #terminology}

The specification uses the following terms:

* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

The terms _array_, _JSON object_, _number_, and _string_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].

## 2. Content State
{: #content-state}

The content state data structure must allow the client to load the resources required, and present a particular part of the resource to the user. While _load Manifest M_ is the simplest case, a more specific state would provide more detail, for example:

* _load Manifest M, navigate to Canvas C, and zoom in to xywh=X,Y,W,H_
* _load manifest M, navigate such that Range R is selected, and start playing the time-based canvas C within Range R at time t=T_

A description like this can be expressed in purely IIIF terms, as an annotation that targets the intended part of the resource. This _content state_ is distinct from the state of a particular viewer's user interface. A viewer state is likely to be client-specific and would concern which panels are open, which options are selected and similar user interface details.  

### 2.1. Annotation Model for Content State

The target of the annotation is the IIIF resource, using exactly the same patterns as any other IIIF-targeting annotation that a IIIF viewer might encounter. A content state annotation has the motivation `highlighting`.

The target could be any resource described by the Presentation API, for example, a:

* Manifest
* Range
* Canvas
* spatial or temporal fragment of a Canvas
* spatial or temporal point on a Canvas

The annotation must contain enough information about dereferenceable resources to show the content in context. For example, a Canvas is almost certainly not enough information for a viewer to show the intended view; the Manifest the canvas is part of needs to be indicated so that the client can load it first and then find the Canvas within it.

### 2.2 Form of annotation

The content state data may be passed to a client in one of several forms, and a client _SHOULD_ be able to accept and process it in all of these forms.

* As the URL of an annotation, that the client must de-reference
* As JSON-LD, in the form of a full annotation
* As JSON-LD, as the value of the `target` property of an implied annotation with the motivation `highlighting`

If a client is capable of reading the content state from the value of an HTTP GET or POST request parameter, it _MUST_ look for the content state in a request parameter called `iiif-content`.

If a client is capable of reading the content state from an HTML attribute, the client _SHOULD_ look for the content state in an attribute called `data-iiif-content`.

Clients _MAY_ implement other mechanisms of accepting content state data; some suggestions are given in the next section.

A client _MUST_ be able to read and process the value in any of the three forms listed above. Consider the following, simplest possible content state annotation:

{% include api/code_header.html %}
``` json
{
  "@context": "http://iiif.io/api/presentation/{{ page.major }}/context.json",
  "id": "https://example.org/annotation-server/bookmarks/b1",
  "type": "Annotation",
  "motivation": ["highlighting"],
  "target": {
     "id": "https://example.org/iiif/item1/manifest",
     "type": "Manifest"
  }
}
```

If the string `https://example.org/annotation-server/bookmarks/b1` is passed as the value of `iiif-content` or `data-iiif-content`, the client _MUST_ load the resource at that URL and process it. The resource at that URL _MUST_ be the full annotation as in the example above.

The JSON-LD body given above may be passed directly in a request parameter, HTML attribute or other supported mechanism, for immediate processing. In this scenario the annotation does not require the `id` property.

The value passed to a client via this parameter (or other supported mechanisms) may be the `target` property of an implied annotation:

{% include api/code_header.html %}
``` json
{"id":"https://example.org/iiif/item1/manifest","type":"Manifest"}
```

This form is better suited to scenarios where compactness is important, for example a query string parameter.

The client _MUST_ examine the form of the string value of the property to determine whether it is JSON-LD or a URL, and if it is JSON-LD the client _MUST_ check the `type` property to determine whether it is a full annotation or just the target content state.

__Queries__<br/><br/>Does the inline full annotation version require `id`?<br/>Does it require `@context`?<br/>Should we require a different parameter name when the value is just the target of the annotation, rather than the full annotation, or should we stick to one parameter and require the client to check its `type` and process accordingly?<br/>For nicer query string parameters, should we permit a syntax that is invalid JSON-LD but valid JSON in the same form (i.e., no quotes, and/or single quotes), or even not valid JSON?:<br/><br/>`viewer.html?iiif-content={"id":"https://example.org/iiif/item1/manifest","type":"Manifest"}`<br/><br/><a href="http://tify.sub.uni-goettingen.de/demo.html?manifest=https://manifests.sub.uni-goettingen.de/iiif/presentation/PPN857449303/manifest">See TIFY to get an idea of what this feels like</a> (observe the `tify` parameter as you change the content state).<br/><br/>Should the client be required to accept the JSON-LD in base64-encoded form?
{: .warning}

## 3. Initialisation
{: #initialisation}

This specification does not impose limits on the mechanisms that IIIF compatible software can use to expose, share and transfer content state descriptions, nor what form IIIF compatible software itself may take (e.g., a web page, a JavaScript web application, a native mobile application, a desktop application, or display kiosk hardware). Please see the [IIIF Cookbook][annex-cookbook] for examples of the patterns listed below.

### 3.1. Initialisation mechanisms
{: #initialisation-mechanisms}

The data structure _MAY_ be made available to the client via a number of methods, including (but not limited to):

* The client looks for the content state URL or data as the value of an HTTP GET request parameter `iiif-content` on its containing page (subject to the 2 KB limit)
* The client looks for the content state URL or data as the value of an HTTP POST request parameter `iiif-content`
* The client allows the content state URL or data to be pasted into part of its UI (e.g., from a "Load..." option). This same mechanism may also accept a Manifest or Collection resource URL directly.
* The client exposes the current content state in its UI (e.g., "Share this")
* The client looks for the content state URL or data in an initialisation parameter `data-iiif-content`
* The data is a parameter in an HTML5 Drag and Drop operation (LINK TO COOKBOOK RECIPE...)


## 4. Further Examples

The following examples demonstrate the use of the existing IIIF Presentation API and W3C Web Annotation Data Model to describe parts of resources. The full form of the annotation (as if it were available at the URL given in the `id` property) has been used in each case.  Further examples can be found in the [IIIF Cookbook][annex-cookbook]

### 4.1. A region of a canvas in a manifest

{% include api/code_header.html %}
``` json
{
  "@context": "http://iiif.io/api/presentation/{{ page.major }}/context.json",
  "id": "https://example.org/import/1",
  "type": "Annotation",
  "motivation": ["highlighting"],
  "target": {
     "id": "https://example.org/object1/canvas7#xywh=1000,2000,1000,2000",
     "type": "Canvas",
     "partOf": [{
        "id": "https://example.org/object1/manifest",
        "type": "Manifest"
     }]
   }
}
```

When processed by a viewer, the user should see the rectangle `1000,2000,1000,2000` highlighted on the Canvas given in the `id` parameter; the viewer loads the manifest linked to in the `partOf` property and navigates to that canvas, and then fills the viewport with that rectangle or otherwise draws attention to it.


### 4.2. Start playing at a point in a recording

{% include api/code_header.html %}
``` json
{
  "@context": "http://iiif.io/api/presentation/{{ page.major }}/context.json",
  "id": "https://example.org/import/2",
  "type": "Annotation",
  "motivation": ["highlighting"],
  "target": {
    "type": "SpecificResource",
    "source": {
        "id": "https://example.org/iiif/id1/canvas1",
        "type": "Canvas",
        "partOf": [{
            "id": "https://example.org/iiif/id1/manifest",
            "type": "Manifest"
        }]
    },
    "selector": {
        "type": "PointSelector",
        "t": 14.5
	  }
  }
}
```

This example should cause a viewer to open Manifest https://example.org/iiif/id1/manifest, navigate to Canvas https://example.org/iiif/id1/canvas1, and start playing at 14.5 seconds into that canvas.


### 4.3. Multiple targets for a comparison view

{% include api/code_header.html %}
``` json
{
  "@context": "http://iiif.io/api/presentation/{{ page.major }}/context.json",
  "id": "https://example.org/import/3",
  "type": "Annotation",
  "motivation": "highlighting",
  "target": [
      {
          "id": "https://example.org/iiif/item1/canvas37",
          "type": "Canvas",
          "partOf": [
              {
                  "id": "https://example.org/iiif/item1/manifest",
                  "type": "Manifest"
              }
          ]
      },
      {
          "id": "https://example.org/iiif/item2/canvas99",
          "type": "Canvas",
          "partOf": [
              {
                  "id": "https://example.org/iiif/item2/manifest",
                  "type": "Manifest"
              }
          ]
      }
  ]
}
```

Here the viewer should open two manifests at once (if it is capable of such a view).


### 4.4. Search Results

The following example uses the compact, query string form of the content state to demonstrate what HTML search results linking to a particular viewer might look like.

{% include api/code_header.html %}
``` html
<h2>Results for "cats"</h2>
<ol>
  <li>
    <h3><a href='viewer.html?iiif-content={"id":"https://example.org/alice/canvas77#xywh=1000,2000,1000,2000","type":"Canvas","partOf":[{"id":"https://example.org/alice/manifest","type":"Manifest"}]}'>Alice in Wonderland</a></h3>
    <p>...she has often seen a <b>cat</b> without a grin but never a grin without a <b>cat</b></p>
  </li>
  <!-- ... more results -->
</ol>
```


## Appendices

### A. Acknowledgements
{: #acknowledgements}

Many thanks to the members of the [IIIF community][iiif-community] for their continuous engagement, innovative ideas, and feedback.

Many of the changes in this version are due to the work of the [IIIF Discovery Technical Specification Group][groups-discovery], chaired by Antoine Isaac (Europeana), Matthew McGrattan (Digirati) and Rob Sanderson (J. Paul Getty Trust). The IIIF Community thanks them for their leadership, and the members of the group for their tireless work.

### B. Change Log
{: #change-log}

| Date       | Description           |
| ---------- | --------------------- |
| 2018-10-31 | Version 0.1 (unnamed) |

{% include links.md %}

