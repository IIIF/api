---
title: Registry of Accessibility Values
layout: spec
tags: [annex, service, services, specifications]
cssversion: 2
editors:
  - name: Michael Appleby
    ORCID: https://orcid.org/0000-0002-1266-298X
    institution: Yale University
  - name: Dawn Childress
    ORCID: https://orcid.org/0000-0003-2602-2788
    institution: UCLA
  - name: Tom Crane
    ORCID: https://orcid.org/0000-0003-1881-243X
    institution: Digirati
  - name: Jeff Mixter
    ORCID: https://orcid.org/0000-0002-8411-2952
    institution: OCLC
  - name: Robert Sanderson
    ORCID: https://orcid.org/0000-0003-4441-6852
    institution: Yale University
  - name: Julie Winchester
    ORCID: https://orcid.org/0000-0001-6578-764X
    institution: Duke University
---

## Status of this Document
{:.no_toc}

This document is not subject to [semantic versioning][notes-versioning].
Changes will be tracked within the document.

**Editors:**

{% include api/editors.md editors=page.editors %}

{% include copyright.md %}

## Abstract
{:.no_toc}
This document lists a set of allowed values for the Presentation API `provides` property that have been identified as useful for implementations, especially related to accessibility. They may be defined by the IIIF community, or outside of it.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]


## 1. Introduction

This is one of a number of [IIIF registries][registry]. It lists a set of allowed values for the Presentation API `provides` property that have been identified as useful for implementations, especially related to accessibility. They may be defined by the IIIF community, or outside of it.

### 1.1. Disclaimer

The inclusion of entries in this document that are outside of the IIIF domain _MUST NOT_ be interpreted as endorsement, support, or approval from the editors, the IIIF community or any individual. This annex is provided as a registry to advertise the existence of these extensions and attempt to ensure some consistency between implementations for common but not universal requirements.

### 1.2. Inclusion Process

The process for having a new entry added to this registry is [described here][registry-process].

## 2. Requirements for Inclusion

## 3. Registry

This table summarizes the known values available for use with the [Presentation API][prezi-api] `provides` property, which defines accessibility functionality that a linked resource enables for its target, describing why and how a client might use it rather than what the resource is by type or format.

The definitions in this table are the definitions of the values for use with `provides`. Where a value originates in an external source, principally the [Accessibility Properties for Discoverability Vocabulary][schema-accessibility] published by the W3C Accessibility Discoverability Vocabulary for Schema.org Community Group, but also others, the Source column links to the original term for reference only; the definition given here takes precedence. Values with the source IIIF are defined by the IIIF Community.

| Value | Definition | Source |
| ----- | ---------- | ------ |
| `closedCaptions`{: #closedCaptions} | Synchronized text of the dialogue together with descriptions of sound effects, relevant musical cues and other relevant audio information. Content that transcribes only the dialogue is `subtitles`. | Adapted from [W3C a11y-discov-vocab CG, §4.2.2.4](https://www.w3.org/community/reports/a11y-discov-vocab/CG-FINAL-vocabulary-20241209/#closedCaptions) |
| `alternativeText`{: #alternativeText} | Textual content to be provided to users that cannot or do not wish to interact with the image, audio or video file directly. | Adapted from [W3C a11y-discov-vocab CG, §4.2.2.1](https://www.w3.org/community/reports/a11y-discov-vocab/CG-FINAL-vocabulary-20241209/#alternativeText) |
| `audioDescription`{: #audioDescription} | Audio narration that describes the visual content of a video or image, for users who cannot see it. | Adapted from [W3C a11y-discov-vocab CG, §4.2.2.2](https://www.w3.org/community/reports/a11y-discov-vocab/CG-FINAL-vocabulary-20241209/#audioDescription) |
| `longDescription`{: #longDescription} | A textual representation of visual, auditory or complex structured data. | Adapted from [W3C a11y-discov-vocab CG, §4.2.2.6](https://www.w3.org/community/reports/a11y-discov-vocab/CG-FINAL-vocabulary-20241209/#longDescription) |
| `signLanguage`{: #signLanguage} | A sign language interpretation of audio or video content. | Adapted from [W3C a11y-discov-vocab CG, §4.2.2.8](https://www.w3.org/community/reports/a11y-discov-vocab/CG-FINAL-vocabulary-20241209/#signLanguage) |
| `highContrastAudio`{: #highContrastAudio} | An alternative form of the audio where the contrast is high, making it easier to hear. | Adapted from [W3C a11y-discov-vocab CG, §4.2.5.1](https://www.w3.org/community/reports/a11y-discov-vocab/CG-FINAL-vocabulary-20241209/#highContrastAudio) |
| `highContrastDisplay`{: #highContrastDisplay} | An alternative form of visual content where the contrast is high, making it easier to see. | Adapted from [W3C a11y-discov-vocab CG, §4.2.5.2](https://www.w3.org/community/reports/a11y-discov-vocab/CG-FINAL-vocabulary-20241209/#highContrastDisplay) |
| `braille`{: #braille} | A braille representation of the content. | Adapted from [W3C a11y-discov-vocab CG, §4.2.6.1](https://www.w3.org/community/reports/a11y-discov-vocab/CG-FINAL-vocabulary-20241209/#braille) |
| `tactileGraphic`{: #tactileGraphic} | A tactile graphic version of visual content, for users who read by touch. | Adapted from [W3C a11y-discov-vocab CG, §4.2.6.2](https://www.w3.org/community/reports/a11y-discov-vocab/CG-FINAL-vocabulary-20241209/#tactileGraphic) |
| `transcript`{: #transcript} | A text transcription of the content of the resource, which is not necessarily synchronized with it. | Adapted from [W3C a11y-discov-vocab CG, §4.2.2.9](https://www.w3.org/community/reports/a11y-discov-vocab/CG-FINAL-vocabulary-20241209/#transcript) |
| `translation`{: #translation} | A translation of the content into another language. | IIIF |
| `subtitles`{: #subtitles} | A transcription or translation of the dialogue only, synchronized with audio or video content. It does not include descriptions of sound effects, music or other non-speech audio; content that does is `closedCaptions`. | Adapted from [HTML Standard, `track` `kind` subtitles](https://html.spec.whatwg.org/multipage/media.html#attr-track-kind-subtitles) |
{: .api-table}


## Appendices

### A. Acknowledgements

Thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### B. Change Log

| Date       | Description                                        |
| ---------- | -------------------------------------------------- |
| 2026-XX-YY | New Version 4 Registries                           |

{% include acronyms.md %}
{% include links.md %}
