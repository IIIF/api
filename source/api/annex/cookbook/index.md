---
title: Presentation API Cookbook
layout: spec
tags: [annex, service, services, specifications]
cssversion: 2
---

# Cookbook of Presentation API Recipes

The [IIIF Presentation API][prezi3] specifies a standardised way to describe complex digitial objects. The resource types and properties of the specification are the building blocks of interoperable representations, for rendering by viewers and other software clients. This cookbook gathers together many examples of these representations (usually IIIF Manifests), in order to:

* provide many more examples than the specification alone can do, for reference and learning;
* encourage publishers to adopt common patterns in modelling classes of complex objects;
* enable client software developers to support these patterns, for consistency of user experience (when desirable);
* demonstrate the applicability of IIIF to a broad range of use cases.

# Process

Anyone can submit a recipe to the cookbook. (TRC role...)

Recipes should not be substantially the same as an existing recipe (though may well demonstrate an extension of an existing recipe and therefore reproduce it).

A recipe must have the following features:

* A short and clear name
* A use case (why the pattern is important to include)
* Implementation notes
    * with references to the specifcation and other recipes
* All referended content resources, external annotations and other links should resolve: they must exist on the web or be included in the submitted recipe. Any client that implements support for a recipe should expect the published recipe to work
* Restrictions (optional): where this pattern is usable or not usable, with explanation
* A full example, comprising:
    * A prose description;
    * code samples (JSON-LD representation, following the formatting instructions (todo)
* See also: similar or otherwise related recipes


# The Recipes

## Building a manifest in stages, adding more complexity at each stage

_The corresponding 2.1 test fixture(s) is given like this, where appropriate: ..(3,5)_

* Minimum Viable Manifest (1) (use static image as content resource, w.h)
* Minimum Viable Manifest (1) (use single audio as content resource, d)
* Minimum Viable Manifest (1) (use single video as content resource, w,h,d)
* Image different size to canvas (26)
* Image Service for single image (24,25)
* metadata and summary (2,5)
* Multiple values and languages (3,4,6)
* Multiple formats of strings (text, html, markdown...?) (64)
* Rights statement(s) (7)
* Book (simplest, > 1 canvas) (19)
* Book (viewingDirection variations) (11,12,13,14)
* Book (paging variations) (15,16,17) 
* thumbnail algorithm / discussion
* Alternative sequences, applications of (20,22,23)
* museum object (fwd ref to renderings)
* video - more complex examples
* audio - more complex examples 
* placeholderCanvas
* accompanyingCanvas
* start (65)

## Textual and other supplementary content

* Transcription of image-based content - various examples gathered (43,44,45,46,47,48)
* Transcription of audio and video

## Other kinds of annotations 
_(leading on to segmentation examples later)_

* comments - various examples (51,52,54)
* Fragment selectors (61)
* tagging
* hotspot linking
* Annotation in the context of a particular content resource https://github.com/IIIF/iiif-stories/issues/101

## Internal structure

* table of contents (ranges) - book chapters
* table of contents (ranges) - articles in a newspaper
* table of contents (ranges) - acts of an opera
* Alternative Sequence (via `sequence` Range)
* `sequence` Range with partial canvases
* metadata on any resource (21)

## Higher-level structure

* multi-volume work
* bound multi-volume work
* paged Collections (from #1343)

## Segmentation and complex resources

* Choice (simplest) (28)
* Choice - multispectral flavoured example, with image services (29)
* foldouts, etc (Choice or non-paged interlude (flaps vs maps))? 
* Multiple images (master/detail) (30,31)
* Multiple images and multiple choices (32,33,34)
* basic segmentation (crop out scanner) (35,36,37,38)
* Image with CSS Rotation (39)
* Reusing an image service (ImageApiSelector) (41)
* non-rectangular segmentation
* temporal segmentation
* Audio only from video (and other xxxContentSelector scenarios)
* canvas on canvas (#1191)
* detail images 
* CSS styling 

## Linking

* alternative representations (rendering (?))
* Linking from Image API to Presentation API (via partOf as per #600, #1507)
* Linking from Image API to external metadata
* Linking from external metadata to Image API
* Linking from external metadata to Presentation API
* Linking between Presentation API representations
* seeAlso scenarios (incl other manifests) (8)

## Technical 

* extensions (18)
* services (9,10)
* Mixed version scenarios (Prezi 3+Image 2)
* Publishing v2 and v3 versions

## Real-world complex objects (ideally taken from actual collections)

* An Image gallery
* A complex printed work with foldouts and choice
* A music album's audio resources
* ...and its image resoures
* ...combined to demonstrate _together_
* An opera on one Canvas
* An opera on multiple Canvases
* Adaptive bit rate AV examples
* A field recording
* A newspaper
* Example with extensions and services 
* A manuscript with multiple orderings
* a Sammelband
* Archival collection (hierarchy, paging)
* Thumbnail range for video navigation
* Video with captions in multiple languages
* Mixed Image Service references (a mashup, with img2 and img3 services)
* Glenn Gould - score and performance scenarios (transcribing)

## Access Control 
_this might be in a separate auth cookbook_

* probe service for simple resource
* auth for adaptive bit rate media (MPEG-DASH)
* [Anyone can deep zoom, auth reqd for hi-res download](https://digirati-co-uk.github.io/iiif-auth-client/?image=https://iiifauth.digtest.co.uk/img/11_kitty_joyner.jpg/info.json)

{% include acronyms.md %}
{% include links.md %}
