---
title: IIIF Conference Call Meeting Minutes, 23 July 2014
author: Simeon Warner
date: 2014-07-23
tags: [minutes, meetings]
layout: post
---

* contents (will be replaced by macro)
{:toc}

Agenda
------
 1. Image API 2.0 Changes 
 2. Presentation API 2.0 Changes [

Minutes
-------

# 2014-07-23 IIIF Call Notes

## Present

  * Michael Appleby
  * Kevin Clarke
  * Tom Crane
  * Chip Goines
  * Matt McGrattan
  * Glen Robson
  * Rob Sanderson (facilitator)
  * Ed Silverton
  * Rashmi Singhal
  * Jon Stroop
  * Ken Tsang
  * Simeon Warner (notes)
  * Drew Winget
  * William Straub
  * Charles Zeng  

## 1. Image API 2.0 Changes and Proposals

### Changes to the `info.json` structure

In 1.1 profiles said "I support this set of features" and there was no way to indicate support for features in a profile, plus some others. This ability was requested and a field `supports` was added to the 2.0 `profiles` to allow addition support to be declared (see <http://iiif.io/api/image/2.0/#image-information>). Servers should be able to generate this information automatically/across the board.

  * This feature can be ignore by server or client is not understood/needed
  * Also provides extension mechanism for extension beyond IIIF API using URIs as opposed to reserved terms (which the JSON-LD context maps to URIs in iiif.io namespace).
  * Tom/Ed - is there and expected format for extra info? No, the URI is the key information. Might usefully resolve to a description but not required and no particular format specified.

Addition of `viewing_hints` for `sizes`: Discussion of the addition of viewing hints to the array of preferred (level1+) or available (level0) sizes. Original idea was sizes as "w,h" strings but that moved to separate width and height. With that move there was a proposal to add an optional `viewing_hint` similar to that used in Presentation API. Idea was to optionally bring out things like "this size appropriate for thumbnail". Latest discussion cast doubt on utility of `viewing_hint` given that one probably needs to use size also. So, is `viewing_hint` useful? If so, what should values be?

  * Charles - why do we need `viewing_hint` at all? Would likely use size instead
  * Michael Appleby - for caching want to drive clients to preferred sizes
  * Tom - thumbnail hint likely the most useful to avoid random size hits on server
  * Simeon - agree with importance of preferred sizes for caching/performance, but think that `viewing_hint` not actually useful in selecting it. Clients better off selecting a preferred
  * Rob - +1 for not needing `viewing_hint` unless it implies something even more preferred than the other preferred sizes
  * Michael - might be good to drive requests to an extra-preferred size
  * Jon - `viewing_hint` optional, is the thumbnail case compelling enough? or just cruft? other use cases?
  * Some unease about subtlety of preferred vs. extra-preferred?
  * Rob - anyone disappointed if we took away `viewing_hint`? Some "no" responses, nobody argued to keep it

Confidence/Provenance of Physical Scale service: Based on feedback from Phil Comstock (Harvard) we've had discussion about additional information about accuracy or the source of the physical scale. Options: 1. Subjective confidence scale (0.0-1.0), 2. String label for source of info, 3. Do nothing (at least for now), 4. Others? Concerns that implementations may not be consistent. If goal is to drive a label then how much specificity is required?

  * Simeon - if we simply want show vs. don't show a ruler, isn't that handled by either including or not including the scale information?
  * Michael - like three levels of confidence for ruler: show, show-with-warning, don't show
  * Michael - separate from machine readable information it might be useful to have a place for a human description
  * Simeon - would that need to include markup for links?
  * Michael - not necessarily. Big difference between "hand measured by curator" and "recorded by machine and checked ever 1000 items"
  * Jon - is there consensus that this information is useful?
  * Michael - yes, this would be useful information for user to assess value. Better to have statement than machine confidence.
  * Drew - yes, confidence of measurements was heavily requested in Mirador demo. Had in mind putting a rating (like 0-4 stars by ruler). Could also add link (warning triangle or question mark) to any description.
  * Michael - argue for some bucketing of confidence (like high/low)
  * Tom/Ed - have good data about dimensions, haven't given though to showing scale reliability but will solicit opinions at Welcome.
  * Tom/Ed - this in service description so we could have multiple service entries for an image? Rob - yes, could conflict. Notes also
  * => more discussion on iiif-discuss

Services and the `@context` discussion with the JSON-LD folk: Issue is that with current structure using embedded `@context` has a problem that is one attempts to re-serialize then only the first context is recovered. Did not discuss further.

## 2. Presentation API 2.0 Changes

Collections - Lots of discussion about how to pass to a client a list of Manifests. Current proposal is Collection with lists Manifests and other Collections (hence hierarchical). Can be used to initialize client with a set of manifests, set of search results, or for navigation via hierarchy (e.g. current Mirador divides by repo but doesn't support hierarchical navigation).

  * Tom/Ed - Wellcome use case is delivering journal with several thousand issues/Manifests. Concerned about scalability for such a large number of Manifests. Mike - tactical solution, probably not ideal for complete collection description unless deep hierarchy used. Rob - Collection doesn't include all info from Manifest, just had link and label (inclusion by ref not value) so scales reasonably well.
  * William - How does this relate to sub-Collections? Mike - set of entries in a Collection can list other Collections giving hierarchy, note UI issues not yet explored.
  * William - Nesting limit? Mike - No limit to levels of nesting, so depending on client paradigm there might be issues with too many
  * Drew - Similar to Layers? Rob - Layers within Manifest, this collects Manifests together
  * Tom/Ed - in their use case need a bit more than just ref/label to construct navigation <http://wellcomeplayer-examples.azurewebsites.net/journal.html>. Player here is getting flat structure and then inferring hierarchy in date or issues. Too niche or too general? General principle is to have lightweight structure that conveys enough structure for viewer to build UI.
  * Glen - notes issues with recommendation that Collections should not be inline which could make some UIs slow.


Other Presentation API 2.0 Changes Postponed for Next Call


