---
title: "Presentation API 2.1: Zones Notes"
title_override: "IIIF Presentation API 2.1: Zones Notes"
layout: spec
tags: [specifications, presentation-api]
major: 2
minor: 1
patch: 0
pre: draft1
sitemap: false
redirect_from:
  - /api/presentation/2.0/zones.html
---

## Zones Notes

``` none
URI pattern:  {scheme}://{host}{/prefix}/{identifier}/zone/{name}.json
```
{: .uriTemplate}

``` json-doc
{
  "@id": "mandatory-uri",
  "@type": "sc:Zone",
  "label": "optional label",
  "height": 1200,           // mandatory
  "width": 800,             // mandatory

  // other fields for zone manipulation
  // in a service?
  "viewing_orientation": 270,

  // should be merged into spec's enumeration
  "viewing_hint": "foldout",

  "images": [ ... ],
  "other_content": [ ... ]
}
```

Then aggregate them in an AnnotationList referenced from other_content from the Canvas that it is associated with.
