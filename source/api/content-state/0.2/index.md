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
redirect_from:
  - /api/content-state/index.html
  - /api/0/content-state/index.html
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

The resources made available via the [IIIF Presentation API][prezi-api] are only useful only if they can be found. While the [Change Discovery API][discovery02] specifies systems that allow these resources to be found, this document specifies a mechanism that allows a user to then open the found resource in a compatible environment, such as a viewer, Annotation tool or other IIIF-compatible software.

This specification makes use of existing techniques and specifications in order to promote widespread adoption. It provides a way of describing a resource, or a part of a resource, in a compact format that can be used to initialize the view of that resource in any client that implements this specification. Linking from a search result to a viewer showing the relevant part of a found resource is one application of this specification. More generally, it provides a description of a _content state_, allowing such states to be shared between applications regardless of their different user interfaces and capabilities.

### 1.1. Objectives and Scope
{: #objectives-and-scope}

The objective of the IIIF Content State API is to describe a standardized format which enables the sharing of a particular view of one or more IIIF Presentation API resources, typically Manifests or Collections, or parts thereof. The intended audience is developers of IIIF-aware systems who also wish to support a widespread IIIF ecosystem on the web, though other communities may benefit as well.

The standardized format is a JSON-LD data structure that uses the models described by the [IIIF Presentation API][prezi-api] and [W3C Web Annotation Data Model][org-w3c-webanno] specifications. Viewers built to those specifications will already understand at least some of the model. This specification allows a content state to be passed to the viewer from another system or application, so that a viewer can show the intended part of the resource (or resources) to the user. The same model can be used by a viewer to _export_ a state, for example to enable a user to share a particular view with another user or publish it as a reference or citation.

This specification also describes a common set of mechanisms for the import and export of content states, thus enabling client and server software to implement interoperable solutions. Different IIIF clients will have different user interfaces and audiences, and may choose which of the patterns to support. Further detailed examples may be found in the [IIIF Cookbook][annex-cookbook].

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

A description like this can be expressed in purely IIIF terms, as an Annotation that targets the intended part of the resource. This _content state_ is distinct from the state of a particular viewer's user interface. A viewer state is likely to be client-specific and would concern which panels are open, which options are selected and similar user interface details.  

### 2.1. Annotation Model for Content State

The target of the Annotation is the IIIF resource, using exactly the same patterns as any other IIIF-targeting Annotation that a IIIF viewer might encounter. A content state Annotation has the motivation `highlighting`.

The target could be any resource described by the Presentation API, for example, a:

* Manifest
* Range
* Canvas
* spatial or temporal fragment of a Canvas
* spatial or temporal point on a Canvas

The Annotation must contain enough information about dereferenceable resources to show the content in context. For example, a Canvas is almost certainly not enough information for a viewer to show the intended view; the Manifest the canvas is part of needs to be indicated so that the client can load the Manifest first, and then find the Canvas within it.

### 2.2 Form of Annotation

The content state data may be passed to a client in one of several forms, and a client _SHOULD_ be able to accept and process it in all of these forms.

* As the URL of an Annotation with the motivation `highlighting`, that the client must de-reference
* As JSON-LD, in the form of a full Annotation with the motivation `highlighting`
* As JSON-LD, as the value of the `target` property of an implied Annotation with the motivation `highlighting`

If a client is capable of reading the content state from the value of an HTTP GET or POST request parameter, it _MUST_ look for the content state in a request parameter called `iiif-content`.

If a client is capable of reading the content state from an HTML attribute, the client _SHOULD_ look for the content state in an attribute called `data-iiif-content`.

The content state _MAY_ be Base64-encoded, and a client _SHOULD_ accept it in that form. It is _RECOMMENDED_ that when passing the content state as a query string parameter, Base64-Encoding is used, as unencoded JSON is vulnerable to corruption when passed as a link parameter.

The content state _MAY_ be URL-encoded, and a client _SHOULD_ accept it in that form.

A client _MUST_ be able to read and process the value in any of the three forms listed above. Consider the following, simplest possible content state Annotation:

```json
{
  "@context": "http://iiif.io/api/presentation/3/context.json",
  "id": "https://example.org/Annotation-server/bookmarks/b1",
  "type": "Annotation",
  "motivation": ["highlighting"],
  "target": {
     "id": "https://example.org/iiif/item1/manifest",
     "type": "Manifest"
  }
}
```

If the string `https://example.org/Annotation-server/bookmarks/b1` is passed as the value of `iiif-content` or `data-iiif-content`, the client _MUST_ load the resource at that URL and process it. The resource at that URL _MUST_ be the full Annotation as in the example above.

The JSON-LD body given above may be passed directly in a request parameter, HTML attribute or other supported mechanism, for immediate processing. In this scenario the Annotation does not require the `id` property. The client should inspect the value to determine whether it needs to be base64-decoded, or Url-decoded. [How?]

The value passed to a client via this parameter (or other supported mechanisms) may be the `target` property of an implied Annotation:

```json
{"id":"https://example.org/iiif/item1/manifest","type":"Manifest"}
```

This form is better suited to scenarios where compactness is important, for example a query string parameter, where it is also more likely to be combined with Base64-encoding.

The client _MUST_ examine the form of the string value, or the decoded string value, of the property to determine whether it is JSON-LD or a URL, and if it is JSON-LD the client _MUST_ check the `type` property to determine whether it is a full Annotation or just the target content state.

__Queries__<br/><br/>Does the inline full Annotation version require `id`?<br/>Does it require `@context`?<br/>Should we require a different parameter name when the value is just the target of the Annotation, rather than the full Annotation, or should we stick to one parameter and require the client to check its `type` and process accordingly?<br/>For nicer query string parameters, should we permit a syntax that is invalid JSON-LD but valid JSON in the same form (i.e., no quotes, and/or single quotes), or even not valid JSON?:<br/><br/>`viewer.html?iiif-content={"id":"https://example.org/iiif/item1/manifest","type":"Manifest"}`<br/><br/><a href="http://tify.sub.uni-goettingen.de/demo.html?manifest=https://manifests.sub.uni-goettingen.de/iiif/presentation/PPN857449303/manifest">See TIFY to get an idea of what this feels like</a> (observe the `tify` parameter as you change the content state).<br/><br/>Should the client be required to accept the JSON-LD in base64-encoded form? [Yes!]
{: .warning}

## 3. Initialisation
{: #initialisation}

This specification provides mechanisms that IIIF compatible software can use to expose, share and transfer content state descriptions, but does not specify what form IIIF compatible software itself may take (e.g., a web page, a JavaScript web application, a native mobile application, a desktop application, or display kiosk hardware). Please see the [IIIF Cookbook][annex-cookbook] for further examples of the patterns listed below.

TODO - provide cookbook links to fully working examples for all of these

### 3.1. Initialisation mechanisms (protocol)
{: #initialisation-mechanisms}

The data structure _MAY_ be made available to the client via a number of methods, including (but not limited to):

#### 3.1.1 Linking: HTTP GET (query string) parameter
{: #initialisation-mechanisms-link}

In the following examples, the same Annotation is used each time. As JSON:

```json
{
  "type": "Annotation",
  "motivation": ["highlighting"],
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

The client looks for the content state URL or data as the value of an HTTP GET request parameter `iiif-content` on its containing page (subject to the 2 KB limit):

```html
{% raw %}
<a href='https://example.org/viewer?iiif-content={"type":"Annotation","motivation":"highlighting","target":{"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/canvas/4389772.json","type":"Canvas","partOf":[{"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json","type":"Manifest"}]}}'>Link to Viewer</a>
{% endraw %}
```

This may be URL-encoded:

```html
{% raw %}
<a href='https://example.org/viewer?iiif-content={%22type%22:%22Annotation%22,%22motivation%22:%22highlighting%22,%22target%22:{%22id%22:%22http://dams.llgc.org.uk/iiif/2.0/4389767/canvas/4389772.json%22,%22type%22:%22Canvas%22,%22partOf%22:[{%22id%22:%22http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json%22,%22type%22:%22Manifest%22}]}}'>Link to Viewer</a>
{% endraw %}
```

Or, as _RECOMMENDED_, Base-64 encoded:

```html
{% raw %}
<a href='https://example.org/viewer?iiif-content=eyJ0eXBlIjoiQW5ub3RhdGlvbiIsIm1vdGl2YXRpb24iOiJoaWdobGlnaHRpbmciLCJ0YXJnZXQiOnsiaWQiOiJodHRwOi8vZGFtcy5sbGdjLm9yZy51ay9paWlmLzIuMC80Mzg5NzY3L2NhbnZhcy80Mzg5NzcyLmpzb24iLCJ0eXBlIjoiQ2FudmFzIiwicGFydE9mIjpbeyJpZCI6Imh0dHA6Ly9kYW1zLmxsZ2Mub3JnLnVrL2lpaWYvMi4wLzQzODk3NjcvbWFuaWZlc3QuanNvbiIsInR5cGUiOiJNYW5pZmVzdCJ9XX0sImdlbmVyYXRvciI6eyJpZC'>Link to Viewer</a>
{% endraw %}
```

The content state may be passed as just the `target` property of an implied Annotation with motivation highlighting, that is:

```json
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

This results in a more compact form: the first plain HTML version is shown for comparison:

```html
{% raw %}
<a href='https://example.org/viewer?iiif-content={"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/canvas/4389772.json","type":"Canvas","partOf":[{"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json","type":"Manifest"}]}'>Link to Viewer</a>
{% endraw %}
```


#### 3.1.2 Linking: HTTP POST (form) parameter
{: #initialisation-mechanisms-post}

The same data structure, in the same forms, may instead be passed in a POST parameter. This is suited to server-side web applications, such as a web page rendering citations or a view initialized on the server. It is not suited to a standalone JavaScript application, as the POST data is typically unavailable.

```
curl -d 'iiif-content={"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/canvas/4389772.json","type":"Canvas","partOf":[{"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json","type":"Manifest"}]}' -X POST https://example.org/citation-renderer
```

In this example, the server at `https://example.org/citation-renderer` should expect to process the content state in the same forms and variants as above.

#### 3.1.3 Accepting the content state as a paste operation
{: #initialisation-mechanisms-paste}

The client allows the content state URL or data to be pasted into part of its UI (e.g., from a "Load..." option exposing a `textarea` element for the user to manually paste into). A client can also accept a paste operation transparently, by reading from the clipboard:

```html
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
{: #initialisation-mechanisms-dragdrop}

In this scenario, one client provides a _draggable_ element:

```html
<img src="http://iiif.io/img/logo-iiif-34x30.png" draggable="true" ondragstart="drag(event)" />

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

```html
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

```html
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
* The client looks for the content state URL or data in an initialisation parameter `data-iiif-content`
* The data is a parameter in an HTML5 Drag and Drop operation (LINK TO COOKBOOK RECIPE...)

### 3.1.6 Load by reference

This is a variant of 3.1.1, with the parameter value a URI rather than the content itself.

```html
<a href='https://example.org/viewer?iiif-content=https://publisher.org/fragment123.json'>Link to Viewer</a>
```

The same rules apply; the viewer _SHOULD_ process the same text


### 3.1.7 Common initialisation parameter

TODO - how should this read as spec? Makes too many assumptions about how a viewer bootstraps. The idea is that Mirador, UV, etc use the same name by convention if they support acceptance of content state data.

This is probably not spec. It's a recipe.

Viewers should standardise on the attribute `data-iiif-content` for supplying content state via HTML attribute. A viewer that accepts content state _SHOULD_ process an Annotation in any of the forms described in the GET parameter section.


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

```json
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

```json
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

```json
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

```html
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
