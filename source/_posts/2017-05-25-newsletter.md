---
title: IIIF Community Newsletter, Volume 1 Issue 3
author: Sheila Rabun
date: 2017-05-25
tags: [news, newsletter, announcements]
layout: post
excerpt: >
  Community Snapshot, IIIF Adopters Survey, Community Events, Technical Work, Community Groups,
  Implementations and Adoption
---

## Community Snapshot
 * [IIIF-Discuss][iiif-discuss] = 692 members  
 * [IIIF Slack][join-slack] = 362 members  
 * [IIIF Consortium][iiif-c]  = The IIIF-C continues to welcome founding members. See the [IIIF Consortium][iiif-c] information page for details and how to join.
 * Search process for a [IIIF Technology Coordinator][tech-coordinator] is currently underway.

### IIIF Adopters Survey
Many thanks to the 70 institutions who have completed the [Basic IIIF Adopters Survey][survey-basic]. The [IIIF Community List][comm] has been updated, and there are over 100 institutions participating in the IIIF community. Survey results indicate that there are currently **over 335 million images** on the web that comply with one or more IIIF APIs. This number is growing on a daily basis as many institutions are continuously adding additional IIIF images to their digital repositories. Survey results, at a glance:
 * **IIIF Image API:**
    * 51 institutions are currently using either version 1.X or 2.X of the IIIF Image API
    * 34 institutions are investigating or developing support for the IIIF Image API
 * **Presentation API:**
    * 39 institutions have adopted either version 1.X or 2.X of the IIIF Presentation API
    * 39 institutions are currently investigating or developing support for the IIIF Presentation API
 * **Content Search API:**
    * According to the survey, five institutions support the IIIF Content Search API in production: The British Library, North Carolina State University (NCSU), University College Dublin, the National Library of Wales, and the Wellcome Trust.
    * 34 institutions are currently investigating or developing support for the IIIF Content Search API
 * **Authentication API:**
    * The British Library and the Wellcome Trust are the only known institutions currently using the IIIF Authentication API.
    * 30 institutions are currently investigating or developing support for the IIIF Authentication API

### To Participate in the Ongoing Survey:
 * Are you researching, experimenting with, or fully supporting IIIF at your institution? Please help us scope the IIIF Universe and levels of adoption across the community by completing this quick, 5 minute, [Basic IIIF Adopters Survey][survey-basic].
 * We are also gathering information to assess and inform IIIF on-boarding and training materials, through the [Extended IIIF Adopters Survey][survey-extended], expected to take 10-15 minutes to complete.

## Community Events and Outreach

### 2017 IIIF Conference
The 2017 International Image Interoperability Framework (IIIF) [Conference in The Vatican][vatican] is quickly approaching the first week of June. Intended for a wide range of participants and interested parties, conference events include:
 * **Monday, June 5** - Pre-conference meetings for [Mirador Viewer][mirador] and [Universal Viewer][uv]
     * No registration needed
     * [View Schedule][preconf-sched]

 * **Tuesday, June 6** - IIIF Showcase: Unlocking the World’s Digital Images
     * Showcase [Registration][showcase-reg] is free, but capacity is limited. There is still time to register!
     * [View Schedule][showcase-sched]

 * **Wednesday, June 7 - Friday, June 9** - IIIF Conference
     * Registration is closed, and the event is at capacity.
     * [View Schedule][conf-sched]

Many thanks to our 2017 IIIF Conference sponsors:
* The [IIIF Consortium][iiif-c]
* [Cogapp][cogapp] - Silver Sponsor
* [Digirati][digirati] - Silver Sponsor
* [Klokan Technologies][klokan] - Silver Sponsor
* [OCLC][oclc] - Silver Sponsor
* [Synaptica][synaptica] - Silver Sponsor
* [Zegami][zegami] - Silver Sponsor
* [4Science][4science] - Silver Sponsor

