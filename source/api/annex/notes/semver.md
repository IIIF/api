---
title: "Versioning of APIs"
layout: spec
tags: [annex, presentation-api, image-api]
---

Starting with the 2.0.0 releases of both the IIIF [Image API][image-api] and [Presentation API][prezi-api], the specifications will follow [Semantic Versioning][semver] with version numbers of the form "MAJOR.MINOR.PATCH" where:

  * MAJOR version increment indicates incompatible API changes.
  * MINOR version increment indicates addition of functionality in a backwards-compatible manner.
  * PATCH version increment indicates backwards-compatible bug fixes.

This versioning system will be implemented in the following ways:

  * URIs for compliance and context will be updated with major versions only, and otherwise edited in place.
  * URIs for the specifications will be updated with major and minor versions, with patch versions edited in place.
  * The protocol URI does not change with versioning.

In the case of the Image API, changes to either the API itself or the corresponding [compliance document][image-compliance] will increment the version number as appropriate. In all cases, major and minor releases will be accompanied by a change log, while changes in patch releases will be appended to the change log for the  latest major or minor release.

While the Presentation and Image APIs should always be compatible, the editors do not necessarily intend to keep their version numbers synchronized. A change in one API will not advance the version number of the other.

[semver]: http://semver.org/spec/v2.0.0.html "Semantic Versioning 2.0.0"
[image-api]: /api/image/{{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }}/ "Image API 2.0"
[prezi-api]: /api/presentation/{{ site.presentation_api.latest.major }}.{{ site.presentation_api.latest.minor }}/ "Presentation API 2.0"
[image-compliance]: /api/image/{{ site.image_api.latest.major }}.{{ site.image_api.latest.minor }}/compliance.html "Image API Compliance"

{% include acronyms.md %}

