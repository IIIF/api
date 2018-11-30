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
redirect_from:
  - /api/import/index.html
  - /api/0/import/index.html
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
This is a work in progress and may change without notice. Implementers should be aware that this document is not stable. Implementers are likely to find the specification changing in incompatible ways. Those interested in implementing this document before it reaches beta or release stages should join the IIIF [mailing list][iiif-discuss] and the [Discovery Specification Group][groups-discovery], take part in the discussions, and follow the [emerging issues][github-discovery-issues] on Github.
{: .warning}

----

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Introduction
{: #introduction}

The resources made available via the [IIIF Presentation API][prezi-api] are only useful if they can be found. While the [Change Discovery API][discovery01] specification describes systems that allow these resources to be found, how does a user then open the resource in an environment of their choosing, such as a viewer, annotation tool or other IIIF-compatible software?

This specification makes use of existing techniques and specifications in order to promote widespread adoption. It provides a way of describing a resource, or a part of a resource, in a compact format that can be used to initialise the view of that resource in any client that implements this specification. Linking from a search result to a viewer showing the relevant part of a found resource is one application of this specification. More generally, it provides a description of a _content state_, allowing such states to be shared between applications regardless of their different user interfaces and capabilities.

### 1.1. Objectives and Scope
{: #objectives-and-scope}

The objective of the IIIF Import to Viewers API is to enable the sharing of a standardised description of a view of one or more IIIF Presentation API resources, typically Manifests or Collections. The intended audience is developers of other IIIF-aware systems that can display the resources. While this work may benefit others outside of the IIIF community directly or indirectly, the objective of the API is to specify an interoperable solution that best and most easily fulfills these needs within the community of participating organizations.

The standardised view is a JSON-LD data structure that uses the models described by the [IIIF Presentation API][prezi-api] and [W3C Web Annotation Data Model][org-w3c-webanno] specifications. Viewers built to those specifications will already understand at least some of the model. This specification allows a content state to be passed to the viewer from outside, so that a viewer can show the intended part of the resource (or resources) to the user. The same model can be used by a viewer to _export_ a state, for example to share a particular view with another user or publish it as a reference.

The specification describes the model for a content state, but does not mandate a particular mechanism for a viewer accepting the state for initialisation. Different IIIF clients have different user interfaces and audiences. The specification discusses several mechanisms, and more detailed examples may be found in the [IIIF Cookbook][annex-cookbook].


### 1.2. Terminology
{: #terminology}

The specification uses the following terms:

* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

The terms _array_, _JSON object_, _number_, and _string_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].

## 2. Content State
{: #content-state}

The data structure must allow the client to load the resources required, and present a particular part of the resource to the user. While _load Manifest M_ is the simplest case, a more specific state would provide more detail, for example:

* _load Manifest M, navigate to Canvas C, and zoom in to xywh=X,Y,W,H_
* _load manifest M, navigate such that Range R is selected, and start playing the time-based canvas C within Range R at time t=T_

A description like this can be expressed in purely IIIF terms, as an annotation that targets the part of the resource. These _content states_ are distinct from the state of a viewer as a user interface. A viewer state is likely to be client-specific and would concern such things as the state of the user interface, which panels are open, which options are selected and so on. 

### 2.1. Annotation Model for Content State

The target of the annotation is the IIIF resource, using exactly the same patterns as any other IIIF-targeting annotation that a IIIF viewer might encounter. A content state annotation has the motivation `highlighting`.

The target could be any resource described by the Presentation API, for example, a:

* Manifest
* Range
* Canvas
* spatial or temporal fragment of a Canvas
* spatial or temporal point on a Canvas

The annotation must contain enough information about dereferenceable resources to show the content in context. For example, a Canvas is almost certainly not enough information for a viewer to show the intended view; the Manifest the canvas is part of needs to be indicated so that the client can load it first.

## 3. Examples

Further examples can be found in the [IIIF Cookbook][annex-cookbook].

### 3.1. A region of a canvas in a manifest

```json
{
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

When processed by a viewer, the user should see the rectangle `1000,2000,1000,2000` highlighted on the Canvas given in the `id` parameter; the viewer loads the manifest linked to in the `partOf` property and navigates to that canvas, then can fill the viewport with that rectangle or otherwise draw attention to it.


### 3.2. Start playing at a point in a recording

```json
{
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

### 3.3. A simple link to a manifest

```json
{
  "type": "Annotation",
  "motivation": ["highlighting"],
  "target": {
     "id": "https://example.org/iiif/item1/manifest",
     "type": "Manifest"
  }
}
```

In this example the viewer is simply instructed to open a manifest. See "compact form" note below.


### 3.4. Multiple targets; send a comparison view

```json
{
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


## 4. Initialisation
{: #initialisation}

This specification does not impose limits on the mechanisms that IIIF compatible software can use to expose, share and transfer content state descriptions. Please see the [IIIF Cookbook][annex-cookbook] for examples of the patterns listed below.

### 4.1. Initialisation mechanisms
{: #initialisation-mechanisms}

The data structure could be made available to the client via a number of methods, including (but not limited to):

* The client looks for the data structure as the value of an HTTP GET request parameter on its containing page (subject to the 2 KB limit)
* The client allows the data structure to be pasted into part of its UI
* The client exposes the current content state in its UI (e.g., "Share this")
* The data is a parameter in an HTML5 Drag and Drop operation (recipe...)
* The data can be passed to the client as an initialisation parameter by its containing page (very viewer-specific in mechanism but not in model)


__Compact form - suggestion__<br><br/>Do we want a compact form of these annotations for more pleasing appearance on query strings? The trouble with that is where to stop. But some very simple and common scenarios could have short forms. I favour _not_ inventing a new parameter language or JSON-LD serialisation, as the compacted JSON-LD cruft isn't really all that huge compared to typical URLs. However, a short form could just be the value of the `target` of the anno, with the type and motivation implied by the object being passed using a particular query string param, perhaps `iiif-target`.<br/><br/>`https://example.org/viewer.html?iiif-target={"id":"https://example.org/iiif/item1/manifest","type":"Manifest"}`<br/><br/>This doesn't look too bad and remains easily hackable (i.e., editable) by users.
{: .warning}


## 5. Search Results

The following example uses the compact, query string form of the content state to demonstrate what HTML search results linking to a particular viewer might look like.

```html
<h2>Results for "cats"</h2>
<ol>
  <li>
    <h3><a href='viewer.html?iiif-target={"id":"https://example.org/alice/canvas77#xywh=1000,2000,1000,2000","type":"Canvas","partOf":[{"id":"https://example.org/alice/manifest","type": "Manifest"}]}'>Alice in Wonderland</a></h3>
    <p>...she has often seen a <b>cat</b> without a grin but never a grin without a <b>cat</b></p>
  </li>
  <!-- ... more results -->
</ol>
```

## 6. Drag and Drop

Doesn't belong here? Refer to cookbook? Or should spec cover it?


## 7. Processing Algorithm

Is this obvious or does it need spelling out?


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
 