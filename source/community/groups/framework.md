---
title: "IIIF Groups Framework"
layout: spec
tags: []
cssversion: 2
---

## Introduction

This document provides a framework for the formation and management of community and Technical Specification Groups within the IIIF community. Given the breadth and scale of IIIF, groups allow for focused work in concentrated areas of common interest, while also providing appropriate transparency and inclusiveness across the community.

The IIIF Groups Framework is derived from the [Hydra Project group structure][hydra-groups], which is in turn informed by the experiences and guidelines of related organizations, including the W3C, the Research Data Alliance, and the Apache Software Foundation. The IIIF Groups Framework aims to:

  * Be lightweight enough that work is not prevented from being done
  * Facilitate visibility and discovery of ongoing beneficial work
  * Allow work within the community to take place within the group structure, while not preventing work from occurring outside of formal groups new participants to join ongoing development
  * Encourage the development of products by the community
  * Be fair and transparent with regards to any decision making process

## IIIF Groups

Two different types of groups exist within IIIF: **Community Groups**, to allow for discussion, collaboration and coordinated work in areas of particular interest to multiple individuals and institutions engaged with IIIF, and **Technical Specification Groups** for working together toward specific, agreed-upon goals in relation to the IIIF APIs. Both types of groups rely on an open community mentality and leveraging participation from all interested members of the IIIF Community.

Successful groups:

  * Are based on mutual respect and follow the [IIIF Code of Conduct][conduct]
  * Entail a commitment to share expertise, effort and engagement
  * Are deeply and continually engaged with the wider IIIF community to ensure that shared requirements are first understood and then met
  * Develop high quality products through agreed processes and timeframes
  * Encourage participation based on a breadth of familiarity with IIIF and openly support new participants in an inclusive environment that fosters participation and contributions from throughout the community

## Communication Channels

