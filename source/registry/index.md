---
title: IIIF Registry of Known Extensions
layout: spec
tags: [annex, service, services, specifications]
cssversion: 2
---

# Process

The process for having an entry included in one of the IIIF extension registries is described in the [Process for Adding Entries to Registries][registry-process].

# Registries

## Table of Services and Extensions

This table summarizes the services and extensions available and in which APIs they may be used.

| Icon                       | Meaning     |
| -------------------------- | ----------- |
| ![required][icon3-req]      | Required    |
| ![recommended][icon3-rec]   | Recommended |
| ![optional][icon3-opt]      | Optional    |
| ![not allowed][icon3-na]    | Not Allowed |
{: .api-table #table-reqs-icons}

| Service/Extension | Type       | Image 2 API | Image 3 API | Presentation 2 API | Presentation 3 API |
| ----------------- | ---------- | ----------- | ----------- | ------------------ | ------------------ |
| [Image 2 API][image21]    | service | N/A  | N/A     | ![recommended][icon3-rec] | ![recommended][icon3-rec] |
| [Image 3 API][image-api]  | service | N/A  | N/A     | ![optional][icon3-opt]    | ![recommended][icon3-rec] |
| Image Information         | service | N/A  | N/A     | ![recommended][icon3-rec] | ![recommended][icon3-rec] |
| Search 1                  | service | N/A  | N/A     | ![recommended][icon3-rec] | ![optional][icon3-opt] (prefer search2) |
| Search 2 (in development) | service | N/A  | N/A     | ![not allowed][icon3-na]  | ![recommended][icon3-rec] |
| PhysDim           | service   | ![recommended][icon3-rec] | ![not allowed][icon3-na] | ![recommended][icon3-rec] | ![not allowed][icon3-na] |
| PhysDim           | extension | ![not allowed][icon3-na] | ![recommended][icon3-rec] | ![not allowed][icon3-na]  | ![recommended][icon3-rec] |
| GeoJSON           | service   | ![recommended][icon3-rec] | ![not allowed][icon3-na] | ![recommended][icon3-rec] | ![not allowed][icon3-na] |
| navPlace          | extension | ![not allowed][icon3-na] | ![recommended][icon3-rec] | ![not allowed][icon3-na]  | ![recommended][icon3-rec] |
| Text Granularity  | extension | N/A                      | N/A                       | ![not allowed][icon3-na]  | ![recommended][icon3-rec] |
| [IIIF Authentication API 1.0][auth10] | service   | ![recommended][icon3-rec] |   |   |   |
| Auth 2 (in development) | service | ![not allowed][icon3-na] | ![recommended][icon3-rec] | ![not allowed][icon3-na] | ![recommended][icon3-rec] |
| [IIIF Change Discovery API][discovery-stable-version] | service   | N/A     | N/A     | ![recommended][icon3-rec]| ![recommended][icon3-rec] |
| [IIIF Content State API][contentstate03] | service   |      |      | ![not allowed][icon3-na] | ![recommended][icon3-rec] |
| Image API Selector  | extension |  |  | ![recommended][icon3-rec] | ![recommended][icon3-rec]  |
| Point Selector  | extension | ![not allowed][icon3-na] | ![not allowed][icon3-na] | ![not allowed][icon3-na] | ![recommended][icon3-rec]  |
| Content Selectors | extension | ![not allowed][icon3-na] | ![not allowed][icon3-na] | ![not allowed][icon3-na] | ![recommended][icon3-rec]  |

## Presentation API Registries

* [Behaviors][registry-behaviors]
* [Presentation API Extensions][extensions]
* [Motivations][registry-motivations]
* [Profiles][registry-profiles]
* [Services][registry-services]
* [TimeModes][registry-timeModes]
* [Types][registry-types]
* [ViewingDirections][registry-viewingDirections]

## Image API Registries

* [Image API Extensions][registry-image-extensions]

## Other Registries

The [IIIF Registry of Activity Streams][registry-activity-streams] supports keeping up to date with IIIF resource changes according to the [IIIF Change Discovery API][discovery-api].

{% include acronyms.md %}
{% include links.md %}
