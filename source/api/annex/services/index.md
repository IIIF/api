---
title: Linking to External Services
layout: spec
tags: [annex, service, services, specifications]
---

## Status of this Document
{:.no_toc}

This document is not subject to [semantic versioning][semver].
Changes will be tracked within the document.

_Copyright © 2012-2014 Editors and contributors. Published by the IIIF under the [CC-BY][cc-by] license._

**Editors**

  * Benjamin Albritton, _Stanford University_
  * Michael Appleby, _Yale University_
  * Robert Sanderson, _Stanford University_
  * Jon Stroop, _Princeton University_
  * Simeon Warner, _Cornell University_
  {: .names}

## Abstract
{:.no_toc}
This document describes the set of related services that have been identified within the IIIF as useful to reference from within the IIIF APIs.  This primarily relates to the [Presentation API][prezi-api] but may be of use beyond that.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Introduction

There are many additional features that could be included in resource descriptions beyond those already defined in the [Presentation API][prezi-api]. In order to keep the API manageable and lean enough to be understood, implemented, and validated, any feature which is not able to be justified as universally applicable will be imported as a service from an external resource. The adoption of [JSON-LD][json-ld] is paramount in this respect, as it provides a basis for interoperability and disambiguation between systems.

The inclusion of services in this document that are outside of the IIIF domain _MUST NOT_ be interpreted as endorsement, support, or approval from the editors, the IIIF community or any individual. This annex is provided as a registry of services to advertise their existence and attempt to ensure some consistency between implementations for common but not universal requirements.

## 2. Requirements

Service information included in the [Presentation API][prezi-api] response _MUST_ be both valid [JSON-LD][json-ld], and include a service-specific `@context`.  Services _SHOULD_ have an `@id` that can be dereferenced, and if so, the representation retrieved from that URI _SHOULD_ be JSON-LD.  The service at the URI in `@id` _MAY_ require additional parameters, generate representations other than JSON-LD, or have no JSON-LD representation at all.

Services _SHOULD_ have a `profile` URI which can be used to determine the type of service, especially for services that do not provide a JSON-LD representation.  The representation retrieved from the `profile` URI _SHOULD_ be a human or machine readable description of the service.  Services _MAY_ have a `label` property to provide a human readable string to display to the user in the situation that the service has to be selected or manually linked to rather than automatically processed.

Services _MAY_ be included either by reference or embedded within the [Presentation API][prezi-api] response.  The decision as to whether to embed or reference is left up to the implementer, however embedded descriptions should be kept as short as possible.  If the only properties of the object are `@context`, `@id`, `profile` and/or `label`, then the client _SHOULD_ retrieve the resource from the URI given in `@id`.

{% highlight json %}
{
  "service": {
    "@context": "http://example.org/ns/jsonld/context.json",
    "@id": "http://example.org/service/example.json",
    "profile": "http://example.org/docs/example-service.html",
    "label": "Example Service"
    // Additional keys may be embedded here, if not then the @id should be retrieved
  }
}
{% endhighlight %}

## 3. Recognized Services

### 3.1 Image Information
_Added: 2014-05-20_

The Image Information service allows the [Presentation API][prezi-api] to reference content to be displayed via the [Image API][image-api].  The JSON-LD content to be referenced or embedded is the Image Information document, also known as `info.json`.  The service _MUST_ have the `@context`, `@id` and `profile` keys, pointing to the context document, service base URI and compliance level profile respectively.

{% highlight json %}
{
  "service": {
    "@context" : "http://iiif.io/api/image/{{ site.image_api.latest.major }}/context.json",
    "@id" : "http://www.example.org/image-service/abcd1234",
    "profile": "http://iiif.io/api/image/{{ site.image_api.latest.major }}/level2.json"
  }
}
{% endhighlight %}

The service _MAY_ have additional information embedded from the Image Information document to prevent the need to retrieve and parse it separately.  In this case, the profile _MAY_ also point to the profile of what functionality is supported, as described in the Image API.

{% highlight json %}
{
  "service": {
    "@context" : "http://iiif.io/api/image/{{ site.image_api.latest.major }}/context.json",
    "@id" : "http://www.example.org/image-service/abcd1234",
    "profile": "http://iiif.io/api/image/1/level2.json",
    "protocol": "http://iiif.io/api/image",
    "width" : 6000,
    "height" : 4000,
    "scale_factors" : [ 1, 2, 4 ],
    "sizes" : [ "150,100", "360,240", "3600,2400" ],
    "tile_width" : 1024,
    "tile_height" : 1024
  }
}
{% endhighlight %}

### 3.2 GeoJSON
_Added: 2014-05-20_

