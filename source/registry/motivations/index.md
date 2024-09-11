---
title: Registry of Motivations
layout: spec
tags: [registry, motivations, specifications]
cssversion: 2
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
- name: Simeon Warner
  ORCID: https://orcid.org/0000-0002-7970-7855
  institution: Cornell University
- name: Dawn Childress
  ORCID: https://orcid.org/0000-0003-2602-2788
  institution: UCLA
- name: Jeff Mixter
  ORCID: https://orcid.org/0000-0002-8411-2952
  institution: OCLC Research
---

## Status of this Document
{:.no_toc}

This document is not subject to [semantic versioning][notes-versioning].
Changes will be tracked within the document.

**Editors:**

{% include api/editors.md editors=page.editors %}

{% include copyright.md %}

## 1. Introduction

This is one of a number of [IIIF registries][registry]. It lists a set of Web Annotation motivations that have been identified as useful for implementations, for the Presentation and Search APIs.  They may be defined by the IIIF community, or outside of it.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]

### 1.1. Disclaimer

The inclusion of entries in this document that are outside of the IIIF domain _MUST NOT_ be interpreted as endorsement, support, or approval from the editors, the IIIF community or any individual. This annex is provided as a registry to advertise the existence of these extensions and attempt to ensure some consistency between implementations for common but not universal requirements.

### 1.2. Inclusion Process

The process for having a new entry added to this registry is [described here][registry-process].

## 2. Requirements for Inclusion

## 3. Registry

This table summarizes the motivations available for use within the current versions of the suite of IIIF specifications. There may be other motivations available for use with older versions of the specification.

| Motivation    | Reference |
|--------------------|------|
| `painting`	| [Presentation API: Values for Motivation][prezi30-values-for-motivation] |
| `supplementing` | [Presentation API: Values for Motivation][prezi30-values-for-motivation] |
| `contextualizing` | [Content Search API: Search Term Context][search20-match-context] |
| `contentState` | [Content State API: Form of Annotation][contentstate10-22-form-of-annotation] |
{: .api-table}

Additional motivations are available from the [W3 Web Annotation motivations][org-w3c-webanno-motivation]. This table includes W3 motivations that are common or recommended for use in IIIF.

| Motivation    | Reference |
|--------------------|------|
| `highlighting` | [Content Search API: Search Term Highlighting][search20-match-highlighting] |
| `commenting`	| [Recipe: Simplest Annotation](https://iiif.io/api/cookbook/recipe/0266-full-canvas-annotation/) |
| `tagging`	| [Recipe: Simple Annotation - Tagging](https://iiif.io/api/cookbook/recipe/0021-tagging/) |

## Appendices

### A. Acknowledgements

Thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### B. Change Log

| Date       | Description                                        |
| ---------- | -------------------------------------------------- |
| 2022-11-15 | Add links to Content Search motivations |
| 2022-05-26 | Add known motivations, plus new `contextualizing` motivation |
| 2020-06-03 | New Version 3 Registries                           |

{% include acronyms.md %}
{% include links.md %}
