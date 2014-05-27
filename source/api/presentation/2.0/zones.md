---
title: "Presentation API 2.1: Zones Notes"
title_override: "IIIF Presentation API 2.1: Zones Notes"
layout: spec
tags: [specifications, presentation-api]
major: 2
minor: 0
patch: 0
pre: draft1
---

## Zones Notes

```
URI pattern:  {scheme}://{host}{/prefix}/{identifier}/zone/{name}.json
```
{: .uriTemplate}

{% highlight json %}
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
{% endhighlight %}

Then aggregate them in an AnnotationList referenced from other_content from the Canvas that it is associated with.
