---
title: "Image API 3.0 Implementation Notes"
layout: spec
cssversion: 2
redirect_from:
  - /api/image/3/implementation.html
---

## Image API Implementation Notes

  * For use cases that enable the saving of the image, use the HTTP `Content-Disposition` header ([RFC6266][rfc-6266]) to provide a convenient filename that distinguishes the image, based on the identifier and parameters provided.
  * Server implementations may rely on components or frameworks that unescape the URI path, such as Python's [WSGI][wsgi]. In such situations, the requested URI may be parsed from the right in order to handle identifiers possibly containing slashes, given the knowledge of the API parameters and the prefix for which the server handles requests.
  * Additional [Apache HTTP Server implementation notes][apache-notes] are available.
  * Linked data implementations may construct the info.json response using the frame supplied in the [JSON-LD framing implementation note][annex-frames].
  * When requesting sizes using the `w,` canonical syntax, if a particular height is desired, the following algorithm can be used:

``` python
    # Calculate request width for `w,` syntax from desired height
    request_width = image_width * desired_height / image_height
```

  * When requesting image tiles, the [Region][region] and [Size][size] parameters must be calculated to take account of partial tiles along the right and lower edges for a full image that is not an exact multiple of the scaled tile size. The algorithm below is shown as Python code and assumes integer inputs and integer arithmetic throughout (ie. remainder discarded on division). Inputs are: size of full image content `(width,height)`, scale factor `s`, tile size `(tw,th)`, and tile coordinate `(n,m)` counting from `(0,0)` in the upper-left corner. Note that the rounding method is implementation dependent.


``` python
    # Calculate region parameters /xr,yr,wr,hr/
    xr = n * tw * s
    yr = m * th * s
    wr = tw * s
    if (xr + wr > width):
        wr = width - xr
    hr = th * s
    if (yr + hr > height):
        hr = height - yr
    # Calculate size parameters /ws,hs/
    ws = tw
    if (xr + tw*s > width):
        ws = (width - xr + s - 1) / s  # +s-1 in numerator to round up
    hs = th
    if (yr + th*s > height):
        hs = (height - yr + s - 1) / s
```

  * As described in [Rotation][rotation], in order to retain the size of the requested image contents, rotation will change the width and height dimensions of the image returned. A formula for calculating the dimensions of the image returned for a given starting size and rotation is given below. Note that the rounding method is implementation dependent and that some languages require conversion of the angle from degrees to radians.

``` python
    # (w,h) are size parameters, n is rotation angle
    w_returned = abs(w*cos(n)) + abs(h*sin(n))
    h_returned = abs(h*cos(n)) + abs(w*sin(n))
```

## Appendices

###  A. Change Log

| Date       | Description |
| ---------- | ----------- |
| 2018-02-20 | Extracted from Image API and updated |
{: .api-table .first-col-normal}

[region]: {{ site.url }}{{ site.baseurl }}/api/image/3.0/#region "4.1. Region"
[size]: {{ site.url }}{{ site.baseurl }}/api/image/3.0/#size "4.2. Size"
[rotation]: {{ site.url }}{{ site.baseurl }}/api/image/3.0/#rotation "4.3. Rotation"
[wsgi]: https://www.python.org/dev/peps/pep-0333/
[rfc-6266]: http://tools.ietf.org/html/rfc6266 "Use of the Content-Disposition Header Field in the Hypertext Transfer Protocol (HTTP)"
[apache-notes]: {{ site.url }}{{ site.baseurl }}/api/annex/notes/apache/ "Apache HTTP Server Implementation Notes"
[annex-frames]: {{ site.url }}{{ site.baseurl }}/api/annex/notes/jsonld/ "JSON-LD Frames Implementation Notes"

{% include acronyms.md %}
