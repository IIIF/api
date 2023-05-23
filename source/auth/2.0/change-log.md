---
title: "Authorization Flow API 2.0 Change Log"
title_override: "Changes for IIIF Authorization Flow API Version 2.0"
id: auth-api-20-change-log
layout: spec
cssversion: 3
tags: [specifications, auth-api, change-log]
major: 2
minor: 0
# no patch
pre: final
redirect_from:
  /auth/2.0/change-log.html
---

This document is a companion to the [IIIF Authorization Flow API Specification, Version 2.0][auth20]. It describes the changes to the API specification made in this major release. While the approach taken by the specification is fundamentally the same as the [previous version][auth10], this specification is backwards incompatible.


## 1. Breaking changes

Several existing properties were renamed for consistency, developer convenience, or to better reflect the intended semantics. Some of the semantics were also clarified based on implementation experience from previous versions. The specification was aligned with current versions of the other IIIF APIs in its use of JSON-LD 1.1.

### 1.1. Use JSON-LD 1.1 

The Authorization Flow API Version 2.0 adopts JSON-LD 1.1 in order to align with the IIIF Presentation 3.0 API. See the [IIIF Presentation 3.0 API Change Log, Section 1.1](https://iiif.io/api/presentation/3.0/change-log/#11-external-specifications) for details.

### 1.2. Rename `@id` to `id`, `@type` to `type`

These properties were renamed to enable Javascript developers to use the "dot notation" (`service.id`) instead of the square-brackets-based equivalent needed with the @ character (`service['@id']`). This follows JSON-LD community best practices established by schema.org, the JSON-LD, Web Annotation and Social Web working groups. See issue [#590](https://github.com/IIIF/api/issues/590).

### 1.3. Every class has a `type`

In the previous version, services defined by this specification did not have a `@type` and were instead identified by their `profile` property. Version 2.0 provides a `type` for all services defined by this specification.

### 1.4. Removal of `profile` where no longer necessary; use of @context-aliased URIs

Resources that can now be understood by their `type` property alone no longer have the `profile` property. Resources that need further classification (the [Access Service][auth20-access-service] and [Access Token Error Response][auth20-access-token-error-format]) retain the `profile` property. These profiles are now simple strings (e.g., `kiosk`) defined in the JSON-LD `@context` rather than fully-qualified URIs in the JSON, in line with the Presentation API 3.0.

### 1.5. Use Language Maps

In further alignment with Presentation 3.0, the resources defined by this specification now use Language Maps for any strings that will be presented to a user. This also means that some resources in the previous version that were not JSON-LD now become JSON-LD resources and therefore introduce the new types `AuthAccessToken2` and `AuthAccessTokenError2`. See [#1247](https://github.com/IIIF/api/issues/1247). The specification also clarifies where user-facing strings are required. See [#2112](https://github.com/IIIF/api/issues/2112).

### 1.6. Remove the "clickthrough" and "login" patterns, merge into new "active" interaction pattern

In the previous version, clickthrough and login were distinct interaction patterns for the Cookie Service. The clickthrough pattern had ceased to work cross-domain in most browsers as a result of changing treatment of third-party cookies. A similar user interaction can still be implemented if the user performs a significant _user gesture_ (such as a click) at the access service. This eliminates any difference between login and clickthrough as far as the authorization flow is concerned, and the single `active` service simply implies that the user has some interaction with the web page(s) offered by the access service. See [#2035](https://github.com/IIIF/api/issues/2035).


## 2. New Features

### 2.1. Support Access Control on any Content Resource

The previous version defined only services declared on IIIF Image API service descriptions (info.json). The new version supports _Authorization Flow_ patterns on any content resource, as described in the [introduction][auth20-introduction]. 

### 2.2. Introduce concept of "Authorizing aspect"

The previous version assumed that access to Image Service responses would be authorized by the server based on the presence of an _access cookie_. While this is still fully supported, the specification does not assume it. The new version introduces the concept of _Authorizing aspect_: the content or characteristics of an HTTP request for a content resource, that the server bases an access control decision on. This may be a cookie, but can be anything, it is independent of this specification. See [#2017](https://github.com/IIIF/api/issues/2017) and [#1959](https://github.com/IIIF/api/issues/1959). This therefore allows "ambient" aspects of the request, such as IP address, to be considered as the Authorizing aspect. See [#2112](https://github.com/IIIF/api/issues/2112).

### 2.3. Introduce a Probe Service

In the previous version the client learned the user's access to IIIF API Image responses from the HTTP response status code of the IIIF Image API Service Description (info.json). To support access control on any resource, the new version introduces a _Probe Service_, which returns a Probe Service Response (of new type `AuthProbeResult2`) that conveys the access status as the field of a JSON object. The Image API Service is no longer used as a probe, and clients are no longer required to base flow decisions on HTTP status codes. For all access-controlled resources, the probe service acts as a proxy returning JSON that browser-based scripts can easily interact with. See [#1290](https://github.com/IIIF/api/issues/1290), [#1166](https://github.com/IIIF/api/issues/1166), [#2194](https://github.com/IIIF/api/issues/2194) and [#2201](https://github.com/IIIF/api/issues/2201).

#### 2.4. Allow responses to provide user-facing strings

In the previous version, most user-facing strings were defined on the service description, including failure messages. In the new version, these can be also returned in service responses, allowing for greater flexibility in the messages shown to users. Examples are the `heading` and `note` fields on the [Probe Service response][auth20-probe-service] (see below).


## 3. Editorial and Naming Changes

### 3.1. Rename specification

The specification has been renamed, using the term _Authorization Flow_ rather than _Authentication_ to avoid the implication that it describes an Authentication _protocol_ (e.g., like OAuth2). Instead, the specification is clearer that it defines a set of formal _interaction patterns_ that allow client software (such as a viewer) to learn whether the user has access to a resource, and direct them to an external access control system if they don't.

### 3.2. Rename Cookie Service to Access Service

Now that the _Authorizing aspect_ may be something other than a cookie, the former _Cookie Service_ becomes the more general _Access Service_: the service that grants the Authorizing aspect.





{% include links.md %}
{% include acronyms.md %}