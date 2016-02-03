---
title: "Proposed Breaking Changes"
layout: spec
tags: [annex, presentation-api, image-api]
redirect_from:
  - /api/annex/notes/proposed-changes.html
---

# Introduction

This document records changes that are intended to be made in the future, but must wait for new major releases as they are backwards incompatible.

# Image API

* Require support for the `square` region at compliance level 1. [Issue][square]
* Clarify the semantics of height and width for calculating aspect ratio only, as there is no 'source' image. [Issue][aspectratio]
* Remove support for the `pct:` syntax for the region and size parameters.[Issue][deprecatepct]

# Presentation API

* Require a URI for non sc:painting Annotations. [Issue][nonpainting]
* Update model to use the Web Annotation specifications. [Issue][webanno]
  * Make Choice a list of options in descending priority. [Issue][choice]
  * Make AnnotationList follow Web Annotation list specifications. [Issue][annolist]

[square]: https://github.com/IIIF/iiif.io/issues/501
[aspectratio]: https://github.com/IIIF/iiif.io/issues/477
[nonpainting]: https://github.com/IIIF/iiif.io/issues/456
[webanno]: https://github.com/IIIF/iiif.io/issues/496
[choice]: https://github.com/IIIF/iiif.io/issues/368
[annolist]: https://github.com/IIIF/iiif.io/issues/496
[deprecatepct]: https://github.com/IIIF/iiif.io/issues/478
