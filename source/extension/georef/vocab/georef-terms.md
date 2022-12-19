# New terms introduced in the Allmaps + IIIF Georeferencing Extension

## resourceCoords
A property that appears inside of a GeoJSON Feature's `properties`.  It is a pixel coordinate array representing a pixel coordinate point on the resource.  It is used to align the pixel coordinate point from the resource to a WGS84 geographic coordinate point.

## georeferencing
The Web Annotation `motivation` value for when the user intends to georeference the target resource so that the target resource can be displayed within a finite area of a projection of the surface of the Earth.

## transformation
A property that appears on a Feature Collection to supply the preferred transformation algoritm for all of its Features.  The data in the `transformation` property is used to create a complete mapping from pixel coordinates to geographic coordinates (and vice versa), based on a list of GCPs. The value is a JSON object which includes the properties `type` and `options`.

## options
A property that appears within a `transformation` JSON object to supply additional parameters related to the selected transformation `type`.  Not all transformation types require the `options` property.

## order
A property that appears within a `transformation` JSON object with a `polynomial` transformation type.  The value will be `1` for first order linear transformations, `2` for second order quadratic transformation, or `3` for third order cubic transformations.

## polynomial
A typical transformation type that means...

## thinPlateSpline
A typical transformation type that means...also known as "rubber sheeting"



