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

This table summarizes the known values available for use with the [Presentation API][prezi-api] `provides` propery, which defines accessibility functionality that a linked resource enables for its target, describing why and how a client might use it rather than what the resource is by type or format. The current approved values are defined by Schema.org's [Accessibility Properties for Discoverability Vocabulary][schema-accessibility] and the IIIF Community.

| Value                       | Description | Source |
| ------------------------------ | |
| `closedCaptions` | ... | Schema.org |
| `alternativeText` | ... | Schema.org |
| `audioDescription` | ... | Schema.org |
| `longDescription` | ... | Schema.org |
| `signLanguage` | ... | Schema.org |
| `highContrastAudio` | ... | Schema.org |
| `highContrastDisplay` | ... | Schema.org |
| `braille` | ... | Schema.org |
| `tactileGraphic` | ... | Schema.org |
| `transcript` | ... | Schema.org |
| `translation` | ... | IIIF |
| `subtitles` | ... | IIIF |
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
