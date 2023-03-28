---
title: "IIIF Authorization Flow API 2.0"
title_override: "IIIF Authorization Flow API 2.0"
id: auth-api
layout: spec
tags: [specifications, auth-api]
major: 2
minor: 0
patch: 0
pre: alpha
cssversion: 2
redirect_from:
  - /auth/2/index.html
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
    orcid: https://orcid.org/0000-0002-8411-2952
    institution: OCLC
  - name: Robert Sanderson
    ORCID: https://orcid.org/0000-0003-4441-6852
    institution: Yale University
  - name: Simeon Warner
    ORCID: https://orcid.org/0000-0002-7970-7855
    institution: Cornell University
hero:
  image: ''
---

## Status of this Document
{:.no_toc}

__This Version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest Stable Version:__ [{{ site.data.apis.auth.latest.major }}.{{ site.data.apis.auth.latest.minor }}.{{ site.data.apis.auth.latest.patch }}][auth-stable-version]

__Previous Version:__ [1.0.0][auth1]

**Editors:**

{% include api/editors.md editors=page.editors %}

{% include copyright2015.md %}

----

## 1. Introduction
{: #introduction}

The IIIF (pronounced "Triple-Eye-Eff") specifications are designed to support uniform and rich access to images, audio, video and other resources hosted around the world. Open access to content is desirable, but internal policies, sensitive material, legal regulations, business models, and other constraints can require users to authenticate and be authorized to interact with some resources. The authentication process could range from a simple restriction by IP address or a click-through agreement, to a multi-factor scheme with a secure identity provider.

Providing interoperable access to restricted content through client applications running in a web browser poses many challenges:

* A single IIIF Presentation API Manifest can reference content resources at multiple institutions and hence from multiple domains.
* Each version of a resource must have a distinct URI to prevent web caches from providing the wrong version.
* Institutions have different existing access control systems.
* Most IIIF viewers are browser-based JavaScript applications, and may be served from a domain that is different from, and unknown to, the domain hosting the content it is required to load.
* Content resources are typically loaded indirectly by HTML elements like `<img />`, `<audio />` and `<video />`. While authentication protocols like [OAuth2][oauth2] serve the needs of identified, trusted clients making direct HTTP requests for API resources, they do not serve the HTML element case.

Additionally, the IIIF community has the following goals for this specification:

* A IIIF client should not accept credentials and authenticate the user itself and should have no access to this information.
* The user cannot be redirected away from the client in order to authenticate. In order to maintain state, the client must be able to stay running while the user interacts with an access control system in another tab.
* A registry of trusted IIIF client domains should not be required. Anyone should be able to create any kind of viewer and run it from anywhere.
* Institutions should be able to work with their existing authentication systems without modifying them.
* It should be possible to offer tiered access to substitute versions instead of simple all-or-nothing access. These substitute versions could be of lower quality based on resolution, watermarking, or compression.

To meet these challenges and goals, this specification describes services that allow the client to guide the user through existing access control systems. The process of authenticating and authorizing the user is outside the scope of this specification and may involve a round-trip to a CAS server, or an OAuth2 provider, or a bespoke login system. In this sense, the IIIF Authorization Flow API is not a protocol like OAuth2; it is a pattern for interacting with arbitrary third party protocols. The patterns established by this specification act as a bridge to the access control systems without the client requiring knowledge of those systems.

In summary, this specification describes how to:

* From within a client application such as a viewer, initiate an interaction with an access control system so that a user can acquire any credentials they need to view restricted content.
* Give the client application just enough knowledge of the user's state with respect to the content provider to ensure a good user experience: that is, allow the client to learn whether the user currently has access to a resource, without needing to know anything about how they are authorized.


### 1.1. Terminology
{: #terminology}

This specification distinguishes between two types of resource:

* __IIIF API resources__: the Manifests, Collections and other resources described by the IIIF [Presentation API][prezi-api], including external Annotation Pages, and the [image information][image30-information] document (info.json) provided by the [IIIF Image API][image-api]. These resources are typically loaded directly by JavaScript using the `fetch` API or `XMLHttpRequest` interface.
* __Access-controlled resources__: images, videos, PDFs and other resources that are linked from IIIF Manifests, Annotation Pages and other IIIF API resources. This includes image responses (e.g., tiles for deep zoom) from the [IIIF Image API][image-api]. These resources are typically loaded indirectly via browser interpretation of HTML elements.

This specification uses the following terms:

* __Authorizing aspect__: the aspect of the request that a content provider uses to authorize a request for a content resource. This is often a cookie used as a credential, but can be another aspect of the request, such as the IP address.
* __Access token__: a proxy for the authorizing aspect of the request. An access token can be seen by a IIIF client without revealing to the client what the authorizing aspect is.

The terms _array_, _JSON object_, _number_, and _string_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].


### 1.2. Common Specification Features
{: #common}

All IIIF specifications share common features to ensure consistency across the IIIF ecosystem. These features are documented in the [Presentation API][prezi3-considerations] and are foundational to this specification. Common principles for the design of the specifications are documented in the [IIIF Design Principles][annex-patterns].


## 2. Authorization Flow Services
{: #authorization-flow-services}

This specification defines four services to support authorization flows:

* The __access service__, a user interface presented by the content provider and opened by the client in a new tab (typically the content provider's login page).
* The __token service__ from which the client obtains an access token. The client needs to present to the token service the same authorizing aspect that the browser will present to the corresponding access-controlled resource.
* The __probe service__, an endpoint defined by this specification that the client uses to learn about the user's relationship to the access-controlled resource the probe service is for. An access-controlled Content Resource has a probe service. An [image information][image30-information] document (info.json) also has a probe service, if the image responses it produces are access-controlled.
* The __logout service__, an optional service for logging out.

The purpose of this specification is to support access control for IIIF resources and hence security is a core concern. To prevent misuse, cookies and bearer tokens described in this specification need to be protected from disclosure in storage and in transport. Implementations _MUST_ use [HTTP over TLS][org-rfc-2818], commonly known as HTTPS, for all communication. Furthermore, all IIIF clients that interact with access-controlled resources _SHOULD_ also be run from pages served via HTTPS. All references to HTTP in this specification should be read assuming the use of HTTPS.

This specification protects resources such as images by making the access token value available to the script of the client application, for use in requesting a probe service. Knowledge of the access token is of no value to a malicious client, because (for example) the access _cookie_ (which the client cannot see) is the credential accepted for Content Resources.


### 2.1. Declaring Services
{: declaring-services}

Authorization flow services are declared in IIIF API resources using the `service` property, defined by the [Presentation API][prezi3-service] as an array of JSON objects. The probe service is declared in the `service` property of an access-controlled resource. The access service is declared in the `service` property of the probe service. The token and logout services are declared in the `service` property of the access service.

For content resources such as audio, video, PDFs and other documents, the probe service is present in a IIIF Manifest or other IIIF API Resource. For IIIF Image API services, the probe service _MUST_ be declared in the Image Information Document (info.json) and _MAY_ additionally be declared in the Manifest with the image service.

An example access-controlled resource with authorization flow services:

{% include api/code_header.html %}
```json
{
   "id": "https://auth.example.org/my-video.mp4",
   "type": "Video",
   "service": [
     {
       "id": "https://auth.example.org/probe/my-video",
       "type": "AuthProbeService2",
       "service" : [
        {
          "id": "https://auth.example.org/login",
          "type": "AuthAccessService2",
          "profile": "active",
          "label": { "en": [ "Login to Example Institution" ] },
          "service" : [
            {
              "id": "https://auth.example.org/token",
              "type": "AuthAccessTokenService2"
            },
            {
              "id": "https://auth.example.org/logout",
              "type": "AuthLogoutService2",
              "label": { "en": [ "Logout from Example Institution" ] }
            }
          ]
        }
       ]
      }
   ]
}
```

If the access service is embedded within an Image API 3.0 service, or a Presentation API 3.0 resource, the `@context` key _SHOULD NOT_ be present within the service. Instead the value `http://iiif.io/api/auth/{{ page.major }}/context.json` _MUST_ be included in the list of values for `@context` at the beginning of that Image service or Presentation API resource. It _MUST_ come before the Image or Presentation API context value. See the section [Linked Data Context and Extensions][prezi30-ldce] in the Presentation API.


### 2.2. Simple Authorization Flow
{: #simple-authorization-flow}

This section illustrates the use of these services in a successful authorization flow.

A user wishes to see an access-controlled resource such as an image, video, PDF, or image service tiles for deep zoom. The client recognizes from the above JSON structure in the Manifest or info.json that the resource has authorization flow services, and determines that the user will have to authenticate. The client then progresses through a series of interactions with these services:
1. The client opens the content provider's access service in a new tab.  In a typical case, the user logs in and the access service sets a cookie for use by the access token service. The tab closes.
2. The client detects that the access service tab has closed and makes a request to the access token service.  The access token service evaluates the cookie or other authorizing aspect of the request and returns an access token.
3. The client sends the access token to the probe service.  The probe service indicates that the request for the access-controlled resource would succeed.  The client renders the access-controlled resource.
4. Later, the user logs out.

<table class="ex_table">
  <tbody>
    <tr>
      <td>
        <img src="{{ site.api_url | absolute_url }}/assets/images/auth2-sequence.png" alt="Authorization Flow Service Interactions diagram" class="fullPct" />
        <p><strong>1</strong> Client Interactions With Authorization Flow Services </p>
      </td>
    </tr>
  </tbody>
</table>

## 3. Access Service
{: #access-service}

The access service either grants the authorizing aspect or determines whether the user already has that aspect. The client obtains the link to an access service from a service description in a probe service, then opens that URI in a new browser tab. The user interacts with the access service in the opened tab while the client waits until it detects that the opened tab has closed. The client then continues with the authorization flow to determine whether the authorizing aspect is present.

The client has no knowledge of the user's interactions in the opened tab, such as any cookies set, or redirects that happened. The final response in the opened tab _SHOULD_ contain JavaScript that will attempt to close the tab, in order to trigger the next step in the workflow.

The access service is not required to set a cookie, as the authorizing aspect may be an ambient aspect of the request such as IP address, user-agent, or even the time of day. In some scenarios, what happens at the access service may have no effect on subsequent steps, but the client does not know this and should always follow the same flow.

There are three different interaction patterns based on the user interface that must be rendered for the user. The different patterns are indicated by the `profile` property given in the service description.


### 3.1. Access Service Description
{: #access-service-description}

The service description is included in the IIIF API Resource and has the following technical properties:

| Property    | Required?  | Description |
| ----------- | ---------- | ----------- |
| `id`        | _see description_ | The URI of the access service. |
| `type`      | _REQUIRED_ | The value _MUST_ be the string `AuthAccessService2`. |
| `profile`   | _REQUIRED_ | The profile for the service _MUST_ be one of the profile values from the table below.|
| `service`   | _REQUIRED_ | References to access token and other related services, described below.|

#### id

The URI of the access service that the client opens in a new tab. The `id` property _MUST_ be present if the `profile` property is `active` or `kiosk`. The value _MUST_ be a string containing the HTTPS URI of the service.

If the profile property is `external`, the `id` property _SHOULD NOT_ be present, and any value _MUST_ be ignored.

```json-doc
{ "id": "https://auth.example.org/login" }
```

#### type

The type of the service. The `type` property _MUST_ be present in the JSON, and the value _MUST_ be the string `AuthAccessService2`.

```json-doc
{ "type": "AuthAccessService2" }
```

#### profile

There are three interaction patterns by which the client can use the access service, each identified by a different value of the `profile` property. These patterns are described in more detail in the following sections.

| Value of `profile` | Description |
|------------------- | ----------- |
|`active`            | The user will be required to visit the user interface of an external authentication system. |
|`kiosk`             | The user will not be required to interact with an authentication system, the client is expected to use the access service automatically. |
|`external`          | The user is expected to have already acquired the authorizing aspect, and no access service will be used. |
{: .api-table .first-col-normal }

The `active` profile requires additional properties in the service description, defined in the [Active Interaction Pattern][auth20-active-interaction-pattern] section below.

```json-doc
{ "profile": "active" }
```

#### service

The value _MUST_ be an array of JSON objects. Each object _MUST_ have the `id` and `type` properties. The `service` array _MUST_ contain exactly one [access token service][auth20-access-token-service] and _MAY_ contain a [logout service][auth20-logout-service].

```json-doc
"service" : [
  {
    "id": "https://auth.example.org/token",
    "type": "AuthAccessTokenService2"
  },
  {
    "id": "https://auth.example.org/logout",
    "type": "AuthLogoutService2",
    "label": { "en": [ "Logout from Example Institution" ] }
  }
]
```

### 3.2. Client Interaction with Access Services
{: #interaction-with-access-services}

The client _MUST_ append the following query parameter to all requests to an access service URI, regardless of the interaction pattern, and open this URI in a new window or tab.

| Parameter | Description |
| --------- | ----------- |
| `origin`  | A string containing the origin of the page in the window, consisting of a protocol, hostname and optionally port number, as described in the [postMessage API][org-mozilla-postmessage] specification. |
{: .api-table}

For example, given an access service URI of `https://auth.example.org/login`, a client instantiated by the page `https://client.example.org/viewer/index.html` would make its request to:

{% include api/code_header.html %}
```
https://auth.example.org/login?origin=https://client.example.org/
```

The server _MAY_ use this information to validate the origin supplied in subsequent requests to the access token service.

### 3.3. Interaction Patterns

There are three distinct interaction patterns, identified by the `profile` property. These enable different styles of user, client and server interaction.

#### 3.3.1 Active Interaction Pattern
{: #active-interaction-pattern}

This pattern requires the user to interact in the opened tab. Typical scenarios are:

* The user interface presents a login process, in which the user provides credentials to the content provider and the content provider sets an access cookie.
* The user interface presents a usage agreement, a content advisory notice, or some other form of clickthrough interaction in which credentials are not required, but deliberate confirmation of terms is required, to set an access cookie.
* The access service stores the result of a user interaction in browser local storage, which is later available to the token service.

To support these user-facing interactions, the access service description for the `active` profile includes the following additional descriptive properties for constructing a user interface in the client:

| Property       | Required?     | Description |
| -------------- | ------------- | ----------- |
| `label`        | _REQUIRED_    | The name of the access service. |
| `heading`      | _RECOMMENDED_ | Heading text to be shown with the user interface element that opens the access service. |
| `note`         | _RECOMMENDED_ | Additional text to be shown with the user interface element that opens the access service. |
| `confirmLabel` | _RECOMMENDED_ | The label for the user interface element that opens the access service. |
{: .api-table}


#### label

The text to be shown to the user to initiate the loading of the access service. The value _MUST_ clearly indicate the domain or institution to which the user is authenticating. The value of the property _MUST_ be a JSON object as described in the [Language of Property Values][prezi3-languages] section of the Presentation API.

```json-doc
{ "label": { "en": [ "Login to Example Institution" ] } }
```

#### confirmLabel

The text to be shown to the user on the button or element that triggers opening of the access service. If not present, the client supplies text appropriate to the interaction pattern if needed. The value of the property _MUST_ be a JSON object as described in the [Language of Property Values][prezi3-languages] section of the Presentation API.


```json-doc
{ "confirmLabel": { "en": [ "Login" ] } }
```

#### heading

Heading text to be shown with the user interface element that opens the access service. If present, it _MUST_ be shown to the user. The value of the property _MUST_ be a JSON object as described in the [Language of Property Values][prezi3-languages] section of the Presentation API.

```json-doc
{ "heading": { "en": [ "Please Log In" ] } }
```


#### note

Additional text to be shown with the user interface element that opens the access service. If present, it _MUST_ be shown to the user. The value of the property _MUST_ be a JSON object as described in the [Language of Property Values][prezi3-languages] section of the Presentation API.

```json-doc
{ "note": { "en": [ "Example Institution requires that you log in with your example account to view this content." ] }
```

#### Complete Service Description

An example service description for the `active` interaction pattern:

{% include api/code_header.html %}
``` json
{
  // ...
  "service" : {
    "id": "https://auth.example.org/login",
    "type": "AuthAccessService2",
    "profile": "active",
    "label": { "en": [ "Login to Example Institution" ] },
    "heading": { "en": [ "Please Log In" ] },
    "note": { "en": [ "Example Institution requires that you log in with your example account to view this content." ] },
    "confirmLabel": { "en": [ "Login" ] },
    "service": [
      // Access token and Logout services ...
    ]
  }
}
```

##### 3.3.1.1. Active Pattern Interaction

The interaction has the following steps:

* If the `heading` and/or `note` properties are present, before opening the access service URI, the client _MUST_ display the values of the properties to the user. The properties will describe what is about to happen when they click the element with the `confirmLabel`.
* When the `confirmLabel` element is activated, the client _MUST_ then open the URI from `id` with the added `origin` query parameter. This _MUST_ be done in a new window or tab to help prevent spoofing attacks. Browser security rules prevent the client from knowing what is happening in the new tab, therefore the client can only wait for and detect the closing of the opened tab.
* After the opened tab is closed, the client _MUST_ then use the related access token service, as described below.

At the time of writing, browsers will only send cookies to third party domains when the user has performed a _user gesture_ at that domain. For more information see [Appendix A][auth20-user-interaction-at-access-service].

#### 3.3.2. Kiosk Interaction Pattern
{: #kiosk-interaction-pattern}

This pattern requires no user interaction in the opened tab. This pattern supports exhibitions, in-gallery interactives and other IIIF user experiences on managed devices that are configured in advance.

For the `kiosk` pattern the interaction has the following steps:

* There is no user interaction before opening the Access Service URI.
* The client _MUST_ immediately open the URI from `id` with the added `origin` query parameter. This _MUST_ be done in a new window or tab.
* After the opened window or tab is closed, the client _MUST_ then use the related access token service, as described below.

Non-user-driven clients simply access the URI from `id` to obtain any access cookie, and then use the related access token service, as described below.

__Warning__<br/>
If the content resources and access service are on a different origin from the client, and the authorization is based on an access cookie, the `kiosk` pattern will likely fail unless the user has recently interacted with the access service origin in a first party context as described in [Appendix A][auth20-user-interaction-at-access-service].
{: .alert}

An example service description for the `kiosk` pattern:

{% include api/code_header.html %}
``` json-doc
{
  // ...
  "service" : {
    "id": "https://auth.example.org/cookiebaker",
    "type": "AuthAccessService2",
    "profile": "kiosk",
    "service": {
      // Access token service ...
    }
  }
}
```

#### 3.3.3. External Interaction Pattern
{: #external-interaction-pattern}

This pattern involves no user interaction with an access service. Typical scenarios are:

* Clients are authorized by ambient aspects of the request such as IP address or user-agent.
* Avoiding displaying unnecessary login prompts to users who are already logged in some out-of-band interaction such as a normal login outside the scope of this specification.
* This pattern can be used instead of the kiosk pattern when the managed devices have an ambient authorizing aspect of the request (e.g., a particular IP range for in-gallery devices).

The interaction has the following steps:

* There is no access service. Any URI specified in the `id` property _MUST_ be ignored.
* The client _MUST_ immediately use the related access token service, as described below.

__Warning__<br/>
If the content resources and token service are on a different origin from the client, and the authorization is based on an access cookie, the `external` pattern will likely fail unless the user has recently interacted with the token service origin in a first party context as described in [Appendix A][auth20-user-interaction-at-access-service].
{: .alert}

An example service description for the `external` pattern:

{% include api/code_header.html %}
``` json-doc
{
  // ...
  "service" : {
    "type": "AuthAccessService2",
    "profile": "external",
    "label": { "en": [ "External Authentication Required" ] },
    "service": {
      // Access token service ...
    }
  }
}
```

## 4. Access Token Service
{: #access-token-service}

The access token service is used by the client to obtain an access token, which it then sends to a probe service.

The access token service URI is opened by setting the `src` property of an `<iframe />` HTML element and waiting for a message from that frame, as described in the [Access Token Service Request][auth20-access-token-service-request] section. This approach is necessary because the access token service needs to be presented with the same authorizing aspect that browser-initiated requests will present to the corresponding access-controlled resource.

### 4.1. Access Token Service Description
{: #access-token-service-description}

The access token service _MUST_ be included in the `service` property of the access service it is associated with, and the client uses that access token service after the user interacts with the parent access service. It has the following properties:

| Property       | Required?  | Description |
| -------------- | ---------- | ----------- |
| `id`           | _see description_ | The URI of the access token service. |
| `type`         | _REQUIRED_ | The value _MUST_ be the string `AuthAccessTokenService2`. |
| `errorHeading` | _OPTIONAL_ | Default heading text to render if an error occurs. |
| `errorNote`    | _OPTIONAL_ | Default additional text to render if an error occurs. |

#### id

The URI of the access token service that the client opens in a frame. The `id` property _MUST_ be present. The value _MUST_ be a string containing the HTTPS URI of the service.

#### type

The type of the service. The `type` property _MUST_ be present in the JSON, and the value _MUST_ be the string `AuthAccessTokenService2`.

#### errorHeading

Default heading text to render if an error occurs. If the access token service returns an [error object][auth20-access-token-error-format], the `heading` property of the error object _MUST_ be used instead if supplied.

#### errorNote

Default additional text to render if an error occurs. If the access token service returns an [error object][auth20-access-token-error-format], the `note` property of the error object _MUST_ be used instead if supplied. If present, `errorHeading` _MUST_ also be present.

#### Example Service Description

{% include api/code_header.html %}
``` json
{
  // Probe Service
  {
    "id": "https://auth.example.org/probe",
    "type": "AuthProbeService2",
    "service": [
      {
        // Access Service
        "service" : [
          {
            "id": "https://auth.example.org/login",
            "type": "AuthAccessService2",
            "profile": "active",
            "label": { "en": [ "Login to Example Institution" ] },
            // ... other recommended strings for user interface

            // Access Token Service
            "service": [
              {
                "id": "https://auth.example.org/token",
                "type": "AuthAccessTokenService2",
                "errorHeading": { "en": [ "Something went wrong" ] },
                "errorNote": { "en": [ "Could not get a token." ] },
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### 4.2. Access Token Service Request
{: #access-token-service-request}

If the client is a JavaScript application running in a web browser, it needs to make a request for the access token and store the result. The client can't use `XMLHttpRequest` or `fetch` because it can't include any access cookie in a cross-domain request. Such `fetch` requests do not have the same security context as requests made by the browser interpreting `src` attributes on HTML media elements. Instead, the client _MUST_ open the access token service in a frame using an `<iframe />` element and be ready to receive a message posted by a script in that frame using the [postMessage API][org-mozilla-postmessage].

To trigger this behavior, the client _MUST_ append the following query parameters to the access token service URI, and open this new URI in the frame:

| Parameter   | Description |
| ----------- | ----------- |
| `messageId` | Used by the client to correlate the token service requests it makes with the messages received from the postMessage frame. The value _MUST_ be a string. |
| `origin`    | A string containing the origin of the page in the window, consisting of a protocol, hostname and optionally port number, as described in the [postMessage API][org-mozilla-postmessage] specification. |
{: .api-table}

For example, a client instantiated by the page at `https://client.example.org/viewer/index.html` would request:

{% include api/code_header.html %}
```
https://auth.example.org/token?messageId=ae3415&origin=https://client.example.org
```

The frame _SHOULD NOT_ be shown to the user. It is a mechanism for cross-domain messaging. The client _MUST_ register an event listener to receive the message that the access token service page in the frame will send. The client can reuse the same listener and frame for multiple calls to the access token service, or it can create new ones for each invocation.

The exact implementation may vary but _MUST_ include features equivalent to the following steps.

The client must first register an event listener to receive a cross domain message:

{% include api/code_header.html %}
``` javascript
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

{% include api/code_header.html %}
``` javascript
document.getElementById('messageFrame').src =
  'https://auth.example.org/token?messageId=ae3415&origin=https://client.example.org';
```


### 4.3. Access Token Service Response

When the server receives a request for the access token service, it _MUST_ respond with an HTML web page. The web page _MUST_ contain a script that sends a message to the opening page using the postMessage API. The message body will be a JSON object that either provides an access token or describes an error condition. These are specified in the [Access Token Message Format][auth20-access-token-message-format] and [Access Token Error Format][auth20-access-token-error-format] sections respectively. The postMessage web page response _MUST_ use the 200 HTTP status code to ensure that the body is received by the client correctly.

The server _MAY_ use the `origin` provided in the request for further authorization logic, even though the user is already authenticated. If the client sends an incorrect `origin` value, it will not receive the posted message, as the postMessage API will not dispatch the event. The `targetOrigin` parameter of the `postMessage()` function call _MUST_ be the same `origin` value.

Example access token response:

{% include api/code_header.html %}
``` html
<html>
<body>
<script>
    window.parent.postMessage(
      {
        "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
        "type": "AuthAccessToken2",
        "accessToken": "ddc76e416e3804e2369e6c9cee806f5e438a5cdc",
        "expiresIn": 300,
        "messageId": "ae3415"
      },
      'https://client.example.org'
    );
</script>
</body>
</html>
```

### 4.4. Access Token Message Format
{: #access-token-message-format}

If the request presents the required authorizing aspect, the access token message returned via postMessage _MUST_ be a JSON-LD object with the following properties:

| Property       | Required?  | Description                                                                              |
| -------------- | ---------- | ---------------------------------------------------------------------------------------- |
| `@context`     | _REQUIRED_ | The URI of the context document, `http://iiif.io/api/auth/{{ page.major }}/context.json` |
| `type`         | _REQUIRED_ | The value _MUST_ be the string `AuthAccessToken2`.                                       |
| `messageId`    | _REQUIRED_ | The message identifier supplied by the client.                                           |
| `accessToken`  | _REQUIRED_ | The access token to be sent to the probe service.                                        |
| `expiresIn`    | _OPTIONAL_ | The number of seconds until the token ceases to be valid.                                |


#### messageId

The `messageId` property _MUST_ be present, and the value _MUST_ be the value originally sent in the `messageId` query parameter when the token service was requested. The value _MUST_ be a string. Clients _MUST_ ignore messages with `messageId` values that they do not recognize.

```json-doc
{ "messageId": "ae3415"}
```

#### accessToken

The value is the access token to be sent to the probe service. The value _MUST_ be a string. Once obtained, the access token _MUST_ be included with all future requests for the parent [probe service][auth20-probe-service].

The access token _MUST NOT_ be sent anywhere else. Access tokens _SHOULD_ have limited lifetimes, whether the `expiresIn` property is provided or not.

```json-doc
{ "accessToken": "ddc76e416e3804e2369e6c9cee806f5e438a5cdc" }
```

__Warning__<br/>
Any client can see this access token. The access token must not contain any sensitive information. It should be an opaque string different from any cookie value or other credential. For example, using an access cookie value as the access token value would allow an attacker to construct a cookie with the same content as the token and gain access to resources.
{: .alert}

#### expiresIn

The `expiresIn` property _MAY_ be present. Its value _MUST_ be a positive integer and is the number of seconds until the token ceases to be valid.

```json-doc
{ "expiresIn": 300 }
```

#### Example Access Token Message Body

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
  "type": "AuthAccessToken2",
  "accessToken": "ddc76e416e3804e2369e6c9cee806f5e438a5cdc",
  "expiresIn": 300,
  "messageId": "ae3415"
}
```


### 4.5. Access Token Error Format
{: #access-token-error-format}

If the request does not present the required authorizing aspect, the access token message returned via postMessage _MUST_ be a JSON-LD object with the following properties:

| Property    | Required?     | Description                                                                              |
| ----------- | ------------- | ---------------------------------------------------------------------------------------- |
| `@context`  | _REQUIRED_    | The URI of the context document, `http://iiif.io/api/auth/{{ page.major }}/context.json` |
| `type`      | _REQUIRED_    | The value _MUST_ be the string `AuthAccessTokenError2`.                                  |
| `profile`   | _REQUIRED_    | The specific type of error.                                                              |
| `messageId` | _REQUIRED_    | The message identifier supplied by the client.                                           |
| `heading`   | _OPTIONAL_    | Heading text to render with the user interface element that conveys the error.           |
| `note`      | _OPTIONAL_    | Additional text to render with the user interface element that conveys the error.        |

#### profile

The `profile` property classifies the error and _MUST_ have one of the values in the following table:

| Value            | Description |
| ---------------- | ----------- |
| `invalidRequest` | The service could not process the access token request. |
| `invalidOrigin`  | The request came from a different origin than that specified in the access service request, or an origin that the server rejects for other reasons. |
| `missingAspect`  | The access token request did not have the required authorizing aspect. |
| `invalidAspect`  | The access token request had the aspect used for authorization but it was not valid. |
| `expiredAspect`  | The request had credentials that are no longer valid for the service.  |
| `unavailable`    | The request could not be fulfilled for reasons other than those listed above, such as scheduled maintenance. |
{: .api-table}

#### messageId

The `messageId` property _MUST_ be present, and the value _MUST_ be the value originally sent in the `messageId` query parameter when the token service was requested. The value _MUST_ be a string. Clients _MUST_ ignore messages with `messageId` values that they do not recognize.

#### heading

Heading text to render with the user interface element that conveys the error. If present, it _SHOULD_ be shown to the user if the client can't recover from the error without user interaction. The value of the property _MUST_ be a JSON object as described in the [Language of Property Values][prezi3-languages] section of the Presentation API.

#### note

Additional human-readable information about the error to render with the user interface element that conveys the error. If present, it _SHOULD_ be shown to the user if the client can't recover from the error without user interaction. The value of the property _MUST_ be a JSON object as described in the [Language of Property Values][prezi3-languages] section of the Presentation API. If present, `heading` _MUST_ also be present.


#### Example Access Token Error Response

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
  "type": "AuthAccessTokenError2",
  "profile": "missingAspect",
  "heading": { "en": [ "Unauthorized" ] },
  "note": { "en": [ "Call Bob at ext. 1234 to refill the cookie jar" ] },
  "messageId": "ae3415"
}
```

## 5. Probe Service
{: #probe-service}

The probe service is used by the client to understand whether the user has access to the access-controlled resource for which the probe service is declared. The client sends the token obtained from the corresponding access token service to the probe service.

### 5.1. Probe Service Description

| Property       | Required?  | Description |
| -------------- | ---------- | ----------- |
| `id`           | _REQUIRED_ | The URI of the probe service. |
| `type`         | _REQUIRED_ | The value _MUST_ be the string `AuthProbeService2`. |
| `errorHeading` | _OPTIONAL_ | Default heading text to render if the probe indicates the user cannot access the resource. |
| `errorNote`    | _OPTIONAL_ | Default additional text to render if the probe indicates the user cannot access the resource. |

#### id

The URI of the probe service. The `id` property _MUST_ be present. The value _MUST_ be a string containing the HTTPS URI of the service.

#### type

The type of the service. The `type` property _MUST_ be present in the JSON, and the value _MUST_ be the string `AuthProbeService2`.

#### errorHeading

Default heading text to render if the probe indicates the user cannot access the resource. If the probe response `status` property indicates access would not be granted, the `heading` property of the probe response _MUST_ be used instead if supplied.

#### errorNote

Default additional text to render if the probe indicates the user cannot access the resource. If the probe response `status` property indicates access would not be granted, the `note` property of the probe response _MUST_ be used instead if supplied. If present, `errorHeading` _MUST_ also be present.


### 5.1. Probe Service Request

The client passes the access token to the probe service using the `Authorization` HTTP request header and the [bearer token][org-rfc-6570-1-2] pattern. The header value is the string `Bearer` followed by a space and the access token, for example:

{% include api/code_header.html %}

```
Authorization: Bearer ddc76e416e3804e2369e6c9cee806f5e438a5cdc
```

### 5.2. Probe Service Response

The response from the probe service is a JSON-LD object with the following properties:

| Name          | Required?  | Description |
| ------------- | ---------  | ----------- |
| `@context`    | _REQUIRED_ | The URI of the context document, `http://iiif.io/api/auth/{{ page.major }}/context.json`. |
| `type`        | _REQUIRED_ | The type of the service, `AuthProbeResult2`. |
| `status`      | _REQUIRED_ | The HTTP status code that would be returned for the access-controlled resource. |
| `substitute`   | _OPTIONAL_ | A reference to one or more substitute resources, such as watermarked or other less preferable versions. |
| `location`   | _OPTIONAL_  | If present, the client should request this resource instead of the the resource the probe service was declared for. |
| `heading`      | _OPTIONAL_ | heading text for the error UI |
| `note` | _OPTIONAL_ | Block text for the error UI |
{: .api-table .first-col-normal }

#### type

The type of the probe result. The `type` property _MUST_ be present in the JSON, and the value _MUST_ be the string `AuthProbeResult2`.

#### status

The HTTP status code that the client should expect to receive if it were to issue the same request to the resource as it has just issued to the probe service. Note well that the HTTP status code of the response itself _MUST_ be 200. The `status` property _MUST_ be present in the JSON, and the value _MUST_ be an integer drawn from the list of [HTTP status codes][org-rfc-7231-status].

```json
{
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "type": "AuthProbeResult2",
    "status": 200
}
```

#### substitute
{: #substitute}

A list of alternate resources that a client _MAY_ use instead of the access-controlled resource if the user is not authorized to retrieve that resource. The `substitute` property _MAY_ be present in the JSON if the value of the `status` property indicates that access to the access-controlled resource would be denied, and _MUST NOT_ be present otherwise. The value _MUST_ be an array of JSON objects, each of which describes an substitute resource.

If multiple substitute resources are available, clients _SHOULD_ allow the user to choose between them, using the `label` or other descriptive properties available on the resources.

Clients _SHOULD_ expect to encounter substitute resources with the following properties, however any property from the IIIF Presentation API that is valid for a content resource _MAY_ be present.

| Name      | Required?  | Description |
| --------- | ---------  | ----------- |
| `id`      | _REQUIRED_ | The URI of the substitute resource. |
| `type`    | _REQUIRED_ | The type of the substitute resource, which _SHOULD_ be the same as the access-controlled resource. |
| `label`   | _OPTIONAL_ | The name, title, or label to display to the user for the substitute resource. The value _MUST_ be a JSON object as described in the [Language of Property Values][prezi3-languages] section of the Presentation API. |
| `service` | _OPTIONAL_ | A list of services that apply to the substitute resource. |

When IIIF API resources refer to access-controlled resources with substitute resources, the access-controlled resource _SHOULD_ be the resource most users would prefer to see, typically the highest quality version. A substitute resource may declare new IIIF Authorization Flow services, including its own probe services, allowing for [tiered access][auth20-tiered-access]. If present, and no further IIIF Authorization Flow services are declared on it, a substitute resource _MUST_ be accessible to the user who requested the probe service.

```json
{
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "type": "AuthProbeResult2",
    "status": 401,
    "substitute": [{
      "id": "https://auth.example.org/my-video-lo-res.mp4",
      "type": "Video"
    }]
}
```

#### location

The location property describes a resource that the client _MUST_ request instead of the access-controlled resource. A probe response _MUST NOT_ provide a resource for `location` if the `status` is anything other than a `30x` redirect response. The value _MUST_ be a JSON object which describes this resource.

Clients _SHOULD_ expect to encounter a resource with the following properties, however any property from the IIIF Presentation API that is valid for a content resource _MAY_ be present.

| Name      | Required?  | Description |
| --------- | ---------  | ----------- |
| `id`      | _REQUIRED_ | The URI of the resource. |
| `type`    | _REQUIRED_ | The type of the resource, which _MUST_ be the same as the access-controlled resource. |
| `service` | _OPTIONAL_ | A list of services that apply to the resource. |

```json
{
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "type": "AuthProbeResult2",
    "status": 302,
    "location": {
      "id": "https://auth-cdn-2.example.org/my-video.m3u8",
      "type": "Video"
    }
}
```

#### heading

If the status code does not indicate success, the response _SHOULD_ include the `heading` property. This provides heading text to render with the user interface element that conveys the error. If present, it _SHOULD_ be shown to the user if the client can't recover from the error without user interaction. The value of the property _MUST_ be a JSON object as described in the [Language of Property Values][prezi3-languages] section of the Presentation API.

```json
{
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "type": "AuthProbeResult2",
    "status": 401,
    "heading":  { "en": [ "You can't see this" ] },
    "note": { "en": [ "Sorry" ] }
}
```

#### note

If the status code does not indicate success, the response _SHOULD_ include the `note` property. This provides additional human-readable information about the error to render with the user interface element that conveys the error. If present, it _SHOULD_ be shown to the user if the client can't recover from the error without user interaction. The value of the property _MUST_ be a JSON object as described in the [Language of Property Values][prezi3-languages] section of the Presentation API. If present, `heading` _MUST_ also be present.

## 6. Logout Service
{: #logout-service}

In the case of the `active` access service pattern, the client may need to know if and where the user can go to log out. For example, the user may wish to close their session on a public terminal, or to log in again with a different account.  If the authentication system supports users intentionally logging out, there _SHOULD_ be a logout service associated with the access service.

### 6.1. Logout Service Description
{: #logout-service-description}

| Property       | Required?  | Description                                          |
| -------------- |------------|------------------------------------------------------|
| `id`           | _REQUIRED_ | The URI of the logout service.                       |
| `type`         | _REQUIRED_ | The value _MUST_ be the string `AuthLogoutService2`. |
| `label`        | _REQUIRED_ | The name of the logout service.                      |

#### id

The URI of the logout service. The `id` property _MUST_ be present. The value _MUST_ be a string containing the HTTPS URI of the service.

#### type

The type of the service. The `type` property _MUST_ be present and the value _MUST_ be the string `AuthLogoutService2`.

#### label

The text to be shown to the user to initiate the interaction with the logout service. The `label` property _MUST_ be present. The value _MUST_ clearly indicate the domain or institution from which the user is logging out. The value of the property _MUST_ be a JSON object as described in the [Language of Property Values][prezi3-languages] section of the Presentation API.

```json-doc
{ "label": { "en": [ "Logout from Example Institution" ] } }
```

#### Example Service Description

{% include api/code_header.html %}
``` json-doc
{
  // ...
  "service" : {
    "@context": "http://iiif.io/api/auth/{{ page.major }}/context.json",
    "id": "https://auth.example.org/login",
    "type": "AuthAccessService2",
    "profile": "active",
    "label": { "en": [ "Login to Example Institution" ] },
    "service" : [
      {
        "id": "https://auth.example.org/token",
        "type": "AuthAccessTokenService2"
      },
      {
        "id": "https://auth.example.org/logout",
        "type": "AuthLogoutService2",
        "label": { "en": [ "Logout from Example Institution" ] }
      }
    ]
  }
}
```

### 6.2. Logout Interaction
{: #logout-interaction}

The client _SHOULD_ present the results of an HTTP `GET` request on the service's URI in a separate tab or window with an address bar. At the same time, the client _SHOULD_ discard any access token that it has received from the corresponding service. The server _SHOULD_ reset the user's logged in status when this request is made and delete any access cookie previously set.

If possible, the server _SHOULD_ invalidate any authorizing aspects it controls and any access tokens representing those aspects.

## 7. Workflow from the Browser Client Perspective
{: #workflow-from-the-browser-client-perspective}

<table class="ex_table">
  <tbody>
    <tr>
      <td>
        <img src="{{ site.api_url | absolute_url }}/assets/images/auth2-client-flow.png" alt="Client Authorization Flow" class="fullPct" />
        <p><strong>2</strong> Client Authorization Flow Workflow</p>
      </td>
    </tr>
  </tbody>
</table>


Browser-based clients will perform the following workflow in order to access access controlled resources:

* The client requests the Probe Service and checks the status code of the response.
* If the response is a 200 and no `location` property is present, the client can proceed to request the Content Resource.
* If the response is a 200 and the `location` property is present, the client _MUST_ use the supplied location to request the Content Resource.
* If the response is a 401,
  * The client does not have access to the Content Resource or images from an image service, and thus the client __checks for authentication services__ associated with the Content Resource or Image Service - e.g., in the Manifest, or in the Image Information Document (info.json).
  * If the probe response has a `location` property, the client can choose to show this immediately while offering the authentication flow to the user. If the Content Resource in the `location` property itself has authentication services (including a probe service), the client should... **FIXME wording! keep this succinct!**
* If the response is neither 200 nor 401, the client must handle other HTTP status codes.

* When the client checks for authentication services:
  * First it looks for a External access service pattern as this does not require any user interaction. If present, it opens the Access Token service to see if the user has the authorizing aspect required to meet the authorization requirement.
  * If no External service is present, the client checks for a Kiosk access service pattern as it does not involve user interaction. If present, it opens the Access Service in a separate window.
  * If no Kiosk access service is present, the client presents any Active Access Service patterns available and prompts the user to interact with one of them. When the user selects the access service to interact with the client opens that service URI in a separate tab (or window).
  * When the Access service window closes, either automatically or by the user, the client Opens the Access Token Service.

* After the Access Token service has been requested, if the client receives a token, it tries the Probe Service again with this newly acquired token.
  * If the client instead receives an error, it returns to look for further authentication services to interact with.
  * If there are no further authentication services, then the user does not have the credentials to interact with any of the Content Resource versions, and the client cannot display anything.

### 7.1 Tiered Access
{: #tiered-access}

When a probe service indicates that the user would be denied access to an access-controlled resource, it may also indicate that one or more [substitute][auth20-substitute] resources are potentially available, each at a different URI. In many cases there will be an access-controlled version available to certain authorized users, and then substitute that is openly available.

It is also possible that a substitute resource is itself an access-controlled resource, indicated by the presence of a new set of IIIF Authorization Flow services. In this case a client will re-enter the [workflow][auth20-workflow-from-the-browser-client-perspective] above. A useful user experience requires the substitute resource to have a different authorization scope and thus at least the probe service _MUST_ be different from that of the original access-controlled resource.

This pattern supports multiple tiers of access, and choices of substitute resource. The server _MAY_ hide some tiers and immediately present a much lower tier that it knows the user can access.

When there are no lower tiers and the user is not authorized to access the access-controlled resource, the client _SHOULD_ present information about the access service(s) included in last tier's access-controlled resource to allow the user to attempt to authenticate again.

## Appendices

### A. User Interaction at the Access Service and Third Party Cookies
{: #user-interaction-at-access-service}

While it is possible for the access service to immediately set a cookie in the response and generate client-side script that closes the opened tab, this behavior will likely result in browsers failing to send that cookie on subsequent requests for the token service or content resources if the client is hosted on a different domain. In this scenario, the user has not interacted with the access service origin in a _first party context_ as defined in the [Storage Access API][org-mozilla-storageaccess], and therefore that origin does not have access to _first party storage_, which means that any cookies for that origin are not included in requests to that origin.

For this reason, if the subsequent token service and access to content resources require the presence of a cookie, the user interface of the access service _MUST_ involve a [user gesture][org-whatwg-user-gesture] such as a click or a tap. Logging in with credentials, or clicking acceptance of a usage agreement, typically meet the definition of a user gesture.

If the token service and Content Resources will depend on some other authorizing aspect, such as IP address, then the Access Service tab _MAY_ be closed without user interaction.

If the client informs the access service that it is on the same domain, via the `origin` parameter, then the Access Service tab _MAY_ be closed without user interaction on that domain. For example, the initial login step in a multi-step single sign-on. If the domain of the content resources is the same as the client, it's not going to have third party cookie issues so could bounce immediately to the single sign on provider.

### B. Token Response for non-browser client

When returning JSON directly, the service _MUST_ use the appropriate HTTP status code for the response to describe the error (for example 400, 401, or 503).


(explain how invoked, extra param)

{: #interaction-for-non-browser-client-applications}

The simplest access token request comes from a non-browser client that can send cookies across domains, where CORS and third-party cookie restrictions do not apply. An example URI:

{% include api/code_header.html %}
```
https://auth.example.org/token
```
{: .urltemplate}

Would result in the HTTP Request:

{% include api/code_header.html %}
```
GET /token HTTP/1.1
Cookie: <cookie-acquired-during-login>
```
{: .urltemplate}

The response is the JSON access token object with the media type `application/json`:

{% include api/code_header.html %}
``` json-doc
{
  "accessToken": "ddc76e416e3804e2369e6c9cee806f5e438a5cdc",
  "expiresIn": 300
}
```


### C. Versioning

Starting with version 0.9.0, this specification follows [Semantic Versioning][org-semver]. See the note [Versioning of APIs][notes-versioning] for details regarding how this is implemented.

### D. Acknowledgments

We gratefully acknowledge the support from [Wellcome Collection](https://wellcomecollection.org/) that allowed one of the editors, Tom Crane, to devote a significant amount of time to this specification. Many thanks to the members of the [IIIF Community][iiif-community] for their continuous engagement, innovative ideas and feedback.

### E. Change Log

| Date       | Description |
| ---------- | ----------- |
| 2022-      | Version 2.0-alpha |
| 2017-01-19 | Version 1.0 (Alchemical Key) |
| 2016-10-05 | Version 0.9.4 (Incrementing Integer) add to security notes |
| 2016-08-22 | Version 0.9.3 (Wasabi KitKat) separate profiles, remove client identity service, add query parameters |
| (unreleased) | Version 0.9.2 (unnamed) postMessage instead of JSONP |
| 2015-10-30 | Version 0.9.1 (Table Flip) add missing @context, clarifications |
| 2015-07-28 | Version 0.9.0 (unnamed) draft |
{: .api-table .first-col-normal}

{% include links.md %}
{% include acronyms.md %}
