---
title: "Image API 3.0 Implementation Notes"
layout: spec
cssversion: 2
redirect_from:
  - /api/image/3/implementation.html
---

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

## 1. HTTP implementation

  * For use cases that enable the saving of the image, use the HTTP `Content-Disposition` header ([RFC6266][org-rfc-6266]) to provide a convenient filename that distinguishes the image, based on the identifier and parameters provided.
  * Server implementations may rely on components or frameworks that unescape the URI path, such as Python's [WSGI][org-wsgi-pep333]. In such situations, the requested URI may be parsed from the right in order to handle identifiers possibly containing slashes, given the knowledge of the API parameters and the prefix for which the server handles requests.
  * See also [Apache HTTP Server implementation notes][notes-apache] that are relevant to the Image API and other IIIF specifications.

## 2. Linked data implementation

  * Linked data implementations may construct the `info.json` response using the frame supplied in the [JSON-LD framing implementation note][annex-json-ld].

## 3. Tile region parameter calculation

When requesting image tiles, the [Region][image3-region] and [Size][image3-size] parameters must be calculated to take account of partial tiles along the right and lower edges for a full image that is not an exact multiple of the scaled tile size. The algorithm below is shown as Python code and assumes integer inputs and integer arithmetic throughout (ie. remainder discarded on division). Inputs are: size of full image content `(width,height)`, scale factor `s`, tile size `(tw,th)`, and tile coordinate `(n,m)` counting from `(0,0)` in the upper-left corner. Note that the rounding method is implementation dependent.

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

## 4. Maximum size calculation

If a server implementation constrains maximum sizes with `maxWidth`, `maxHeight` and/or `maxArea` (defined in [Technical Properties][image3-technical-properties]) then the implementation must check the size of the extracted region when handling the [Size][image3-size] parameter:

  * If the `max` size parameter is specified then the implementation must check the default or full size of the extracted region against the constraints. If the size is constrained, the extracted region is scaled to a smaller size.
  * If another size parameter is used then the implementation must check the size of the resulting scaled image content against the constraints. If the size is constrained, the extracted and scaled region is further scaled to a smaller size.

The [specification][image3-technical-properties] does not define the algorithm by which a constrained image is scaled to fit within the constraints. Image servers may implement algorithms that scale images to match the constraints as closely as possible, or may implement algorithms that scale images with a focus on preserving the aspect ratio which might result in smaller dimensions.

The following Python code takes image content dimensions `width,height` and optional constraints `maxWidth`, `maxWidth`, `maxHeight`. It returns a image content size `w,h` that is within, but close to the constraints.

``` python
    # default without constraints
    (w, h) = (width, height)
    # use size constraints if present, else full
    if maxArea and maxArea < (w * h):
        # approximate area limit, rounds down to avoid possibility of
        # slightly exceeding maxArea
        scale = (float(maxArea) / float(w * h)) ** 0.5
        w = int(w * scale)
        h = int(h * scale)
    if maxWidth:
        if not maxHeight:
            maxHeight = maxWidth
        if maxWidth < w:
            # calculate wrt original width, height rather than
            # w, h to avoid compounding rounding issues
            w = maxWidth
            h = int(float(height * maxWidth) / float(width) + 0.5)
        if maxHeight < h:
            h = maxHeight
            w = int(float(width * maxHeight) / float(height) + 0.5)
```

## 5. Image size calculation for rotated images

As described in [Rotation][image3-rotation], in order to retain the size of the requested image contents, rotation will change the width and height dimensions of the image returned. A formula for calculating the dimensions of the image returned for a given starting size and rotation is given below. Note that the rounding method is implementation dependent and that some languages require conversion of the angle from degrees to radians.

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

{% include links.md %}
{% include acronyms.md %}
