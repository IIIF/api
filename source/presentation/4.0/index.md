---
title: "Presentation API 4.0"
title_override: "IIIF Presentation API 4.0"
id: presentation-api
layout: spec
cssversion: 3
tags: [specifications, presentation-api]
major: 4
minor: 0
patch: 0
pre: 
redirect_from:
  - /presentation/index.html
  - /presentation/4/index.html
editors:
  - name: Michael Appleby
    ORCID: https://orcid.org/0000-0002-1266-298X
    institution: Yale University
  - name: Tom Crane
    ORCID: https://orcid.org/0000-0003-1881-243X
    institution: Digirati
  - name: Robert Sanderson
    ORCID: https://orcid.org/0000-0003-4441-6852
    institution: J. Paul Getty Trust
  - name: Dawn Childress
    ORCID:
    institution: UCLA
  - name: Julie Winchester
    ORCID: 
    institution: Duke University
  - name: Jeff Mixter
    ORCID: 
    institution: OCLC
hero:
  image: ''
---

## Status of this Document
{:.no_toc}
__This Version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest Stable Version:__ [{{ site.data.apis.presentation.latest.major }}.{{ site.data.apis.presentation.latest.minor }}.{{ site.data.apis.presentation.latest.patch }}][prezi-stable-version]

__Previous Version:__ [3.0][prezi30]

**Editors:**

{% include api/editors.md editors=page.editors %}

{% include copyright.md %}

----

## Introduction

Presentation, the clue is in the name


(non-exhaustive) List of use cases

1. Digitized books and manuscripts   (images, paged things, transcripts, translations)
2. Artworks and Maps                 (navPlace, maybe commenting annos)
3. Audio and Video recordings        (time-based, transcriptions)
4. 3D scans of objects               (3D)
5. Periodicals                       (Collections, Ranges, navDate)
6. Archival collections              (Collections, Ranges, navDate)
7. Storytelling and exhibitions      (State, annotations)

see Terminology at the end

Mention model.md

Mention cookbook



## Foundations

Simple model diagram

Manifests and Containers briefly


### Manifests

The document, the unit of distribution of IIIF

A sequence of Containers that carry the content.


### Containers

Timeline, Canvas, Scene


### Painting Annotations

Everything is an anno but these are special and core

### Content Resources

Image, Sound, Video, Model, Text 
(see model)

SpecificResource



## Presenting Content Resources - what you came here for

### Images

A painting

A paged thing


### Audio and Video

A timeline - audio only

A video on a Canvas with duration


### 3D

Whale bone with a camera and a light


## Annotations and State

### Annotations

non-painting

Comments, tags, etc

transcripts (and back ref to OCR on images etc)


### State

Content State

Activating annos


## Navigation

### navXXXX

These are just extracts as examples

```json
"navDate": "1776-01-01T00:00:00+00:00",
```

See this in Periodicals



```json
"navPlace": {
  "id": "https://iiif.io/api/cookbook/recipe/0318-navPlace-navDate/feature-collection/1",
  "type": "FeatureCollection",
  "features": [
    {
      "id": "https://iiif.io/api/cookbook/recipe/0318-navPlace-navDate/feature/1",
      "type": "Feature",
      "properties": {
        "label": { "en": ["Castel Sant'Angelo, Rome"] }
      },
      "geometry": {
        "type": "Point",
        "coordinates": [12.4663, 41.9031]
      }
    }
  ]
}
```
Map example

navDate
??? example


### Ranges

Periodical example - with navDate again
Table of Contents as simple example
thumbnail-nav
sequence


### Collections

Multi-vol work
Archive example
back ref to periodical?

Paged collections and conceptual collections




## Protocol



## Terminology

The principles of [Linked Data][org-linked-data] and the [Architecture of the Web][org-w3c-webarch] are adopted in order to provide a distributed and interoperable framework. The [Shared Canvas data model][shared-canvas] and [JSON-LD][org-w3c-json-ld] are leveraged to create an easy-to-implement, JSON-based format.

This specification uses the following terms:

* __embedded__: When a resource (A) is embedded within an embedding resource (B), the complete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will not result in additional information. Example: Canvas A is embedded in Manifest B.
* __referenced__: When a resource (A) is referenced from a referencing resource (B), an incomplete JSON representation of resource A is present within the JSON representation of resource B, and dereferencing the URI of resource A will result in additional information. Example:  Manifest A is referenced from Collection B.
* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

The terms _array_, _JSON object_, _number_, _string_, and _boolean_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].
