---
title: Image API 2.0
title_override: "IIIF Image API 2.0"
id: image-api
layout: sub-page
categories: [specifications, image-api, spec-doc]
major: 2
minor: 0
patch: 0
pre: draft1
---

## Status of this Document
{:.no_toc}

__This Version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest Stable Version:__ {{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }}.{{ site.image_api.latest.patch }}

**Editors:**

  * Michael Appleby, _Yale University_
  * Robert Sanderson, _Stanford University_
  * Stuart Snydman, _Stanford University_
  * Jon Stroop, _Princeton University_
  * Simeon Warner, _Cornell University_
  {: .names}

_Copyright © 2012-2014 Editors and contributors. Published by the IIIF under the CC-BY license._

----

## Abstract
{:.no_toc}

This document describes an image delivery API proposed by the International Image Interoperability Framework (IIIF) group. The IIIF Image API specifies a web service that returns an image in response to a standard http or https request. The URI can specify the region, size, rotation, quality characteristics and format of the requested image. A URI can also be constructed to request basic technical information about the image to support client applications. It was conceived of to facilitate systematic reuse of image resources in digital image repositories maintained by cultural heritage organizations. This API could be adopted by any image repository or service, and can be used to retrieve static images in response to a properly constructed URI.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

##  1. Audience and Scope

This document is intended for architects and developers building applications that share and consume digital images, particularly from cultural heritage institutions, museums, libraries and archives. Target applications include:

  * Digital image repositories and distributed content networks
  * Image focused web applications, such as pan/zoom viewers, book-readers, etc.
  * Client applications using image content for analysis or comparison

This specification concerns the use of the images by a client, but not management of the images by the server. It therefore covers how to respond to the requests given in a particular URI syntax. It does not cover methods of implementation such as rotation algorithms, transcoding, color management, compression, or how to respond to URIs that do not conform to the specified syntax. This allows flexibility for implementation in domains with particular constraints or specific community practices, while supporting interoperability in the general case.

## 2. URI Syntax

The IIIF Image API can be called in two ways:

 * Request an image, which may be part of a larger image
 * Request a description of the image characteristics and functionality available for that image

Both convey the request's information in the path segments of the URI, rather than as query parameters. This makes responses easier to cache, either at the server or by standard web-caching infrastructure. It also permits a minimal implementation using pre-computed files in a matching directory structure.

There are four parameters shared by the requests, and other IIIF specifications:

| Name   | Description |
| ------ | ----------- |
| scheme | Indicates the use of the http or https protocol in calling the service. |
| server | The host server on which the service resides. |
| prefix | The path on the host server to the service. This prefix is optional, but may be useful when the host server supports multiple services. The prefix _MAY_ contain multiple path segments, delimited by slashes, but all other special characters _MUST_ be encoded. See [URI Encoding and Decoding][uri-encoding-and-decoding] for more information. |
| identifier | The identifier of the requested image, expressed as a string. This may be an ark, URN, filename, or other identifier. Special characters _MUST_ be URI encoded. |
{: .image-api-table}

The combination of these parameters forms the image’s Base URI and identifies the underlying image content. It is constructed according to the following URI Template ([RFC6570][rfc-6570]):

```
{scheme}://{server}{/prefix}/{identifier}
```
{: .urltemplate}

The behavior of HTTP requests on the Base URI is not defined by this specification, but is reserved for use in future IIIF specifications.  To allow for extensions, this specification does not define the server behavior when it receives requests that do not match either the Base URI or one of the described URI syntaxes below.


###  2.1. Image Request URI Syntax

The IIIF Image API URI for requesting an image _MUST_ conform to the following URI Template:

```
{scheme}://{server}{/prefix}/{identifier}/{region}/{size}/{rotation}/{quality}.{format}
```
{: .urltemplate}

For example:

```
http://www.example.org/image-service/abcd1234/full/full/0/default.jpg
```
{: .urltemplate}

The sections of the Image Request URI include region, size, rotation, quality and format parameters, which define the characteristics of the returned image. These are described in detail in [Image Request Parameters][image-request-parameters].

###  2.2. Image Information Request URI Syntax

The URI for requesting image information _MUST_ conform to the following URI Template:

```
{scheme}://{server}{/prefix}/{identifier}/info.json
```
{: .urltemplate}

For example:

```
http://www.example.org/image-service/abcd1234/info.json
```
{: .urltemplate}

For each image made available, the server, prefix and identifier components of the information request _MUST_ be identical to those for the image request described above.

##  3. Identifier

