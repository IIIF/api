---
title: "IIIF Import to Viewers API 0.1"
title_override: "IIIF Import to Viewers API 0.1"
id: discovery-api-import
layout: spec
cssversion: 3
tags: [specifications, presentation-api]
major: 0
minor: 1
patch: 0
pre: final
redirect_from:
  - /api/import/index.html
  - /api/0/import/index.html
---


## Status of this Document
{:.no_toc}
__This Version:__ {{ page.major }}.{{ page.minor }}.{{ page.patch }}{% if page.pre != 'final' %}-{{ page.pre }}{% endif %}

__Latest Stable Version:__ None

__Previous Version:__ None

**Editors**

  * **[Michael Appleby](https://orcid.org/0000-0002-1266-298X)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-1266-298X), [_Yale University_](http://www.yale.edu/)
  * **[Tom Crane](https://orcid.org/0000-0003-1881-243X)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0003-1881-243X), [_Digirati_](http://digirati.com/)
  * **[Robert Sanderson](https://orcid.org/0000-0003-4441-6852)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0003-4441-6852), [_J. Paul Getty Trust_](http://www.getty.edu/)
  * **[Jon Stroop](https://orcid.org/0000-0002-0367-1243)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-0367-1243), [_Princeton University Library_](https://library.princeton.edu/)
  * **[Simeon Warner](https://orcid.org/0000-0002-7970-7855)** [![ORCID iD]({{ site.url }}{{ site.baseurl }}/img/orcid_16x16.png)](https://orcid.org/0000-0002-7970-7855), [_Cornell University_](https://www.cornell.edu/)
  {: .names}

{% include copyright.md %}

__Status Warning__
This is a work in progress and may change without notice. Implementers should be aware that this document is not stable. Implementers are likely to find the specification changing in incompatible ways. Those interested in implementing this document before it reaches beta or release stages should join the IIIF [mailing list][iiif-discuss] and the [Discovery Specification Group][groups-discovery], take part in the discussions, and follow the [emerging issues][github-discovery-issues] on Github.
{: .warning}

----

## Table of Contents
{:.no_toc}

* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Introduction
{: #introduction}

The resources made available via the IIIF (pronounced "Triple-Eye-Eff") [Image][image-api] and [Presentation][prezi-api] APIs are only useful if they can be found. The Change Discovery API describes how systems are built that allow these resources to be found. Once found, how does a user open the resource in an environment of their choosing, such as a viewer, annotation tool or other IIIF-compatible software?

This specification leverages existing techniques and specifications in order to promote widespread adoption. It provides a way of describing a resource, or a part of a resource, in a compact format that can be used to initialise the view of that resource in any client that implements this specification.

### 1.1. Objectives and Scope
{: #objectives-and-scope}

The objective of the IIIF Import to Viewers API is to provide the information needed to initialise discover and subsequently make use of IIIF resources.  The intended audience is other IIIF aware systems that can leverage the content and APIs. While this work may benefit others outside of the IIIF community directly or indirectly, the objective of the API is to specify an interoperable solution that best and most easily fulfills the discovery needs within the community of participating organizations.

The discovery of IIIF resources requires a consistent and well understood pattern for content providers to publish lists of links to their available content. This allows a baseline implementation of discovery systems that process the list, looking for resources that have been added or changed.

This process can be optimized by allowing the content providers to publish descriptions of when their content has changed, enabling consuming systems to only retrieve the resources that have been modified since they were last retrieved. These changes might include when content is deleted or otherwise becomes unavailable. Finally, for rapid synchronization, a system of notifications pushed from the publisher to a set of subscribers can reduce the amount of effort required to constantly poll all of the systems to see if anything has changed. 

Work that is out of scope of this API includes the recommendation or creation of any descriptive metadata formats, and the recommendation or creation of metadata search APIs or protocols. The diverse domains represented within the IIIF community already have already have successful standards fulfilling these use cases, and the results of previous attempts to reconcile these standards across domains have not seen widespread adoption. Also out of scope is optimization of the transmission of content, for example recommendations about transferring any source media or data between systems.


### 1.2. Terminology
{: #terminology}

The specification uses the following terms:

* __HTTP(S)__: The HTTP or HTTPS URI scheme and internet protocol.

The terms _array_, _JSON object_, _number_, and _string_ in this document are to be interpreted as defined by the [Javascript Object Notation (JSON)][org-rfc-8259] specification.

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, _MAY_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][org-rfc-2119].


## 2. Section
{: #section}


### 2.1. Sub section
{: #sub-section}


#### 2.1.1. Sub sub section
{: #sub-sub-section}

Example JSON:

```
{ 
  "type": "Update",
  "object": {
    "id": "https://example.org/iiif/1/manifest",
    "type": "Manifest"  	
  }
}
```

##### term


##### anotherTerm


## Appendices

### A. Acknowledgements
{: #acknowledgements}

Many thanks to the members of the [IIIF community][iiif-community] for their continuous engagement, innovative ideas, and feedback.

Many of the changes in this version are due to the work of the [IIIF Discovery Technical Specification Group][groups-discovery], chaired by Antoine Isaac (Europeana), Matthew McGrattan (Digirati) and Rob Sanderson (J. Paul Getty Trust). The IIIF Community thanks them for their leadership, and the members of the group for their tireless work.

### B. Change Log
{: #change-log}

| Date       | Description           |
| ---------- | --------------------- |
| 2018-10-31 | Version 0.1 (unnamed) |

{% include links.md %}
 