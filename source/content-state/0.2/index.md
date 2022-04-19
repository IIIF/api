---
title: "IIIF Content State API 0.2"
title_override: "IIIF Content State API 0.2"
id: discovery-api-content-state
layout: spec
cssversion: 3
tags: [specifications, presentation-api]
major: 0
minor: 2
patch: 0
pre: final
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

__Latest Stable Version:__ [{{ site.data.apis.content-state.latest.major }}.{{ site.data.apis.content-state.latest.minor }}.{{ site.data.apis.content-state.latest.patch }}][contenstate-stable-version]

__Previous Version:__ [0.1][contentstate01]

**Editors:**

{% include api/editors.md editors=page.editors %}

{% include copyright.md %}

__Status Warning__
This is a work in progress and may change without notice. Implementers should be aware that this document is not stable. Implementers are likely to find the specification changing in incompatible ways. Those interested in implementing this document before it reaches beta or release stages should join the IIIF [mailing list][iiif-discuss] and the [Discovery Specification Group][groups-discovery], take part in the discussions, and follow the [emerging issues][github-discovery-issues] on Github.
{: .warning}

----



## 1. Introduction
{: #introduction}

The resources made available via the [IIIF Presentation API][prezi-api] are useful only if they can be found. While the [Change Discovery API][discovery-api] is for implementing systems that allow these resources to be found, this document specifies a mechanism that allows a user to then open the found resource in a compatible environment, such as a viewer, annotation tool or other IIIF-compatible software. This is one example of sharing a resource, or a particular view of a resource. Other examples include bookmarks, citations and deep linking into digital objects.

This specification makes use of existing specifications in order to promote widespread adoption. It describes a way of describing a resource, or a part of a resource, in a compact format that can be used to initialize the view of that resource in any client that implements this specification. One application is linking from a search result to a viewer showing the relevant part of a found resource. More generally, it provides a description of _content state_, for sharing between applications regardless of their different user interfaces and capabilities.

This _content state_ is distinct from the state of any particular viewer's user interface. A viewer state is likely to be client-specific and would concern which panels are open, which options are selected and similar user interface details.  

### 1.1. Objectives and Scope
{: #objectives-and-scope}

The objective of the IIIF Content State API is to describe a standardized format which enables the sharing of a particular view of one or more [IIIF Presentation API][prezi-api] resources, typically Manifests or Collections, or parts thereof. The intended audience of this document is developers of applications that implement the Presentation API, although other communities may benefit as well.

This specification also describes a number of mechanisms for the import and export of content states, thus enabling client and server software to implement interoperable solutions. Different IIIF clients will have different user interfaces and audiences, and may choose which of these mechanisms to support. Further detailed examples may be found in the [IIIF Cookbook][annex-cookbook].

### 1.2. Terminology
{: #terminology}

The specification uses the following terms:

* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

The terms _array_, _JSON object_, _number_, and _string_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].

## 2. Content State
{: #content-state}

A content state is a JSON-LD data structure that uses the models described by the [IIIF Presentation API][prezi-api] and [W3C Web Annotation Data Model][org-w3c-webanno] specifications. Viewers built to those specifications will already understand at least some of these models. This specification shows how a content state is passed to the viewer from another system or application, so that the viewer can show the intended part of the resource (or resources) to the user. A viewer can also _export_ a state, for example to enable a user to share a particular view with another user or publish it as a reference or citation.

The content state data structure must allow the client to load the resources required, and present a particular part of the resource to the user. While _load Manifest M_ is the simplest case, a more complex content state would provide more detail about the intended target, for example:

* _load Manifest M, navigate to Canvas C, and zoom in to the region defined by xywh=X,Y,W,H_
* _load Manifest M, navigate such that Range R is selected, and start playing the time-based canvas C within Range R at time t=T_

Such a description can be expressed as an Annotation that targets the intended resource, or part of the resource.

### 2.1. Annotation Model for Content State

The target of the Annotation is the IIIF resource, using exactly the same patterns as any other IIIF-targeting Annotation that a IIIF viewer might encounter.

The target could be any resource described by the Presentation API, for example, a:

* Manifest
* Range
* Canvas
* spatial or temporal fragment of a Canvas
* spatial or temporal point on a Canvas

The Annotation must contain enough information about de-referenceable resources to show the content in context. For example, a Canvas is often not enough information for a viewer to show the intended view; the Manifest the Canvas is part of needs to be declared so that the client can load that Manifest first, and then find the Canvas within it.

### 2.2 Form of Annotation

A content state Annotation has the motivation `contentState`. This motivation is not defined by either the [W3C Web Annotation Data Model][org-w3c-webanno] or the Presentation API, and is chosen to avoid potential ambiguity when the target of the content state Annotation is itself an Annotation. This section shows four possible forms the content state may take, all of which are equivalent to the following example:

{% include api/code_header.html %}
``` json
{
  "@context": "http://iiif.io/api/presentation/3/context.json",
  "id": "https://example.org/Annotation-server/bookmarks/b1",
  "type": "Annotation",
  "motivation": ["contentState"],
  "target": {
     "id": "https://example.org/iiif/item1/manifest",
     "type": "Manifest"
  }
}
```

#### 2.2.1 Full Annotation

The content state may be supplied as JSON-LD, as a full Annotation with the motivation `contentState`, as in the example above.

The target of the annotation is in this case a complete IIIF resource (here, a Manifest) but in more complex cases, the target could be a part of a IIIF resource. A client _SHOULD_ be able to accept and process the content state value in all of these forms.

#### 2.2.2 Annotation URL

The content state may be supplied as a string whose value is the URL of an Annotation with the motivation `contentState`, that the client must de-reference and process. For the example above, this would be the URL `https://example.org/Annotation-server/bookmarks/b1`.

#### 2.2.3 Target body

The content state may be supplied as JSON-LD, as the value of the `target` property of an implied Annotation with the motivation `contentState`. For the example above, this would be:

{% include api/code_header.html %}
``` json
{
    "id": "https://example.org/iiif/item1/manifest",
    "type": "Manifest"
}
```

This form is better suited to scenarios where compactness is important, for example a query string parameter, where it is will be combined with Base64-encoding as described in Section 2.3.

#### 2.2.4 Target URL

This is the simplest form and is just the URL of a resource. The content state may be supplied as a string whose value is the `id` (the URL) of the `target` property only. For the example above, this would be the URL `https://example.org/iiif/item1/manifest`. The client would simply load this Manifest and display it.

While supporting many requirements for sharing resources and initializing a client application, this form is not capable of expressing content states that are part of a IIIF resource, such as a Canvas within a Manifest, or a region of a Canvas. One of the other forms must be used for these purposes.


### 2.3 Protocol

There are many ways in which the content state data shown in Section 2.2 could be passed to, or exported from, IIIF compatible software such as a viewer. This section defines a Protocol for the transfer of this data, so that implementing software can receive or pass a content state without specific knowledge of other participating software.

If a client is capable of reading the content state from the value of an HTTP GET or POST request parameter, it _MUST_ look for the content state in a request parameter called `iiif-content`.

If a client is capable of reading the content state from the value of an attribute on an HTML element that instantiates the client, it _SHOULD_ look for the content state in an attribute called `data-iiif-content`.

A content state annotation may be published inline as part of an HTML document, as in the preceding `data-iiif-content` example, or as a query string parameter forming part of the `href` property of an HTML anchor tag.
Any content state that is in JSON-LD form, rather than a simple URL string, _MUST_ be Base64-encoded when declared inline in an HTML document, and a client _MUST_ accept it in that form. The destination character set when encoding _MUST_ be UTF-8. For example, when passing the content state as JSON-LD in a query string parameter, Base64-Encoding is used, as unencoded JSON is vulnerable to corruption. Simple URL forms _SHOULD_ be plain strings.

When published as inline, Base-64-encoded JSON-LD in the full form given in 2.2, the content state Annotation _MAY_ omit the `id` and `@context` properties.

If the content state is a simple URL, it _MAY_ be URL-encoded, and a client _SHOULD_ accept it in that form.

If the content state is a simple URL, the client _MUST_ load the resource at that URL and process it. The resource at that URL _MUST_ be the full Annotation as in 2.2.2. above, or a IIIF Resource as in 2.2.4. That is, the de-referenced response _MUST_ be JSON-LD, and _SHOULD_ have a value of `type` taken from `Annotation`, `Collection` and `Manifest`. The response _MUST_ use UTF-8 encoding.

(TODO - _MAY_ be `Canvas`, `Range`, but prefer to do that as an annotation target not as a raw resource.)

If the content state is JSON-LD the client _MUST_ inspect the `type` property to decide whether the value is the full content state Annotation (indicated by the additional presence of the `contentState` motivation), or the value of the `target` property of an implied content state Annotation.


## 3. Initialization
{: #initialization}

This specification provides mechanisms that IIIF compatible software can use to expose, share and transfer content state descriptions, but does not specify what form IIIF compatible software itself may take (e.g., a web page, a JavaScript web application, a native mobile application, a desktop application, or display kiosk hardware). Please see the [IIIF Cookbook][annex-cookbook] for further examples of the patterns listed below.

TODO - provide cookbook links to fully working examples for all of these

### 3.1. Initialization mechanisms (protocol)
{: #initialization-mechanisms}

The data structure _MAY_ be made available to the client using the following mechanisms. Other mechanisms are possible, but outside the scope of the specification.

#### 3.1.1 Linking: HTTP GET (query string) parameter
{: #initialization-mechanisms-link}

If the intention is that the linked-to client loads an entire IIIF resource without focusing on any particular part, the simplest form of the content state _SHOULD_ be used:

{% include api/code_header.html %}
``` html
{% raw %}
<a href='https://example.org/viewer?iiif-content=http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json'>Link to Viewer</a>
{% endraw %}
```

In this case the client at `https://example.org/viewer` would load the resource provided, determine that it is a Manifest (rather than, say, a Collection), and process accordingly.

When the intention is to initialize the viewer at a particular part of the resource, more options are available.

In the following examples, the same Annotation is used each time. As JSON:

{% include api/code_header.html %}
``` json
{
  "type": "Annotation",
  "motivation": ["contentState"],
  "target": {
    "id": "http://dams.llgc.org.uk/iiif/2.0/4389767/canvas/4389772.json",
    "type": "Canvas",
    "partOf": [
      {
        "id": "http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json",
        "type": "Manifest"
      }
    ]
  }
}
```

An example of this usage would be a link from search results to a particular page of a digitized book, or a stored bookmark of a particular page (i.e., Canvas).

Without encoding, the link to the viewer would look like this:

{% include api/code_header.html %}
``` html
{% raw %}
<a href='https://example.org/viewer?iiif-content={"type":"Annotation","motivation":"contentState","target":{"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/canvas/4389772.json","type":"Canvas","partOf":[{"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json","type":"Manifest"}]}}'>Link to Viewer</a>
{% endraw %}
```

However, as JSON-LD, this _MUST_ be Base-64 encoded UTF-8:

{% include api/code_header.html %}
``` html
{% raw %}
<a href="https://example.org/viewer?iiif-content=eyJ0eXBlIjoiQW5ub3RhdGlvbiIsIm1vdGl2YXRpb24iOiJzZWxlY3RpbmciLCJ0YXJnZXQiOnsiaWQiOiJodHRwOi8vZGFtcy5sbGdjLm9yZy51ay9paWlmLzIuMC80Mzg5NzY3L2NhbnZhcy80Mzg5NzcyLmpzb24iLCJ0eXBlIjoiQ2FudmFzIiwicGFydE9mIjpbeyJpZCI6Imh0dHA6Ly9kYW1zLmxsZ2Mub3JnLnVrL2lpaWYvMi4wLzQzODk3NjcvbWFuaWZlc3QuanNvbiIsInR5cGUiOiJNYW5pZmVzdCJ9XX19">Link to Viewer</a>
{% endraw %}
```

The content state may be passed as just the `target` property of an implied Annotation with motivation `contentState`, that is:

{% include api/code_header.html %}
``` json
{
  "id": "http://dams.llgc.org.uk/iiif/2.0/4389767/canvas/4389772.json",
  "type": "Canvas",
  "partOf": [
    {
      "id": "http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json",
      "type": "Manifest"
    }
  ]
}
```

This results in a more compact form, unencoded, this would be:

{% include api/code_header.html %}
``` html
{% raw %}
<a href='https://example.org/viewer?iiif-content={"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/canvas/4389772.json","type":"Canvas","partOf":[{"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json","type":"Manifest"}]}'>Link to Viewer</a>
{% endraw %}
```

However, as JSON-LD again, this _MUST_ be Base-64 encoded UTF-8:

{% include api/code_header.html %}
``` html
{% raw %}
<a href="https://example.org/viewer?iiif-content=eyJpZCI6Imh0dHA6Ly9kYW1zLmxsZ2Mub3JnLnVrL2lpaWYvMi4wLzQzODk3NjcvY2FudmFzLzQzODk3NzIuanNvbiIsInR5cGUiOiJDYW52YXMiLCJwYXJ0T2YiOlt7ImlkIjoiaHR0cDovL2RhbXMubGxnYy5vcmcudWsvaWlpZi8yLjAvNDM4OTc2Ny9tYW5pZmVzdC5qc29uIiwidHlwZSI6Ik1hbmlmZXN0In1dfQ==">Link to Viewer</a>
{% endraw %}
```

#### 3.1.2 Linking: HTTP POST (form) parameter
{: #initialization-mechanisms-post}

The same data structure, in the same forms, may instead be passed in a POST parameter. This is suited to server-side web applications, such as a web page rendering citations or a view initialized on the server. It is not suited to a standalone JavaScript application, as the POST data is typically unavailable.

```
curl -d 'iiif-content=eyJpZCI6Imh0dHA6Ly9kYW1zLmxsZ2Mub3JnLnVrL2lpaWYvMi4wLzQzODk3NjcvY2FudmFzLzQzODk3NzIuanNvbiIsInR5cGUiOiJDYW52YXMiLCJwYXJ0T2YiOlt7ImlkIjoiaHR0cDovL2RhbXMubGxnYy5vcmcudWsvaWlpZi8yLjAvNDM4OTc2Ny9tYW5pZmVzdC5qc29uIiwidHlwZSI6Ik1hbmlmZXN0In1dfQ==' -X POST https://example.org/citation-renderer
```

In this example, the server at `https://example.org/citation-renderer` should expect to process the content state in the same forms and variants as above.

_Outstanding Question:_ Should POST be in the body, or as www-form-encoded? ...citation search engine exchanging state to another page that then generates a view.


#### 3.1.3 Accepting the content state as a paste operation
{: #initialization-mechanisms-paste}

The client allows the content state URL or data to be pasted into part of its UI (e.g., from a "Load..." option exposing a `textarea` element for the user to manually paste into). A client can also accept a paste operation transparently, by reading from the clipboard:

{% include api/code_header.html %}
``` html
<script>
    document.addEventListener('paste', event => {
        const text = event.clipboardData.getData('text/plain');
        Annotation = JSON.parse(text);
        //... process Annotation
    });
</script>
```

In that scenario the user can paste the content state directly into the view.

Refer to Section 3.2 below for methods of exporting data, including the _Copy to clipboard_ pattern, a natural pairing with a paste operation, from one viewer to another.

_Question_ combine copy to clipboard and paste? Not have section 3.2? These two aren't dependent on each other.

This same mechanism may also accept a Manifest or Collection resource URL directly. _Question_ should the spec go into that possibility?


#### 3.1.4 Drag and Drop
{: #initialization-mechanisms-dragdrop}

In this scenario, one client provides a _draggable_ element:

{% include api/code_header.html %}
``` html
<img src="{{ site.api_url | absolute_url }}/assets/images/logo-iiif-34x30.png" draggable="true" ondragstart="drag(event)" />

<script>
    function getContentState(){
        // return a stringified representation of the required content state
    }

    function drag(ev) {
        var json = getContentState();
        ev.dataTransfer.setData("Annotation", json);
    }
</script>
```

And another client provides an element capable of receiving a `drop` event:

{% include api/code_header.html %}
``` html
    <div id="dropbox" ondrop="drop(event)" ondragover="allowDrop(event)" ondragexit="deselect(event)">
        <!-- this could be the viewport -->
    </div>

    <script>

        function drop(ev) {
            ev.preventDefault();
            var dropDiv = document.getElementById("dropbox");
            var json = ev.dataTransfer.getData("Annotation");
            // process the Annotation
        }

        function allowDrop(ev) {
            ev.preventDefault();
            // indicate visually that the drop area is ready to receive a drop
        }

        function deselect(ev) {
            // remove visual indication that drop is possible
        }

    </script>
```

This technique can also be used within the same client, to drag a content state from one part to another.


#### 3.1.5  "Upload" file

_Question_ again, is a whole manifest itself a content state?

A JavaScript client can accept content state from the client machine via the `FileReader` interface:

{% include api/code_header.html %}
``` html
<form>
    <input type="file" id="selectFiles" value="Import" /><br />
    <button id="import" onclick="return loadAnnotation()">Import</button>
</form>    

<script>

    function loadAnnotation() {
        var files = document.getElementById('selectFiles').files;
        var fr = new FileReader();
        fr.onload = function(e) {
            loadJson(e.target.result);
        }
        fr.readAsText(files.item(0));
        return false;
    }

    function loadJson(json) {
        var contentState = JSON.parse(json);
        // process contentState
    }
</script>
```

(see cookbook recipe)

* The client exposes the current content state in its UI (e.g., "Share this")
* The client looks for the content state URL or data in an initialization parameter `data-iiif-content`
* The data is a parameter in an HTML5 Drag and Drop operation (LINK TO COOKBOOK RECIPE...)

### 3.1.6 Load by reference

This is a variant of 3.1.1, with the parameter value a URI rather than the content itself.

{% include api/code_header.html %}
``` html
<a href='https://example.org/viewer?iiif-content=https://publisher.org/fragment123.json'>Link to Viewer</a>
```

The same rules apply; the viewer _MUST_ dereference and process the Annotation at that URL.

### 3.1.7 Common initialization parameter

TODO - how should this read as spec? Makes too many assumptions about how a viewer bootstraps. The idea is that Mirador, UV, etc use the same name by convention if they support acceptance of content state data.

This is probably not spec. It's a recipe.

Viewers should standardize on the attribute `data-iiif-content` for supplying content state via HTML attribute. A viewer that accepts content state _SHOULD_ process an Annotation in any of the forms described in the GET parameter section.

{% include api/code_header.html %}
``` html

<p>Loading a whole manifest</p>
<div
    id="iiif-viewer"
    data-iiif-content="http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json">
</div>

<p>Loading a manifest to show a particular Canvas</p>
<div
    id="iiif-viewer"
    data-iiif-content="eyJpZCI6Imh0dHA6Ly9kYW1zLmxsZ2Mub3JnLnVrL2lpaWYvMi4wLzQzODk3NjcvY2FudmFzLzQzODk3NzIuanNvbiIsInR5cGUiOiJDYW52YXMiLCJwYXJ0T2YiOlt7ImlkIjoiaHR0cDovL2RhbXMubGxnYy5vcmcudWsvaWlpZi8yLjAvNDM4OTc2Ny9tYW5pZmVzdC5qc29uIiwidHlwZSI6Ik1hbmlmZXN0In1dfQ==">
</div>
```


### 3.2 Exporting state

This part is less reliant on spec. The means by which a viewer allows a content state to get onto the user's clipboard, or on the user's hard drive, or posted to a service that can expose it as a URL (like an Annotation server) are not really the protocol of this spec. So does it cover them:

* copy to clipboard
* download file - save
* display for copying
* Send external (to citation adaptor etc) 0 a good recipe
* Send to JSON-blob


## 4. Examples of content states

The following examples demonstrate the use of the existing IIIF Presentation API and W3C Web Annotation Data Model to describe parts of resources. The full form of the Annotation (as if it were available at the URL given in the `id` property) has been used in each case.  Further examples can be found in the [IIIF Cookbook][annex-cookbook]

### 4.1. A region of a canvas in a manifest

{% include api/code_header.html %}
``` json
{
  "@context": "http://iiif.io/api/presentation/{{ page.major }}/context.json",
  "id": "https://example.org/import/1",
  "type": "Annotation",
  "motivation": ["contentState"],
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
  "motivation": ["contentState"],
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
  "motivation": "contentState",
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
| 2019-02-04 | Version 0.2 (unnamed) |

{% include links.md %}
