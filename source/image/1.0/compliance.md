---
title: Image API Compliance, 1.0
id: index
layout: spec
sitemap: false
redirect_from:
  - /image/1.0/compliance.html
---

<section class="wrapper">
<div class="toc">
<h2>Table of Contents</h2>
<p class="toc">1. <a href="#intro">Introduction</a><br>
2. <a href="#intro">Compliance Level Summary</a><br>
3. <a href="#level0">Level 0 Compliance</a><br>
4. <a href="#level1">Level 1 Compliance</a><br>
5. <a href="#level2">Level 2 Compliance</a><br>
</p>
</div>

<hr>

<div class="body">
<h2 id="intro">1. Introduction</h2>
This document is a companion to the <a href="{{ site.api_url | absolute_url }}/image/1.0/">
International Image Interoperability Framework Image API Specification, version 1.0</a>. It defines the set of supported parameters that correspond to
different levels of compliance to the IIIF Image API.

<h2 id="service">2. Compliance Level Summary</h2>
<p>Three levels
of compliance are defined. Level 0 is defined as the
minimum set of supported parameters and features to qualify an
implementation of the service as compliant to the IIIF standard. Level
1 is defined as the RECOMMENDED set of parameters and features to be
implemented.</p>

<table class="image-api-table">
  <tbody>
    <tr>
      <th></th>
      <th>Level 0</th>
      <th>Level 1</th>
      <th>Level 2</th>
      <th>Optional</th>
    </tr>
    <tr>
      <td><strong>Region</strong></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp; full</td>
      <td>x</td>
      <td>x</td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;x,y,w,h</td>
      <td></td>
      <td>x</td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;pct:x,y,w,h</td>
      <td></td>
      <td><br>
      </td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td><strong>Size</strong></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp; full</td>
      <td>x</td>
      <td>x</td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;w,</td>
      <td></td>
      <td>x</td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;,h</td>
      <td></td>
      <td>x</td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;pct:x</td>
      <td></td>
      <td>x</td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;w,h</td>
      <td></td>
      <td></td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;!w,h</td>
      <td></td>
      <td></td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td><strong>Rotation</strong></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp; 0</td>
      <td>x</td>
      <td>x</td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp; 90,180,270</td>
      <td></td>
      <td>x</td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;arbitrary</td>
      <td></td>
      <td></td>
      <td></td>
      <td>x</td>
    </tr>
    <tr>
      <td><strong>Quality</strong></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp; native</td>
      <td>x</td>
      <td>x</td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;color</td>
      <td></td>
      <td></td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;grey</td>
      <td></td>
      <td></td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;bitonal</td>
      <td></td>
      <td></td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td><strong>Format</strong></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;jpg</td>
      <td></td>
      <td>x</td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;jp2</td>
      <td></td>
      <td></td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;png</td>
      <td></td>
      <td></td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;tif</td>
      <td></td>
      <td></td>
      <td></td>
      <td>x</td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;gif</td>
      <td></td>
      <td></td>
      <td></td>
      <td>x</td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;pdf</td>
      <td></td>
      <td></td>
      <td></td>
      <td>x</td>
    </tr>

    <tr>
      <td><span style="font-weight: bold;">Image Information
&nbsp;Request</span></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp; json response</td>
      <td>x</td>
      <td>x</td>
      <td>x</td>
      <td></td>
    </tr>
    <tr>
      <td>&nbsp; xml response</td>
      <td>x</td>
      <td>x</td>
      <td>x</td>
      <td></td>
    </tr>
  </tbody>
</table>

<h2 id="level0">3. Level 0 Compliance</h2>
Servers indicate compliance with level 0 by including the following
header in IIIF responses:

<div class="urltemplate">Link:
&lt;http://library.stanford.edu/iiif/image-api/compliance.html#level0&gt;;rel="profile"</div>

<br>
A level 0 compliant image server MAY specify scaling_factors and/or
tile_width and tile_height values in the Image information response. At
Level 0 compliance, a server is only required to deliver images of
sizes computed using the scaling factors declared in the Image
Information response. If
specified they should be interpreted with the following special
meanings:
<ul>
  <li>scaling_factors -
only the specified scaling factors are supported</li>
  <li>tile_width,
tile_height - clients should request only regions that correspond to
output tiles of the specified dimensions</li>
</ul>
If a client requests an scaling or region outside these parameters then
the image server MAY reject the request with a 400 Bad Request error.<br>


<h2 id="level1">4. Level 1 Compliance</h2>
Servers indicate compliance with level 1 by including the following
header in IIIF responses:

<div class="urltemplate">Link:
&lt;http://library.stanford.edu/iiif/image-api/compliance.html#level1&gt;;rel="profile"<br>
</div>

<h2 id="level2">5. Level 2 Compliance</h2>

Servers indicate compliance with level 2 by including the following
header in IIIF responses:
<div class="urltemplate">Link:
&lt;http://library.stanford.edu/iiif/image-api/compliance.html#level2&gt;;rel="profile"<br>
</div>

</div>

</section>
