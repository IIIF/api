---
title: "Apache HTTP Server Implementation Notes"
layout: spec
redirect_from:
  - /annex/notes/apache.html
---

## Allow Encoded Slashes

As [specified in the Image API][uri-encoding-and-decoding], slashes ("`/`", "`\`") in the identifer portion of the base uri MUST be encoded. This may cause problems with some HTTP servers. Apache servers from version 2.2.18 support the `AllowEncodedSlashes NoDecode` [configuration directive][apache-aesnd] which will correctly pass these characters to client applications without rejecting or decoding them.

{% include api/code_header.html %}
```
AllowEncodedSlashes On
```
{: .urltemplate}

Servers using older versions of Apache and local identifiers which include these characters will need to use a workaround such as internally translating or escaping slash and backslash to safe value (perhaps by double URI-encoding them).

## Enabling CORS

Both specifications prefer to have cross-origin resource sharing enabled. This may be enabled with the following configuration snippet:

{% include api/code_header.html %}
```
LoadModule headers_module modules/mod_headers.so
Header set Access-Control-Allow-Origin "*"
```
{: .urltemplate}

## Set Compliance Link Header

The Image API states that a server [may indicate its compliance level in a link header][image-compliance-levels]. This can be done as follows:

{% include api/code_header.html %}
```
Header set Link '<http://iiif.io/api/image/2/level1.json>;rel="profile"'
```
{: .urltemplate}

## Conditional Content Types

Both the [Image][image-api] and [Presentation][prezi-api] APIs state that clients may request JSON-LD, as opposed to plain JSON.

In the Image API, this may be enabled with the following configuration snippet (note that this assumes the compliance level Link header has been set [as above][set-compliance-link-header]):

{% include api/code_header.html %}
```
<FilesMatch "\.json">
    SetEnvIf Accept "application/ld\+json" WANTS_jsonld
    Header set Content-Type "application/ld+json" env=WANTS_jsonld
    Header append Link '<http://iiif.io/api/image/2/context.json>;rel="http://www.w3.org/ns/json-ld#context";type="application/ld+json"' env=!WANTS_jsonld
</FilesMatch>
```
{: .urltemplate}

The above configuration snippet may also be used for Presentation API implementations that have URIs ending in `.json`, but the line starting `Header append Link` should be deleted and it will not work for the recommended URI pattern. The following snippet will work for the recommended patterns:

{% include api/code_header.html %}
```
<LocationMatch "^/prefix/(collection/.*|.*/manifest|.*/(sequence|canvas|annotation|list|range|layer)/.*)$">
    SetEnvIf Accept "application/ld\+json" WANTS_jsonld
    Header set Content-Type "application/json"
    Header set Content-Type "application/ld+json" env=WANTS_jsonld
</LocationMatch>
```
{: .urltemplate}

Note that for version 3.0 of the [Presentation][prezi30] and [Image][image30] APIs, these media types should also have the appropriate `profile` parameter as part of the `Content-Type` value.

[uri-encoding-and-decoding]: {{ site.api_url | absolute_url }}/image/2.0#uri-encoding-and-decoding "Image API: URI Encoding and Decoding"
[image-compliance-levels]: {{ site.api_url | absolute_url }}/image/2.0#compliance-levels "Image API: Compliance Levels"
[apache-aesnd]: http://httpd.apache.org/docs/2.2/mod/core.html#allowencodedslashes "Allow Encoded Slashes directive"
[set-compliance-link-header]: #set-compliance-link-header
[image-api]: {{ site.api_url | absolute_url }}/image/2.0/
[prezi-api]: {{ site.api_url | absolute_url }}/presentation/2.0/
[image30]: {{ site.api_url | absolute_url }}/image/3.0/ "Image API 3.0"
[prezi30]: {{ site.api_url | absolute_url }}/presentation/3.0/ "Image API 3.0"

{% include acronyms.md %}
