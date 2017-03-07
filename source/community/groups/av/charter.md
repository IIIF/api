---
title: "IIIF A/V Technical Specification Group Charter"
layout: spec
tags: []
cssversion: 2
---


## Introduction

While IIIF has focused primarily on Image based content, there has always been interest around the community in extending the paradigm to include Video and Audio resources, following the same successful pattern as for Images. Early experiments in this direction included the linking of audio segments to the regions of a canvas that depict a musical score and linking video of commentary about the resource. More recently, the British Library was successful in obtaining a grant to work on preserving and making accessible audio content, with explicit resourcing for advancing IIIF's specifications in this area.

The IIIF A/V Technical Specification Group will create technical specifications that enable interoperability of access to audio and video content following the same [design principles][design-principles] as existing IIIF specifications, allowing the integration of that content with the Presentation API. The group will assist with and steer the implementation of community infrastructure, such as reference implementations and validators, as well as transformation tools to generate the required data from existing systems and APIs.

If successful, the work will enable the same degree of interoperability for audio and video resources as the community has already provided for image based resources. This will create greater access to our digital and digitized time-based cultural heritage.

## Scope

The scope of the group's efforts is divided into two primary areas, access to the bitstreams of the audio and video content, and integration with and extension of the existing Presentation API to accommodate its appropriate rendering.

Work that is initially out of scope for this group includes the creation of client-side integration tooling for existing third party APIs, such as controlling site-specific videos in the same way as more HTML5-friendly content. While useful, this would be dependent on the API version of the third party systems, over which we have no control or method of providing feedback. This is more suitable for the "shimming" process or re-hosting of the content.

The group commits to following the requirements for the [IIIF specification process][editorial-process], including the production of two independent implementations of each feature specified, and to reach out to other communities for feedback and to encourage adoption.


### 1. Presentation API Extension

As outlined in the [IIIF AV - Content APIs and the Presentation API][av-gist] document, the Presentation API and its underlying model, Shared Canvas, will be updated to include the missing facilities for time-based media. In particular, the following significant changes are anticipated:

 * Add a duration dimension to Canvases, and make height/width non-mandatory
 * ViewingHints for transitions between canvases
 * Recast the Annotation section as a separate cookbook, and define A/V annotation patterns such as captions
 * Update the Annotation model to W3C standard, and adopt further community conventions

Anticipated Deliverables:

 * Recommendations for version 3.0 of the Presentation API to enable the rendering of time-based media
 * Examples of and recipes for using the Presentation API 3.0 to express A/V use cases
 * Reference implementations of the API
 * Updated validation services for the new version

### 2. Audio and Video Content APIs

The Audio and Video Content APIs will mirror the existing Image API in function - they provide interoperable access to temporal and spatial segmentation and transformation of the content to enable its use and reuse in multiple contexts. This has the same division as the Image API between access to the bits and a JSON-LD description of the features provided by the service. Because, unlike images, audio and video may be played back in a streaming fashion by browsers without need of server-side temporal and spatial segmentation, Audio and Video Content APIs may not be necessary for basic “level 0” use cases supported directly through the Presentation API.In work on both the Presentation and Content APIs, the interactions are to focus on web-based delivery of the content, but not to the exclusion of non-browser-based client systems.

Anticipated Deliverables:

 * Specification for Audio and Video APIs that provide access to audio and video bitstreams
 * Reference implementations of those APIs
 * Examples of and recipes for using Audio and Video Content APIs to express A/V use cases
 * Validation services for those APIs

## Development Roadmap:

 * Q2 2016: Initial workshop, group formation
 * Q3-4 2016: Use Case discussion and research
 * Q1-2 2017: Alpha draft of Presentation API 3.0 recommendations to support A/V
 * Q3-4 2017: Beta draft of Presentation API 3.0 recommendations to support A/V, Alpha Audio/Video Content APIs
 * Q1-2 2018: Alpha2 Audio/Video Content APIs
 * Q3 2018: Beta Audio/Video Content APIs, V3.0 Presentation API with validators, implementations
 * Q4 2018: V1.0 for Audio/Video Content APIs with validators, implementations


## Communication Channels

* Email: [IIIF-Discuss][iiif-discuss], subject line: \[AV\]
* Slack: [#av][av-slack]
* Github: https://github.com/IIIF/iiif-av
* Calls: Biweekly, Tuesday 9am PST / Noon EST: [https://bluejeans.com/222002812][https://bluejeans.com/222002812]
* Face to Face: IIIF Conference and WG meetings, others as coincidental travel allows, including:
   * April 2016: Workshop at British Library
   * Feb 2017: Invited workshop at British Library
   * 6-9 June 2017: IIIF Conference at the Vatican
   * Mid-October 2017: IIIF working groups meeting (TBD)
   * Fall 2017 British Library Mellon grant meeting (TBD)
   * Spring 2018 British Library Mellon grant meeting (TBD)
   * Fall 2018 British Library Mellon grant meeting (TBD)

## Community Support

### Organizations

* British Library
* Cornell University
* Digirati
* Harvard University
* Indiana University
* J. Paul Getty Trust
* National Library of Israel
* National Library of Wales
* North Carolina State University Libraries
* Oxford University
* Princeton University
* Yale Center for British Art

### Technical Editors

* Michael Appleby
* Tom Crane
* Rob Sanderson
* Jon Stroop
* Simeon Warner

[av-slack]: https://iiif.slack.com/messages/av/details/
[iiif-discuss]: https://groups.google.com/forum/#!forum/iiif-discuss
[design-principles]: http://iiif.io/api/annex/notes/design_patterns/
[editorial-process]: http://iiif.io/api/annex/notes/editors/
[av-gist]: https://docs.google.com/document/d/1X7b7zQGDsiEvAfvb1WboDXe360mz7Zmm0o0LT43nozk/edit
[https://bluejeans.com/222002812]: https://bluejeans.com/222002812

{% include acronyms.md %}
