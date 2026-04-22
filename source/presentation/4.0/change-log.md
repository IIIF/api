---
title: Presentation API 4.0 Change Log
layout: spec
tags: [presentation-api, change-log]
cssversion: 2
---

# IIIF Presentation API 4.0 Change Log

This document accompanies the IIIF Presentation API Specification, Version 4.0, and describes the changes made in this major release, including backwards incompatible modifications from version 3.0.

---

## 1. Breaking Changes

### 1.1. Classes

#### 1.1.1. Introduce an abstract Container class with three concrete subtypes

Version 3.0 used Canvas as the single container class for all content, relying on optional `height`, `width`, and `duration` properties to accommodate both spatial (image) and temporal (audio) use cases. This created ambiguity: an audio-only Canvas carries no meaningful spatial dimensions, but was still modelled as a two-dimensional surface.

Version 4.0 introduces an abstract **Container** class with three concrete subtypes. **Canvas** remains the container for two-dimensional spatial content and may have an optional temporal range. **Timeline** is a new purely temporal container without spatial coordinates, intended for audio-only content; it requires `duration` and has no `height` or `width`. **Scene** is a new unbounded three-dimensional container using a right-handed Cartesian coordinate system; it may also carry `duration` for time-based 3D content.

Canvas-based Manifests conforming to version 3.0 remain valid. Publishers with audio-only resources currently modelled as Canvases without spatial dimensions should migrate those resources to Timeline.

#### 1.1.2. Canvas now requires `height` and `width`

In version 3.0, `height` and `width` were recommended on Canvas but could be omitted for audio resources. Because audio-only content now has its own Timeline container, Canvas `height` and `width` become required in version 4.0. Publishers who previously omitted these properties on audio Canvases must migrate to Timeline.

### 1.2. Property Renames

#### 1.2.1. Rename `placeholderCanvas` to `placeholderContainer`

The `placeholderCanvas` property introduced in version 3.0 has been renamed `placeholderContainer`. The semantics are unchanged—the referenced Container provides content displayed before the primary resource loads or when it cannot be rendered—but the name now correctly reflects that any Container type (Canvas, Timeline, or Scene) may serve this role.

#### 1.2.2. Rename `accompanyingCanvas` to `accompanyingContainer`

Similarly, `accompanyingCanvas` has been renamed `accompanyingContainer`. The referenced Container still provides supplementary content rendered alongside the primary resource (such as a still image shown during audio playback), but the name is generalised to accommodate the full Container hierarchy.

### 1.3. Protocol

#### 1.3.1. Update context for new major version

The JSON-LD context document URI has been updated for the new major version. The `@context` value must be the new 4.0 context URI, or include it as the final item in an array when extension contexts are also present.

---

## 2. Non-Breaking Changes

### 2.1. Three-Dimensional Content

#### 2.1.1. Add Scene as a three-dimensional Container

The Scene Container class represents an infinite three-dimensional space using a right-handed Cartesian coordinate system, with the coordinate origin at (0, 0, 0). Scenes may optionally have `duration`, enabling time-based 3D content such as animations. Content resources and other Containers are positioned within a Scene using Specific Resources with Transform annotations.

Scene provides a first-class container for 3D models, spatial compositions, and interactive three-dimensional experiences, complementing Canvas for two-dimensional and Timeline for audio-only content.

#### 2.1.2. Add Lights for illuminating Scenes

Five light types are defined for Scenes. **AmbientLight** provides non-directional uniform illumination across the entire Scene. **DirectionalLight** simulates a distant source with parallel rays from a specified direction. **PointLight** radiates from a specific position in all directions. **SpotLight** emits a cone of light from a position and direction, with a configurable angle. **ImageBasedLight** uses an environment map to provide both illumination and reflections, enabling physically-based rendering.

Scenes should include at least one light; clients may supply a default if none is specified.

#### 2.1.3. Add Cameras for viewpoints into Scenes

Two Camera types define viewpoints into Scene space. **PerspectiveCamera** simulates the human eye with a field-of-view angle and near/far clipping planes. **OrthographicCamera** uses parallel projection, useful for technical, architectural, or orthographic visualisations. Cameras specify their position and orientation, and the client presents this viewpoint to the user on load.

#### 2.1.4. Add Audio Emitters for spatial audio in Scenes

Three audio emitter types enable spatially-positioned audio within Scenes. **AmbientAudio** applies equally throughout the Scene regardless of viewer position. **PointAudio** emanates from a specific three-dimensional position, with volume attenuating by distance. **SpotAudio** emits a cone of audio from a position and direction with a configurable angle. Emitters have `source` and `volume` properties, associating them with audio content resources.

