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

Open access to content is desirable, but policy, regulations or business models mean that sometimes users must authenticate and be authorized to interact with access-controlled resources. For interoperable content accessed through client applications running in a web browser, this poses many challenges:

* A single manifest can reference content resources at multiple institutions and hence from multiple domains.
* Institutions have different existing access control systems (e.g., CAS). The IIIF (pronounced "Triple-Eye-Eff") specification can't force an institution to adopt a new protocol beyond the scope of image interoperability.
* The specification can't require that a browser-based client destroys its state during an authentication flow.
* The client can be a JavaScript viewer served from a different domain from the image services, and the authentication services that protect them. This domain is _untrusted_ - the authorising server must not require any prior knowledge of the domain hosting the viewer. The specification must not introduce or require any registry of trusted IIIF viewer domains and must assume that for image delivery, anyone can create any kind of viewer and run it from anywhere.  
* A IIIF client should not ask for or accept any credentials itself; the server hosting the content must be responsible for capturing credentials from a user and the IIIF viewer needs no knowledge of or access to this exchange.

To meet these challenges, the IIIF Authentication specification describes a process for orchestrating the user through a content provider's existing access control system. What happens at the content provider (i.e., your server) is mostly outside the scope of the specification. It may involve a round-trip to a CAS server, or an OAuth2 provider, or a bespoke login system. In this sense, IIIF Authentication is not the same as a protocol like CAS; it is a pattern for interacting with arbitrary third party protocols. 

A IIIF Authentication implementation provides a link to user interface (the login service) and a discovery mechanism modelled after elements of the OAUth2 workflow (the token service). Together they act as a bridge to the access control system in use on the server, without the client requiring knowledge of that system.

Some access to content is generally better than no access. In the case of images, grayscale instead of color, a version with a watermark, a version with more compression, or a smaller size is likely better than no image at all. Providing this functionality is more complex than traditional yes-or-no access controls, and serving the correct image and associated image information for the degraded version is necessary to prevent web caches from providing incorrect content. The same notion of degraded access might apply for other types of resources.

In summary, the specification describes how to:

* from within a viewer, initiate an interaction with a content provider's access control so that a user can acquire the cookie(s) they need to view that content
* give the client just enough knowledge of the user's state with respect to the content provider to ensure a good user experience

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]

### 1.1. Terminology

This specification distinguishes between Content Resources, such as images or videos, and Description Resources which conform to IIIF specifications, such as [Image API][image-api] image information (info.json) and [Presentation API][prezi-api] collection or manifest resources.  

From the point of view of a client JavaScript application, Content Resources are loaded indirectly, by the browser, whereas Description Resources are typically loaded by script using the XMLHttpRequest interface. The [Cross Origin Resource Sharing][cors-spec] specification implemented in modern browsers describes the security rules that apply for these two different kinds of interaction.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][rfc-2119].

### 1.2. Authentication for Content Resources

Content Resources, such as images, are generally secondary resources embedded in a web page or application. In the case of web pages, images might be included via the HTML `img` tag, and retrieved via additional HTTP requests by the browser. When a user is not authorised to load a web page, the server can redirect the user to another page and offer the opportunity to authenticate. This redirection is not possible for embedded Content Resources, and the user is simply presented with a broken image icon. If the image is access controlled, the browser must avoid broken images by sending a cookie that the server can accept as a credential that grants access to the image. The specification describes the process by which the user acquires this cookie.

### 1.3. Authentication for Description Resources

Description Resources, such as a Presentation API manifest or an Image API information document (info.json), give the client application the information it needs to make the browser request the Content Resources. A Description Resource must be on the same domain as the Content Resource it describes, but there is no requirement that the executing client code is also hosted on this domain.

A browser running script from one domain cannot use XMLHttpRequest to load a Description Resource from another domain and include that domain's cookies in the request, without violating the requirement introduced above that the client must work when _untrusted_.  Instead, the client sends a **bearer token**. The Authentication Specification describes how, once the browser has acquired the cookie for the Content Resources, the client acquires the bearer token to use when making direct requests for Description Resources.

