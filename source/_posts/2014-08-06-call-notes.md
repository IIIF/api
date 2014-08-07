---
title: IIIF Conference Call Meeting Minutes, 6 August 2014
author: Rob Sanderson / William Straub
date: 2014-08-06
tags: [minutes, meetings]
layout: post
---

* contents (will be replaced by macro)
{:toc}

Agenda
------
 1. Introductions [5 minutes]
 2. Presentation API 2.0 Changes [30 minutes]
 3. Authentiation [25 minutes]

## Introductions / Attendees

 * Ben Albritton (Stanford)
 * Mike Appleby (Yale)
 * Markus Enders (British Library)
 * Stephanie Gehrke (Biblissima)
 * Christy Henshaw (Wellcome)
 * Paul Jones (British Library)
 * Sean Martin (Freelance?)
 * Matt McGrattan (Oxford)
 * Regis Robineau (Biblissima)
 * Glen Robson (National Library of Wales)
 * Mark Patton (Johns Hopkins University)
 * Rob Sanderson (Stanford) __(Convenor)__
 * Rashmi Singhal (HarvardX)
 * William Straub (HMML, St Johns University) __(Notes)__
 * Jon Stroop (Princeton) 
 * Simeon Warner (Cornell)
 * Drew Winget (Stanford)
 * Charles Zeng (Artstor)

Apologies: 

 * Stu Snydman (Stanford)

Welcome new participants: JHU is beginning a new project that will use the shared canvas/IIIF Standard; Markus Enders from the British Library is very interested in the additions that IIIF version 2 will bring; Regis is from Biblissima project working with the French National Library.


## Presentation API Discussion

### Thumbnail, Logo, Related
[link](http://iiif.io/api/presentation/2.0/#linking-properties)

Thumbnails can be associated with an object so users can more easily identify it (use recommended). A logo can be added, e.g. unique distinguishing graphic for a library or university (optional).

__Discussion:__ can links be added to the logo? Answer: not now, and would be difficult. A logo just points to a single image. Discussion: there can only be one logo per page. An example was given of an institution that serves as a clearinghouse, directing users to other repositories from other institutions. In that case, a bulleted list of other institutions would not have logos but could instead have an attribution hold this link data.

### Page turning and table of contents
[link](http://iiif.io/api/presentation/2.0/#ranges)

Ranges (7.1) are a method to provide more structural information about an object beyond sequences. In version 2.0, a range could display a table of contents or top of hierarchy with viewer hints.

Page turning can be set to not be a normal part of the page sequence – so as to not throw off openings.
Viewing hint "start" (later will be renamed "begin") -to skip some amount of content to jump ahead. This was previously discussed as necessary because of course manuscripts depend upon context. However there is a minor bug: if there are multiple sequences and the start canvas is different but not defined in earlier sequential listings, then the first defined" start" hint will always be shown first. 

__Discussion:__ Christy is pretty sure that, for example, the Internet Archive always opens to the title page. Markus said that this is getting away from the object model and wondered if we will also have a printing hint. Example was given of palimpsest. Simeon noted that there are these "buggy edge cases." Rob gave a fuller explanation of the bug after William asked for clarification. Will the “start hint” be kept on the canvas? Markus says that it depends upon the context and further stated that canvases can have multiple sequences. 

Example from Markus, the Homepage of DFG viewer: 
  [http://dfg-viewer.de/demo/](http://dfg-viewer.de/demo/)
and an item in the dfg viewer: 
  [example](http://dfg-viewer.de/show/?tx_dlf%5Bid%5D=http%3A%2F%2Fdbs.hab.de%2Foai%2Fwdb%3Fverb%3DGetRecord%26metadataPrefix%3Dmets%26identifier%3Doai%3Adiglib.hab.de%3Appn_549837965) 
Michael agrees with Simeon and says that it depends upon what the content creator has decided. Rob concluded the discussion by saying that he would take it back to the list since it is more complex, to look at it more closely and give it more thought. 

Do we need to have a blank page indicator? Yes.

Markus brought up the case of multiple images of the same manuscript. Will we need to indicate which should be displayed first? Yes, use "choice" as defined in the API. For example, choice allows creators to default to showing the color image of a manuscript, despite the same manuscript  also being available in black and white. Cf. [link](http://iiif.io/api/presentation/2.0/#choice-of-alternative-resources)

Question about ranges by Glen: suitable for newspaper articles across pages or multiple articles on one page? Answer: yes, both.

### HTML in Properties
[link](http://iiif.io/api/presentation/2.0/#content-details)

HTML may be in description, attribution, or metadata properties. It needs to be well formed XML, wrapped in <p> or <span>. However don't assume that HTML formatting will be included – it may well be stripped out. This is designed to allow for basic HTML links, but disallow injection of bad data.

__Discussion:__ Mark Patton has security concerns with previously discussed HTML – may have arbitrary HTTP get requests via image. Rob suggests client remove all mouse over and other potentially harmful tags.

## Authentication

Christy described various scenarios we need to accommodate, e.g. IIIF and pulling images – mimic access through website. Images have both (a) access status and (b) licensing info. These overlap, e.g. an institution might have a license for something but somebody might not have permission to access it. Therefore access status needs to be applied for everything so we can restrict access to certain images. E.g. lower res. images unless authenticated. We have “license” in the API, but not “access” yet. 

Charles offered the example of subscribers – restrict by IP, subscription, or by manifest? Or other?  Christy would like to know how will IIIF limit access?

Discussion: various scenarios from Markus, Simeon, Rob, Matt, Michael and William. Charles' conclusion: "these are some complex use cases."



Actions
-------

 * Set up a test bed to see what will be required, soon after 2.0 final is released to learn from these experiences. Stanford, Yale, and Christy agreed to help.
 * On IIIF Discuss everyone should add their use cases. It's good to have use cases in writing so that we can analyze them down to the features. Yes, this includes technical use scenarios.