To facilitate coordination within and across groups, IIIF maintains a common set of communications channels. IIIF Groups make use of these to ensure appropriate access, transparency and retention of discussions. These channels are:

  * **Email lists**: The primary channel of communication for all IIIF Groups is the [IIIF-Discuss][iiif-discuss] email list. When using a shared channel, individual groups should start the subject line with their name in \[\]s, such as \[av\] for the Audio/Visual Technical  Specification group, or \[newspapers\] for the Newspapers Community Group. Keeping email discussions on a common list helps to prevent splintering of communication and allows for cross-pollination of information, building interest for emerging topics. New group-specific lists should be formed only when the traffic is too high for useful discussion in the shared channel. If and when a dedicated email list is needed, the new list should be created as a Google Group using the iiif-(topic)@googlegroups.com name pattern, should be open to any interested subscribers, and should include the IIIF Community and Communications Officer as a manager.

  * **Slack**: The IIIF Community uses a [Slack team][iiif-slack] for instant messaging. Any interested person can join slack via [bit.ly/iiif-slack][join-slack]. Groups are encouraged to create channels dedicated to their topic; these channels should be open.

  * **Calls**: The IIIF Community holds bi-weekly open calls on topics of general interest. Group members are encouraged to join these calls to participate in the discussion and to represent the work happening within their groups. IIIF Groups also hold both regular and ad hoc calls as needed. The IIIF Community and Communications Officer can set up calls using the preferred videoconferencing platform (currently BlueJeans) for any interested group.

  * **Calendar**: The IIIF Community maintains a [calendar][calendar] of scheduled calls, meetings and events; Community Groups should reflect their activities on this calendar. Group convener(s) can be granted write access to the calendar; the IIIF Community and Communications Officer owns the maintenance of this calendar overall.

  * **Documents**: IIIF uses the [IIIF Google Drive][iiif-drive] as a common platform to produce and organize its documents. Each Community Group should use this as a place for collaborative note taking and storing relevant documents.

  * **Code Repositories**: GitHub is widely used within IIIF for code, documentation and issue tracking. The IIIF organization (<https://github.com/IIIF>) is used for core community products (such as the iiif.io website, technical infrastructure and specifications). Groups are encouraged to make use of GitHub repositories to manage the production of their deliverables and tracking issues and actions.

  * **IIIF Working Meetings**: IIIF groups are encouraged to participate in regular in-person IIIF events, including helping to shape the agenda and allocating time/space for group discussion.  

## IIIF Community Groups

Community Groups provide interest-specific forums for general discussion, brainstorming, sharing of use cases and demos, as well as working to produce tutorials and presentations based on existing IIIF APIs. Content-specific best practices and guides may be produced from Community Groups in conjunction with the wider community and technical editors. While technical issues related to existing APIs may arise from within Community Groups, such issues will need to be raised to the wider community via the [IIIF-Discuss][iiif-discuss] email list, and upon discussion added as issues to GitHub for prioritization and action as necessary.

### Community Group Formation and Approval

  * Community Groups should emerge naturally from discussions and needs within the community. The focus, scope and objectives of the group are ideally identified via open discussion on the [IIIF-Discuss][iiif-discuss] email list.
  * Community Groups can be formed as needed by sending a lightweight statement of the topic, scope, and objectives of discussion for the proposed Community Group to the IIIF Community and Communications Officer. Proposals will then be assessed by the IIIF Coordinating Committee.  
  * Once approved, Community Groups should be documented on the iiif.io website, noting the following information:
    1. Statement of the group focus and/or goals, and how the group came to be formed
    2. Chair(s) of the group
    3. Communication channels ([Slack][iiif-slack], [IIIF-Discuss][iiif-discuss], etc.)
    4. Link to group folder in the IIIF Google Drive for Call Notes and Group Documents
    5. Regular call schedule
    6. Call connection information
  * At least three organizations must be represented in a Community Group at all times. Anyone may be part of a Community Group. To join, follow the specified channels for the group, which may include adding your name to the group member roster, joining the [Slack][iiif-slack] channel, and following conversation on [IIIF-Discuss][iiif-discuss] and group meetings via the [IIIF calendar][calendar].
  * Community Groups must always have at least one member designated as Chair, and preferably two or at most three. Chairs are responsible for promoting continued activity within the group, but have no additional powers or rights than any other participant.
  * The discussions of the Community Group must be transparent and public, with notes made available through the [IIIF Google Drive][iiif-drive].

### Community Group Dissolution

Community Groups can be dissolved if the participants decide that the topic has been fully explored.  The document describing the group should be updated to state this termination of the group, and otherwise left intact for future reference.

## IIIF Technical Specification Groups

Technical Specification Groups are the main working vehicle for adding new APIs or making changes to existing specifications within the IIIF Community. Technical Specification Groups are typically created to perform specific tasks in a defined realm and timescale, thereby allowing collaborative work to flourish in a structured environment.

### Technical Specification Group Formation and Approval

  * Technical Specification Groups should emerge naturally from discussions and needs within the community.
  * Participants in discussions that show promise of inter-institutional convergence on common models or methods should document the shared needs and requirements in a Google document, resulting in a common understanding of:
    1. The overall domain into which the work will fall
    2. The shared needs and requirements within that domain
    3. Use cases that demonstrate these needs and requirements
    4. A path towards one or more specifications and complementary implementations   that would meet the requirements
    5. The organizations willing to commit resources towards realizing the specifications and implementations
    6. The timeframe in which the specifications and implementations are needed and should be possible
  * The document outlining the above must be sent to the IIIF Community and Communications Officer for subsequent discussion and initial approval by the IIIF Coordinating Committee, typically within a one week timeframe. (Note: There are two stages of approval: initial approval by the Coordinating Committee, followed by an official approval by the wider community - see CfP process below).
  * Once initially approved, the group document becomes the group’s charter, providing definition of the group and its deliverables. The charter is not a contract and may be changed with the consensus of the members of the group at any time. However, significant changes such as a 6 month or more delay in timeframes, the abandonment of a deliverable, or the change in the overall scope of the work should be announced to the community via the regular channels.
  * Once the draft charter is acceptable to the participants in the discussion, a Call for Participation (CfP) is issued to appropriate lists (including [IIIF-Discuss][iiif-discuss] at the least) that announces the document and seeks the engagement of additional participants.
    * Individuals from organizations across the IIIF community must respond to the CfP indicating that they are willing to take part and commit resources towards the Technical Specification Group's goals.  
    * At least three IIIF participating institutions  must respond positively, and no more than three institutions may respond negatively, for the group to be officially approved by the wider community.  
    * If fewer than three institutions are willing to contribute, then the group's topic is likely too specific and the work should be done outside of the Technical Specification Group process.  If more than three institutions object to the work being done, then there is a significant issue that should be resolved before committing resources.
    * For Technical Specification Groups where deliverables would involve additions or changes to existing technical specifications, at least two current members of the editorial board must sign up as members of the group to ensure consistency with existing and ongoing work.
  * At least two calendar weeks must pass between the CfP and official approval of the group.  If only one or two institutions are interested after four calendar weeks, then the CfP is considered closed and the original proposers of the charter should lead continued discussion and modify the charter before re-announcing.
  * Once officially approved, Technical Specification Groups should be documented on the iiif.io website, noting the following information:
    1. Statement of the group focus and/or goals, and how the group came to be formed
    2. Chair(s) of the group
    3. Communication channels ([Slack][iiif-slack], [IIIF-Discuss][iiif-discuss], etc.)
    4. Link to group folder in the IIIF Google Drive for Call Notes and Group Documents
    5. Regular call schedule
    6. Call connection information

### Technical Specification Group Requirements

All members of a Technical Specification Group must agree to have any contributed work licensed under a CC-BY license, or similar.  Participants meeting this requirement may join at any time, without any prior approval process: the gateway is activity, not reputation.

All discussion within the Technical Specification Group must be transparent and public, made available through the [IIIF Google Drive][iiif-drive] and the [IIIF-Discuss][iiif-discuss] email list.  This means that meetings must have notes taken about the attendance and any decisions or action items, general discussions take place on mailing lists maintained by the community, chat logs should be posted and so forth.  

Any meetings, face-to-face or by teleconference, at which decisions are made must be announced in advance and open to any group participant, otherwise any opinions expressed at the meeting must also be discussed on a mailing list.  Meeting times should be published far enough in advance to allow members to schedule their participation, and preferably use a consistent schedule. Every participant is encouraged to take an active role in ensuring the transparency of the work.

Technical Specification Groups must remain active. Any group that does not respond to comments, questions or concerns either from participants or the community within three months will be closed and removed from the list of active groups.  

Technical Specification Groups must strive to meet their timelines and produce the deliverables designated in their charter.  The groups must always have at least one member designated as Chair, and preferably two or at most three.  Chairs are responsible for promoting continued activity within the group but have no additional powers or rights than any other participant.  Chairs do not need to be from a IIIF Consortium member organization. A group with only inactive chairs is considered to be inactive, and the group should select one or more new chairs.

Technical Specification Groups may self-organize in the most convenient manner to accomplish their tasks, including creation and assignment of additional roles and responsibilities as appropriate.  Sub groups may be formed and disbanded at will, consisting only of members of the group, often called Task Forces. They do not need to separately meet the requirements of the group, such as having their own Chair.

### Technical Specification Group Dissolution

Technical Specification Groups are dissolved under the following circumstances:

  * All of the deliverables have been met. Hooray!
  * The group becomes inactive
  * The group does not have participants from three or more institutions
  * The group has insufficient participation from the [IIIF Editorial Committee][editors] (at least two)
  * The group does not have anyone willing to be the Chair

  At such a time as a group is dissolved, it is moved from the active list of working groups into a working group archive page with the reason for its dissolution noted.

## Updates

This community framework is an evolving document, and will be updated by the IIIF Coordinating Committee as required. *Last updated: 13 January 2017*.

## IIIF Community and Communications Contact

Sheila Rabun  
IIIF Community and Communications Officer  
srabun@iiif.io  


[hydra-groups]: https://wiki.duraspace.org/pages/viewpage.action?pageId=67241635
[iiif-discuss]: https://groups.google.com/forum/#!forum/iiif-discuss
[join-slack]: https://docs.google.com/forms/d/e/1FAIpQLSdGV9QSFo8i2z1R5iIMP7B2JVhS9akHqcykWF5_y4mtWqVrBA/viewform
[calendar]: http://iiif.io/community/groups/
[iiif-drive]: https://drive.google.com/drive/folders/0B9EeoRu2zWeraXpHNXpnZThUZVE
[iiif-slack]: http://iiif.slack.com
[editors]: http://iiif.io/api/annex/notes/editors/#contents
[conduct]: http://iiif.io/event/conduct/




{% include acronyms.md %}