The server on the Resource Domain treats the bearer token as a representation of or proxy for the cookie that gains access to the Content Resources. When the client makes requests for the Description Resources and presents the token, the responses tell the client what will happen when the browser requests the corresponding content resources with the cookie the token represents. These responses let the client decide what user interface and/or Content Resources to show to the user.

__Note:__
TC: An annotation is not a description resource like an info.json or a manifest; it IS the resource being access controlled rather than a description of it, and may require a more complex exchange; perhaps a 2-way postMessage handshake that is not required for "binary" content resources. v1.1?
{: .note}

## 2. Authentication Services

Authentication services follow the pattern described in the IIIF [Linking to External Services][ext-services] note, and are referenced in one or more `service` blocks from the descriptions of the resources that are protected. There is a primary login service profile for authenticating users, and it has related services nested within its description.  The related services include a mandatory access token service, and optional client identity and logout services.

### 2.1. Login Service

In order to have the client prompt the user to login, it must display part of the content provider's user interface. The login service is a link to that user interface, which the client must launch in a new window or tab. Browser security rules prevent the client from knowing what is happening in the new tab. The client can only wait for and detect the closing of the opened tab.

#### 2.1.1. Service Description

The Description Resource _MUST_ include a service using the following template:

``` json-doc
{
  // ...
  "service" : {
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "@id": "https://authentication.example.org/login",
    "profile": "http://iiif.io/api/auth/{{ page.major }}/login",
    "label": "Login to Example Service",
    "description": "Institution X requires that you log in with your X account to view this content."
    "service": [
      // Related services ...
    ]
  }
}
```

Where the `@id` field _MUST_ be present and contains the URI that the client should load in order to allow the user to authenticate. The `@context` field _MUST_ be present with the value `http://iiif.io/api/auth/{{ page.major }}/context.json`, specifying the context to resolve the keys into RDF if necessary. The value of `profile` _MUST_ be `http://iiif.io/api/auth/{{ page.major }}/login`, allowing clients to understand the use of the service. The `label` property _MUST_ be present and its value is to be shown to the user to initiate the loading of the authentication service. The `description` property is _RECOMMENDED_ as it can be used by the client to provide additional information about the interaction that will take place at the login service.  The `service` field _MUST_ be present and will contain related services described below.

#### 2.1.2. Interaction

User-interactive clients, such as web browsers, _MUST_ present the results of an HTTP `GET` request on the service's URI in a separate tab or window with a URL bar to help prevent spoofing attacks.

The purpose of the login service opened in the new tab is to set a cookie during the user's interaction with the content server, so that when the client then makes image requests to the content server, the requests will succeed. The client has no knowledge of what happens at the login service, and it cannot see any cookies set for the content domain during the user's interaction with the login service. The browser may be redirected one or more times in the open tab as the user interacts with the institution's access control system, but this is invisible to the client application. The final response in the opened tab _SHOULD_ contain JavaScript that will attempt to close the tab, in order to trigger the next step in the workflow.  For more information about the process, see [Step 3][user-auths] in the workflow.

If the client identity service, described below, is present in the description, then the client _MUST_ include the authorization code in the URL as a query parameter named `code` when making its request to the service.

With out-of-band knowledge, authorized non-user driven clients _MAY_ use POST to send the pre-authenticated user's information to the service.  As the information required depends on authorization business logic, the details are not specified by this API.  In these situations, use of the client identity service is strongly _RECOMMENDED_.

### 2.2. Access Token Service

The access token service provides the client with a bearer token. The client then includes this token in  requests for description resources. A request to the token service must include any cookies for the content domain acquired from the user's interaction with the parent login service, so that the server can issue the token.

#### 2.2.1. Service Description

The login service description _MUST_ include a token `service` following the template below:

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