The API places no restrictions on the form of the identifiers that a server may use or support, although the identifier _MUST_ be expressed as a string. All special characters (e.g. ? or #) _MUST_ be URI encoded to avoid unpredictable client behaviors. The URI syntax relies upon slash (/) separators so any slashes in the identifier _MUST_ be URI encoded (aka. percent-encoded, replace / with %2F ). See discussion in [URI Encoding and Decoding][uri-encoding-and-decoding].

##  4. Image Request Parameters

All parameters described below are required for compliant construction of a IIIF image API URI. The sequence of parameters in the URI _MUST_ be in the order described below. The order of the parameters is also intended as the order of the operations by which the service should manipulate the image content. Thus, the requested image content is first extracted as a region of the complete image, then scaled to the requested size, rotated and transformed into the color depth and format. This resulting image content is returned as the representation for the URI. Image and region dimensions in pixels are always given as an integer numbers. Intermediate calculations may use floating point numbers and the rounding method is implementation specific. Some parameters, notably percentages, may be specified with floating point numbers. These should have at most 10 decimal digits and consist only of decimal digits and "." with a leading zero if less than 1.

###  4.1. Region

The region parameter defines the rectangular portion of the full image to be returned. Region can be specified by pixel coordinates, percentage or by the value "full", which specifies that the entire image should be returned.

| Form |  Description |
| ------------------------ | ------------ |
| `full`                   | The complete image is returned, without any cropping. |
| x,y,w,h                  | The region of the full image to be returned is defined in terms of absolute pixel values. The value of x represents the number of pixels from the 0 position on the horizontal axis. The value of y represents the number of pixels from the 0 position on the vertical axis. Thus the x,y position 0,0 is the upper left-most pixel of the image. w represents the width of the region and h represents the height of the region in pixels.  |
| pct:x,y,w,h              | The region to be returned is specified as a sequence of percentages of the full image's dimensions, as reported in the Image Information document. Thus, `x` represents the number of pixels from the 0 position on the horizontal axis, calculated as a percentage of the reported width. `w` represents the width of the region, also calculated as a percentage of the reported width. The same applies to y and h respectively. These may be floating point numbers. |
{: .image-api-table}

If the request specifies a region which extends beyond the reported dimensions of the full image, then the service _SHOULD_ return an image cropped at the image's edge, rather than adding empty space.

If the requested region's height or width is zero, or if the region is entirely outside the bounds of the full image's reported dimensions, then the server _SHOULD_ return a 400 status code.

Examples:

  1. `http://www.example.org/image-service/abcd1234/full/full/0/default.jpg`
  2. `http://www.example.org/image-service/abcd1234/125,15,120,140/full/0/default.jpg`
  3. `http://www.example.org/image-service/abcd1234/pct:41.6,7.5,40,70/full/0/default.jpg`
  4. `http://www.example.org/image-service/abcd1234/125,15,200,200/full/0/default.jpg`
       _N.B. Returned image is 175,185 px_
  5. `http://www.example.org/image-service/abcd1234/pct:41.6,7.5,66.6,100/full/0/default.jpg`
       _N.B. Returned image is 175,185 px_
  {: .examplelist }

|:----:|:----:|
|![Full Image](img/full.png){: .fullPct}__1__ region=full||
|![Region by Pixels](img/region_px.png){: .fullPct}__2__ region=125,15,120,140|![Region by Percent](img/region_pct.png){: .fullPct}__3__ region=pct:41.6,7.5,40,70|
|![Region by Pixels](img/region_px_over.png){: .fullPct}__4__ region=125,15,200,200|![Region by Percent](img/region_pct_over.png){: .fullPct}__5__ region=pct:41.6,7.5,66.6,100|
{: .fullPct}

###  4.2. Size

The size parameter determines the dimensions to which the extracted region is to be scaled.

| Form | Description |
|----------------|-----------------------|
| `full`         | The extracted region is not scaled, and is returned at its full size. |
| w,             | The extracted region should be scaled so that its width is exactly equal to w, and the height will be a calculated value that maintains the aspect ratio of the requested region. |
| ,h             | The extracted region should be scaled so that its height is exactly equal to h, and the width will be a calculated value that maintains the aspect ratio of the requested region. |
| pct:n          | The width and height of the returned image is scaled to n% of the width and height of the extracted region. The aspect ratio of the returned image is the same as that of the extracted region. |
| w,h            | The width and height of the returned image are exactly w and h. The aspect ratio of the returned image _MAY_ be different than the extracted region, resulting in a distorted image. |
| !w,h           | The image content is scaled for the best fit such that the resulting width and height are less than or equal to the requested width and height. The exact scaling _MAY_ be determined by the service provider, based on characteristics including image quality and system performance. The dimensions of the returned image content are calculated to maintain the aspect ratio of the extracted region. |
{: .image-api-table}

If the resulting height or width is zero, then the server _SHOULD_ return a 400 (bad request) status code.

The image server _MAY_ support scaling beyond the full size of the extracted region.

Examples:

  1. `http://www.example.org/image-service/abcd1234/full/full/0/default.jpg`
  2. `http://www.example.org/image-service/abcd1234/full/150,/0/default.jpg`
  3. `http://www.example.org/image-service/abcd1234/full/,150/0/default.jpg`
  4. `http://www.example.org/image-service/abcd1234/full/pct:50/0/default.jpg`
  5. `http://www.example.org/image-service/abcd1234/full/225,100/0/default.jpg`
  6. `http://www.example.org/image-service/abcd1234/full/!225,100/0/default.jpg`
       _N.B. Returned image is 150,100 px_

  {: .examplelist}

|:----:|:----:|
|![Full Size](img/full.png){: .fullPct}__1__ region=full|![Size by Width](img/size_wc.png){: .fullPct}__2__ size=150,|
|![Size by Height](img/size_ch.png){: .fullPct}__3__ size=,150|![Size by Percent](img/size_pct.png){: .fullPct}__4__ size=pct:50|
|![Size by Width,Height](img/size_wch.png){: .fullPct}__5__ size=225,100|![Size By Bang Width Height](img/size_bwch.png){: .fullPct}__6__ size=!225,100|
{: .fullPct}


###  4.3. Rotation

The rotation value represents the number of degrees of clockwise rotation from the original, and may be any floating point number from 0 to 360. Initially most services will only support 0, 90, 180 or 270 as valid values.

| Form | Description |
| ---- | ----------- |
| n    | The degrees of clockwise rotation from the original, from 0 up to 360. |
{: .image-api-table}

A rotation value that is out of range or unsupported _SHOULD_ result in a 400 status code.

Examples:

  1. `http://www.example.org/image-service/abcd1234/full/full/0/default.jpg`
  2. `http://www.example.org/image-service/abcd1234/full/full/180/default.jpg`
  3. `http://www.example.org/image-service/abcd1234/full/full/90/default.jpg`
  4. `http://www.example.org/image-service/abcd1234/full/full/22.5/default.jpg`
  {: .examplelist}

|:----:|:----:|
|![Rotation 0](img/full.png){: .fullPct}__1__ rotation=0|![Rotation 180](img/rotate_180.png){: .fullPct}__2__ rotation=180|
|![Rotation 90](img/rotate_90.png){: .fullPct}__3__ rotation=90|![Rotation 22.5](img/rotate_22-5.png){: .fullPct}__4__ rotation=22.5|
{: .fullPct}

In most cases a rotation will change the width and height dimensions of the returned image file. The service _SHOULD_ return an image file that contains all of the image contents requested in the region and size parameters, even if the dimensions of the returned image file are different than specified in the size parameter. The image contents _should not_{: .rfc} be scaled as a result of the rotation, and there _SHOULD_ be no additional space between the corners of the rotated image contents and the bounding box of the returned image file.

For non-90-degree rotations the API does not specify the background color.

###  4.4. Quality

The quality parameter determines whether the image is delivered in color, grayscale or black and white.

| Quality   | Parameter Returned |
| --------- | ------------------ |
| `default` | The image is returned using the server's default quality (e.g. color, gray or bitonal as below) for the image. |
| `color`   | The image is returned in full color. |
| `gray`    | The image is returned in grayscale, where each pixel is black, white or any shade of gray in between. |
| `bitonal` | The image returned is bitonal, where each pixel is either black or white. |
{: .image-api-table}

A quality value that is unsupported _SHOULD_ result in a 400 status code.

Examples:

  1. `http://www.example.org/image-service/abcd1234/full/full/0/default.jpg`
  2. `http://www.example.org/image-service/abcd1234/full/full/0/color.jpg`
  3. `http://www.example.org/image-service/abcd1234/full/full/0/gray.jpg`
  4. `http://www.example.org/image-service/abcd1234/full/full/0/bitonal.jpg`
  {: .examplelist}

|:----:|:----:|
|![Default Quality](img/full.png){: .fullPct}__1__ quality=default|![Color Quality](img/full.png){: .fullPct}__2__ quality=color|
|![Gray Quality](img/gray.png){: .fullPct}__3__ quality=gray|![Bitonal Quality](img/bitonal.png){: .fullPct}__4__ quality=bitonal|
{: .fullPct}

###  4.5. Format

The format of the returned image is expressed as an extension at the end of the URI.  The list of supported formats is given in the `formats` property of the Image Information document.

| Extension | MIME Type |
| --------- | --------- |
| `jpg`     | image/jpeg |
| `tif`     | image/tiff |
| `png`     | image/png |
| `gif`     | image/gif |
| `jp2`     | image/jp2 |
| `pdf`     | application/pdf |
{: .image-api-table}

A format value that is unsupported _SHOULD_ result in a 400 status code.

Examples:

  1. `http://www.example.org/image-service/abcd1234/full/full/0/default.jpg`
  2. `http://www.example.org/image-service/abcd1234/full/full/0/default.png`
  3. `http://www.example.org/image-service/abcd1234/full/full/0/default.tif`
  {: .examplelist}

### 4.6. Order of Implementation

The sequence of parameters in the URI is intended to express the order in which image manipulations are made against the original. This is important to consider when implementing the service because applying the same parameters in a different sequence will often result in a different image being delivered. The order is critical so that the application calling the service reliably receives the output it expects.

The parameters should be interpreted as if the the sequence of image manipulations were:

`Region THEN Size THEN Rotation THEN Quality THEN Format`

|:----:|
|![Order of implementation illustration](img/transformation.png){:. fullPct}|
|__1__ region=`125,15,120,140` size=`90,` rotation=`345` quality=`gray`|

### 4.7. Canonical URI Syntax

There are several reasons why a canonical URI syntax is desirable:

  * It enables static, file-system based implementations, which will have only a single URI at which the content is available.
  * Caching becomes significantly more efficient, both client and server side, when the URIs used are the same between systems and sessions.
  * Response times can be improved by avoiding redirects from a requested non-canonical URI syntax to the canonical syntax by using the canonical form directly

In order to support the above requirements, clients should construct the image request URIs using to following canonical parameter values where possible.

| Parameter | Canonical value |
| --------- | --------------- |
| region    | "full" if the whole image is requested, otherwise the x,y,w,h description of the region. |
| size      | "full" if the default size is requested, otherwise the pixel dimensions w,h. |
| rotation  | An integer if possible, and trimming any trailing zeros in a decimal value. |
| quality   | "default" unless a quality that is different from the default quality is requested. |
| format    | Explicit format string required |
{: .image-api-table}

When the client requests an image, the server _MAY_ add a link header that indicates the canonical URI for that request:

```
Link: <http://iiif.example.com/server/full/full/0/default.jpg>;rel="canonical"
```
{: .urltemplate}

##  5. Information Request

The Image Information document contains both metadata about the image, such as maximum available height and width, and functionality available for it, such as the formats in which it may be retrieved.  The service _MUST_ return this information about the image. The request for technical information _MUST_ conform to the URI Template:

```
{scheme}://{server}{/prefix}/{identifier}/info.json
```
{: .urltemplate}

The syntax for the response is [JSON-LD][json-ld-w3c]. The content-type of the response _MUST_ be either "application/json" (regular JSON), or "application/ld+json" (JSON-LD).  If the client explicitly wants the JSON-LD content-type, then it must specify this in an Accept header, otherwise the server must return the regular JSON content-type.

If the regular JSON content-type is returned, then it is _RECOMMENDED_ that the server provide a link header to the context document. The syntax for the link header is below, and further [described in section 6.8 of the JSON-LD specification][json-as-json-ld]. If the client requests "application/ld+json", the link header _MAY_ still be included but _MUST_ be ignored. The entity body is identical regardless of the content-type, including the @context field.

```
Link: <http://iiif.io/api/image/{{ site.image_api.latest.major }}/context.json>
            ; rel="http://www.w3.org/ns/json-ld#context"
            ; type="application/ld+json"
```
{: .urltemplate}

Servers _SHOULD_ send the Access-Control-Allow-Origin header with the value \* in response to information requests. The syntax is shown below and is described int the [CORS][cors-spec] specification. This header is required in order to allow the JSON responses to be used by Web applications hosted on different servers.

```
Access-Control-Allow-Origin: *
```
{: .urltemplate}

### 5.1. Image Information

The JSON in the response will include the following properties:

| Property   | Required? | Description |
| ---------- | --------- | ----------- |
| `@context` | Required | The context document that describes the semantics of the terms used in the document. This must be the URI: [http://iiif.io/api/image/{{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }}/context.json] for version {{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }} of the IIIF Image API. This document allows the response to be interpreted as RDF, using the [JSON-LD][json-ld-org] serialization. |
| `@id` | Required | The Base URI of the image (as defined in [URI Syntax][uri-syntax], including scheme, server, prefix and identifier without a trailing slash. |
| `width` | Required | The width of the full image. |
| `height` | Required | The height of the full image. |
| `protocol` | Required | The URI "http://iiif.io/api/image" which can be used to determine that the document describes an image service which is a version of the IIIF Image API. |
| `profile` | Required | An array of profiles, indicated by either a URI or an object describing the features supported.  The first entry in the array _MUST_ be a compliance level URI, as defined below. |
| scale_factors | Optional | Some image servers support the creation of multiple resolution levels for a single image in order to optimize the efficiency in delivering images of different sizes. The scale_factors property expresses a set of resolution scaling factors. For example, a scale factor of 4 indicates that the service can efficiently deliver images at 25% of the height and width of the full image. |
| `sizes` | Optional | A set of dimensions that the server has available, expressed in the "w,h" syntax. This may be used to let a client know the sizes that are available when the server does not support requests for arbitrary sizes, or simply as a hint that requesting an image of this size may result in a faster response. |
| `tile_width` | Optional | Some image servers efficiently support delivery of predefined tiles enabling easy assembly of portions of the image. It is assumed that the same tile sizes are used for all scale factors supported. The tile_width element expresses the width of the predefined tiles. |
| `tile_height` | Optional | The tile_height element expresses the height of the predefined tiles. See description of tile_width. |
{: .image-api-table}

Image profiles have the following properties:

| Property  | Required? | Description |
| --------- | --------- | ----------- |
| `formats` | Optional | The set of image format parameter values available for the image. |
| `qualities` | Optional | The set of image quality parameter values available for the image. |
| `supports` | Optional | The set of additional features supported beyond those declared in the compliance level document |
{: .image-api-table}

The set of features that may be specified in the `supports` property are:

| Feature Name | Description |
| ------------ | ----------- |
| `canonical_link_header` | The canonical image URI HTTP link header is provided on image responses |
| `cors` |  The CORS HTTP header is provided on all responses  |
| `jsonld_media_type` | The JSON-LD media type is provided when JSON-LD is requested|
| `profile_link_header` | The profile link header is provided on image responses |
| `region_by_pct` |  Regions of images may be requested by percentage  |
| `region_by_px` |   Regions of images may be requested by pixel dimensions  |
| `rotation_arbitrary` |   Rotation of images may be requested by degrees other than multiples of 90  |
| `rotation_by_90s` |   Rotation of images may be requested by degrees in multiples of 90  |
| `size_above_full` | Size of images may be requested larger than the "full" size |
| `size_by_forced_wh` |   Size of images may be requested in the form "!w,h"  |
| `size_by_h` |   Size of images may be requested in the form ",h"  |
| `size_by_pct` |   Size of images may be requested in the form "pct:n"  |
| `size_by_w` |   Size of images may be requested in the form "w,"  |
| `size_by_wh` |   Size of images may be requested in the form "w,h"  |
{: .image-api-table}

The set of features, formats and qualities supported is the union of those declared in all of the external profile documents and any embedded profile objects.  If a property is not present in either the profile document or the `supports` property of an embedded profile, then a client _MUST_ assume that the feature is not supported.

The JSON response _MUST_ conform to the structure shown in the following example:

```javascript
{
  "@context" : "http://iiif.io/api/image/{{ site.image_api.latest.major }}/context.json",
  "@id" : "http://www.example.org/image-service/abcd1234/1E34750D-38DB-4825-A38A-B60A345E591C",
  "protocol" : "http://iiif.io/api/image",
  "width" : 6000,
  "height" : 4000,
  "scale_factors" : [ 1, 2, 4 ],
  "sizes" : [ "150,100", "360,240", "3600,2400" ],
  "tile_width" : 1024,
  "tile_height" : 1024,
  "profile" : [
    "http://iiif.io/api/image/{{ site.image_api.latest.major }}/level2.json",
    {
      "formats" : [ "jpg", "png" ],
      "qualities" : [ "default" ],
      "supports" : [
          "cors", "region_by_pct", "region_by_px", "rotation_arbitrary", "rotation_by_90s",
          "size_by_forced_wh", "size_by_h", "size_by_pct", "size_by_w", "size_by_wh"
      ]
    }
  ]
}
```
{: .codetemplate}

### 5.2 Extensions

Local additions to the image information document _MAY_ be specified in two ways:

1.  Extra properties _MAY_ be added to the document to provide information not defined in this specification. Clients _MUST_ ignore properties that are not understood.
2.  URIs _MAY_ be added to the supports list of a profile to cover features not defined in this specification, and similarly clients _MUST_ ignore URIs that are not understood.

```javascript
{
  "@context" : "http://iiif.io/api/image/{{ site.image_api.latest.major }}/context.json",
  // ...
  "documentation" : "http://www.example.com/my/documentation.html",
  // ...
  "profile" : [
    "http://iiif.io/api/image/{{ site.image_api.latest.major }}/level2.json",
    "http://www.example.com/my/profile-level-42.json",
    {"supports" : ["http://www.example.com/my/feature.html"]}
  ]
}
```
{: .codetemplate}

##  6. Compliance Levels

The Image Information document _MUST_ specify the extent to which the API is supported by including a compliance level URI as the first entry in the `profile` property.  This URI links to a description of the highest compliance level for which all requirements are met. The URI _MUST_ be one of those given in [Image API Compliance][compliance]. This description contains the profile related features, as discussed in [Image Information][image-information]. A server _MAY_ declare different compliance levels for different images.

The compliance level URI _MAY_ also be given in the HTTP Link header ([RFC5988][rfc-5988]) with the parameter `rel="profile"`, and thus a complete header might look like:

```
Link: <http://iiif.io/api/image/{{ site.image_api.latest.major }}/level1.json>;rel="profile"
```
{: .urltemplate}


##  7. Server Responses

###  7.1. Successful Responses

Servers may transmit HTTP responses with 200 (Successful) or 3xx (Redirect) status codes when the request has been successfully processed. If the status code is 200, then the entity-body _MUST_ be the requested image or information response. If the status code is 301, 302, 303, or 304, then the entity-body is unrestricted, but it is _RECOMMENDED_ to be empty. If the status code is 301, 302, or 303 then the Location HTTP Header _MUST_ be set containing the URI of the image that fulfills the request. This enables servers to have a single canonical URI to promote caching of responses. Status code 304 is handled exactly as per the HTTP specification. Clients should therefore expect to encounter all of these situations and not assume that the entity-body of the initial response necessarily contains the image data.

###  7.2. Error Conditions

The order in which servers parse requests and detect errors is not specified. A request will fail on the first error encountered and return an appropriate http status code, with common codes given in the list below. It is recommended that the body of the error response includes a human-readable description of the error in either plain text or html.

| Status Code | Description |
| ---------- | ----------- |
| 400 Bad Request | This response is used when it is impossible for the server to fulfil the request, as the syntax of the request is incorrect.  For example, this would be used if the size parameter does not match any of the specified syntaxes. |
| 401 Unauthorized | Authentication is required and not provided. See Section 7 below for details. |
| 403 Forbidden | The user, authenticated or not, is not permitted to perform the requested operation. |
| 404 Not Found | The image resource specified by [identifier] does not exist, or the value of one or more of the parameters is not supported for this image. |
| 500 Internal Server Error | The server encountered an unexpected error that prevented it from fulfilling the request. |
| 501 Not Implemented | A valid IIIF request that is not implemented by this server. |
| 503 Service Unavailable | Used when the server is busy/temporarily unavailable due to load/maintenance issues. An alternative to connection refusal with the option to specify a back-off period. |
{: .image-api-table}

##  8. Authentication

This API does not specify whether the image server will support authentication or what mechanism it might use. In the case of "401 Unauthorized" HTTP response, the content of the WWW-Authenticate header will depend on the authentication mechanism supported by the server. If the server supports HTTP Basic or Digest authentication then the header should follow [RFC2617][rfc-2617], for example:

```
WWW-Authenticate: Basic realm="Images"
```
{: .urltemplate}

##  9. URI Encoding and Decoding

The URI syntax of this API relies upon slash (/) separators which _MUST NOT_ be encoded. Clients _MUST_ percent-encode special characters (the to-encode set below: percent and gen-delims of [RFC3986][rfc-3986] except the colon) within the components of requests. For example, any slashes within the identifier part of the URI _MUST_ be percent-encoded. Encoding is necessary only for the identifier because other components will not include special characters.

```
to-encode = "/" / "?" / "#" / "[" / "]" / "@" / "%"
```
{: .urltemplate}

Upon receiving an API request, a server _MUST_ first split the URI path on slashes and then decode any percent-encoded characters in each component.

Additionally, if identifiers include any characters outside the US-ASCII set then the encoding to octets must be defined consistently on client and server, and the octets _MUST_ be percent-encoded. Percent-encoding other characters introduces no ambiguity but is unnecessary.

| Parameters | URI path |
| ---------- | -------- |
| identifier=id1 region=full size=full rotation=0 quality=default | `id1/full/full/0/default` |
| identifier=id1 region=0,10,100,200 size=pct:50 rotation=90 quality=default format=png | `id1/0,10,100,200/pct:50/90/default.png` |
| identifier=id1 region=pct:10,10,80,80 size=50, rotation=22.5 quality=color format=jpg | `id1/pct:10,10,80,80/50,/22.5/color.jpg` |
| identifier=bb157hs6068 region=full size=full rotation=270 quality=gray format=jpg | `bb157hs6068/full/full/270/gray.jpg` |
| identifier=ark:/12025/654xz321 region=full size=full rotation=0 quality=default | `ark:%2F12025%2F654xz321/full/full/0/default` |
| identifier=urn:foo:a123,456 region=full size=full rotation=0 quality=default | `urn:foo:a123,456/full/full/0/default` |
| identifier=urn:sici:1046-8188(199501)13:1%3C69:FTTHBI%3E2.0.TX;2-4 region=full size=full rotation=0 quality=default | `urn:sici:1046-8188(199501)13:1%253C69:FTTHBI%253E2.0.TX;2-4/full/full/0/default` |
| identifier=http://example.com/?54#a region=full size=full rotation=0 quality=default | `http:%2F%2Fexample.com%2F%3F54%23a/full/full/0/default` |
{: .image-api-table}

Servers which are incapable of processing arbitrarily encoded identifiers _SHOULD_ make their best efforts to expose only image identifiers for which typical clients will not encode any of the characters, and thus it is _RECOMMENDED_ to limit characters in identifiers to letters, numbers and the underscore character.

##  10. Security Considerations

This API defines a URI syntax and the semantics associated with its components. The composition of URIs has few security considerations except possible exposure of sensitive information in URIs or revealing of browse/view behavior of users.

Server applications implementing this API must consider possible denial-of-service attacks, and authentication vulnerabilities based on DNS spoofing. Applications must be careful to parse incoming requests (URIs) in ways that avoid overflow or injection attacks.

Early sanity checking of URI’s (lengths, trailing GET, invalid characters, out-of-range parameters) and rejection with appropriate response codes is recommended.

## 11. Appendices

###  A. Implementation Notes

  * For use cases that enable the saving of the image, it is _RECOMMENDED_ to use the HTTP Content-Disposition header ([RFC6266][rfc-6266]) to provide a convenient filename that distinguishes the image, based on the identifier and parameters provided.
  * This specification makes no assertion about the rights status of requested images or metadata, whether or not authentication has been accomplished. Please see the IIIF Metadata API for rights information.
  * This API does not specify how image servers fulfill requests, what quality the returned images will have for different parameters, or how parameters may affect performance. See the compliance document for more discussion.
  * Image identifiers that include the slash (/ %2F) or backslash (\ %5C) characters may cause problems with some HTTP servers. Apache servers from version 2.2.18 support the "AllowEncodedSlashes NoDecode" (link to ) configuration directive which will correctly pass these characters to client applications without rejecting or decoding them. Servers using older versions of Apache and local identifiers which include these characters will need to use a workaround such as internally translating or escaping slash and backslash to safe value (perhaps by double URI-encoding them).
  * As described in [Rotation][rotation], in order to retain the size of the requested image contents, rotation will change the width and height dimensions of the returned image file. A formula for calculating the dimensions of the returned image file for a given rotation can be found here.

### B. Versioning

Starting with version 2.0, this specification follows [Semantic Versioning][semver] with version numbers of the form "MAJOR.MINOR.PATCH" where:

  * MAJOR version increment indicates incompatible API changes.
  * MINOR version increment indicates addition of functionality in a backwards-compatible manner.
  * PATCH version increment indicates backwards-compatible bug fixes.

This versioning system will be implemented in the following ways:

  * URIs for compliance and context will be updated with major versions only, and otherwise edited in place.
  * URIs for the specifications will be updated with major and minor versions, with patch versions edited in place.
  * The protocol URI does not change with versioning.

###  C. Acknowledgments

The production of this document was generously supported by a grant from the [Andrew W. Mellon Foundation][mellon].

Many thanks to  Ben Albritton, Matthieu Bonicel, Anatol Broder, Kevin Clarke, Tom Cramer, Ian Davis, Neil Jefferies, Scotty Logan, Sean Martin, Roger Mathisen, Lynn McRae, Willy Mene, Mark Patton, Petter Rønningsen, and Brian Tingle for your thoughtful contributions to the effort and written feedback.  Thanks also to the members of the [IIIF Community][iiifCommunity] for their continuous engagement, innovative ideas and feedback.

###  D. Change Log

| Date | Editor |  Description |
| ---- | ------ | ------------ |
| 2014-05-XX | rsanderson | Version 2.0 (Voodoo Bunny) RFC [View change log][change-log] |
| 2013-09-17 | ssnydman | Version 1.1 released. |
| 2013-09-04 | ssnydman | Added @context to Image Information Request table in section 5. |
| 2013-06-26 | ssnydman | Changed quality parameter definitions in section 4.4. |
| 2013-06-17 | ssnydman | Draft release 1.1. [View change log][change-log11]. |
| 2012-08-10 | ssnydman | Release 1.0 |
| 2012-07-13 | rsanderson | Incorporates responses to RFC feedback |
| 2012-03-09 | ssnydman | Initial release |
| 2012-04-13 | ssnydman | 0.2 after internal review and IIIF April Meeting |
| 2012-05-02 | ssnydman | RFC version |
{: .image-api-table}

[change-log11]: /api/image/1.1/change-log.html "Change Log for Version 1.1"
[change-log]: /api/image/2.0/change-log.html "Change Log for Version 2.0"
[compliance]: /api/image/2.0/compliance.html "Image API Compliance"
[cors-spec]: http://www.w3.org/TR/cors/ "Cross-Origin Resource Sharing"
[iiif-discuss]: mailto:iiif-discuss%40googlegroups.com "Email Discussion List"
[json-as-json-ld]: http://www.w3.org/TR/json-ld/#interpreting-json-as-json-ld "JSON-LD 1.0: 6.8 Interpreting JSON as JSON-LD"
[json-ld-org]: http://www.json-ld.org/ "JSON for Linking Data"
[json-ld-w3c]: http://www.w3.org/TR/json-ld/ "JSON-LD 1.0"
[mellon]: http://www.mellon.org/ "The Andrew W. Mellon Foundation"
[rfc-2617]: http://tools.ietf.org/html/rfc2617 "HTTP Authentication: Basic and Digest Access Authentication"
[rfc-3986]: http://tools.ietf.org/html/rfc3986 "Uniform Resource Identifier (URI): Generic Syntax"
[rfc-5988]: http://tools.ietf.org/html/rfc5988 "Web Linking"
[rfc-6266]: http://tools.ietf.org/html/rfc6266 "Use of the Content-Disposition Header Field in the Hypertext Transfer Protocol (HTTP)"
[rfc-6570]: http://tools.ietf.org/html/rfc6570 "URI Template"
[semver]: http://semver.org/spec/v2.0.0.html "Semantic Versioning 2.0.0"
[iiifCommunity]: /community.html "IIIF Community"

[audience-and-scope]: #audience-and-scope "1. Audience and Scope"
[uri-syntax]: #uri-syntax "2. URI Syntax"
[image-request-uri-syntax]: #image-request-uri-syntax "2.1. Image Request URI Syntax"
[image-information-request-uri-syntax]: #image-information-request-uri-syntax "2.2. Image "Information Request URI"
[identifier]: #identifier "3. Identifier"
[image-request-parameters]: #image-request-parameters "4. Image Request Parameters "
[region]: #region "4.1. Region"
[size]: #size "4.2. Size"
[rotation]: #rotation "4.3. Rotation"
[quality]: #quality "4.4. Quality"
[format]: #format "4.5. Format"
[order-of-implementation]: #order-of-implementation "4.6. Order of Implementation"
[canonical-uri-syntax]: #canonical-uri-syntax "4.7. Canonical URI Syntax"
[information-request]: #information-request "5. Information Request"
[image-information]: #image-information "5.1. Image Information"
[extensions]: #extensions "5.2 Extensions"
[compliance-levels]: #compliance-levels "6. Compliance Levels"
[server-responses]: #server-responses "7. Server Responses"
[successful-responses]: #successful-responses "7.1. Successful Responses"
[error-conditions]: #error-conditions "7.2. Error Conditions"
[authentication]: #authentication "8. Authentication"
[uri-encoding-and-decoding]: #uri-encoding-and-decoding "9. URI Encoding and Decoding"
[security-considerations]: #security-considerations "10. Security Considerations"
[appendices]: #appendices "11. Appendices"
[a-implementation-notes]: #a-implementation-notes "A. Implementation Notes"
[b-versioning]: #b-versioning "B. Versioning"
[c-acknowledgments]: #c-acknowledgments "C. Acknowledgments"
[d-change-log]: #d-change-log "D. Change Log"

{% for acronym in site.data.acronyms %}
  *[{{ acronym[0] }}]: {{ acronym[1] }}
{% endfor %}
