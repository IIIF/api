---
title: "IIIF-6: London 2014 Authentication Scenarios"
layout: spec
redirect_from:
  - /event/2014/london_auth_scenarios.html
---
# Granular IIIF Authorization Scenarios

Notes distributed on iiif-discuss 2014-10-22 and discussed at [IIIF 6 London Working Group](/event/2014/london_notes/).

*Assumption 1:* In both the Image API and the Presentation API, a given URI for an Image Information request, an Image request, or a Manifest request will result in the same bytestream if access is granted, irrespective of credentials and user identity.

*Assumption 2:* The Image Information response always correctly describes the Image requests supported for the given base URI (scheme://server/prefix/identifier). This implies that different base URIs are required to support degraded and full access (or multiple levels of degraded access).

## U1. \<img\> tag inclusion of access controlled IIIF image

In the case of an IIIF Image API URI in a HTML \<img\> tag, where credentials are required for access, it would be good for a user with no credentials to be directed to an authentication page to obtain credentials (or explain other circumstances such as location based access restrictions).

## U2. \<img\> tag inclusion of access controlled IIIF image with a degraded version

In the case of an IIIF Image API URI in a HTML \<img\> tag where credentials are required for high-quality access, but where a degraded version is available without these credentials, a user viewing the HTML page should see the degraded version without the need for any intervention. (No means provided to obtain credentials.)

## U3. Image API client with access controlled image

A user without appropriate credentials attempts to access an access controlled image. The user should be directed to obtain credentials with sufficient information to understand what they need credentials for and where they have been sent. On successfully obtaining credentials the user should see the image as if they had had the credentials originally.

## U4. Image API client provides public access to degraded image, credentials provide better access

A user without appropriate credentials should see the image in degraded form without the need for any additional intervention. They should be made aware that a higher quality image is available if they obtain certain credentials. They should have the option to click through to the authentication page where they can obtain these credentials (or explaining other circumstances such as location based access restrictions). On successfully obtaining credentials the user should be back in the same state as before but have access to the higher quality image (perhaps non-degraded at the same resolution, offering a higher maximum resolution, or perhaps with download enabled). If the user fails to obtain credentials they should be able to get back to where they were before.

## U5. Presentation API client where the view includes access controlled images

A user should see in the client view all images that are public or for which they have appropriate credentials. They should be made aware of any images for which they are denied access and provided with directions allowing them to obtain credentials (or explaining other circumstances such as location based access restrictions). There may be multiple images from multiple authorization domains that require different credentials, requiring this process to be repeated for the different authorization domains.

## U6. Presentation API client provides public access to degraded images, credentials provide better access.

A user should see in the client view all images that are public and the degraded public access versions of images for which they do not have credentials to see the higher quality versions. They should be made aware that in some cases a higher quality image is available if they obtain certain credentials. They should have the option to click through to an authentication page where they can obtain these credentials (or see an explanation of other circumstances such as location based access restrictions). There may be multiple images from multiple authorization domains that require different credentials. On successfully obtaining credentials that unlock a higher quality image the user should be back in the same state as before but have access to the higher quality image (perhaps non-degraded at the same resolution, offering a higher maximum resolution, or perhaps with download enabled). If the user fails to obtain credentials they should be able to get back to where they were before. This process may be repeated for multiple authorization domains and may be combined with U5.

## U7. Handle access controlled Manifest in Presentation API client

A user without appropriate credentials to access a manifest should understand that access has been denied and be directed to an authorization page to obtain credentials (or explain other circumstances such as location based access restrictions). On successfully obtaining credentials they should see the same view as they would have had had access been granted initially.

## U8. Provide degraded access Manifest in Presentation API client, credentials provide Manifest for higher-quality view

A user without appropriate credentials to see the high-quality view should see a rendering based on the "degraded access Manifest" (might have some images missing, have limited additional information, or point to degraded images). They should be made aware that a higher quality view is available if they obtain certain credentials. They should have the option to click through to an authentication page where they can obtain these credentials (or see an explanation of other circumstances such as location based access restrictions). On successfully obtaining credentials the user should see the high-quality view (there may still be individual images with access conditions: U5, U6). If the user fails to obtain credentials they should be able to return to the degraded view.
