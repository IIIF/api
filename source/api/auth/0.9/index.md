---
title: "IIIF Authentication: Version 0.9.2"
title_override: "IIIF Authentication: Version 0.9.2"
id: auth-api
layout: spec
tags: [specifications, image-api]
major: 0
minor: 9
patch: 2
pre: final
cssversion: 2
redirect_from:
  - /api/auth/index.html
---

## Status of this Document
{:.no_toc}

__This Version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Beta Specification for Trial Use__
This is a work in progress. We are actively seeking implementations and feedback.  No section should be considered final, and the absence of any content does not imply that such content is out of scope, or may not appear in the future.  Please send any feedback to [iiif-discuss@googlegroups.com][iiif-discuss].
{: .alert}

**Editors:**

  * **[Michael Appleby](https://orcid.org/0000-0002-1266-298X)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0002-1266-298X), [_Yale University_](http://www.yale.edu/)
  * **[Tom Crane](https://orcid.org/0000-0003-1881-243X)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0003-1881-243X), [_Digirati_](http://digirati.com/)
  * **[Robert Sanderson](https://orcid.org/0000-0003-4441-6852)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0003-4441-6852), [_Stanford University_](http://www.stanford.edu/)
  * **[Jon Stroop](https://orcid.org/0000-0002-0367-1243)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0002-0367-1243), [_Princeton University Library_](https://library.princeton.edu/)
  * **[Simeon Warner](https://orcid.org/0000-0002-7970-7855)** [![ORCID iD](/img/orcid_16x16.png)](https://orcid.org/0000-0002-7970-7855), [_Cornell University_](https://www.cornell.edu/)
  {: .names}

{% include copyright.md %}

----

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}


## 1. Introduction

The IIIF (pronounced "Triple-Eye-Eff") specifications are designed to support uniform and rich access to resources hosted around the world. Open access to content is desirable, but policy, regulations, or business models can require users to authenticate and be authorized to interact with access-controlled resources. The authentication process could range from a simple click-through agreement to a multi-factor scheme with a secure identity provider.

Content providers often offer tiers of access beyond a simple all-or-nothing distinction. These tiers could provide versions of the resource that differ based on resolution, watermarking, or compression. Each version must have a distinct URI to prevent web caches from providing the wrong version. 

Providing interoperable content through client applications running in a web browser poses many challenges:

* A single IIIF Presentation API manifest can reference content resources at multiple institutions and hence from multiple domains.
* Institutions have different existing access control systems and should not have to adopt a new one to participate.
* A IIIF client can be a JavaScript viewer served from a different domain from the image services, and the authentication services that protect them. This domain is _untrusted_ - the authorizing server must not require any prior knowledge of the domain hosting the viewer. The specification must not introduce or require any registry of trusted IIIF viewer domains and must assume that for image delivery, anyone can create any kind of viewer and run it from anywhere.  
* A IIIF client should not ask for or accept any credentials itself; the server hosting the content must be responsible for capturing credentials from a user and the IIIF viewer needs no knowledge of or access to this exchange.
* A browser-based IIIF client must be able to maintain its state during an authentication flow.

To meet these challenges, the IIIF Authentication specification describes a process for orchestrating the user through an existing access control system. The process of authenticating the user is mostly outside the scope of the specification. It may involve a round-trip to a CAS server, or an OAuth2 provider, or a bespoke login system. In this sense, IIIF Authentication is not the same as a protocol like CAS; it is a pattern for interacting with arbitrary third party protocols. 

IIIF Authentication provides a link to a user interface for logging in, and services that provide credentials, modelled after elements of the OAuth2 workflow. Together they act as a bridge to the access control system in use on the server, without the client requiring knowledge of that system.

In summary, the specification describes how to:

* From within a viewer, initiate an interaction with an access control system so that a user can acquire the credentials they need to view that content.
* Give the client just enough knowledge of the user's state with respect to the content provider to ensure a good user experience.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss].

### 1.1. Terminology

This specification distinguishes between Content Resources, such as images or videos, and Description Resources which conform to IIIF specifications, such as [Image API][image-api] image information (info.json) and [Presentation API][prezi-api] collection or manifest resources.  From the point of view of a browser-based application, Content Resources are loaded indirectly via browser interpretation of HTML elements, whereas Description Resources are typically loaded directly by JavaScript using the `XMLHttpRequest` interface. The [Cross Origin Resource Sharing][cors-spec] (CORS) specification implemented in modern browsers describes the different security rules that apply to the interactions with these two types of resource.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][rfc-2119].

### 1.2. Authentication for Content Resources

Content Resources, such as images, are generally secondary resources embedded in a web page or application. In the case of web pages, images might be included via the HTML `img` tag, and retrieved via additional HTTP requests by the browser. When a user is not authorized to load a web page, the server can redirect the user to another page and offer the opportunity to authenticate. This redirection is not possible for embedded Content Resources, and the user is simply presented with a broken image icon. If the image is access controlled, the browser must avoid broken images by sending a cookie that the server can accept as a credential that grants access to the image. This specification describes the process by which the user acquires this **access cookie**.

### 1.3. Authentication for Description Resources

Description Resources, such as a Presentation API manifest or an Image API information document (info.json), give the client application the information it needs to have the browser request the Content Resources. A Description Resource must be on the same domain as the Content Resource it describes, but there is no requirement that the executing client code is also hosted on this domain.

A browser running JavaScript retrieved from one domain cannot use `XMLHttpRequest` to load a Description Resource from another domain and include that domain's cookies in the request, without violating the requirement introduced above that the client must work when _untrusted_.  Instead, the client sends an **access token**, technically a type of [bearer token][bearer-token], as a proxy for the access cookie. This specification describes how, once the browser has acquired the access cookie for the Content Resources, the client acquires the access token to use when making direct requests for Description Resources.

The server on the Resource Domain treats the access token as a representation of, or proxy for, the cookie that gains access to the Content Resources. When the client makes requests for the Description Resources and presents the access token, the responses tell the client what will happen when the browser requests the corresponding content resources with the access cookie the access token represents. These responses let the client decide what user interface and/or Content Resources to show to the user.


## 2. Authentication Services

Authentication services follow the pattern described in the IIIF [Linking to External Services][ext-services] note, and are referenced in one or more `service` blocks from the descriptions of the resources that are protected. There is a primary login service profile for authenticating users, and it has related services nested within its description.  The related services include a mandatory access token service, and optional client identity and logout services.

### 2.1. Access Cookie Service

The client uses this service to obtain a cookie that will be used when interacting with content such as images, and with the access token service. There are several different interaction patterns in which the client will use this service, based on the user interface that must be rendered for the user, indicated by a profile URI. The client obtains the link to the access cookie service from a service block in a description of the protected resource.

The purpose of the access cookie service is to set a cookie during the user's interaction with the content server, so that when the client then makes image requests to the content server, the requests will succeed. The client has no knowledge of what happens at the login service, and it cannot see any cookies set for the content domain during the user's interaction with the login service. The browser may be redirected one or more times but this is invisible to the client application. The final response in the opened tab _SHOULD_ contain JavaScript that will attempt to close the tab, in order to trigger the next step in the workflow.  For more information about the process, see [Step 3][user-auths] in the workflow.

If the client identity service, described below, is present in the description, then the client _MUST_ include the authorization code in the URL as a query parameter named `code` when making its request to the service.

#### 2.1.1. Service Description

There are four interaction patterns by which the client can obtain an access cookie, each identified by a profile URI. These patterns are described in more detail in the following sections.

| Pattern      | Profile URI | Description |
| ------------ | ----------- | ----------- |
| Login        | `http://iiif.io/api/auth/{{ page.major }}/login` | The user will be required to log in using a separate window with a UI provided by an external authentication system. |
| Clickthrough | `http://iiif.io/api/auth/{{ page.major }}/clickthrough` | The user will be required to click a button within the client using content provided in the service description. |
| Kiosk        | `http://iiif.io/api/auth/{{ page.major }}/kiosk` | The user will not be required to interact with an authentication system, the client is expected to use the access cookie service automatically. |
| External     | `http://iiif.io/api/auth/{{ page.major }}/external` | The user is expected to have already acquired the appropriate cookie, and the access cookie service will not be used at all. |
{: .api-table}

The service description is included in the Description Resource and has the following properties:

| Property     | Required?   | Description |
| ------------ | ----------- | ----------- |
| @context     | _REQUIRED_    | The context document that describes the IIIF Authentication API. The value _MUST_ be `http://iiif.io/api/auth/{{ page.major }}/context.json`.|
| @id          | _see description_ | It is _REQUIRED_ with the Login, Clickthrough, or Kiosk patterns, in which the client opens the URI in order to obtain an access cookie. It is _OPTIONAL_ with the External pattern, as the user is expected to have obtained the cookie by other means and any value provided is ignored. |
| profile      | _REQUIRED_    | The profile for the service _MUST_ be one of the profile URIs from the table above.|
| label        | _REQUIRED_    | The text to be shown to the user to initiate the loading of the authentication service when there are multiple services required. The value _MUST_ include the domain or institution to which the user is authenticating. |
| confirmLabel | _RECOMMENDED_ | The text to be shown to the user on the button or element that triggers opening of the access cookie service. If not present, the client supplies text appropriate to the interaction pattern if needed. |
| header       | _RECOMMENDED_ | A short text to be shown to the user as a header for the description, or alone if no description is given. |
| description  | _RECOMMENDED_ | Text that, if present, _MUST_ be shown to the user before opening the access cookie service. |
| failureHeader | _OPTIONAL_ | A short text to be shown to the user as a header after failing to receive a token, or using the token results in an error. |
| failureDescription | _OPTIONAL_ | Text that, if present, _SHOULD_ be shown to the user after failing to receive a token, or using the token results in an error. |
| service      | _REQUIRED_    | References to access token and other related services, described below.|
{: .api-table}


#### 2.1.2. Login Interaction Pattern

In order to have the client prompt the user to log in, it must display part of the content provider's user interface. For the Login interaction pattern, the value of the `@id` property is the URI of that user interface.  The interaction has the following steps:

* If the `header` and/or `description` properties are present, before opening the provider's authentication interface, the client _SHOULD_ display the values of the properties to the user.  The properties will describe what is about to happen when they click the element with the `confirmLabel`. 
* When the `confirmLabel` element is activated, the client _MUST_ then open the URI from `@id`. This _MUST_ be done in a new window or tab to help prevent spoofing attacks. Browser security rules prevent the client from knowing what is happening in the new tab, therefore the client can only wait for and detect the closing of the opened tab.
* After the opened tab is closed, the client _MUST_ then use the related access token service, as described below.

With out-of-band knowledge, authorized non-user-driven clients _MAY_ use POST to send the pre-authenticated user’s information to the service. As the information required depends on authorization logic, the details are not specified by this API. In these situations, use of the client identity service is strongly _RECOMMENDED_.

An example service description for the Login interaction pattern:

``` json-doc
{
  // ...
  "service" : {
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "@id": "https://authentication.example.org/login",
    "profile": "http://iiif.io/api/auth/{{ page.major }}/login",
    "label": "Login to Example Institution",
    "header": "Please Log In",
    "description": "Example Institution requires that you log in with your example account to view this content.",
    "confirmLabel": "Login",
    "failureHeader": "Authentication Failed",
    "failureDescription": "<a href=\"http://example.org/policy\">Access Policy</a>",
    "service": [
      // Access token and Logout services ...
    ]
  }
}
```

### 2.1.3. Clickthrough Interaction

For the Clickthrough interaction pattern, the value of the `@id` property is the URI of a service that _MUST_ set an access cookie and then immediately close its window or tab without user interaction.  The interaction has the following steps:

* If the `header` and/or `description` properties are present, before opening the service, the client _MUST_ display the values of the properties to the user.  The properties will describe the agreement implied by clicking the element with the `confirmLabel`. 
* When the `confirmLabel` element is activated, the client _MUST_ then open the URI from `@id`. This _SHOULD_ be done in a new window or tab. Browser security rules prevent the client from knowing what is happening in the new tab, therefore the client can only wait for and detect the closing of the opened window or tab or iframe.
* After the opened tab is closed, the client _MUST_ then use the related access token service, as described below.

Non-user-driven clients _MUST_ not use access cookie services with the Clickthrough interaction pattern, and instead halt.

An example service description for the Clickthrough interaction pattern:

``` json-doc
{
  // ...
  "service" : {
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "@id": "https://authentication.example.org/clickthrough",
    "profile": "http://iiif.io/api/auth/{{ page.major }}/clickthrough",
    "label": "Terms of Use for Example Institution",
    "header": "Restricted Material with Terms of Use",
    "description": "<span>... terms of use ... </span>",
    "confirmLabel": "I Agree",
    "failureHeader": "Terms of Use Not Accepted",
    "failureDescription": "You must accept the terms of use to see the content.",
    "service": {
      // Access token service ...
    }
  }
}
```

### 2.1.4. Kiosk Interaction

For the Kiosk interaction pattern, the value of the `@id` property is the URI of a service that _MUST_ set an access cookie and then immediately close its window or tab without user interaction.  The interaction has the following steps:

* There is no user interaction before opening the access cookie service URI, and therefore any of the `label`, `header`, `description` and `confirmLabel` properties are ignored if present.
* The client _MUST_ immediately open the URI from `@id`. This _SHOULD_ be done in a new window or tab. Browser security rules prevent the client from knowing what is happening in the new tab, therefore the client can only wait for and detect the closing of the opened window or tab or frame.
* After the opened tab is closed, the client _MUST_ then use the related access token service, as described below.

Non-user-driven clients simply access the URI from `@id` to obtain the access cookie, and then use the related access token service, as described below.

An example service description for the Kiosk interaction pattern:

``` json-doc
{
  // ...
  "service" : {
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "@id": "https://authentication.example.org/cookiebaker",
    "profile": "http://iiif.io/api/auth/{{ page.major }}/kiosk",
    "label": "Internal cookie granting service",
    "failureHeader": "Ooops!",
    "failureDescription": "Call Bob at ext. 1234 to reboot the cookie server",
    "service": {
      // Access token service ...
    }
  }
}
```


### 2.1.5. External Interaction

For the External interaction pattern, the user is required to have acquired the access cookie by out of band means. If the access cookie is not present, the user will receive the failure messages. The interaction has the following steps:

* There is no user interaction before opening the __access token__ service URI, and therefore any of the `label`, `header`, `description` and `confirmLabel` properties are ignored if present.
* There is no access cookie service. Any URI specified in the `@id` property _MUST_ be ignored. 
* The client _MUST_ immediately use the related access token service, as described below.

Non-user-driven clients simply use the related access token service with a previously acquired access cookie, as described below.

An example service description for the External interaction pattern:

``` json-doc
{
  // ...
  "service" : {
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "profile": "http://iiif.io/api/auth/{{ page.major }}/external",
    "label": "External Authentication Required",
    "failureHeader": "Restricted Material",
    "failureDescription": "This material is not viewable without prior agreement",
    "service": {
      // Access token service ...
    }
  }
}
```

### 2.2. Access Token Service

The access token service provides the client with a bearer access token. The client then includes this access token in requests for description resources. A request to the access token service must include any cookies for the content domain acquired from the user's interaction with the parent login service, so that the server can issue the access token.

#### 2.2.1. Service Description

The login service description _MUST_ include an access token `service` following the template below:

``` json-doc
{
  // ...
  "service" : {
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "@id": "https://authentication.example.org/login",
    "profile": "http://iiif.io/api/auth/{{ page.major }}/login",
    "label": "Login to Example Service",
    "service": [
      {
        "@id": "https://authentication.example.org/token",
        "profile": "http://iiif.io/api/auth/{{ page.major }}/token"
      }
    ]
  }
}
```

The `@id` field _MUST_ be present, and its value _MUST_ be the URI from which the client can obtain the access token. The `profile` property _MUST_ be present and its value _MUST_ be `http://iiif.io/api/auth/{{ page.major }}/token` to distinguish it from other services. There is no requirement to have a `label` property for this service, as it does not need to be presented to a user. There is no requirement for a duplicate `@context` field.


#### 2.2.2. The JSON access token response

If the request has a valid cookie that the server recognises as having been issued by the login service, the access token service response _MUST_ include a JSON (not JSON-LD) object with the following structure:

``` json-doc
{
  "accessToken": "TOKEN_HERE",
  "tokenType": "Bearer",
  "expiresIn": 3600
}
```

Where the value of the `accessToken` field is the access token to be passed back in future requests, `tokenType` is always `Bearer`, and `expiresIn` is the number of seconds in which the access token will cease to be valid.  If there is no timeout for the access token, then `expiresIn` may be omitted from the response.

Once obtained, the access token _MUST_ be passed back to the server on all future requests via the `XMLHttpRequest` interface by adding an `Authorization` request header, with the value `Bearer TOKEN_HERE`.  The access token _SHOULD_ be added to all requests for resources from the same domain and subdomains that have a reference to the service, regardless of which API is being interacted with. It _MUST NOT_ be sent to other domains.

If the client is not a web browser, and can send cookies to the access token service, it _SHOULD_ request the access token service's URI directly, with all of the cookies sent to or established by the login service, and the server _MUST_ respond with the above access token structure as the entire response body.

#### 2.2.3. Interaction for non-browser client applications

The simplest access token request comes from a non-browser client that can send cookies across domains, where the CORS restrictions do not apply. If an authorization code was obtained using the client identity service, described below, then this _MUST_ be passed to the access token service as the value of a query parameter called `code`. 

An example URL:

``` none
https://authentication.example.org/token?code=AUTH_CODE_HERE
```
{: .urltemplate}

Would result in the HTTP Request:

``` none
GET /iiif/token?code=AUTH_CODE_HERE HTTP/1.1
Cookie: <cookie-acquired-during-login>
```
{: .urltemplate}

The response is the JSON access token object with the media type `application/json`:

``` json-doc
{
  "accessToken": "TOKEN_HERE",
  "tokenType": "Bearer",
  "expiresIn": 3600
}
```


#### 2.2.4. Interaction for browser-based client applications

If the client is a JavaScript application running in a web browser, it needs to make a direct request for the access token and store the result. The client can't use `XMLHttpRequest` because it can't include the cookie acquired from the login service in a cross-domain request.

Instead, the client _MUST_ open the access token service in a frame using an `iframe` element and be ready to receive a message posted by script in that frame using the [postMessage API][postmessage]. To trigger this behaviour, the client _MUST_ append the following query parameters to the token service URI, and open this new URI in the frame.

| Parameter | Description |
| --------- | ----------- |
| messageId | A string that both prompts the server to respond with a web page instead of JSON, and allows the client to match access token service requests with the messages received.  If a client has no need to interact with multiple token services, it can use a dummy value for the parameter, e.g., `messageId=1`. |
| origin    | A string containing the origin of the window, consisting of the protocol, hostname and optionally port number of the server the client is instantiated from, as described in the [postMessage API][postmessage] specification.  |
| code      | The client authorization code obtained, if any, as described below. |
{: .api-table}

For example, a client running at `https://client.example.com/viewer/index.html` would request:

```
https://authentication.example.org/token?code=AUTH_CODE_HERE&messageId=1&origin=https://client.example.com/
```

When the server receives a request for the access token service with the `messageId` parameter, it _MUST_ respond with an HTML web page rather than raw JSON. The web page _MUST_ contain script that sends a message to the opening page using the postMessage API. The message body is the JSON access token object, with the value of the supplied `messageId` as an extra property, as shown in the examples in the next section.  

The server _MAY_ use the origin information for further authorization logic, even though the user is already authenticated. For example, the server may trust only specific domains for certain actions like creating or deleting resources compared to simply reading them. If the client sends an incorrect value, it will not receive the posted response, as the postMessage API will not dispatch the event. The `targetOrigin` parameter of the `postMessage()` function call _MUST_ be the origin provided in the request.

The frame _SHOULD NOT_ be shown to the user. It is a mechanism for cross-domain messaging. The client _MUST_ register an event listener to receive the message that the token service page in the frame will send. The client can reuse the same listener and frame for multiple calls to the access token service, or it can create new ones for each invocation.

The exact implementation will vary but _MUST_ include features equivalent to the following steps.

The client must first register an event listener to receive a cross domain message:

```javascript
window.addEventListener("message", receive_message);

function receive_message(event) {
    data = event.data;
    var token, error;
    if (data.hasOwnProperty('accessToken')) {
        token = data.accessToken;
    } else {
        // handle error condition
    }
    // ...
}
```
It can then open the access token service in a frame:

```javascript
document.getElementById('messageFrame').src = 
  'https://authentication.example.org/token?messageId=1234&origin=https://client.example.com/';
```

The server response will then be a web page with a media type of `text/html` that can post a message to the registered listener:

```html
<html>
<body>
<script>    
    window.parent.postMessage(
      {
        "messageId": "1234",
        "accessToken": "TOKEN_HERE",
        "tokenType": "Bearer",
        "expiresIn": 3600
      }, 
      'https://client.example.com/'
    );    
</script>
</body>
</html>
```

#### 2.2.5. Using the access token

The access token is sent on all subsequent requests for Description Resources. For example, a request for the image information in the Image API would look like:

``` none
GET /iiif/identifier/info.json HTTP/1.1
Authorization: Bearer TOKEN_HERE
```
{: .urltemplate}


### 2.3. Logout Service

Once the user has authenticated, the client will need to know if and where the user can go to logout.

#### 2.3.1. Service Description

If the authentication system supports users intentionally logging out, there _SHOULD_ be a logout service associated with the login service following the template below:

``` json-doc
{
  // ...
  "service" : {
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "@id": "https://authentication.example.org/login",
    "profile": "http://iiif.io/api/auth/{{ page.major }}/login",
    "label": "Login to Example Service",
    "service" : [
      {
        "@id": "https://authentication.example.org/token",
        "profile": "http://iiif.io/api/auth/{{ page.major }}/token"
      },
      {
        "@id": "https://authentication.example.org/logout",
        "profile": "http://iiif.io/api/auth/{{ page.major }}/logout",
        "label": "Logout from Example Service"
      }
    ]
  }
}
```

The same semantics and requirements for the fields as the login service apply to the logout service.  The value of the `profile` property _MUST_ be `http://iiif.io/api/auth/{{ page.major }}/logout`.

#### 2.3.2. Interaction

The client _SHOULD_ present the results of the an HTTP `GET` request on the service's URI in a separate tab or window with a URL bar.  At the same time, the client _SHOULD_ discard any access token that it has received from the corresponding service. The server _SHOULD_ reset the user's logged in status when this request is made.


### 2.4. Client Identity Service

The client identity service allows software clients to authenticate themselves and receive an authorization code to use with the associated access token and login services. The service might be used by applications in library readng rooms, kiosk exhibits in museums or other environments where the client application is locked down. It would typically not be used on the open web in a general purpose client.

#### 2.4.1. Service Description

The login service description _MAY_ include a client identity service description following this template:

``` json-doc
{
  // ...
  "service" : {
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "@id": "https://authentication.example.org/login",
    "profile": "http://iiif.io/api/auth/{{ page.major }}/login",
    "label": "Login to Example Service",
    "service" : [
      {
        "@id": "https://authentication.example.org/token",
        "profile": "http://iiif.io/api/auth/{{ page.major }}/token"
      },
      {
        "@id": "https://authentication.example.org/clientId",
        "profile": "http://iiif.io/api/auth/{{ page.major }}/clientId"
      }
    ]
  }
}
```

The `@id` field _MUST_ be present, and its value _MUST_ be the URI at which the client can obtain an authorization code. The `profile` property _MUST_ be present and its value _MUST_ be `http://iiif.io/api/auth/{{ page.major }}/clientId` to distinguish it from other services. There is no requirement to have a `label` property for this service, as it does not need to be presented to a user. There is no requirement to have a duplicate `@context` property for the service.

#### 2.4.2. Interaction

The client _MUST_ POST a document containing its client id and a pre-established client secret key.  It will receive in response an authorization code to use when requesting the access token for the user.

The request body _MUST_ be JSON and _MUST_ conform to the following template:

``` json-doc
{
  "clientId" : "CLIENT_ID_HERE",
  "clientSecret" : "CLIENT_SECRET_HERE"
}
```

The body of the response from the server _MUST_ be JSON and _MUST_ conform to the following template:

``` json-doc
{
  "authorizationCode" : "AUTH_CODE_HERE"
}
```


### 2.5. Error Conditions

The response from the client identity service or the access token service may be an error. The error _MUST_ be supplied as JSON with the following template. For browser-based clients using postMessage, the error object must be sent to the client via script, in the same way the access token is sent. For direct requests the response body is the raw JSON.

``` json-doc
{
  "error": "ERROR_TYPE_HERE",
  "description": ""
}
```

Where `ERROR_TYPE_HERE` _MUST_ be one of the types in the following table:  

| Type | Description |
| ---- | ----------- |
| `invalidRequest`      | The service could not process the information sent in the body of the request |
| `missingCredentials`  | The request did not have the credentials required |
| `invalidCredentials`  | The request had credentials that are not valid for the service |
| `invalidClient`       | The client identity provided is unknown to the service |
| `invalidClientSecret` | The client secret provided is not the secret expected by the service |
{: .api-table}

The `description` property is _OPTIONAL_ and may give additional information to client developers for debugging the interaction. This information _SHOULD NOT_ be presented to end users.

When returning JSON directly, the service _MUST_ use the appropriate HTTP status code for the response to describe the error (for example 400, 401 or 403).  The postMessage web page response _MUST_ use the 200 HTTP status code to ensure that the body is received by the client correctly.

### 2.6. Example JSON Response

The example below is a complete image information response for an example image with three of the four possible services referenced.

``` json-doc
{
  "@context" : "http://iiif.io/api/image/2/context.json",
  "@id" : "https://www.example.org/images/image1",
  "protocol" : "http://iiif.io/api/image",
  "width" : 600,
  "height" : 400,
  "sizes" : [
    {"width" : 150, "height" : 100},
    {"width" : 600, "height" : 400}
  ],
  "profile" : [
    "http://iiif.io/api/image/2/level2.json",
    {
      "formats" : [ "gif", "pdf" ],
      "qualities" : [ "color", "gray" ],
      "supports" : [
          "canonicalLinkHeader", "rotationArbitrary"
      ]
    }
  ],
  "service" : {
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "@id": "https://authentication.example.org/login",
    "profile": "http://iiif.io/api/auth/{{ page.major }}/login",
    "label": "Login to Example Service",
    "service": [
      {
        "@id": "https://authentication.example.org/clientId",
        "profile": "http://iiif.io/api/auth/{{ page.major }}/clientId"
      },
      {
        "@id": "https://authentication.example.org/token",
        "profile": "http://iiif.io/api/auth/{{ page.major }}/token"
      }
    ]
  }
}
```

## 3. Workflow

The following workflow steps through the basic interactions for authenticating and requesting access to resources using the IIIF authentication services.  It assumes no prior interactions with the services. This section makes extensive use of the [terminology](#terminology) defined in the introduction.

### 3.1. Step 1: Request Description Resource

The first step for the client is to request the desired Description Resource, such as an image information document (info.json), or a [Presentation API][prezi-api] manifest, collection, or annotation list.  The response will dictate the client's next step, which is likely to be to present the user with a login service in a new browser tab or window.

The response from the server _MUST_ include the service descriptions, as shown above, and any required properties such as `@context` and `@id`, thus allowing a client to present something to the user, regardless of whether the user is authenticated or not.

If a server does not support degraded access to the resource, and wishes to require authentication, it _MUST_ return a response with a 401 (Unauthorized) HTTP status code. This response _MUST NOT_ include a `WWW-Authenticate` header, and if basic authentication is required, then it _MUST_ be delivered from a different URI listed in the `@id` field of the login service block.

If a server supports degraded access for users that are not authenticated, then it _MUST_ use a different identifier for the degraded resource from that of the higher quality version. When the higher quality resource is requested and the user is not authorized to access it, the server _MUST_ issue a 302 (Found) HTTP status response to redirect to the degraded version.

### 3.2. Step 2: Obtain Client Authorization Code (Optional)

In cases where the server requires client software to be registered, there _MUST_ be a client identity service in the response.  The client _MUST_ use the service to obtain an authorization code prior to requesting an access token for the user.

### 3.3. Step 3: User Authenticates

After receiving the response, the client will have a URL for a login service where the user can authenticate.  The client _MUST_ present the login service to the user by opening the URL in a separate tab or window with a URL bar, not in an iFrame or otherwise imported into the client user interface, in order to help prevent spoofing attacks.

The client has no visibility of or access to the user's interactions with the login service in the separate tab or window. If the user successfully authenticates, the login service _MUST_ ensure that the client has a cookie that identifies the user and will be visible to the access token service. It _SHOULD_ also contain JavaScript to try and automatically close the tab or window. The tab or window closing is the trigger for the client to request the access token for the user.

(link to implementation note? Access to win.closed?)

### 3.4. Step 4: Obtain Access Token

The client requests an access token from the access token service. If [step 2](#step-2-obtain-client-authorization-code-optional) was performed, the client authorization code _MUST_ also be sent. The server _MUST_ detect and evaluate any cookie(s) obtained from the login service, and if present and valid it _MUST_ return an access token. The access token _MUST_ be added by the client to all future requests for Description Resources that have the same access token service, by including it in an `Authorization` header.

If the cookie is not present, or is present but invalid for any reason (for example, it represents an expired session), the server _MUST_ return an error message, and the client _SHOULD_ allow the user to attempt to login again.

### 3.5. Step 5: Re-request Description Resource

Now with the access token added in the `Authorization` header, the client retries the request for the Description Resource to determine whether the user is now successfully authenticated and authorized. Clients _SHOULD_ store the URIs of login services that have been accessed by the user and not prompt the user to login again when they are already authenticated. Clients _SHOULD_ make use of the `expiresIn` property from the access token response.

If there is a logout service described in the Description Resource then the client _SHOULD_ provide a logout link. The client _SHOULD_ present this URL to the user in a separate tab or window with a URL bar to help prevent spoofing attacks.

If the user is successfully authenticated but not authorized, or business logic on the server dictates that authorization will never be possible, then the server _MUST_ respond to Description Resource requests with the 403 (Forbidden) HTTP status code.

### 3.6. Step 6: Request Content Resource (Optional)

Now that the client has the access cookie from [step 4](#step-4-obtain-access-token), it may then make futher requests for access-controlled, non-degraded Content Resources. Requests for Content Resources do not rely on the `Authorization` header because JavaScript clients are unable to set this for resources included via HTML.

If the server supports degraded access and the user is authenticated but not authorized for the higher quality version of the Content Resource, or business logic dictates that authorization will never be possible, then the server _SHOULD_ respond to requests with the 302 (Found) HTTP status code and the `Location` header set to the degraded version's URI.

## 4. Workflow from the Server Perspective

<table class="ex_table">
  <tbody>
    <tr>
      <td>
        <img style="width: 300px" src="img/auth-flow-server.png" alt="Server Authentication Flow" class="fullPct" />
        <p><strong>1</strong> Server Authentication Workflow</p>
      </td>
    </tr>
  </tbody>
</table>

When the server receives a request for a Description Resource, (1), it first must determine if the user is authorized to access the resource or any content described by that resource, given the current credentials (if any) passed to it via the `Authorization` header.  If the user is authorized, then the server returns a 200 status response with the full information (2).  If not, and there is a description of a degraded resource available, the server returns a 302 status response redirecting the client to the degraded version (3).  If the server does not have a degraded version and the client is authenticated but not authorized to access the resource, it returns a 403 status response to tell the client that it should not continue trying (4).  Finally, if the client is not authenticated, the server returns a 401 status response with a JSON representation that contains the service link to where the user can authenticate (5).

## 5. Workflow from the Client Perspective

<table class="ex_table">
  <tbody>
    <tr>
      <td>
        <img style="max-width: 650px" src="img/auth-flow-client.png" alt="Client Authentication Flow" class="fullPct" />
        <p><strong>2</strong> Client Authentication Workflow</p>
      </td>
    </tr>
  </tbody>
</table>


__TODO:__ 
We need to say something here about detecting the 302 status, which cannot be seen directly by XHR as described in [implementation notes][tmp-impl-302]. Also some other parts of that document might be useful here.
{: .warning}

The client first requests the desired Description Resource (1).  If the response is a 200 with the expected information, the client does not need to authenticate and should proceed to use the resource as expected (2).  If not, and the response is a 302 redirect, then the client follows the redirect to retrieve a new resource (3).  If the client has seen that resource already, by comparing its URI with those in a list of seen URIs, then the user is not authorized to access the requested version, and it should use the degraded version from the current response (4).  Otherwise, if it has not seen the response before, or the initial response is a 401 status with a link to the service (5), the client follows the link to the login service in a newly created tab or window (6) and records that it has seen the URI.  The user must then attempt to authenticate using the service (7), and the client waits until the tab or window is closed, either automatically or manually by the user.  Once the tab or window is closed, the client retrieves an access token for the user and retries the request for the original Description Resource (8), and proceeds back to make the same tests.  Finally, if the client receives a 403 response from the server, the user cannot gain authorization to interact with the resource and there is no degraded version available, and hence the client should not render anything beyond an error message.

## Appendices

### A. Implementation Notes

 * Care is required to implement this specification in a way that does not expose credentials thus compromising the security of the resources intended to be protected, or other resources within the same security domain.
 * Services using authentication should use HTTPS, and thus clients should also be run from pages served via HTTPS.
 * Implementations must not reuse the access cookie value as the access token value, as it could be copied across domains when the access token is obtained from a malicious client.
 * Without a client identity

(how much of [implementation notes][tmp-impl] could go here?)


### B. Versioning

Starting with version 0.9.0, this specification follows [Semantic Versioning][semver]. See the note [Versioning of APIs][versioning] for details regarding how this is implemented.

###  C. Acknowledgments

The production of this document was generously supported by a grant from the [Andrew W. Mellon Foundation][mellon].

Many thanks to the members of the [IIIF Community][iiif-community] for their continuous engagement, innovative ideas and feedback.

###  D. Change Log

| Date       | Description |
| ---------- | ----------- |
| 2015-10-30 | Version 0.9.1 (Table Flip) add missing @context, clarifications |
| 2015-07-28 | Version 0.9.0 (unnamed) draft |
{: .api-table}

[postmessage]: https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage "window.postMessage"
[tmp-impl]: implementation/
[tmp-impl-sec]: implementation/#security-for-server-implementors
[tmp-impl-302]: implementation/#redirects-and-degraded-images
[cors-spec]: http://www.w3.org/TR/cors/ "Cross-Origin Resource Sharing"
[iiif-discuss]: mailto:iiif-discuss@googlegroups.com "Email Discussion List"
[client-auth-img]: img/auth-flow-client.png
[server-auth-img]: img/auth-flow-server.png
[semver]: http://semver.org/spec/v2.0.0.html "Semantic Versioning 2.0.0"
[iiif-community]: /community/ "IIIF Community"
[versioning]: /api/annex/notes/semver/ "Versioning of APIs"
[mellon]: http://www.mellon.org/ "The Andrew W. Mellon Foundation"
[change-log]: /api/image/2.0/change-log/ "Change Log for Version 2.0"
[rfc-2119]: http://tools.ietf.org/html/rfc2119
[prezi-api]: /api/presentation/
[image-api]: /api/image/
[ext-services]: /api/annex/services/
[user-auths]: #step-3-user-authenticates
[bearer-token]: https://tools.ietf.org/html/rfc6750#section-1.2 "OAuth2 Bearer Tokens"

{% include acronyms.md %}