The `@id` field _MUST_ be present, and its value _MUST_ be the URI from which the client can obtain the token. The `profile` property _MUST_ be present and its value _MUST_ be `http://iiif.io/api/auth/{{ page.major }}/token` to distinguish it from other services. There is no requirement to have a `label` property for this service, as it does not need to be presented to a user. There is no requirement for a duplicate `@context` field.


#### 2.2.2. The JSON token response

If the request has a valid cookie that the server recognises as having been issued by the login service, the token service response _MUST_ include a JSON (not JSON-LD) object with the following structure:

``` json-doc
{
  "accessToken": "TOKEN_HERE",
  "tokenType": "Bearer",
  "expiresIn": 3600
}
```

Where the value of the `accessToken` field is the token to be passed back in future requests, `tokenType` is always `Bearer`, and `expiresIn` is the number of seconds in which the token will cease to be valid.  If there is no timeout for the token, then `expiresIn` may be omitted from the response.

Once obtained, the token value _MUST_ be passed back to the server on all future requests via the XMLHttpRequest interface by adding an `Authorization` request header, with the value `Bearer TOKEN_HERE`.  The token _SHOULD_ be added to all requests for resources from the same domain and subdomains that have a reference to the service, regardless of which API is being interacted with. It _MUST NOT_ be sent to other domains.

If the client is not a web browser, and can send cookies to the token service, it _SHOULD_ request the access token service's URI directly, with all of the cookies sent to or established by the login service, and the server _MUST_ respond with the above access token structure as the entire response body.


#### 2.2.3. PostMessage Interaction for browser-based client applications

If the client is a JavaScript application running in a web browser, it needs to make a direct request for the token and store the result. The client can't use XMLHttpRequest because it can't include the cookie acquired from the login service in a cross-domain request.

Instead, the client _MUST_ open the token service in an iFrame and be ready to receive a message posted by script in that iFrame, using the [postMessage API][postmessage]. To trigger this behaviour, the client _MUST_ append the query string parameter `messageId` to the token service URI with a generated value, and open this new URI in the iFrame. 

When the server receives a request for the token service with the `messageId` parameter, it _MUST_ respond with  an HTML web page for the iFrame, rather than raw JSON. The web page _MUST_ contain script that sends a message to the opening page using the [postMessage API][postmessage]. The message body is the JSON token object, with the value of the supplied `messageId` as an extra property, as shown in the examples in the next section.

The iFrame _SHOULD NOT_ be shown to the user. It is a mechanism for cross-domain messaging. The client _MUST_ register an event listener to receive the message that the opened token service page in the iFrame will post. The client can reuse the same listener and iFrame for multiple calls to the token service, or it can create new ones for each invocation depending on the implementation.

The `messageId` parameter serves two purposes. It triggers the server to respond with the web page instead of JSON, and it allows the client to match token service requests with posted messages received by the registered event listener. If a client has no need to keep track of token requests and match them to received messages, it can use a dummy value for the parameter, e.g., `messageId=1`.

#### 2.2.4. Example token requests and responses

The simplest token request comes from a non-browser client that can send cookies across domains:

``` none
GET /iiif/token HTTP/1.1
Cookie: <cookie-acquired-during-login>
```
{: .urltemplate}

The response is the JSON token object:

``` json-doc
{
  "accessToken": "TOKEN_HERE",
  "tokenType": "Bearer",
  "expiresIn": 3600
}
```

If an authorization code was obtained using the client identity service, described below, then this _MUST_ be passed to the access token service as well.  The authorization code is passed to the access token service as the value of a query parameter called `code`. An example URL:

``` none
https://authentication.example.org/token?code=AUTH_CODE_HERE
```
{: .urltemplate}

For browser-based clients, the exact implementation will vary but _MUST_ include features equivalent to the following steps.

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
It can then open the token service in an iFrame:

```javascript
document.getElementById('messageFrame').src = 'https://authentication.example.org/token?messageId=1234';
```

The server response will then be a web page that can post a message to the registered listener:

```html
<html>
<body>
<script>    
    (window.opener || window.parent).postMessage({
        "messageId": "1234",
        "accessToken": "TOKEN_HERE",
        "tokenType": "Bearer",
        "expiresIn": 3600
    }, '*');    
</script>
</body>
</html>
```

