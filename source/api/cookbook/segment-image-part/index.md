---
title: Recipe - Annotating part of an image to a canvas
layout: spec
tags: [annex, service, services, specifications]
cssversion: 2
---

This is a recipe from the [Presentation API Cookbook][annex-cookbook].


# Annotating part of an image to a canvas

## Use Case

It is important to be able to extract parts, or segments, of resources. In particular a very common requirement is to associate a resource with part of a canvas, or part of an image with either the entire canvas or part thereof.   Plus explain real life situations here (some number of these, within reason).

## Implementation notes

Segments of both static images and canvases may be selected by adding a rectangular bounding box after the URI. The fragment takes the form of `#xywh=` where the four numbers are the x and y coordinates of the top left hand corner of the bounding box in the image or canvas, followed by the width and height. Note that only integers are allowed in this syntax, and this may limit accuracy of assignment to canvases with small dimensions. 


## Example

``` json-doc
{
  "id": "http://example.org/iiif/book1/annotation/anno1",
  "type": "Annotation",
  "motivation": "painting",
  "body":{
    "id": "http://example.org/iiif/book1/res/page1.jpg#xywh=40,50,1200,1800",
    "type": "Image",
    "format": "image/jpeg"
  },
  "target": "http://example.org/iiif/book1/canvas/p1"
}
```

# Related recipes

* Link to a recip[e with a reason why it is related to this one, or should be looked at
* Link to a recip[e with a reason why it is related to this one, or should be looked at
* Link to a recip[e with a reason why it is related to this one, or should be looked at


{% include acronyms.md %}
{% include links.md %}

