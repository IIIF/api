---
title: "IIIF Editors Playbook"
layout: spec
tags: [annex, presentation-api, image-api]
cssversion: 2
---

## Status of this Document
{:.no_toc}

This document is not subject to [IIIF's versioning semantics][iiif-semver]. Changes will be tracked within the document and its [internal change log][change-log]

**Authors:**

  * Michael Appleby, _Yale University_
  * Tom Crane, _Digirati_
  * Robert Sanderson, _Stanford University_
  * Jon Stroop, _Princeton University_
  * Simeon Warner, _Cornell University_
  {: .names}

{% include copyright.md %}

----

## Contents
{:.no_toc}
* Table of Discontent (will be replaced by macro)
{:toc}

## 1. Overview

The IIIF Editors are responsible for facilitating discussions across the IIIF community, digesting those discussions into use cases, and reflecting those use cases into new and revised specifications for the community to implement. This process is intended to be as transparent as possible. This document exists to further that intention by defining the IIIF Editorial process and the responsibilities and expectations of the individual Editors.

## 2. Terminology

The key words _MUST_, _MUST NOT_, _REQUIRED_, _SHALL_, _SHALL NOT_, _SHOULD_, _SHOULD NOT_, _RECOMMENDED_, and _OPTIONAL_ in this document are to be interpreted as described in [RFC 2119][rfc-2119].

## 2. Drafting and Revision Process

### 2.1 Process for Suggesting Changes

Editorial collaboration takes place [iiif.io repository on GitHub][iiif-github]. When editors submit changes for revision, they _MUST_ adhere to the following criteria:

 * There _SHOULD_ be a Github issue that explains the reason for the change and serves as a platform for discussion. Discussion regarding smaller changes may take place directly on a pull request.
 * The changes _MUST_ be made in a branch.
 * The branch _MUST_ pass all integration tests before making a pull request.
 * A link to the branch (i.e. _http://mybranch.iiif.io_) _MUST_ be included in the pull request relevant to the change.
 * Changes on the branch _MUST_ be squashed into one commit, with a reasonable commit message, and one parent commit (the latest revision). Multiple commits are allowed when they are logical, but this should generally be avoided as it usually indicates that there are too many changes happening on one branch.

__N.B.:__ The current editors will help new editors with this process as necessary. Prior experience with Git or Github _MUST NOT_ be considered prerequisite knowledge when considering new editors.

### 2.2 Acceptance Criteria for Merging Changes

In addition to adhering to the guidelines above, there _MUST_ be agreement about the change among the editors. _Agreement_ is defined as follows:

 * There _MUST NOT_ be any "-1"s (or similar Emoji) in the latest comment from any Editors before a merge.
 * __A majority__ of the editors _MUST_ actively agree ("+1") on any __non-normative__ change to a specification.
 * __All but one__ of the editors _MUST_ actively agree on any __normative__ change to a specification.
 * __At least one__ editor, in addition to the issuer of the pull request, if applicable, must actively agree to any change to non-specification content on the [iiif.io][iiif-io] website.

What about +0 as a way to say you're not bothered, i.e. you can't empathize with the use case, but don't see a problem with the change?
{: .warning}

In the event that an editor disagrees with a merge that has already happened, they should create a new issue that references the change in question, and explains the objection. This issue then serves as the discussion point for the objection which is subject to this same process.

### 2.3 Frequency of Releases

No specification is perfect. There are always new use cases surfacing, and refinements and clarifications to be made. As such, specifications are generally considered to be under continuous revision. The editors will decide when new releases are proposed for ratification, based on input from the community and and balanced against other IIIF priorities.

Following the 1.0 release of a specification, minor releases, as defined in the [IIIF Versioning Note][iiif-semver], _SHOULD NOT_ be published more than once in a 12-month period, and major releases _SHOULD NOT_ should not be published more than once in a 24-month period.

Changes to specification under development, i.e. those in the O.minor.patch series, may happen with greater frequency, at the editors' discretion.

## 3. Ratification

New and revised specifications are subject to community ratification, and are subject to the following criteria and process.

### 3.1 Criteria for Ratification

New specifications and changes to existing specification _MUST_ have one or more documented use cases, supported by at least two institutions. In the case of breaking changes, the documented use case _MUST_ clearly demonstrate why the previous approach was flawed or insufficient.

"...supported by at least two institutions". Do the institutions need to have other IIIF based technology or services in production? Otherwise is the following para enough to guard us against adding changes that never see implementation?
{: .warning}

New features _MUST_ have two server-side implementations, at least one of which _SHOULD_ be in production. New features _MUST_ also have at least one client-side implementation, which may be a proof-of-concept.

Regarding new features critera above: should we require that the source code be available, at least for proof-of-concept impls?.
{: .warning}

Revised specifications _MUST_ reference a change log as a means to help the community review the changes. This change log _SHOULD_ differentiate between backward compatible changes and breaking changes, and provide a brief summary of each change. See the [Image API 2.0 Change Log][image-20-changelog] for an example.

### 3.2 Ratification Process

New versions of specifications at or above 1.0 _MUST_ be ratified at an open meeting, to which the community is invited. These meetings will be announced on [IIIF-Discuss][iiif-discuss], [IIIF-Announce][iiif-announce] and other relevant community email lists. Such meetings _MUST_ occur at least once per year, and _SHOULD_ occur twice. The specifications _MUST_ be frozen two weeks prior to a ratification meeting, and this review period _MUST_ be announced to the lists above.

Objections _SHOULD_ be registered in advance of the meeting. Individuals who raise objections are not required to attend the ratification meeting.  However, it should be noted that this meeting is intended to be a platform for discussing any final concerns, and lack of attendance is likely to reduce the chances of an objection resulting in changes to a specification that has already been subject to the authorship, editorial, and reference implementation processes described above.

Then what? Those in attendance vote, or do they just not object? I'd prefer the latter, as voting forces an opinion.
{: .warning}

Should we (have we) compile a non-normative list of listservs?
{: .warning}

## 4. Editorial Process

### 4.1 Avenues for Community Feedback

Community members _SHOULD_ propose changes via [IIIF-Discuss][iiif-discuss], however there are a number of ways in which the IIIF Community can reach out to the editors. In particular, IIIF holds a bi-weekly community conference call (details and agenda announced on IIIF Discuss), and the [iiif.io issues on Github][iiif-github-issues] are open. Conversations with individual editors are also possible, but are the least practical when proposing changes. The editors reserve the right to discuss these conversations among themselves, and to raise any issues resulting from the conversation in one or more of the channels listed above.

Revisions please. I feel like the conversation bit is important, but don't feel like I've nailed it. Is it too strong to say nothing is considered until a stakeholder raises the issue on IIIF dicuss?
{: .warning}

### 4.2 Face to Face Meetings

Editors will meet at least four times per year, and all editors _MUST_ attend at least three of those meetings. Every effort will be make to co-locate at least one of the meetings with another meeting at which all or a majority of editors are already likely to be present.

"a majority"?
{: .warning}

The editors _MUST_ provide a summary of all meetings, and _SHOULD_ provide a summary of other   interactions (e.g. closed conference calls leading up to a specification review period) at which changes and new specifications are discussed.

## 5. Editoral Membership and Selection

Per the IIIF-C Memoradum of Understanding, the editors may invite addition editors at any time. All current editors _MUST_ agree before an invitation is issued. Editors will chosen from strong participants within the community and/or experts willing to lend their knowledge and experience to new specifications. Opportunities to better the gender, race, and age balance of the existing editorial team will also be a consideration.

There is no set number of editors, but this does not mean that the number of existing editors will not be taken into account when considering new editors. The existing editors will seek out new or additional editors when they are lacking knowledge or significant empathy for use cases in an area that the community has agreed is important.

Editors _MUST_ agree to all of the processes set out in this document, including attendance at meetings, and to the [intellectual property conditions under which the specifications are published][spec-disclaimer]. They are responsible for confirming that these conditions are also acceptable to their employer, where applicable.

It is not expected that every editor comment on every issue, though they _SHOULD_ make every effort to do so. See [Acceptance Criteria for Merging Changes][merging-changes].

Editors may be dismissed from work on a specification, or the editorial group altogether, when they fail to meet the expectations of their colleagues, as described here.

"Per the IIIF-C Memoradum of Understanding ..." - correct?
{: .warning}

## 6. Change Log

 | Date       | Description                                        |
 | ---------- | -------------------------------------------------- |
 | 2015-12-02 | Initial pass with comments                         |

[change-log]: #change-log "Change Log"
[iiif-announce]: mailto:iiif-announce@googlegroups.com "IIIF Email Announcement List"
[iiif-discuss]: mailto:iiif-discuss@googlegroups.com "IIIF Email Discussion List"
[iiif-github-issues]: https://github.com/IIIF/iiif.io/issues "iiif.io issues"
[iiif-github]: https://github.com/IIIF/iiif.io "iiif.io on Github"
[iiif-io]: http://iiif.io "iiif.io"
[iiif-semver]: /api/annex/notes/semver.html "Versioning of APIs"
[image-20-changelog]: http://iiif.io/api/image/2.0/change-log.html "Changes for IIIF Image API Version 2.0"
[merging-changes]: #acceptance-criteria-for-merging-changes "2.2 Acceptance Criteria for Merging Changes"
[rfc-2119]: https://www.ietf.org/rfc/rfc2119.txt "RFC 2119"
[spec-disclaimer]: http://iiif.io/api/annex/notes/disclaimer.html "Specification Disclaimer"
{% include acronyms.md %}
