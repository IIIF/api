---
title: "Scheduled Changes"
layout: spec
tags: [annex, presentation-api, image-api]
---

# Introduction

This document records scheduled changes that are intended to be made in the future, but must wait for new major releases as they're backwards incompatible.

# Image API

* Require support for the `square` region at compliance level 1. [Issue][square]
* Clarify that height and width are for calculating aspect ratio only, as there is no 'source' image. [Issue][aspectratio]

# Presentation API

* Require a URI for non sc:painting Annotations [Issue][nonpainting]
* Update model to use the Web Annotation specifications [Issue][webanno]
  * Make Choice a list of options in descending priority [Issue][choice]
  * Make AnnotationList follow Web Annotation list specifications [Issue][annolist]

[square]: https://github.com/IIIF/iiif.io/issues/501
[aspectratio]: https://github.com/IIIF/iiif.io/issues/477
[nonpainting]: https://github.com/IIIF/iiif.io/issues/456
[webanno]: https://github.com/IIIF/iiif.io/issues/496
[choice]: https://github.com/IIIF/iiif.io/issues/368
[annolist]: https://github.com/IIIF/iiif.io/issues/496