__TODO:__ 
We need to explain here why '\*' is an acceptable value for origin when the token is a proxy credential for the cookie, and never accepted as a credential for a resource that is valuable in its own right. That is, '\*' is OK if we're protecting image content resources, but not necessarily OK if we're acquiring a token for CRUD operations on annotations. Although postMessage solves injection problems, some of [these comments][tmp-impl-sec] still apply. This is where a "postMessage preflight" could establish trust (possibly including a message during the login step as well) to allow the server to use an explicit (trusted) domain in the postMessage call.
This is not required for 1.0 when it covers description resources that describe cookie-protected content, but needs to extend to annos later.
{: .warning}


#### 2.2.5. Using the token

The token is sent on all subsequent requests for Description Resources. For example, a request for the image information in the Image API would look like:

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

The response from the client identity service or the access token service may be an error. The error _MUST_ be supplied as JSON with the following template. For browser-based clients using postMessage, the error object must be sent to the client via script, in the same way as the token is sent. For direct requests the response body is the raw JSON.

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

After receiving the response, the client will have a URL for a login service where the user can authenticate.  The client _MUST_ present this URL to the user in a separate tab or window with a URL bar, not in an iFrame or otherwise imported into the client user interface, in order to help prevent spoofing attacks.

After the authentication process has taken place, the login service _MUST_ ensure that the client has a cookie that identifies the user and will be visible to the access token service. It _SHOULD_ also contain JavaScript to try and automatically close the tab or window. The tab or window closing is the trigger for the client to request the access token for the user.

### 3.4. Step 4: Obtain Access Token

The client requests an access token from the access token service. If [step 2](#step-2-obtain-client-authorization-code-optional) was performed, the client authorization code _MUST_ also be sent.  The access token _MUST_ be added by the client to all future requests for Description Resources that have the same access token service, by including it in an `Authorization` header.

The server _MUST_ ensure that the client has a cookie which _MUST_ be included in requests for Content Resources, such as images or video.

If the access token service responds with an error condition, the client _SHOULD_ allow the user to attempt to login again.

### 3.5. Step 5: Re-request Description Resource

Now with the access token added in the `Authorization` header, the client retries the request for the Description Resource to determine whether the user is now successfully authenticated and authorized. Clients _SHOULD_ store the URIs of login services that have been accessed by the user and not prompt the user to login again when they are already authenticated.

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

The client first requests the desired Description Resource (1).  If the response is a 200 with the expected information, the client does not need to authenticate and should proceed to use the resource as expected (2).  If not, and the response is a 302 redirect, then the client follows the redirect to retrieve a new resource (3).  If the client has seen that resource already, by comparing its URI with those in a list of seen URIs, then the user is not authorized to access the requested version, and it should use the degraded version from the current response (4).  Otherwise, if it has not seen the response before, or the initial response is a 401 status with a link to the service (5), the client follows the link to the login service in a newly created tab or window (6) and records that it has seen the URI.  The user must then attempt to authenticate using the service (7), and the client waits until the tab or window is closed, either automatically or manually by the user.  Once the tab or window is closed, the client retrieves an access token for the user and retries the request for the original Description Resource (8), and proceeds back to make the same tests.  Finally, if the client receives a 403 response from the server, the user cannot gain authorization to interact with the resource and there is no degraded version available, and hence the client should not render anything beyond an error message.

## Appendices

### A. Implementation Notes

 * Care is required to implement this specification in a way that does not expose credentials thus compromising the security of the resources intended to be protected, or other resources within the same security domain.
 * Services using authentication should use HTTPS, and thus clients should also be run from pages served via HTTPS.
 * Implementations must not reuse the access cookie value as the access token value, as it could be copied across domains when the access token is obtained from a malicious client.


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
[tmp-impl-sec]: http://auth_notes.iiif.io/api/auth/0.9/implementation/#security-for-server-implementors
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


{% include acronyms.md %}
