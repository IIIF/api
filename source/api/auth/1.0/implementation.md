---
title: "IIIF Authentication: Implementation Notes"
title_override: "IIIF Authentication: Implementation Notes"
id: auth-api-notes
layout: spec
tags: [compliance, auth-api]
major: 1
minor: 0
patch: 0
pre: final
cssversion: 2
redirect_from:
  - /api/auth/1.0/implementation.html
---

## Status of this Document
{:.no_toc}

This document applies to version {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %} of the [IIIF Authentication API][auth-api] specification.

## Table of Contents
{:.no_toc}

* Goes Here
{:toc}

## 1. Introduction
{: #introduction}

This document is a companion to the [IIIF Authentication API][auth-api]  specification. It addresses issues that might be met when implementing the specification in a browser-based JavaScript application.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss].

### 1.1 Summary of Authentication Flow
{: #summary-of-authentication-flow}

As detailed in the [IIIF Authentication API][auth-api] specification, clients need to distinguish between Content Resources that are loaded indirectly, such as images or videos, and Description Resources typically loaded directly via the [XmlHttpRequest API][xmlhttprequest] (XHR), such as the info.json document that describes an image service. The client uses a Description Resource to build the elements that will trigger the browser to request the Content Resources

A web page on the *host domain* loads a IIIF client application from the *client domain* (such as a content delivery network) which in turn loads the IIIF descriptions and content from one or more *resource domains*. Therefore all interactions are potentially subject to the cross-domain security polices of modern browsers.

A client implementing the IIIF Authentication Specification orchestrates a sequence of user interactions and HTTP requests that result in the user's browser acquiring an __access cookie__ from the *resource domain* that grants access to Content Resources on that domain. Code from the *client domain* cannot see the access cookie set by the server on the *resource domain* and has limited ability to infer the user's authentication state from observations of the browser's interactions with the Content Resources. Instead, the specification relies on the client's ability to inspect the HTTP status codes and body content of the responses received from requests for Description Resources, typically made via XHR.

When the client requests a Description Resource via XHR, the browser cannot usually send any cookies it has for the *resource domain*, for the reason given in the [CORS support](#cors-support) section. Instead, the client sends an __access token__. The IIIF Authentication Specification describes how, once the browser has acquired the access cookie, the client code acquires the access token to use when making direct requests for Description Resources.

At a minimum, a client implementation following a "happy path" would:

* Request a new Description Resource
* Observe an HTTP status code other than 200 on the response
* Observe that the Description Resource provides a login service
* Offer the user a way to trigger opening of the login service URL in a new tab
* Open the login service in the new tab in response to user action (e.g., clicking a login button)
* Detect the closing of this new tab
* Call the token service and get a valid token
* Re-request the Description Resource with the token in an `Authorization` header
* Observe that the status code is now 200
* Use the information in the Description Resource to display the Content Resource described

There are different ways of implementing this in different styles of client user interface. These notes explore the issues implementers will encounter.

## 2. CORS Support
{: #cors-support}

The [IIIF Authentication API][auth-api] specification requires a CORS-compliant browser. See the [browser-specific issues](#browser-specific-issues) section for more details.

While the CORS and XHR specifications allow for a cross-domain request (from the *client domain* to the *resource domain*) that includes the browser's cookies for the resource domain, the conditions imposed make the approach unsuitable for IIIF use. Under these conditions, clients would make an XHR request with `XMLHttpRequest.withCredentials = true`, which triggers a CORS preflight request. The preflight response from the *resource domain* server must then include an `Access-Control-Allow-Origin` header whose value is the specific trusted *client domain*. In a request made with `XMLHttpRequest.withCredentials = true` the wildcard `*` value for `Access-Control-Allow-Origin` is invalid, and servers servers should not simply echo back the client origin header. Together these restrictions avoid cooked cookie leakage to an untrusted client script.

The IIIF Authentication Specification must work for a client that is untrusted (in CORS terms); anyone should be able to run any IIIF client from anywhere and use it to load any resources. Therefore the specification assumes that any cookie information for the *resource domain* is unavailable to the client code, including the knowledge of the existence or otherwise of any cookies. IIIF clients do not need to make `withCredentials` requests.

## 3. Use of Service Labels and Descriptions
{: #use-of-service-labels-and-descriptions}

Servers supporting the IIIF Authentication Specification will provide a [Service Description][service-description] that includes labels, and may include descriptions and header values, for the login services they expose. In this way the server can influence the presentation of the login services to the user. For example, the header and description could be used by the client as the title and text of a dialog box. Clients should present this text to the user to help them decide what to do; a publisher should assume that the login label will always be made obvious to the user during the authentication flow.

A server could use different login services to provide different messaging to the user, even if the implementation is identical and they share the same token and logout services. One institution could have a single login service, another could have hundreds that differ not in their behavior but in their labels, descriptions and headers, allowing the content provider to customize the displayed text to fit the content. Client software is expected to make prominent use of the provided text. The label and description values can be string literals or JSON-LD value objects.

## 4. Window Behavior Across Devices
{: #window-behavior-across-devices}

In the [browser client workflow][workflow-from-the-browser-client-perspective] an HTTP 401 response to a request for a Description Resource indicates the need to authenticate before any content can be displayed.

### 4.1 Event Initiation
{: #event-initiation}

On detecting a 401 response, a client could trigger the load of the login service URL automatically, in a pop up window or new tab. The advantage of this approach is that if the user is already logged in on the Resource Domain, the window will close automatically straight away, and the client can continue with the login flow without unnecessarily troubling the user for credentials they have already established.

However, this approach stands a strong chance of being blocked on a desktop browser, and an almost certain chance of being blocked on a mobile browser. Popup blockers in general don’t like windows that aren’t opened by an event sequence initiated directly by user click or equivalent, although the user might be notified by a "popup blocked" warning. On most mobile platforms, a “new window” (in this case a browser tab) must ALWAYS be initiated by a user interaction with an element (e.g., button click) and cannot be faked by artificially clicking elements, even if the user has popups enabled.

See also [browser-specific issues](#browser-specific-issues) for other reasons why new windows might be blocked.

A client can still prevent sending the user on unnecessary authentication flows by using the access token service as a probe; a call to the access token service can be used to see whether the user has credentials already, and to construct a request for the Description Resource with the appropriate Authorization header. The workflow in the specification describes the points at which the token service must be called, but client implementations are free to optimize the user experience with additional calls earlier in the flow.

### 4.2 Windows and Tabs
{: #windows-and-tabs}

The ```Window.open()``` API includes an optional parameter that allows the caller to specify various position, size, toolbar and "chrome" features of the opened window. A client confined to desktop browsers could use this to make the presentation of the login service URL feel more like a dialog box rather than a sudden visit to a different site.

However, window features like this are not generally available on mobile devices and clients on those platforms might find the window blocked if it is opened with specific features.

### 4.3 Consistency
{: #consistency}

The preceding comments on window behavior suggest that for consistency of user experience across devices and maximum compatibility, client applications should trigger the login flow in response to an explicit click, and open the login service URL in a new tab whose presentation is left up to the browser.

## 5. Redirects and Degraded Images
{: #redirects-and-degraded-images}

Clients should expect to deal with image services that offer nothing at all to unauthorized users, and those that offer a degraded image. The first use case could be for sensitive or rights-protected material where no access is feasible that would allow a user to read text. The second use case could be for a "premium content" approach, where detailed high-resolution images are only available to authorized users. In the first case, the server responds to an initial unauthenticated Description Resource request with an HTTP 401 status code. In the second case the server responds with status code 302.

A client might attempt to deal with the response like this:

```javascript
switch(myXhr.statusCode){
    case 200:
        // process Content Resource for rendering        	
    case 302:
        // process Content Resource for rendering
        // notify user that image is degraded, encourage user to click "log in"     
    case 401:
        // unauthorized, encourage user to click "log in"
}
```

However, the 302 status code will never be seen by client script interacting with the XmlHttpRequest API. By design, this is transparent to the XHR object in browsers for security reasons, and the response will report only the final HTTP 200 status code of the degraded image. Whether this is significant for a client depends on the approach it takes to the user interface.

### 5.1 User Interface Patterns
{: #user-interface-patterns}

A client can present the authentication service information to the user in at least two distinct user interface patterns:

* **Alongside** - always show a login button in the user interface if one or more login service are provided for the current Content Resource. This pattern may be best in clients expected to deal with degraded content. The user interface has space for a login button, the login service header and ideally the login service description.
* **Challenge** - only present login user interface when the client detects the user is being prevented from seeing the best possible resource. This pattern may be best in clients expected to deal with "all or nothing" scenarios. The login user interface - a button, the header and the description if available - might be seen in a popup dialogue or alert, preventing further interaction by challenging the user.

Other interface designs may combine elements of these approaches to some degree, and a general purpose client should handle degraded and "all or nothing" scenarios equally well.

A user interface that relies on the "challenge" approach therefore has a problem with a degraded image that has been redirected. It cannot tell from the status code and response body of the Description Resource that a redirect has occurred. It looks like a normal 200 response.

Evidence that a redirect has happened is available. If the `@id` of the service returned is not the URI the client asked for (allowing for the presence or absence of `/info.json` on the end), that SHOULD mean that a redirect has happened - but the redirect may not have been for access control reasons. The `@id` of an image service asserted in a manifest may be different because the service has moved since the manifest was published, or for other unknown reasons.

A client could make a decision about what is happening based on a redirect having occurred, an authentication service being present, and perhaps a probe of a token service. The client can’t be completely sure that the user is seeing a degraded image. Implementations where login and logout buttons are always present and enabled for the current visible image if it has a login service don’t need to worry too much about this, as the user can decide from the image's appearance and the labeling of the service whether they are looking at the best possible image.

## 6. Token Storage Strategies
{: #token-storage-strategies}

Clients should keep track of the access tokens they acquire for the user and use them to improve the user experience. Careful use of access tokens can avoid unnecessary authentication interactions for the user, and unnecessary HTTP requests for the client.

An implementation could store a dictionary of acquired access tokens where the key is the `@id` of the token service, and try the most recently used "preemptively" for new requests to the same domain. This dictionary could be saved to browser local storage. The client should not use an expired token, so it needs to keep track of when the token was acquired for comparison with the token's time-to-live.

A client should always be prepared to discard a stored token and should never trust its stored token as a true representation of the user's current authentication status on the Resource Domain. Any point at which the client receives a status code other than 200 could trigger a re-run of the authentication flow, but it could first trigger a call to the token service for the resource to check the user's state.

To encourage the frequent use of requests to the token service to improve the user experience, a client should assume that the token service is a lightweight operation, and servers should ensure that they can handle frequent token requests.

## 7. Security for Server Implementers
{: #security-for-server-implementers}

Server implementations must assume that they could be subject to attacks that attempt to use this IIIF Authentication Specification to trick users into authenticating and revealing secrets to malicious client code. Care is required to implement this specification in a way that does not expose credentials, compromising the security of the protected resources or other resources within the same security domain.

The specification relies on making the access token available to third party script (i.e., any untrusted script running on the client domain). The token is deliberately "leaked" to the client domain by the postMessage interaction. This means that ANY third-party script could acquire a user's access token, if it can persuade the user to follow the authentication flow.

Therefore servers should follow these principles:

* Don't accept the access token as a credential for anything other than Description Resources whose token service is the service the token was acquired from. That is, do not accept the token as a credential on a request made for the full Content Resources, or anything else sensitive such as user account settings. The cookie granted by a content-hosting institution to access the content might often grant access to other areas of the web site as well.
* Don't use the same value for the access token as the access cookie, or use a value for the access cookie that could be deduced or calculated from the access token value.
* Don't include secrets in the Description Resources. Usually the metadata in a Description Resource such as an info.json is not itself secret, even if the Content Resources (e.g. in the case of images, the pixels) requires authorization. However, there may be some Description Resources for which the metadata is sensitive. In these cases the response body for an unauthorized request should omit the secrets. The Description response cannot be empty - it needs to describe the authentication services to the client as well as convey enough information to let the client decide whether it's worth authenticating to view the material. It still needs to describe what it is, but it isn't required to go into the same detail as the fully authorized response.
* Ensure that the web server isn't configured to serve custom error pages - the client needs to see the info.json, even when the HTTP response status is not 200.
* Access cookies should be relatively short-lived - minutes rather than months. Any client can trigger an interaction with the token service. The browser will send the access cookie to the token service and so any client can acquire the token later on. Limiting the access cookie lifetime helps mitigate threats.

If these guidelines are followed, then a malicious script that obtains an access token cannot do anything useful with it. The malicious script can't send the access token somewhere where it can be used to construct a request to gain access to the content resources or other resources protected by the same cookie on the content domain. The access token remains just a token - a symbol of the real credential (the access cookie) that the user has for the resources.

The specification is modeled after elements of the OAuth2 workflow and the [OAuth2 Security Considerations][oauth2-considerations] section provides useful additional guidance regarding threats, mitigations and recommended practices.

__Future extension__
The authentication interaction patterns will need to accommodate future functionality where the client is POSTing annotations or IIIF resources, where the token accompanying an XHR request is not just a proxy for the cookie the user has for the images, but is the "real" credential for writing a resource. The specification already requires that "origin" is appended to both the access cookie request and the token request, for the server to use in white-listing decisions if it wants to e.g., granting tokens that give access to image resources for any origin but only issuing tokens that authorize a state-changing operation to permitted origins. The server could use any additional (currently undefined) information obtained during the access cookie step (as well as the origin) to help it decide whether to then issue a token in the access token step (i.e., respond with a web page that makes a postMessage call to the origin supplied).
{: .note}

## 8. Optimizations at the Presentation API Level
{: #optimizations-at-the-presentation-api-level}

A IIIF client application that loads a manifest would need to load each referenced image service on each image of each canvas in turn to determine in advance whether authentication services were present on all the images the user might interact with. For some applications this knowledge is not required - the client can deal with any authentication concerns at the point the user interacts with a particular image. However, some client applications would benefit from knowledge of the authentication services across all the images, for example:

* rendering large numbers of thumbnails from access controlled services
* adding visual clues to the navigation user interface to indicate that some of the images in the manifest are protected

If a server could convey this information in the manifest the client would have what it needs in the initial load. There's nothing stopping a manifest publisher of the manifest including the full authentication services:

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "@id": "http://example.org/iiif/book1/annotation/p0001-image",
  "@type": "oa:Annotation",
  "motivation": "sc:painting",
  "resource": {
    "@id": "http://example.org/iiif/book1/res/page1.jpg",
    "@type": "dctypes:Image",
    "format": "image/jpeg",
    "service": {
      "@context": "http://iiif.io/api/image/2/context.json",
      "@id": "http://example.org/images/book1-page1",
      "profile": "http://iiif.io/api/image/2/profiles/level2.json",
      "service": {
        "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
        "@id": "http://example.org/iiif/loginservice",
        "profile": "http://iiif.io/api/auth/{{ page.major }}/login",
        "label": "This material requires authorization",
        "header": "This material requires authorization",
        "description": "...",
        "service": [
            {
                "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
                "@id": "http://example.org/iiif/token",
                "profile": "http://iiif.io/api/auth/{{ page.major }}/token"
            },
            {
                "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
                "@id": "http://example.org/iiif/logout",
                "profile": "http://iiif.io/api/auth/{{ page.major }}/logout",
                "label": "Log out"
            }
        ]
      }
    },
    "height":2000,
    "width":1500
  },
  "on": "http://example.org/iiif/book1/canvas/p1"
}
```

However, this would result in a very large manifest if there are a large number of images, and there is a lot of repetition of information. As a JSON-LD document, the login service does not have to be stated in full every time - if the above example provided the full service on the first canvas, then the next canvas could state the same information using the service URL alone:

``` json-doc
{
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "@id": "http://example.org/iiif/book1/annotation/p0002-image",
  "@type": "oa:Annotation",
  "motivation": "sc:painting",
  "resource": {
    "@id": "http://example.org/iiif/book1/res/page2.jpg",
    "@type": "dctypes:Image",
    "format": "image/jpeg",
    "service": {
      "@context": "http://iiif.io/api/image/2/context.json",
      "@id": "http://example.org/images/book1-page2",
      "profile": "http://iiif.io/api/image/2/profiles/level2.json",
      "service": "http://example.org/iiif/loginservice"
    },
    "height":2000,
    "width":1500
  },
  "on": "http://example.org/iiif/book1/canvas/p2"
}
```

This approach represents an optimization only, and clients should never depend on it alone. The server must ensure that the full service is asserted at least once (e.g., on the first occurrence) and the client must be able to deal with the URI-only and expanded forms and treat them the same - it must be able to find the expanded version elsewhere in the document if it encounters the URL on its own.

A client should not assume that a manifest will contain any hints of this nature, and should always assume the information in the Image Service Description Resource is correct if it disagrees with something asserted in the manifest. The above is a suggested approach for clients and servers to follow to convey the authentication information for the images at the manifest level in a concise manner, particularly when all the image services referenced in the manifest are provided by the manifest publisher.

## 9. Browser-Specific Issues
{: #browser-specific-issues}

### 9.1 Internet Explorer
{: #internet-explorer}

#### 9.1.1 CORS and XDomainRequest in IE9 and Below
{: #cors-and-xdomainrequest-in-ie9-and-below}

IE8 and IE9 have the [HttpXmlRequest][xhr] object, but unlike the implementation in IE10+ and current versions of Safari, Chrome and Firefox it does not support CORS, so will not allow clients to attempt any kind of cross domain request.

In IE8 and IE9, Microsoft separated out cross domain activity into the [XDomainRequest][xdr] interface. This sits alongside XmlHttpRequest in IE8 and IE9 (and was dropped in IE10 when XHR became fully CORS compliant). Clients must use XDomainRequest instead of XmlHttpRequest when they need to go cross-domain. This works fine for many Ajax scenarios, and it can be shimmed it into jQuery via libraries such as [jQuery-ajaxTransport-XDomainRequest][moonscript] which hide the distinction between the two interfaces when doing CORS from jQuery.

However, XDomainRequest handles HTTP status codes differently from XmlHttpRequest. Although a client can perform many AJAX operations with it, it treats HTTP status codes in the 4xx range as error conditions, and raises an error. The [XDomainRequest.onerror][xdr-error] does not let the client see the status code or the response body, which makes it impossible to implement the IIIF Authentication API.

This means two things:

1. A client can't see the body of the info.json unless it is returned as HTTP 200. So a client can't see the services.
2. A client can't distinguish between 401 and other errors. They are all just "error" events.

In IE8/9, XmlHttpRequest won't let a client load the info.json at all (unless on the same domain) and XDomainRequest won't let a client do anything with it unless it was a 200. XmlHttpRequest in IE8/9 (and, in fact, even earlier) *will* let a client see the status code.

This means that the IIIF Authentication Specification cannot be implemented in IE8 and IE9 cross-domain. A custom client deployment where the *host domain*, the *client domain* and the *resource domain* are all the same will allow an implementation of the specification that works on IE9; as of 2016 it is possible that some implementations may still have the requirement to work on IE9 and can satisfy this same-origin constraint.

#### 9.1.2 P3P Policy in IE Prior to Edge
{: #p3p-policy-in-ie-prior-to-edge}

Internet Explorer versions prior to the current "Edge" specification (including IE11) implement [P3P], which in the context of the IIIF Authentication specification will prevent a browser sending cookies across domain even for a content resource like an image or for an indirect load of the token via the frame used for postMessage, if those cookies have an explicit expiry and could therefore be used for tracking purposes across browser sessions.

This can lead to hard-to-diagnose problems - one implementation of the specification might work in IE and another might fail, simply because they have different cookie expiry settings.

Internet Explorer *will* send the cookie if the resource domain [publishes a P3P policy][p3p-summary] in the form of a P3P HTTP header that summarizes the privacy policy of the site.

#### 9.1.3 Security Zones in All Versions of IE
{: #security-zones-in-all-versions-of-ie}

Internet Explorer (all versions) assigns all websites to one of four security zones: Internet, Local intranet, Trusted sites, or Restricted sites. The zone to which a website is assigned specifies the security settings that are used for that site. Corporate IT policies can assign sites to zones for all users on a domain.

This can affect an implementation of the Authentication API. If the new tab opened by the client to navigate to the login service URL on the resource domain involves a transition from a less trusted to a more trusted zone, the client script will no longer be able interact with the window - specifically its reference to the opened window is set to `null` and it therefore cannot tell when the window is closed. This zone transition includes any subsequent redirects that happen in the opened login window, including a redirect from the resource domain to a separate authentication server such as a CAS or OAuth2 implementation.

If, for example, the client domain and resource domain are in the *Internet* zone, but the login service on the resource domain involves a redirect to an authentication system which to internal network users is in the *Intranet* zone, the login flow will not work.

## Appendices

###  A. Change Log

| Date       | Description |
| ---------- | ----------- |
| 2018-10-13 | Fix typos |
| 2017-01-19 | Updated to apply to version 1.0.0 |
| 2016-10-05 | Clarifications to text, applies to version 0.9.4 |
| 2016-09-25 | Update implementation notes to apply to version 0.9.3 |
{: .api-table .first-col-normal}


[iiif-discuss]: mailto:iiif-discuss@googlegroups.com "Email Discussion List"
[auth-api]: {{ site.url }}{{ site.baseurl }}/api/auth/{{ page.major }}.{{ page.minor }}/ "Authentication API {{ page.major }}.{{ page.minor }}"
[service-description]: {{ site.url }}{{ site.baseurl }}/api/auth/{{ page.major }}.{{ page.minor }}/#service-description "Authentication API Service Description"
[workflow-from-the-browser-client-perspective]: {{ site.url }}{{ site.baseurl }}/api/auth/{{ page.major }}.{{ page.minor }}/#workflow-from-the-browser-client-perspective "Authentication API Workflow from the Browser Client Perspective"
[xhr]: https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest "HttpXmlRequest"
[xdr]: https://developer.mozilla.org/en-US/docs/Web/API/XDomainRequest "XDomainRequest"
[moonscript]: https://github.com/MoonScript/jQuery-ajaxTransport-XDomainRequest "jQuery-ajaxTransport-XDomainRequest"
[xdr-error]: https://developer.mozilla.org/en-US/docs/Web/API/XDomainRequest/onerror "XDomainRequest.onerror"
[P3P]: https://www.w3.org/P3P/ "P3P"
[p3p-summary]: http://blogs.msdn.com/b/ieinternals/archive/2013/09/17/simple-introduction-to-p3p-cookie-blocking-frame.aspx "P3P minimum details"
[oauth2-considerations]: https://tools.ietf.org/html/rfc6750#section-5 "OAuth2 Security Considerations"
[xmlhttprequest]: https://xhr.spec.whatwg.org/ "XMLHttpRequest API"

{% include acronyms.md %}
