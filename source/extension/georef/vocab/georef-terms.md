# New terms introduced in the Georeference Extension

## `georeferencing`

Georeference Annotations use `georeferencing` as the value for their [motivation](https://www.w3.org/TR/annotation-model/#motivation-and-purpose). The `motivation` property is part of the [Web Annotation specification](https://www.w3.org/TR/annotation-model/).

## `resourceCoords`

The `resourceCoords` property appears inside each `properties` object of each Ground Control Point (GCP).  It defines the resource coordinates of the GCP.

## `transformation`

The `transformation` property may appear in the body of a Georeference Annotation to supply clients with information about the preferred transformation algorithm. Its value is a JSON object with properties `type` and `options`.

## `type`

The preferred transformation algorithm that clients should use for the GCPs in a specific Georeference Annotation.  It appears as the `type` property of a `transformation` object and does not override the meaning of any other `type` property. Valid values are `thinPlateSpline` and `polynomial`.

## `options`

A property that appears within a `transformation` object to supply additional parameters related to the selected transformation type.

## `order`

A property that appears within a `transformation` object with a `polynomial` transformation type.  The value will be `1` for first order linear transformations, `2` for second order quadratic transformation, or `3` for third order cubic transformations.

## `thinPlateSpline`

`thinPlateSpline` is one of the possible values of the transformation `type` property. It means that 'thin plate spline' transformation algorithm should be used. Thin plate spline is also known as _rubbersheeting_.

## `polynomial`

`polynomial` is one of the possible values of the transformation `type` property.  It indicates that a first, second or third order polynomial transformation should be used.