[GeoJSON][geojson] provides the ability to associate a geographical place with a resource, in order to drive a map-based user interface or visualization tool.  This might be a location associated with the provenance of the object such as where it was created, or where it is currently held.  The location might also be related to the content of the resource, such as a city mentioned in the text or the landmark depicted in a photograph.  It is not appropriate to use this feature for tagging of time, people, events, and other semantic metadata outside of the scope of the Presentation API.

The [JSON-LD representation][geojson-ld] of GeoJSON, with `@context` `http://geojson.org/contexts/geojson-base.jsonld` _SHOULD_ be used. See the GeoJSON documentation for a full description of the functionality available.

An external reference example for tagging a place, where the URI would return a GeoJSON description of the city of Paris, France:

{% highlight json %}
{
  "service": {
    "@context" : "http://geojson.org/contexts/geojson-base.jsonld",
    "@id" : "http://www.example.org/geojson/paris.json"
  }
}
{% endhighlight %}

Or embedding the content:

{% highlight json %}
{
  "service": {
    "@context" : "http://geojson.org/contexts/geojson-base.jsonld",
    "@id" : "http://www.example.org/geojson/paris.json",
    "type": "Feature",
    "properties": {"name": "Paris"},
    "geometry": {
      "type": "Point",
      "coordinates" : [48.8567,2.3508]
    }
  }
}
{% endhighlight %}

### 3.3 Physical Dimensions
_Added 2014-05-20_

For digitized objects, it is often useful to know the physical dimensions of the object.  When available, they allow a client to present a ruler, or other rendition of physical scale, to the user.  However, implementers are warned that while this information may be available, frequently:

  * It is not available at all
  * It is unreliable when it is recorded
  * It is different for every view of an object
  * The Canvas dimensions don't accurately reflect only the physical object, but are derived from an image that includes a ruler, color bar, or the scanning bed.

As the [Presentation API][prezi-api] already includes an aspect ratio for the Canvas, the physical dimensions service need only report two additional pieces of information: the scale factor from canvas dimensions to physical dimensions, and the units for those generated physical dimensions.  It is _RECOMMENDED_ that the information always be embedded rather than requiring the client to retrieve it with an additional HTTP request, however some implementers _MAY WISH TO_ keep the information separate.

The physics dimensions description includes the following properties:

| Property         | Required? | Description |
| ---------------- | --------- | ----------- |
| `@context`       | Required  | The string "http://iiif.io/api/annex/service/physdim/1/context.json" |
| `@id`            | Optional  | A URI that will return the information, perhaps generated dynamically from the image |
| `profile`        | Required  | The string "http://iiif.io/api/annex/service/physdim" |
| `physical_scale` | Required  | The floating point ratio to convert from the canvas height and width to the physical objects height and width.  |
| `physical_units` | Required  | The physical units for the generated height and width.  Possible values are: "mm", "cm", in" |

{: .image-api-table}

The following example demonstrates the resulting structure, as embedded within the [Presentation API][prezi-api] response:

{% highlight json %}
{
  "service": {
    "@context": "http://iiif.io/api/annex/service/physdim/1.0/context.json",
    "profile": "http://iiif.io/api/annex/service/physdim",
    "physical_scale": 0.025,
    "physical_units": "mm"
  }
}
{% endhighlight %}

## Appendices

### A. Acknowledgements

The production of this document was generously supported by a grant from the [Andrew W. Mellon Foundation][mellon].

Thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### B. Change Log

| Date       | Description                                        |
| ---------- | -------------------------------------------------- |
| 2014-06-01 | Version 1.0 RFC                                    |

   [semver]: /api/annex/notes/semver.html "Versioning of APIs"
   [cc-by]: http://creativecommons.org/licenses/by/4.0/ "Creative Commons &mdash; Attribution 4.0 International"
   [iiif-discuss]: mailto:iiif-discuss@googlegroups.com "Email Discussion List"
   [image-api]: /api/image/{{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }}/ "Image API"
   [prezi-api]: /api/presentation/{{ site.presentation_api.latest.major }}.{{ site.presentation_api.latest.minor }}/ "Presentation API"
   [json-ld]: http://www.w3.org/TR/json-ld/ "JSON-LD"
   [iiif-community]: /community.html "IIIF Community"
   [mellon]: http://www.mellon.org/ "The Andrew W. Mellon Foundation"
   [geojson]: http://geojson.org/ "GeoJSON"
   [geojson-ld]: http://geojson.org/vocab "GeoJSON-LD"

{% for acronym in site.data.acronyms %}
  *[{{ acronym[0] }}]: {{ acronym[1] }}
{% endfor %}
