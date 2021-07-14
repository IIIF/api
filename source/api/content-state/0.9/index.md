---
title: "IIIF Content State API 0.9"
title_override: "IIIF Content State API 0.9"
layout: spec
major: 0
minor: 9
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

__Previous Version:__ [0.3][contentstate03]

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

## 1. Introduction
{: #introduction}

This specification provides a way of describing a [IIIF Presentation API][prezi-api] resource, or a part of a resource, in a compact format that can be used to initialize the view of that resource in any client that implements this specification. This description is the _content state_. This specification provides the format of the _content state_, and mechanisms for passing it between applications regardless of their different user interfaces and capabilities.


### 1.1. Objectives and Scope
{: #objectives-and-scope}

* A user follows a link from a search result, which opens a IIIF viewer. The viewer focuses on the relevant part of the object, such as a particular line of text that contains the searched-for term. 
* A user opens several IIIF Manifests to compare paintings, then wishes to share this set of views with a colleague.

These are examples of sharing a resource, or a particular view of a resource. Other examples include bookmarks, citations, playlists and deep linking into digital objects.

The objective of the IIIF Content State API is to provide a standardized format for sharing of a particular view of one or more [IIIF Presentation API][prezi-api] resources, such as a Collection, a Manifest, or a particular part of a Manifest. 

This specification also describes how a content state is passed into a viewer or other client application from another system or application, so that the viewer can show the intended part of the resource (or resources) to the user. A simple example would be a content state that tells a viewer to load a IIIF Manifest. 

A viewer can also _export_ a content state, for example to enable a user to share a particular view with another user, or publish it as a reference or citation. Different IIIF clients will have different user interfaces and audiences, and may choose which of these mechanisms to support. Further detailed examples may be found in the [IIIF Cookbook][annex-cookbook].

The _content state_ is distinct from the state of any particular viewer's user interface. A viewer state is likely to be client-specific and would concern which panels are open, which options are selected and similar user interface details. Viewers with very different user interfaces can all implement support for the Content State API.

The intended audience of this document is developers of applications that implement the Presentation API, although other communities may benefit as well.

#### 1.1.1. Relationship with Change Discovery API

The resources made available via the [IIIF Presentation API][prezi-api] are useful only if they can be found. While the [Change Discovery API][discovery-api] is for implementing systems that allow these resources to be found, the Content State API is for opening the found resource in a compatible environment, such as a viewer, annotation tool or other IIIF-compatible software. 


### 1.2. Terminology
{: #terminology}

The specification uses the following terms:

* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

* __array__, __JSON object__, __number__, and __string__ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

* __Annotation__ is to be interpreted as defined in the [W3C Web Annotation Data Model][org-w3c-webanno] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].

## 2. Content State
{: #content-state}

A content state is a JSON-LD data structure that uses the models described by the [IIIF Presentation API][prezi-api] and [W3C Web Annotation Data Model][org-w3c-webanno] specifications. The data structure is a description of a resource, or part of a resource. This data structure must allow the client to load the resource required, and present a particular part of the resource to the user. The state might be very simple: for example, a link to a Manifest. A more complex content state would provide more detail about the intended target. The following are all behaviors a passed-in content state might produce in a compatible client: 

* _load Manifest M_
* _load Manifest M, navigate to Canvas C, and zoom in to the region defined by xywh=X,Y,W,H_
* _load Manifest M, navigate such that Range R is selected, and start playing the time-based canvas C within Range R at time t=T_

These intentions can be expressed formally as an Annotation that targets the intended resource, or part of the resource. This content state Annotation must be easily _passed_ into web applications, for example, as a query string parameter, or an HTML `data-` attribute.

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

Any Annotation may have one or more [motivations][org-w3c-webanno-motivation], that provide the reason(s) why is was created. For example, `bookmarking`. 

A content state Annotation always has the motivation `contentState`. This motivation is not defined by either the [W3C Web Annotation Data Model][org-w3c-webanno] or the IIIF Presentation API, and is chosen to avoid potential ambiguity when the target of the content state Annotation is itself an Annotation. The content state annotation may also have additional motivations such as `bookmarking`, `identifying` and so on, as defined by the W3C Web Annotation Model, but it is its particular `contentState` motivation that produces the required behavior in compatible software.

A content state annotation can be provided in several forms, described in the following sections. 

Publishers _SHOULD_ provide the content state annotation in one of the following forms.
A client _SHOULD_ be able to accept and process the content state in all of these forms. 

#### 2.2.1 Full Annotation

The content state _MAY_ be supplied as JSON-LD, as a full Annotation with the motivation `contentState`, as in this example:

```json
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

The target of the annotation is, in this case, a complete IIIF resource (here, a Manifest) but in more complex cases, the target could be a part of a IIIF resource.  

#### 2.2.2 Annotation URI

The content state _MAY_ be supplied as a string whose value is the URI of an Annotation with the motivation `contentState`, that the client must de-reference and process. For the example in 2.2.1 above, this would be the URI `https://example.org/Annotation-server/bookmarks/b1`. The response from that URI would be the JSON above.

#### 2.2.3 Target Body

The content state _MAY_ be supplied as JSON-LD, as the value of the `target` property of an implied Annotation with the motivation `contentState`. For the example in 2.2.1, this would be:

```json
{
    "id": "https://example.org/iiif/item1/manifest",
    "type": "Manifest"
}
```

This form is better suited to scenarios where compactness is important, for example a query string parameter, where it will be combined with the encoding described in Section 2.3.

#### 2.2.4 Target URI

 The content state _MAY_ be supplied as a string whose value is the `id` (the dereferenceable URI) of the `target` property only. This is the simplest form and is just the URI of a resource. For the example in 2.2.1, this would be the URI `https://example.org/iiif/item1/manifest`. The client would simply load this Manifest and display it. 

Examples 2.2.2 and 2.2.4 are both URIs. It is up to the client to recognise that 2.2.4 is a Manifest, whereas 2.2.2 is a content state Annotation that points to a Manifest. The client _MUST_ inspect the `type` property to determine what the de-referenced resource is. If the `type` is Annotation, the client _MUST_ also look at the `motivation` property to determine if the annotation is a content state. If the `motivation` is not `contentState`, but the annotation has been encountered where a content state is expected, the client _MUST_ assume that the annotation itself is the intended IIIF content. 

#### 2.2.5 Limitations of Simple URIs

While supporting many requirements for sharing resources and initializing a client application, the 2.2.4 form is not capable of expressing content states that are part of a IIIF resource, such as a region of a Canvas, or a Canvas URI that is not itself de-referenceable. One of the other forms must be used for these purposes. 

```json
{
  "@context": "http://iiif.io/api/presentation/3/context.json",
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

This description cannot be conveyed by just a Canvas URI or a Manifest URI; it needs the structure provided by a content state Annotation. It can be reduced to _Target body_ form, but no further:


```json
{
  "id": "https://example.org/object1/canvas7#xywh=1000,2000,1000,2000",
  "type": "Canvas",
  "partOf": [{
    "id": "https://example.org/object1/manifest",
    "type": "Manifest"
  }]
}
```


### 2.3 Protocol and Encoding Requirements

There are many ways in which the content state data shown in Section 2.2 could be exchanged between IIIF-compatible systems. For interoperability, agreeing on the model is not enough. This section defines _Protocols_ for the transfer of this data, so that implementing software can receive or pass a content state without specific knowledge of other participating software. These protocols make use of widely supported features of modern browsers:

* Passing a content state as a query string parameter in an HTTP GET request
* Passing a content state as a parameter in an HTTP POST request
* Reacting to the [Paste][org-mozilla-paste] event, where the pasted data is the URI of a content state
* Reacting to the [Paste][org-mozilla-paste] event, where the pasted data is a full content state
* Using the [Drag and Drop API][org-mozilla-drag-drop] to expose and accept content states
* Uploading content state from the client machine via the [FileReader][org-mozilla-filereader] interface
* Initialising a client via an HTML5 `data-*` attribute

Examples of these protocols are given in Section 3, [Initialization mechanisms][contentstate-initialization].



#### 2.3.1 Content State Encoding

A content state will be passed from client to server, and server to client, by the various methods described in this specification. A content state will contain characters from JSON syntax, and may contain strings from any language. The identifiers of IIIF and other resources within the content state may be Internationalized Resource Identifiers (IRIs), as defined in [RFC 3987][org-rfc-3987]. For these reasons it is essential that the content state can be _encoded_ using an encoding that:

* Is simple to implement, for both decoding and encoding, in a web browser and on the server
* Will safely encode any UTF-16 string from JavaScript
* Is impervious to _double encoding_ - that is, once encoded, any further likely encodings of any request or response parts will not change the already-encoded content state.

For these reasons, this specification defines a two-step encoding that uses both the [encodeURI][org-ecma-encodeuri] function available in web browsers, followed by [Base 64 Encoding with URL and Filename Safe Alphabet][org-rfc-4648-5] ("base64url") encoding, with padding characters removed. The initial encodeURI step allows any UTF-16 string in JavaScript to then be safely encoded to base64url in a web browser. The final step of removing padding removes the "=" character which might be subject to percent-encoding as part of a URL.

**Note that "base64url" is not the same encoding as "base64".** 

To encode:

* encode to a UTF-8 string described by [encodeURI][org-ecma-encodeuri]
* encode the resulting UTF-8 string as [base64url][org-rfc-4648-5]
* remove any "=" padding characters from the end

To decode:

* restore any missing "=" padding characters to the end of the string
* decode the resulting string from base64url to a UTF-8 string
* decode the resulting UTF-8 string as described by [decodeURI][org-ecma-decodeuri]

Code samples for these operations are given in the next section.

Any content state that is in JSON-LD form, rather than a simple URI string, _MUST_ be encoded in this way when declared inline in an HTML document or passed as an HTTP request parameter (e.g., GET or POST), and a client _MUST_ accept it in this form.

Simple URI forms _MAY_ be either plain strings, URI-encoded plain strings, or content-state encoded strings, and a client _MUST_ accept these forms and distinguish between them. 

When published as inline, encoded JSON-LD in the full form given in 2.2, the content state Annotation _MAY_ omit the `id` and `@context` properties.

When published on a server for clients to fetch over HTTP, in the same way a client would fetch a Manifest or Collection, content states _MUST_ be valid JSON-LD documents conforming to the [IIIF Presentation API][prezi-api] and served as described in [Section 5][contentstate-http] below. They _SHOULD NOT_ be encoded, but _MAY_ have other encodings appropriate for JSON content, such as `Content-Encoding: gzip` to reduce the response size.


#### 2.3.2 Examples of Content State Encoding

```javascript

// JavaScript 

function encodeContentState(plainContentState) {
    let uriEncoded = encodeURI(plainContentState);  // using built in function
    let base64 = btoa(uriEncoded);                  // using built in function
    let base64url = base64.replace(/\+/g, "-").replace(/\//g, "_");
    let base64urlNoPadding = base64url.replace(/=/g, "");
    return base64urlNoPadding;
}


function decodeContentState(encodedContentState) {
    let base64url = restorePadding(encodedContentState);
    let base64 = base64url.replace(/-/g, '+').replace(/_/g, '/');
    let base64Decoded = atob(base64);               // using built in function
    let uriDecoded = decodeURI(base64Decoded);      // using built in function
    return uriDecoded;
}


function restorePadding(s) {
    let pad = s.length % 4;
    if (pad) {
        if (pad === 1) {
            throw new Error('InvalidLengthError: Input base64url string is the wrong length to determine padding');
        }
        s += new Array(5 - pad).join('=');
    }
    return s;
}
```

```python

# Python

import base64
import urllib

def encode_content_state(plain_content_state):
    uri_encoded = urllib.parse.quote(plain_content_state, safe=',/?:@&=+$#')  # equivalent of encodeURI
    utf8_encoded = uri_encoded.encode("UTF-8")
    base64url = base64.urlsafe_b64encode(utf8_encoded)
    utf8_decoded = base64url.decode("UTF-8")
    base64url_no_padding = utf8_decoded.replace("=", "")
    return base64url_no_padding


def decode_content_state(encoded_content_state):
    padded_content_state = restore_padding(encoded_content_state)
    base64url_decoded = base64.urlsafe_b64decode(padded_content_state)
    utf8_decoded = base64url_decoded.decode("UTF-8")
    uri_decoded = urllib.parse.unquote(utf8_decoded)
    return uri_decoded


def restore_padding(s):
    pad = len(s) % 4
    padding = ""
    if pad:
        if pad == 1:
            raise Exception("InvalidLengthError: Input base64url string is the wrong length to determine padding")
        padding = "=" * (5 - pad)
    return s + padding

```

Given the following content state annotation:

```json
{
  "id": "https://example.org/object1/canvas7#xywh=1000,2000,1000,2000",
  "type": "Canvas",
  "partOf": [{
    "id": "https://example.org/object1/manifest",
    "type": "Manifest"
  }]
}
```

The JSON can be condensed to remove unnecessary whitespace:


```
{"id":"https://example.org/object1/canvas7#xywh=1000,2000,1000,2000","type":"Canvas","partOf":[{"id":"https://example.org/object1/manifest","type":"Manifest"}]}
```

The condensed form is then encoded (this example in Python):

```python
>>> encode_content_state(condensed)

'JTdCJTIyaWQlMjI6JTIyaHR0cHM6Ly9leGFtcGxlLm9yZy9vYmplY3QxL2NhbnZhczcjeHl3aD0xMDAwLDIwMDAsMTAwMCwyMDAwJTIyLCUyMnR5cGUlMjI6JTIyQ2FudmFzJTIyLCUyMnBhcnRPZiUyMjolNUIlN0IlMjJpZCUyMjolMjJodHRwczovL2V4YW1wbGUub3JnL29iamVjdDEvbWFuaWZlc3QlMjIsJTIydHlwZSUyMjolMjJNYW5pZmVzdCUyMiU3RCU1RCU3RA'
```

The string "JTdC..." is the now URI-safe, encoded form of the content state, suitable for passing to and from web applications.

Not all use cases for providing a content state to a client require encoding, because not all of them are susceptible to HTTP transmission issues. For example, a user interface could allow the user to paste or even type content state JSON-LD directly. Examples are given in section 3. In these scenarios, the client should accept unencoded JSON, too.


#### 2.3.3 Protocol

Values are passed into web applications via request parameters, or attributes on HTML elements.

If a client is capable of reading the content state from the value of an HTTP GET or POST request parameter, it _MUST_ look for the content state in a request parameter called `iiif-content`.

If a client is capable of reading the content state from the value of an attribute on an HTML element that instantiates the client, it _SHOULD_ look for the content state in an attribute called `data-iiif-content`.

A content state Annotation may be published inline as part of an HTML document, as in the preceding `data-iiif-content` example, or as a query string parameter forming part of the `href` property of an HTML anchor tag. 

If the content state is a simple URI, the client _MUST_ load the resource at that URI and process it. The resource at that URI _MUST_ be the full Annotation as in 2.2.2. above, or a IIIF Resource as in 2.2.4. That is, the de-referenced response _MUST_ be JSON-LD, and _SHOULD_ have a value of `type` taken from `Annotation`, `Collection`, `Manifest`, `Canvas` and `Range`. The response _MUST_ use UTF-8 encoding.

If the `type` property of the dereferenced resource is `Canvas` or `Range`, the resource _MUST_ include the Manifest URI that the Canvas or Range is to be found in, using the `partOf` property, as in example 2.3.2 above.

If the content state is JSON-LD the client _MUST_ inspect the `type` property to decide whether the value is the full content state Annotation (indicated by the additional presence of the `contentState` motivation) (as in example 2.2.1), or the value of the `target` property of an implied content state Annotation (example 2.2.3). 



## 3. Initialization
{: #initialization}

This specification provides mechanisms that IIIF compatible software can use to expose, share and transfer content state descriptions, but does not specify what form IIIF compatible software itself may take (e.g., a web page, a JavaScript web application, a native mobile application, a desktop application, or display kiosk hardware). Please see the [IIIF Cookbook][annex-cookbook] for further examples of the patterns listed below.


### 3.1. Initialization Mechanisms (Protocol)
{: #initialization-mechanisms}

The data structure _MAY_ be made available to the client using the following mechanisms. Other mechanisms are possible, but outside the scope of the specification.

#### 3.1.1 Linking: HTTP GET (Query String) Parameter
{: #initialization-mechanisms-link}

If the intention is that the linked-to client loads an entire IIIF resource without focusing on any particular part, the simplest form of the content state _SHOULD_ be used:

```html
{% raw %}
<a href="https://example.org/viewer?iiif-content=http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json">Link to Viewer</a>
{% endraw %}
```

In this case the client at `https://example.org/viewer` would load the resource provided, determine that it is a Manifest (rather than, say, a Collection), and process accordingly.

When the intention is to initialize the viewer at a particular part of the resource, more options are available.

In the following examples, the same Annotation is used each time. As JSON:

```json
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

Without the required encoding, the (invalid) link to the viewer would look like this:

```html
{% raw %}
<a href='https://example.org/viewer?iiif-content={"type":"Annotation","motivation":"contentState","target":{"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/canvas/4389772.json","type":"Canvas","partOf":[{"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json","type":"Manifest"}]}}'>INVALID, unencoded link to Viewer</a>
{% endraw %}
```

However, as JSON-LD, this _MUST_ be encoded as described in section 2.3:

```html
{% raw %}
<a href="https://example.org/viewer?iiif-content=JTdCJTIydHlwZSUyMjolMjJBbm5vdGF0aW9uJTIyLCUyMm1vdGl2YXRpb24lMjI6JTIyY29udGVudFN0YXRlJTIyLCUyMnRhcmdldCUyMjolN0IlMjJpZCUyMjolMjJodHRwOi8vZGFtcy5sbGdjLm9yZy51ay9paWlmLzIuMC80Mzg5NzY3L2NhbnZhcy80Mzg5NzcyLmpzb24lMjIsJTIydHlwZSUyMjolMjJDYW52YXMlMjIsJTIycGFydE9mJTIyOiU1QiU3QiUyMmlkJTIyOiUyMmh0dHA6Ly9kYW1zLmxsZ2Mub3JnLnVrL2lpaWYvMi4wLzQzODk3NjcvbWFuaWZlc3QuanNvbiUyMiwlMjJ0eXBlJTIyOiUyMk1hbmlmZXN0JTIyJTdEJTVEJTdEJTdE">Link to Viewer</a>
{% endraw %}
```

The content state may be passed as just the `target` property of an implied Annotation with motivation `contentState`, that is:

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

This results in a more compact form, unencoded, this would be:

```html
{% raw %}
<a href='https://example.org/viewer?iiif-content={"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/canvas/4389772.json","type":"Canvas","partOf":[{"id":"http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json","type":"Manifest"}]}'>Link to Viewer</a>
{% endraw %}
```

However, as JSON-LD again, this _MUST_ be encoded as in section 2.3:

```html
{% raw %}
<a href="https://example.org/viewer?iiif-content=aHR0cHM6Ly9leGFtcGxlLm9yZy92aWV3ZXI_aWlpZi1jb250ZW50PSU3QiUyMmlkJTIyOiUyMmh0dHA6Ly9kYW1zLmxsZ2Mub3JnLnVrL2lpaWYvMi4wLzQzODk3NjcvY2FudmFzLzQzODk3NzIuanNvbiUyMiwlMjJ0eXBlJTIyOiUyMkNhbnZhcyUyMiwlMjJwYXJ0T2YlMjI6JTVCJTdCJTIyaWQlMjI6JTIyaHR0cDovL2RhbXMubGxnYy5vcmcudWsvaWlpZi8yLjAvNDM4OTc2Ny9tYW5pZmVzdC5qc29uJTIyLCUyMnR5cGUlMjI6JTIyTWFuaWZlc3QlMjIlN0QlNUQlN0Q">Link to Viewer</a>
{% endraw %}
```

#### 3.1.2 HTTP POST (Form) Parameter
{: #initialization-mechanisms-post}

The same data structure, in the same formats, may instead be passed to a server in an HTTP POST. This is suited to server-side web applications, such as a web page rendering citations or a view initialized on the server. It is not suitable for initialising a standalone JavaScript application, as the POST data is typically unavailable.

The data should be sent with the `Content-Type` header value `application/x-www-form-urlencoded`, with the parameter name `iiif-content`, as in the following example. This allows content states to be submitted from simple HTML forms (for example, pasting a citation). Curl uses form-urlencoded by default for POST:

```
curl -d 'iiif-content=aHR0cHM6Ly9leGFtcGxlLm9yZy92aWV3ZXI_aWlpZi1jb250ZW50PSU3QiUyMmlkJTIyOiUyMmh0dHA6Ly9kYW1zLmxsZ2Mub3JnLnVrL2lpaWYvMi4wLzQzODk3NjcvY2FudmFzLzQzODk3NzIuanNvbiUyMiwlMjJ0eXBlJTIyOiUyMkNhbnZhcyUyMiwlMjJwYXJ0T2YlMjI6JTVCJTdCJTIyaWQlMjI6JTIyaHR0cDovL2RhbXMubGxnYy5vcmcudWsvaWlpZi8yLjAvNDM4OTc2Ny9tYW5pZmVzdC5qc29uJTIyLCUyMnR5cGUlMjI6JTIyTWFuaWZlc3QlMjIlN0QlNUQlN0Q' -X POST https://example.org/citation-renderer
```

In this example, the server at `https://example.org/citation-renderer` should expect to process the content state in the same forms and variants as above.


#### 3.1.3 Accepting the Content State as a Paste Operation
{: #initialization-mechanisms-paste}

The client allows the content state URI or data to be pasted into part of its UI (e.g., from a "Load..." option exposing a `textarea` element for the user to manually paste into). A client can also accept a paste operation transparently, by reading from the clipboard:

```html
<script>
    document.addEventListener('paste', event => {
        const text = event.clipboardData.getData('text/plain');
        Annotation = JSON.parse(text);
        //... process Annotation
    });
</script>
```

In that scenario the user can paste the content state directly into the view. If supporting this scenario, the client _SHOULD_ accept unencoded JSON as well as content state encoded JSON, and _SHOULD_ accept resource URIs directly, such as a manifest URI.

Refer to Section 3.2 below for methods of exporting data, including the _Copy to clipboard_ pattern, a natural pairing with a paste operation, from one viewer to another.


#### 3.1.4 Drag and Drop
{: #initialization-mechanisms-dragdrop}

In this scenario, one client provides a _draggable_ element:

```html
<img src="http://iiif.io/img/logo-iiif-34x30.png" draggable="true" ondragstart="drag(event)" />

<script>
    function getContentStateAnnotation(){
        // return a stringified representation of the required content state
    }

    function drag(ev) {
        var json = getContentStateAnnotation();
        ev.dataTransfer.setData("text/plain", json);
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
            var json = ev.dataTransfer.getData("text/plain");
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

The first parameter to `setData` and `getData` is the content type, and for maximum interoperability within the scope of this specification this _MUST_ be "text/plain". Applications can assert multiple additional content types for their own custom behavior, such as dragging from the application to the desktop and saving as a file, but this is outside the scope of the current Content State API. In the above example, the content of the drag and drop operation could be a plain URI, or JSON-LD. If JSON-LD, clients receiving the data (by calling `getData`) _SHOULD_ accept the data in both unencoded and encoded forms.


#### 3.1.5  Upload File

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

### 3.1.6 Load by Reference

This is a variant of 3.1.1, with the parameter value a URI rather than the content itself.

```html
<a href="https://example.org/viewer?iiif-content=https://publisher.org/fragment123.json">Link to Viewer</a>
```

The same rules apply; the viewer _MUST_ dereference and process the Annotation at that URI.

### 3.1.7 Common Initialization Parameter

If a IIIF client can accept a content state via a custom HTML attribute, then it _SHOULD_ use the attribute `data-iiif-content` for this purpose, to assist page developers using that client in understanding what the attribute is for. A viewer that accepts content state _SHOULD_ process an Annotation in any of the forms described in the GET parameter section. 

```html

<p>Loading a whole manifest</p>
<div 
    id="iiif-viewer"
    data-iiif-content="http://dams.llgc.org.uk/iiif/2.0/4389767/manifest.json">
</div>

<p>Loading a manifest to show a particular Canvas</p>
<div 
    id="iiif-viewer"
    data-iiif-content="aHR0cHM6Ly9leGFtcGxlLm9yZy92aWV3ZXI_aWlpZi1jb250ZW50PSU3QiUyMmlkJTIyOiUyMmh0dHA6Ly9kYW1zLmxsZ2Mub3JnLnVrL2lpaWYvMi4wLzQzODk3NjcvY2FudmFzLzQzODk3NzIuanNvbiUyMiwlMjJ0eXBlJTIyOiUyMkNhbnZhcyUyMiwlMjJwYXJ0T2YlMjI6JTVCJTdCJTIyaWQlMjI6JTIyaHR0cDovL2RhbXMubGxnYy5vcmcudWsvaWlpZi8yLjAvNDM4OTc2Ny9tYW5pZmVzdC5qc29uJTIyLCUyMnR5cGUlMjI6JTIyTWFuaWZlc3QlMjIlN0QlNUQlN0Q">
</div>
```


### 3.2 Exporting State

There are further ways in which a client can _export_ state, beyond populating a drag and drop operation as in example 3.1.4. While interoperability concerns require this specification to describe the ways in which a client can _accept_ state, the ways in which a content state might have arrived on a user's clipboard are out of scope here, and are covered in the Cookbook. These include:

* Copy to clipboard
* Download file
* Display for copying
* Send external (to citation-accepting service)


## 4. Examples of Content States

The following examples demonstrate the use of the existing IIIF Presentation API and W3C Web Annotation Data Model to describe parts of resources. Any IIIF resource that can be expressed in the Presentation model can be used in a content state. The full form of the Annotation (as if it were available at the URI given in the `id` property) has been used in each case.  Further examples can be found in the [IIIF Cookbook][annex-cookbook].

Publishers should strive to provide the simplest JSON-LD representation, and not assume that any client can handle arbitrarily complex content states.

### 4.1. A Region of a Canvas in a Manifest

```json
{
  "@context": "http://iiif.io/api/presentation/3/context.json",
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


### 4.2. Start Playing at a Point in a Recording

```json
{
  "@context": "http://iiif.io/api/presentation/3/context.json",
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

This example should cause a viewer to open Manifest `https://example.org/iiif/id1/manifest`, navigate to Canvas `https://example.org/iiif/id1/canvas1`, and start playing at 14.5 seconds into that canvas.


### 4.3. Multiple Targets for a Comparison View

```json
{
  "@context": "http://iiif.io/api/presentation/3/context.json",
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

Firstly, in non-valid, unencoded form to show the annotation:

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

...and then in encoded form:

```html
<h2>Results for "cats"</h2>
<ol>
  <li>
    <h3><a href="viewer.html?iiif-content=JTdCJTIyaWQlMjI6JTIyaHR0cHM6Ly9leGFtcGxlLm9yZy9hbGljZS9jYW52YXM3NyN4eXdoPTEwMDAsMjAwMCwxMDAwLDIwMDAlMjIsJTIydHlwZSUyMjolMjJDYW52YXMlMjIsJTIycGFydE9mJTIyOiU1QiU3QiUyMmlkJTIyOiUyMmh0dHBzOi8vZXhhbXBsZS5vcmcvYWxpY2UvbWFuaWZlc3QlMjIsJTIydHlwZSUyMjolMjJNYW5pZmVzdCUyMiU3RCU1RCU3RA">Alice in Wonderland</a></h3>
    <p>...she has often seen a <b>cat</b> without a grin but never a grin without a <b>cat</b></p>
  </li>
  <!-- ... more results -->
</ol>
```



## 5. HTTP Requests and Responses

This section describes the _RECOMMENDED_ request and response interactions for the API, when served as JSON-LD bodies of HTTP responses. It does not apply to _inline_ content states, which are encoded as described in section 2.3, and transfered by the other mechanisms described above. This section follows the specification given in [Section 6][prezi30-http] of the Presentation API.

###  5.1. Requests

An HTTP request for a content state is the same as an HTTP request for a Presentation API resource. Unlike [IIIF Image API][image-api] requests, or other parameterized services, the URIs for Presentation API resources cannot be assumed to follow any particular pattern. A client that fetches URIs for content states and URIs for Presentation API resources (such as Manifests and Collections) by the same mechanism _MUST_ inspect the response to determine whether it is a Presentation API resource, or a content state that references part of a Presentation API resource.

###  5.2. Responses

The format for content states as HTTP responses is JSON, as described above. It is good practice for all resources with an HTTP(S) URI to provide their description when the URI is dereferenced. If a resource is [referenced][prezi30-terminology] within a response, rather than being [embedded][prezi30-terminology], then it _MUST_ be able to be dereferenced.

If the server receives a request with an `Accept` header, it _SHOULD_ respond following the rules of [content negotiation][org-rfc-7231-conneg]. Note that content types provided in the `Accept` header of the request _MAY_ include parameters, for example `profile` or `charset`.

If the request does not include an `Accept` header, the HTTP `Content-Type` header of the response _SHOULD_ have the value `application/ld+json` (JSON-LD) with the `profile` parameter given as the context document: `http://iiif.io/api/presentation/3/context.json`.

``` none
Content-Type: application/ld+json;profile="http://iiif.io/api/presentation/3/context.json"
```
{: .urltemplate}

If the `Content-Type` header `application/ld+json` cannot be generated due to server configuration details, then the `Content-Type` header _SHOULD_ instead be `application/json` (regular JSON), without a `profile` parameter.

``` none
Content-Type: application/json
```
{: .urltemplate}

The HTTP server _MUST_ follow the [CORS requirements][org-w3c-cors] to enable browser-based clients to retrieve the descriptions. Recipes for enabling CORS and conditional Content-Type headers are provided in the [Apache HTTP Server Implementation Notes][notes-apache].


## Appendices

### A. Acknowledgements
{: #acknowledgements}

Many thanks to the members of the [IIIF community][iiif-community] for their continuous engagement, innovative ideas, and feedback.

This version is due to the work of the [IIIF Discovery Technical Specification Group][groups-discovery], chaired by Antoine Isaac (Europeana), Matthew McGrattan (Digirati) and Rob Sanderson (Yale University). The IIIF Community thanks them for their leadership, and the members of the group for their tireless work.

### B. Change Log
{: #change-log}

| Date       | Description           |
| ---------- | --------------------- |
| 2021-06-21 | Version 0.9 (unnamed) |
| 2020-11-22 | Version 0.3 (unnamed) |
| 2019-02-04 | Version 0.2 (unnamed) |
| 2018-10-31 | Version 0.1 (unnamed) |

{% include links.md %}
