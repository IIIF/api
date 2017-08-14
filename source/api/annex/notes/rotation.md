---
title: "Note: Calculating the Size of a Rotated Image"
layout: spec
tags: [annex, rotation, image-api]
cssversion: 2
redirect_from:
  - /api/annex/notes/rotation.html
---

As described in the IIIF Image API, [Section 4.3. Rotation][image-api-rotation], in order to retain the size of the requested image contents rotation will change the width and height dimensions of the returned image file. To calculate the dimensions of the returned image file for a given rotation in compliance with the IIIF API, the following formula can be used:

![Formula for calculating image size of rotated image][rotation-ill]

[rotation-ill]: {{ site.url }}{{ site.baseurl }}/api/annex/notes/iiif-rotated-img-size.png "Formula for calculating image size of rotated image"
[image-api-rotation]: {{ site.url }}{{ site.baseurl }}/api/image/2.0#rotation "Image API Section 4.3. Rotation"
