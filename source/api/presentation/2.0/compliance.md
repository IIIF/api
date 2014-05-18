---
title: Presentation API Compliance
title_override: "IIIF Presentation API 2.0 DRAFT (Codename: Black Diamond)"
id: presentation-api
layout: sub-page
categories: [specifications, presentation-api, spec-doc]
major: 2
minor: 0
patch: 0
pre: draft0
---


## NOTES

* protocol? "This ... is Triple I F."
* profile for presentation should be defined in terms of features that client needs to be able to support in order to render the manifest.  As such should it be client capabilities required?
* range subclasses  (toc, start)
* document structure?

* Extension contexts should be first; then IIIF will re-overide any fuckups

* Check Media Frags only allows integers.  A bit screwed with canvases that need floats?


## Server

### Level 1:

A level 1 compliant server is capable of returning a Manifest with the following characteristics:

  * Properties:
    * Response has a single @context property
  	* Manifest MUST have an id, type, label and contain at least one Sequence
  	* The Sequence MUST have a type, and contain at least one Canvas
  	* Every Canvas MUST have an id, type, label, height and width.
  	* Every Canvas SHOULD have at least one image associated with it
  * Content-Type is application/json
  * The CORS header is set


### Level 2:

Returns a Manifest with the characteristics of level 1, plus:
  * Every object has an id
  * The Manifest has a description and at least one metadata field

If available, also returns Annotation Lists:



### Level 3:

Returns descriptions of all resources when dereferencing their ids

supports json-ld conneg




## Client

### Level 0

  * Can import the first sequence as an order for the first image



