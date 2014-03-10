# Annex: Calculating the Size of a Rotated Image

As described in the IIIF Image API, [Section 4.3 (Rotation)](image_api.html#43-rotation), in order to retain the size of the requested image contents rotation will change the width and height dimensions of the returned image file. To calculate the dimensions of the returned image file for a given rotation in compliance with the IIIF API, the following formula can be used:

![Formula for calculating image size of rotated image](images/iiif-rotated-img-size.png "Formula for calculating image size of rotated image")

Please send feedback to iiif-feedback@googlegroups.com.
