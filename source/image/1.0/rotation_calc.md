---
title: Calculating the Size of a Rotated Image (1.0)
layout: page
redirect_from:
  - /image/1.0/rotation_calc.html
---

<section class="wrapper">
As described in the <a
 href="{{ site.api_url | absolute_url }}/image/1.0/">IIIF Image 1.0
API, Section 4.2
(Rotation)</a>, in order to retain the size of the requested image
contents rotation will change the
width and height dimensions of the returned image file. To calculate
the dimensions of the returned image file for a given rotation in
compliance with the IIIF API, the
following formula can be used:<br>
<br>
<img style="width: 685px; height: 1000px;"
 alt="Formula for calculating image size of rotated image"
 src="{{ site.api_url | absolute_url }}/annex/notes/iiif-rotated-img-size.png"><br>
</section>