#### 2.1.5. Add Transforms for positioning content within Scenes

Three Transform types modify the local coordinate space when placing content inside a Scene. **TranslateTransform** moves the origin to a new position. **RotateTransform** rotates around a named axis by a given angle. **ScaleTransform** scales dimensions uniformly or independently per axis. Transforms are specified as part of Specific Resource descriptors in painting Annotations, and are applied in the order listed.

#### 2.1.6. Add AnimationSelector for three-dimensional content

The AnimationSelector enables referencing a named animation embedded within a 3D model resource. This supports interactive 3D content where specific animations are activated based on user interaction or scripted viewing sequences.

#### 2.1.7. Add `interactionMode` for Containers

The `interactionMode` property specifies how users are expected to interact with a Container's content. This is particularly relevant for Scene-based content where interaction models (guided tour, free exploration, and so on) differ substantially from the passive consumption of image or audio content.

### 2.2. New and Revised Selectors

#### 2.2.1. Add WktSelector for ISO standard geometries

The WktSelector accepts Well-Known Text (WKT) geometry strings to identify regions within Canvases or positions within Scenes. It supports two-dimensional polygons and multipolygons as well as three-dimensional geometries, enabling precise and complex spatial selections that rectangular fragment identifiers cannot express.

#### 2.2.2. Add AudioContentSelector and VisualContentSelector

AudioContentSelector and VisualContentSelector select, respectively, only the audio or only the visual track from a combined audio-visual resource such as a video file. This enables, for example, painting only the audio component of a video file onto a Timeline, or presenting the visual component of a video independently of its audio.

#### 2.2.3. Incorporate ImageApiSelector into the core specification

The ImageApiSelector, previously defined as an extension, is incorporated into the core specification. It allows Specific Resources to reference an image through IIIF Image API parameters rather than a pre-formed URI, enabling resolution-independent and crop-aware image references.

### 2.3. New Properties

#### 2.3.1. Add `backgroundColor` on Containers

The `backgroundColor` property specifies the background colour for a Container as a hex RGB value (e.g., `#ffffff`). Clients should render this colour behind any content painted onto the Container. This is useful when the background colour of an object is significant, such as an artwork customarily displayed against a particular ground, or a film that begins and ends on black.

#### 2.3.2. Add `spatialScale` on Canvas

The `spatialScale` property maps the coordinate units of a Canvas to real-world physical measurements using the new Quantity class. This enables publishers to express the actual physical dimensions of a depicted object, supporting applications such as on-screen measurement tools, comparison views across objects of different scales, and augmented-reality placement.

#### 2.3.3. Add `provides` for accessibility feature declarations

The `provides` property declares what accessibility features a resource makes available, such as subtitles, captions, audio description, or sign language. This allows clients to present this information to users and to make appropriate interface choices before a resource is loaded or rendered.

#### 2.3.4. Incorporate `navPlace` into the core specification

The `navPlace` property, previously available as a registered community extension, is incorporated into the core specification in version 4.0. It accepts GeoJSON Feature or Feature Collection values and enables geographic navigation interfaces for Collections and Manifests. This complements the existing `navDate` property, which serves the equivalent role for temporal navigation.

#### 2.3.5. Add `fileSize` on content resources

The `fileSize` property declares the size of a content resource in bytes. This allows clients to present file-size information to users before they choose to download or stream a resource, and to make informed decisions about network usage.

### 2.4. Data Model Additions

#### 2.4.1. Add the Quantity class for dimensioned numerical values

The Quantity class pairs a numerical value (`quantityValue`) with a unit of measurement (`unit`). It is used by `spatialScale` and by other properties where a bare number is insufficient without knowing its unit. This avoids encoding unit information in property names and enables unambiguous machine processing of physical measurements.

#### 2.4.2. Reintroduce Collection paging via Collection Page

A Collection Page class, based on the Activity Streams paging model, enables large Collections to be distributed across multiple HTTP responses. Paging was removed from version 3.0 on the grounds that it was not implemented and was insufficiently specified. Version 4.0 reintroduces it with a clearer definition aligned with Activity Streams conventions.

---

## 3. Editorial Changes

### 3.1. Specification divided into two documents

Version 4.0 is published across two documents: a main specification page covering the purpose, use cases, worked examples, and property-by-property definitions; and a separate data model page covering the formal class hierarchy, processing rules, embedding and referencing constraints, and technical requirements. This structure distinguishes practical guidance for publishers from the normative model for implementers, and follows the pattern established by other IIIF specifications.