### IIIF Presence at Conferences and Meetings
Active community participants are encouraged to represent IIIF at conferences, workshops and events around the world. Those planning to present on IIIF at a conference or meeting, please fill out the [IIIF Representation at Conferences and Meetings][outreach-survey] Survey. Recent and upcoming IIIF appearances include:

* [Visual Resources Association Conference][vra], March 2017
* [Coalition for Networked Information (CNI)][cni] Spring Membership Meeting, April 2017
* [International Federation of Library Associations (IFLA) News Media Conference][ifla], April 2017
* [Mirador Symposium][mirador-symposium] (Stanford University), May 2017
* [2+3D Photography - Practice and Prophecies 2017][23d] (Rijksmuseum, Amsterdam), May 2017
* [52nd International Congress on Medieval Studies at Kalamazoo][kalamazoo], May 2017
* [Texas Conference on Digital Libraries][tcdl], May 2017
* [Leeds International Medieval Congress][leeds], July 2017


### Museums Community Letter to Digital Asset Management (DAM) Software Vendors
Led by the IIIF Museums Community Group, with support from museums and other cultural heritage institutions across the globe, an open letter has been sent to a number of DAM software vendors encouraging the adoption of IIIF in DAM products. The letter is available for viewing and sharing online at [http://iiif.io/news/2017/05/01/letter-to-dams/][dams].

### Europeana IIIF Task Force
The Europeana IIIF Task Force is working to identify the current trends and tendencies among Europeana content providers towards the handling of the emerging IIIF technology. Read more at [http://pro.europeana.eu/taskforce/iiif][taskforce].

## Technical Work

### A/V Technical Specification Work
The [IIIF A/V Technical Specification Group][iiif-av] has been modeling various A/V use cases using IIIF manifests and canvases. Wider discussions about ranges within manifests have informed modeling work for both IIIF A/V and other objects with complex hierarchies. Experiments are currently underway to implement the current [IIIF A/V model][av-fixtures], as the group looks to test the model and address [issues related to syncing multiple video and/or audio files in a single player][av-challenges]. The Avalon Media System team at Indiana University and Northwestern University has been working on a proof of concept for [audio][avalon-a] and [video][avalon-v] towards a [new release][avalon] that will include an audio and video player that works with IIIF manifests. The group is still seeking A/V material to experiment with, unencumbered by rights issues that would prevent reuse, and suitable for all audiences, such as:

* A variety of single formats in common use today (mp4, webm with common codecs)
* MPEG-DASH and HLS file sets (no live streaming yet though)
* Media accompanied by common sidecar files (webvtt appears in a few examples)
* No objections to anyone turning your webvtt to web annotations and also publishing those
* Sets of mixed media if you have them - oral history interviews plus transcriptions, albums and images of their covers and inner sleeves; again unencumbered by rights (appreciate that might be tricky for some things)

See the [A/V group page][iiif-av] for details on how to join in the discussion and learn more.

### Discovery of IIIF Resources
The [IIIF Discovery Technical Specification Group][iiif-discovery] is working to solidify a specification for the “IIIF Drag and Drop” functionality that has already been implemented at various institutions across the community. The group is currently soliciting use cases for drag and drop as well as other cases for importing IIIF images to viewers. Use cases may be submitted in the [iiif-stories GitHub repo][iiif-stories]. The group has also been exploring the pros and cons of various mechanisms for crawling and harvesting IIIF collections and objects. To join the discussion and learn more, visit the [IIIF Discovery group page][iiif-discovery].

### IIIF Text Granularity Technical Specification Group
As more institutions and vendors are working with annotations and text in the context of IIIF, a need has grown to specify degrees of granularity for text annotations (such as word, sentence, paragraph, etc.) in relation to the [IIIF Search API][search]. The IIIF Text Granularity Technical Specification Group has just formed to begin this work. If you are interested in participating in Text Granularity group discussions, please review the [group charter][text-charter] and indicate your interest. Stay tuned to the [IIIF-Discuss][iiif-discuss] email list for more details.

### OpenJPEG Improvement Project
Several institutions in the IIIF community have come together to launch the first phase of a collaborative effort to facilitate improvement of [OpenJPEG][openjpeg], an open source [JPEG 2000][jpeg2000] codec, freely available under a [BSD license][bsd]. A project is currently underway to improve performance, scalability, security, and robustness of OpenJPEG, with the initial phase focused on improving decoding speed, region-of-interest decoding, and memory footprint. Project status can be tracked via [GitHub][jpeg-git], and more details can be found on the [OpenJPEG website][jpeg-site]. The project team welcomes additional funding institutions to contribute to future phases and sustain the effort to bring OpenJPEG up to speed with proprietary implementations of the JPEG 2000 standard. To learn more and get involved, please contact Sheila Rabun, IIIF Community and Communications Officer, at <srabun@iiif.io>. See more details at [http://iiif.io/news/2017/04/27/openjpeg-improvement/][jpeg-news].

## Community Groups:
Please see the [IIIF Community Groups page][iiif-calendar] for a calendar of group and community calls, as well as links to more information about each group. All of the community groups will be meeting in person at the [2017 IIIF Conference][vatican] in June.

### Manuscripts Community Group
In addition to making preparations for a number of manuscripts-related presentations and a manuscripts discussion session at the IIIF Conference, participants from the [IIIF Manuscripts Community group][manuscripts] have been involved in ongoing training and pedagogical outreach at Kalamazoo, DHSI, Rare Book School, Medieval Academy, and elsewhere. The manuscripts community is looking to coalesce on basic metadata for manuscripts that might be passed in a IIIF manifest, as well as looking toward discoverability hubs for manuscript materials and creating user-facing documentation and training materials. The group would like to increase collaborative efforts to move the community forward, particularly through integration of existing projects and repositories and developing advocacy lines for encouraging additional digitization efforts and IIIF compliance for manuscript materials.

### Museums Community Group
The museums community recently sent an [open letter to Digital Asset Management (DAM) software vendors][dams], urging the adoption of IIIF. As interest in institutional adoption of IIIF grows in the museums community, the group is working on adding information to the general [IIIF FAQ][iiif-faq], including details on examples of museums that are already using IIIF in their digital repositories. The IIIF Conference in The Vatican (first week of June) will feature a [museums track][museums-sched] on Thursday, 8 June.

### Newspapers Community Group
The [IIIF Newspapers group][newspapers] congratulates the Bavarian State Library on their implementation of [IIIF for newspapers][bsb-news], and the National Library of Wales’ recent release of [IIIF-compliant journals][wales-journals]. Interest in IIIF and text is growing, and the group is preparing to contribute to work on specifying text granularity for IIIF annotations. The community is also preparing to work with Boston Public Library and the University of Utah on their recently awarded [IMLS grant][hydra] to develop IIIF-compliant Hydra solutions for digitized newspapers.

### Software Developers Community Group
The [IIIF Software Developers group][devs] continues to work on developing and documenting IIIF client components that can be mixed and matched in various viewing environments. While demonstrations of IIIF implementations typically occur on the bi-weekly [IIIF Community Calls][comm-call], the Software Developers group invites more in-depth technical discussion of implementations, for sharing strategies and advice on the technical aspects of IIIF implementation in software.

## Implementations and Adoption

### New Releases

* Zegami now supports IIIF Image 2.1 and IIIF Presentation 2.1! [Learn more][zegami-news]
* The Cooper Hewitt Smithsonian Design Museum is now using the IIIF Image API - see [demo][ch-demo] (200,000 images as tiles) and [blog][ch-blog] from Micah Walter, formerly of the Cooper Hewitt, collaborating with Aaron Cope on integrating IIIF/zoomable images for their collection on the web.
* The Biblissima portal (focused on the history of ancient collections of manuscripts and early printed books) is now online in public beta, using Mirador:
    * [Live demo][bib-demo]
    * [Demo video][bib-vid]
* New releases from the Bavarian State Library (BSB):
    * First milestone of IIIF 2.0 for [4,000 medieval manuscripts and 8,000 mostly unique incunabulas][bsb]
    * BSB also now has [~350 newspapers online via IIIF][bsb-news]
    * BSB has also published a [Mirador plugin for a dynamic physical ruler][bsb-ruler]
* New implementation at [Heidelberg University][heidelberg]
* National Library of Wales just released a new website containing [1.2 million Journal images][wales-journals] available as IIIF images, manifests and collections (including sitemaps, IIIF Collections with pointers to EDM metadata, Manifests, and Annotation lists). For technical details, see this [writeup][wales-tech].

### Innovations & Ongoing Work from Across the IIIF Community

* ["Greatest Hits" demo][greatest-hits] from the University of Toronto highlighting new features in their work on IIIF & Mirador in Omeka
* Overview of [new features from the Hill Museum and Manuscript Library][hmml] (HMML) (which will have 25K manuscripts soon!)
* Walk-through of [Trifle][trifle], Durham University's manifest loader and editor
* Introduction of [new features to T-PEN][tpen], the transcription tool from Saint Louis University Center for Digital Humanities
* [Introduction to RERUM][rerum], the public annotation store from Saint Louis University Center for Digital Humanities
* Adoption of IIIF for [digital images in Cuba][cuba], a collaboration including the National Library of Cuba, The Central Library of the University of Havana, and the Library of the Cuban History Institute
* Natural Sciences Institute of the National University of Columbia using IIIF and Loris, see [example][columbia]
* Harvard biology class using Mirador to annotate images of cells, see [example][cell]
* Chrome tab extension to [view a new map from David Rumsey collection][rumsey] every time a new tab is opened
* Polonsky Project - [Three editions of Cicero side by side][cicero]
* [ResearchSpace][researchspace] currently working on implementing IIIF
* [Collection of problematic manifests for testing][problematic], by David Newberry (Carnegie Art Museum)
* [Demo on Linked Data Notifications, IIIF, and Mirador][witt], by Jeffrey Witt (Loyola University Maryland)
* [UB Leipzig adoption of IIIF][leipzig] - try a [live demo][leip-demo]
* [Experimentation with IIIF and IPFS][ipfs] by Edward Silverton (Holoscene)
* IMLS awarded two grant projects that will include support for IIIF:
    * [Newspapers in Hydra][hydra] (Boston Public Library and University of Utah)
    * [Improvement and integration for the Avalon Media System][imls-ava] (Northwestern University and Indiana University)

### Recommended Reading
* New intro to IIIF writing by Tom Crane (Digirati): [An Intro to IIIF][crane-intro] & Second installment: [Where's My Model?][crane-model]
* Heidelberg report (p1-10) on adoption of IIIF: [Data Quality in Europeana][heidel-report]
* Blogs from Cogapp: [IIIF support for the Qatar Digital Library][qatar] and [#FunwithIIIF in Edinburgh!][fun]
* Blog from Digirati on [“Science in the Making: An Archives Project for the Royal Society”][science]
* [Intro to IIIF][gitbook] workshop created for developers at Code4lib, by Stanford developers Drew Winget and Jack Reed
* [Presentations and notes][edin] from the IIIF events in Edinburgh
* [The case for serving your IIIF content over HTTPS][https] by Jack Reed (Stanford)

#### Edited by:
Sheila Rabun, IIIF Community and Communications Officer

#### With contributions from:  

* Benjamin Albritton, Stanford
* Michael Appleby, Yale Center for British Art
* Jon Dunn, Indiana University
* Claire Knowles, University of Edinburgh
* Stuart Snydman, Stanford
* Maria Whitaker, Indiana University


[iiif-discuss]: https://groups.google.com/forum/#!forum/iiif-discuss
[join-slack]: http://bit.ly/iiif-slack
[iiif-c]: /community/consortium/
[tech-coordinator]: https://www.clir.org/about/positions/iiif_technology_coordinator
[outreach-survey]: https://docs.google.com/forms/d/e/1FAIpQLScDBfjLTLsC4trMGVXETeEiU1oqNQZd3H9cDApO1jx2M18BBw/viewform?c=0&w=1
[iiif-events]: /event/
[iiif-av]: /community/groups/av/
[iiif-calendar]: /community/groups/
[manuscripts]: /community/groups/manuscripts/
[museums]: /community/groups/museums/
[newspapers]: /community/groups/newspapers
[devs]: /community/groups/software/
[mirador]: http://projectmirador.org
[survey-basic]: https://goo.gl/forms/47OmXfgXMUNMBVI93
[survey-extended]: https://goo.gl/forms/wHXWrvIMtUbmJRN52
[uk-showcase]: https://iiifshowcaseedinburgh.eventbrite.co.uk/
[uk-tech]: https://iiiftechnicaledinburgh.eventbrite.co.uk/
[showcase-reg]: https://iiif-showcase-vatican2017.eventbrite.com
[conference-reg]: https://iiif-conference-vatican2017.eventbrite.com
[uv]: https://digirati.com/technology/our-solutions/universal-viewer/
[vatican]: /event/2017/vatican
[taskforce]: http://pro.europeana.eu/taskforce/iiif
[iiif-discovery]: /community/groups/discovery
[av-fixtures]: https://github.com/IIIF/iiif-av/tree/master/source/api/av/examples
[vra]: https://vra34.sched.com/
[cni]: https://www.cni.org/event/cni-spring-2017-membership-meeting
[ifla]: https://www.ifla.org/node/11023
[mirador-symposium]: https://library.stanford.edu/events/mirador-images-and-future-digital-research-web
[23d]: https://www.rijksmuseum.nl/en/2and3dphotography
[kalamazoo]: https://wmich.edu/sites/default/files/attachments/u434/2017/medieval-congress-program-2017-for-web.pdf
[tcdl]: https://tcdl-ocs-tdl.tdl.org/tcdl/index.php/TCDL/TCDL2017
[leeds]: https://www.leeds.ac.uk/ims/imc/imc2017.html
[dams]: /news/2017/05/01/letter-to-dams/
[av-challenges]: https://docs.google.com/document/d/1lcef8tjqfzBqRSmWLkJZ46Pj0pm8nSD11hbCAd7Hqxg/edit?usp=sharing
[avalon]: https://wiki.dlib.indiana.edu/display/VarVideo/Avalon+7+Road+Map
[avalon-a]: https://avalonmediasystem.github.io/avalon-poc-standalone/dist/audio.html
[avalon-v]: https://avalonmediasystem.github.io/avalon-poc-standalone/dist/index.html
[iiif-stories]: https://github.com/IIIF/iiif-stories/issues
[text-charter]: https://docs.google.com/document/d/1wTxgcj-AlAE3KwcxP59mTZhOOQKkDEaqwVK_NHOIRvc/edit
[text-poll]: http://doodle.com/poll/b92ste87ri7x5ekh
[openjpeg]: http://www.openjpeg.org/
[jpeg2000]: https://jpeg.org/jpeg2000/
[bsd]: https://github.com/uclouvain/openjpeg/blob/master/LICENSE
[jpeg-git]: https://github.com/uclouvain/openjpeg/projects/1
[jpeg-site]: http://www.openjpeg.org/2017/04/27/Faster-OpenJPEG-is-on-track
[jpeg-news]: http://iiif.io/news/2017/04/27/openjpeg-improvement/
[zegami-news]: https://www.zegami.com/international-image-interoperability-framework-iiif-zegami/
[ch-demo]: https://collection.cooperhewitt.org/objects/18572345/zoom
[ch-blog]: https://labs.cooperhewitt.org/2017/parting-gifts/
[bib-demo]: http://beta.biblissima.fr/en
[bib-vid]: https://youtu.be/g1FQkkg23IA
[bsb]: https://iiif.digitale-sammlungen.de
[bsb-news]: https://digipress.digitale-sammlungen.de/view/bsb00012484_00382_u001/1
[bsb-ruler]: https://github.com/dbmdz/mirador-plugins#physical-document-ruler
[heidelberg]: http://digi.ub.uni-heidelberg.de/diglit/cpg832/0012
[wales-journals]: https://journals.library.wales
[wales-tech]: http://dev.llgc.org.uk/wiki/index.php?title=IIIF_Journals
[greatest-hits]: https://youtu.be/SOUO-2ecHho
[hmml]: https://youtu.be/unqMDZq_R2Y
[trifle]: https://youtu.be/qtwJDN2tFbI
[tpen]: https://youtu.be/dppRNuGPbb8
[rerum]: https://youtu.be/_wTexGTDiAQ
[cuba]: http://imagenes.sld.cu/
[columbia]: http://www.biovirtual.unal.edu.co/en/collections/detail/66509/
[cell]: https://courses.edx.org/courses/course-v1:HarvardX+MCB64.1x+2T2016/d16e07a5cec442eeb7cd9dfcb695dce0/
[rumsey]: https://t.co/1E6dB5yt6G
[cicero]: http://bav.bodleian.ox.ac.uk/news/three-editions-of-cicero-side-by-side
[researchspace]: https://summit2017.lodlam.net/2017/04/12/researchspace/
[problematic]: http://evil-manifests.davidnewbury.com/
[witt]: https://youtu.be/RZih8w37moU
[leipzig]: https://blog.ub.uni-leipzig.de/grenzenlose-bilderwelt/
[leip-demo]: http://papyrusebers.de/
[ipfs]: https://t.co/fSmwR2LZFU
[hydra]: https://www.imls.gov/grants/awarded/lg-70-17-0043-17
[imls-ava]: https://www.imls.gov/grants/awarded/lg-70-17-0042-17
[crane-model]: http://resources.digirati.com/iiif/an-introduction-to-iiif/wheres-my-model.html
[crane-intro]: http://resources.digirati.com/iiif/an-introduction-to-iiif/
[heidel-report]: http://pro.europeana.eu/files/Europeana_Professional/Share_your_data/Technical_requirements/Cases_studies/Heidelbergreport-v0.9.pdf
[qatar]: https://blog.cogapp.com/iiif-support-for-the-qatar-digital-library-bc949f0aa343
[fun]: https://blog.cogapp.com/funwithiiif-in-edinburgh-436d5e2843fe
[science]: https://scienceinthemakingblog.wordpress.com/
[gitbook]: https://iiif.github.io/training/intro-to-iiif/
[edin]: http://bit.ly/2ngOwfi
[https]: https://www.jack-reed.com/2017/05/23/the-case-for-serving-your-iiif-content-over-https.html
[comm]: /community/
[preconf-sched]: https://2017iiifconferencethevatican.sched.com/tag/Pre-conference
[showcase-sched]: https://2017iiifconferencethevatican.sched.com/tag/Showcase
[conf-sched]: https://2017iiifconferencethevatican.sched.com/tag/Conference
[conf-news]: http://iiif.io/news/2017/04/12/vatican-conference/
[cogapp]: http://www.cogapp.com/iiif
[oclc]: http://www.oclc.org/en/contentdm.html
[digirati]: https://digirati.com/
[klokan]: https://www.klokantech.com/
[synaptica]: http://www.synaptica.com/
[zegami]: https://zegami.com/
[4science]: http://www.4science.it/en/iiif-image-viewer/
[search]: /api/search/
[iiif-faq]: /community/faq/
[museums-sched]: https://2017iiifconferencethevatican.sched.com/overview/type/Museums
[comm-call]: /community/call/
