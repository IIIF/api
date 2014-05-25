---
title: Tech Call Notes and M2 progress
author: Drew Winget
date: 2014-05-20
tags: [minutes, meetings, mirador]
layout: post
---

I just wanted to send out some notes from last week's call and also let everyone in on the latest progress on M2, the development effort on the Mirador redesign. Our [latest sprint demo video](https://www.youtube.com/watch?v=jtlwRbVyOKE) is on the new [IIIF youtube channel](https://www.youtube.com/channel/UClcQIkLdYra7ZnOmMJnC5OA). I'll be adding some other useful resources to the channel to support mirador in particular and IIIF in general. It would be great to get the community's help compiling some installation guides for different levels of the stack (Loris, IIPImage, Mirador, etc.).

Here are last week's notes:

## Mirador Tech Call - May 14th, 2014

__Stanford/Harvard Mirador Progress__

: * Architectural work on event system and asynchronous loading.
 * Load menu populating from configuration
 * Adding manifests to the manifest list from a URL now working.
 * Follow progress at https://github.com/IIIF/m2

__ArtStor__

: * Implementing IIIF urls for image resources.
 * Collaboration between ArtStor and Cornel.
 * Using Mirador as a tool for catalogue item comparison (testing phase).
 * Demo of Mirador instance at next call.

__British Library__

: * Producing manifests directly and automatically from the metadata store.
 * Instance of the Wellcome viewer is running with IIIF resources from Stanford (Tom Crane has URL).
 * Demo of image service and viewer near the end of the month.
 * Oxford will also send its endpoints for testing purposes.

__Oxford__

: * Can provide images but not metadata yet.
 * Developing local viewer for core projects, but would be open for deploying others for other purposes.

__Harvard__

: * Mirador updates.

__Sean (BL Emeritus)__

: * Astronomical images served from EC2-hosted IIIF stack working quite well for zoom and pan in Mirador.
 * KlokanTech still enthusiastic about IIPImage. The rumour is that Petr is updating the available branch on github to be more than 1.0 Image API compliant. Sending a query to the IIIF-discuss mailing list should help the group reconnect with them and get

__Jan (National Library of Poland)__

: * As part of the Polona project, have re-implemented openSeadragon with better performance.
 * IIP-image server, curious about adapting to IIIF
 * Another colleague will join the call next time to talk about more technical aspects.
 * [Demo](http://www.polona.pl/item/717521/50/)
