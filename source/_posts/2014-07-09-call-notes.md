---
title: IIIF Conference Call Meeting Minutes, 9 July 2014
author: Jon Stroop
date: 2014-07-09
tags: [minutes, meetings]
layout: post
---

* contents (will be replaced by macro)
{:toc}

Agenda
------
 1. Introductions [5-10 minutes]
 2. Logistics [5-10 minutes]
 3. Image API 2.0 Changes [As needed]
 4. Presentation API 2.0 Changes [As needed, if time allows]

Minutes
-------

### Introductions / Attendees

 * Ben Albritton (Stanford)
 * Mike Appleby (Yale)
 * Kevin Clarke (UCLA)
 * Shaun Ellis (Princeton)
 * Sean Martin (Freelance?)
 * Matt McGrattan (Oxford)
 * Rob Sanderson (Stanford) __(Convenor)__
 * Edward Silverton (Digirati)
 * Rashmi Singhal (HarvardX)
 * Stu Snydman (Stanford)
 * Randy Stern (Harvard)
 * Jon Stroop (Princeton) __(Notes)__
 * Ken Tsang (British Library)
 * Simeon Warner (Cornell)
 * Drew Winget (Stanford)

Rob gave an extra welcome to Kevin Clarke, as it was his first IIIF call. He also noted some of the regular attendees that were missing.

### Scope / Purpose of Calls

Rob Outlined the following:

 * Scope of meetings is both the APIs and the evolution of tools that implement IIIF specification.
 * Meetings serve to document the processes and progression of IIIF.
 * Minutes will be distributed on [IIIF-Discuss][iiif-discuss] and posted to the website as [news items][news].
 * __Attendees who share information or URLs on the call that should not be shared publicly should make it clear during the call!__
 * The agenda is open and a call for topics will be sent out to [IIIF-Discuss][iiif-discuss] the week prior to the call.

### Image API Discussion

The following changes were dicussed (see the [changelog][image-changelog] for details). There were generally no challenges to these changes from the attendees, though some clarifications were required:

 * Quality name changes (`native` to `default`, `grey` to `gray`). This is a significant breaking change, the former to clarify and avoid the implication that there is a 'source image', the latter to use American English consistently (i.e. the spec uses "color" not "colour")
 * The addition of mirroring: adding an exclamation mark ("!") to the front of the rotation segement of hte URI will mirror the image on the vertical axis. Use cases are:
   * Digitized negatives (Stroop)
   * "Reflection" images for carousels and the like (Sanderson)
 * Changes to info.json
   * Addition of protocol
   * Context reflects major version (`/2/`) only
   * Addition of `sizes` array:
      * `viewing_hint` is optional
      * Pre-caching (for better performance) of the specified sizes is implied, but only as a best practice (question raised by Winget)
   * New `tiles` syntax serves to clarify that `scale_factors` applies to tiles, and `sizes` applies to the full image. Addionally, different scale factors can have different tile sizes, and `height` is optional (assumed to be same as `width` if not reported.)
   * `profile` allows implementations to indicate which features they implement in between compliance levels, and option features (solves the "I'm almost level 2 compliant" problem)
   * We ran out of time before `service` could be discussed.

Actions
-------

 * Editors should review the discussion (especially of info.json) to see if there are clarifications that should be made.
 * Discuss `service` applies to both APIs on next call
 * Discuss Presentation API changes on next call

[iiif-discuss]: mailto:iiif-discuss@googlegroups.com
[news]: /news/
[image-changelog]: /api/image/2.0/change-log/
