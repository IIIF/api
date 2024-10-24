---
title: Registry of Rights Statements and Licenses
layout: spec
tags: [registry, rights, specifications]
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
  institution: Yale University
- name: Dawn Childress
  ORCID: https://orcid.org/0000-0003-2602-2788
  institution: UCLA
- name: Jeff Mixter
  ORCID: https://orcid.org/0000-0002-8411-2952
  institution: OCLC Research
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

## 1. Introduction

This is one of a number of [IIIF registries][registry]. It lists a set of rights statements and licenses for use across the IIIF APIs that have been identified as useful for implementations.  They may be defined by the IIIF community, or outside of it.

Please send feedback to [iiif-discuss@googlegroups.com][iiif-discuss]

### 1.1. Disclaimer

The inclusion of entries in this document that are outside of the IIIF domain _MUST NOT_ be interpreted as endorsement, support, or approval from the editors, the IIIF community or any individual. This document is provided as a registry to advertise the existence of these extensions and attempt to ensure some consistency between implementations for common but not universal requirements.

### 1.2. Inclusion Process

The process for having a new entry added to this registry is [described here][registry-process].

## 2. Requirements for Inclusion

## 3. Registry

This table summarizes the known rights statements and licenses available for use with the IIIF APIs.

| Source  | URIs | Notes |
| ------------------------------ | --------------------- | ------------------|
| Creative Commons | `http://creativecommons.org/licenses/by-nc-sa/4.0/`<br>`http://creativecommons.org/licenses/by/4.0/`<br>For the full list of licenses, see [About CC Licenses](http://creativecommons.org/licenses/). | For usage, see the [Presentation 3.0 Rights][prezi30-rights] section |
| Rights Statements | `http://rightsstatements.org/vocab/InC/1.0/`<br>`http://rightsstatements.org/vocab/InC-NC/1.0/`<br>For the full list of statements, see [Rights Statements](http://rightsstatements.org/page/1.0/). | For usage, see the [Presentation 3.0 Rights][prezi30-rights] section |
{: .api-table}


## Appendices

### A. Acknowledgements

Thanks to the members of the [IIIF][iiif-community] for their continuous engagement, innovative ideas and feedback.

### B. Change Log

| Date       | Description                                        |
| ---------- | -------------------------------------------------- |
| 2024-08-02 | Add existing Creative Commons and RightsStatements to table. |

{% include acronyms.md %}
{% include links.md %}
