---
title: Recipe - Name of Recipe
layout: spec
tags: [annex, service, services, specifications]
cssversion: 2
---

This is a recipe from the [Presentation API Cookbook][annex-cookbook].


# Name of Recipe

## Use Case

(why this pattern is important) Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque velit velit, malesuada in ornare ut, commodo a nunc. Interdum et malesuada fames ac ante ipsum primis in faucibus. 

## Implementation notes

(how to implement the pattern) -- style on links to spec references to make them easy to find and back-ref automagically

## Restrictions: (when this pattern is usable / not usable)

If it's deprecated. If it uses multiple specifications, which versions are needed, etc.
Not present if not needed.

## Example

(initial prose description)

(investigate further how best to do line numbers, and whether they're beneficial overall -- maybe hard code to have anchors to lines?)

[eg CSS vs hard coded, preventing selection for copy/paste of examples]


``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ],
  "id": "https://example.org/iiif/book1/manifest",
  "type": "Manifest" 
}
```

# Related recipes

* Link to a recip[e with a reason why it is related to this one, or should be looked at.
* Link to a recip[e with a reason why it is related to this one, or should be looked at.
* Link to a recip[e with a reason why it is related to this one, or should be looked at.


{% include acronyms.md %}
{% include links.md %}

