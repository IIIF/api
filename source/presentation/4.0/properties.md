# Vocabulary?

## Resource Classes

* Collection
* CollectionPage
* Manifest
* Containers
    * Timeline
    * Canvas
    * Scene
* Content Resources
* Range
* Cameras
    * PerspectiveCamera
    * OrthographicCamera
* Lights
    * AmbientLight
    * DirectionalLight
    * PointLight
    * SpotLight
* Transforms
    * TranslateTransform
    * RotateTransform
    * ScaleTransform
* Selectors
    * PointSelector
    * WktSelector (need both LineString Z and Polygon Z)
    * AudioContentSelector
    * VisualContentSelector
    * AnimationSelector
    * ImageApiSelector
* Other Classes
    * Agent
    * Service
    * Value (used for `intensity`)

* Annotation Classes imported from WADM:
    * Annotation
    * AnnotationCollection
    * AnnotationPage
    * SpecificResource
    * FragmentSelector
    * SvgSelector
    * CssStyle
    * TextualBody
    * Choice


## Resource Properties

### Descriptive Properties

##### label

A human readable label, name or title. The `label` property is intended to be displayed as a short, textual surrogate for the resource if a human needs to make a distinction between it and similar resources, for example between objects, pages, or options for a choice of images to display. The `label` property can be fully internationalized, and each language can have multiple values.  This pattern is described in more detail in the [languages][prezi30-languages] section.

The value of the property _MUST_ be a JSON object, as described in the [languages][prezi30-languages] section.

 * A Collection _MUST_ have the `label` property with at least one entry.<br/>
   Clients _MUST_ render `label` on a Collection.
 * A Manifest _MUST_ have the `label` property with at least one entry.<br/>
   Clients _MUST_ render `label` on a Manifest.
 * All Container types _SHOULD_ have the `label` property with at least one entry.<br/>
   Clients _MUST_ render `label` on Container types, and _SHOULD_ generate a `label` for Containers that do not have them.
 * All Content Resource types _MAY_ have the `label` property with at least one entry. If there is a Choice of Content Resource for the same Container, then they _SHOULD_ each have the `label` property with at least one entry.<br/>
   Clients _MAY_ render `label` on Content Resources, and _SHOULD_ render them when part of a Choice.
 * A Range _SHOULD_ have the `label` property with at least one entry. <br/>
   Clients _MUST_ render `label` on a Range.
 * An Annotation Collection _SHOULD_ have the `label` property with at least one entry.<br/>
   Clients _SHOULD_ render `label` on an Annotation Collection.
 * Other types of resource _MAY_ have the `label` property with at least one entry.<br/>
   Clients _MAY_ render `label` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "label": { "en": [ "Example Object Title" ] } }
```

##### metadata

An ordered list of descriptions to be displayed to the user when they interact with the resource, given as pairs of human readable `label` and `value` entries. The content of these entries is intended for presentation only; descriptive semantics _SHOULD NOT_ be inferred. An entry might be used to convey information about the creation of the object, a physical description, ownership information, or other purposes.

The value of the `metadata` property _MUST_ be an array of JSON objects, where each item in the array has both `label` and `value` properties. The values of both `label` and `value` _MUST_ be JSON objects, as described in the [languages][prezi30-languages] section.

 * A Collection _SHOULD_ have the `metadata` property with at least one item. <br/>
   Clients _MUST_ render `metadata` on a Collection.
 * A Manifest _SHOULD_ have the `metadata` property with at least one item.<br/>
   Clients _MUST_ render `metadata` on a Manifest.
 * All Container types _MAY_ have the `metadata` property with at least one item.<br/>
   Clients _SHOULD_ render `metadata` on Containers.
 * Other types of resource _MAY_ have the `metadata` property with at least one item.<br/>
   Clients _MAY_ render `metadata` on other types of resource.

Clients _SHOULD_ display the entries in the order provided. Clients _SHOULD_ expect to encounter long texts in the `value` property, and render them appropriately, such as with an expand button, or in a tabbed interface.

{% include api/code_header.html %}
``` json-doc
{
  "metadata": [
    {
      "label": { "en": [ "Creator" ] },
      "value": { "en": [ "Anne Artist (1776-1824)" ] }
    }
  ]
}
```

##### summary

A short textual summary intended to be conveyed to the user when the `metadata` entries for the resource are not being displayed. This could be used as a brief description for item level search results, for small-screen environments, or as an alternative user interface when the `metadata` property is not currently being rendered. The `summary` property follows the same pattern as the `label` property described above.

The value of the property _MUST_ be a JSON object, as described in the [languages][prezi30-languages] section.

 * A Collection _SHOULD_ have the `summary` property with at least one entry.<br/>
   Clients _SHOULD_ render `summary` on a Collection.
 * A Manifest _SHOULD_ have the `summary` property with at least one entry.<br/>
   Clients _SHOULD_ render `summary` on a Manifest.
 * All Container types _MAY_ have the `summary` property with at least one entry.<br/>
   Clients _SHOULD_ render `summary` on Containers.
 * Other types of resource _MAY_ have the `summary` property with at least one entry.<br/>
   Clients _MAY_ render `summary` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "summary": { "en": [ "This is a summary of the object." ] } }
```

##### requiredStatement

Text that _MUST_ be displayed when the resource is displayed or used. For example, the `requiredStatement` property could be used to present copyright or ownership statements, an acknowledgement of the owning and/or publishing institution, or any other text that the publishing organization deems critical to display to the user. Given the wide variation of potential client user interfaces, it will not always be possible to display this statement to the user in the client's initial state. If initially hidden, clients _MUST_ make the method of revealing it as obvious as possible.

The value of the property _MUST_ be a JSON object, that has the `label` and `value` properties, in the same way as a `metadata` property entry. The values of both `label` and `value` _MUST_ be JSON objects, as described in the [languages][prezi30-languages] section.

 * Any resource type _MAY_ have the `requiredStatement` property.<br/>
   Clients _MUST_ render `requiredStatement` on every resource type.

{% include api/code_header.html %}
``` json-doc
{
  "requiredStatement": {
    "label": { "en": [ "Attribution" ] },
    "value": { "en": [ "Provided courtesy of Example Institution" ] }
  }
}
```

##### rights

A string that identifies a license or rights statement that applies to the content of the resource, such as the JSON of a Manifest or the pixels of an image. The value _MUST_ be drawn from the set of [Creative Commons][org-cc-licenses] license URIs, the [RightsStatements.org][org-rs-terms] rights statement URIs, or those added via the [extension][prezi30-ldce] mechanism. The inclusion of this property is informative, and for example could be used to display an icon representing the rights assertions.

If displaying rights information directly to the user is the desired interaction, or a publisher-defined label is needed, then it is _RECOMMENDED_ to include the information using the `requiredStatement` property or in the `metadata` property.

The value _MUST_ be a string. If the value is drawn from Creative Commons or RightsStatements.org, then the string _MUST_ be a URI defined by that specification.

 * Any resource type _MAY_ have the `rights` property.<br/>
   Clients _MAY_ render `rights` on any resource type.

{% include api/code_header.html %}
``` json-doc
{ "rights": "http://creativecommons.org/licenses/by/4.0/" }
```

__Machine actionable URIs and links for users__<br/>
The machine actionable URIs for both Creative Commons licenses and RightsStatements.org right statements are `http` URIs. In both cases, human readable descriptions are available from equivalent `https` URIs. Clients may wish to rewrite links presented to users to use these equivalent `https` URIs.
{: .note}

##### provider

An organization or person that contributed to providing the content of the resource. Clients can then display this information to the user to acknowledge the provider's contributions.  This differs from the `requiredStatement` property, in that the data is structured, allowing the client to do more than just present text but instead have richer information about the people and organizations to use in different interfaces.

The organization or person is represented as an `Agent` resource.

* Agents _MUST_ have the `id` property, and its value _MUST_ be a string. The string _MUST_ be a URI that identifies the agent.
* Agents _MUST_ have the `type` property, and its value _MUST_ be the string `Agent`.
* Agents _MUST_ have the `label` property, and its value _MUST_ be a JSON object as described in the [languages][prezi30-languages] section.
* Agents _SHOULD_ have the `homepage` property, and its value _MUST_ be an array of JSON objects as described in the [homepage][prezi30-homepage] section.
* Agents _SHOULD_ have the `logo` property, and its value _MUST_ be an array of JSON objects as described in the [logo][prezi30-logo] section.
* Agents _MAY_ have the `seeAlso` property, and its value _MUST_ be an array of JSON object as described in the [seeAlso][prezi30-seealso] section.

The value _MUST_ be an array of JSON objects, where each item in the array conforms to the structure of an Agent, as described above.

 * A Collection _SHOULD_ have the `provider` property with at least one item. <br/>
   Clients _MUST_ render `provider` on a Collection.
 * A Manifest _SHOULD_ have the `provider` property with at least one item. <br/>
   Clients _MUST_ render `provider` on a Manifest.
 * Other types of resource _MAY_ have the `provider` property with at least one item. <br/>
   Clients _SHOULD_ render `provider` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "provider": [
    {
      "id": "https://example.org/about",
      "type": "Agent",
      "label": { "en": [ "Example Organization" ] },
      "homepage": [
        {
          "id": "https://example.org/",
          "type": "Text",
          "label": { "en": [ "Example Organization Homepage" ] },
          "format": "text/html"
        }
      ],
      "logo": [
        {
          "id": "https://example.org/images/logo.png",
          "type": "Image",
          "format": "image/png",
          "height": 100,
          "width": 120
        }
      ],
      "seeAlso": [
        {
          "id": "https://data.example.org/about/us.jsonld",
          "type": "Dataset",
          "format": "application/ld+json",
          "profile": "https://schema.org/"
        }
      ]
    }
  ]
}
```

##### thumbnail

A content resource, such as a small image or short audio clip, that represents the resource that has the `thumbnail` property. A resource _MAY_ have multiple thumbnail resources that have the same or different `type` and `format`.

The value _MUST_ be an array of JSON objects, each of which _MUST_ have the `id` and `type` properties, and _SHOULD_ have the `format` property. Images and videos _SHOULD_ have the `width` and `height` properties, and time-based media _SHOULD_ have the `duration` property. It is _RECOMMENDED_ that a [IIIF Image API][image-api] service be available for images to enable manipulations such as resizing.

 * A Collection _SHOULD_ have the `thumbnail` property with at least one item.<br/>
   Clients _SHOULD_ render `thumbnail` on a Collection.
 * A Manifest _SHOULD_ have the `thumbnail` property with at least one item.<br/>
   Clients _SHOULD_ render `thumbnail` on a Manifest.
 * All Container types _SHOULD_ have the `thumbnail` property with at least one item.<br/>
   Clients _SHOULD_ render `thumbnail` on Containers.
 * Content Resource types _MAY_ have the `thumbnail` property with at least one item. Content Resources _SHOULD_ have the `thumbnail` property with at least one item if it is an option in a Choice of resources.<br/>
   Clients _SHOULD_ render `thumbnail` on a content resource.
 * Other types of resource _MAY_ have the `thumbnail` property with at least one item.<br/>
   Clients _MAY_ render `thumbnail` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "thumbnail": [
    {
      "id": "https://example.org/img/thumb.jpg",
      "type": "Image",
      "format": "image/jpeg",
      "width": 300,
      "height": 200
    }
  ]
}
```

##### navDate

A date that clients may use for navigation purposes when presenting the resource to the user in a date-based user interface, such as a calendar or timeline. More descriptive date ranges, intended for display directly to the user, _SHOULD_ be included in the `metadata` property for human consumption. If the resource contains Canvases that have the `duration` property, the datetime given corresponds to the navigation datetime of the start of the resource. For example, a Range that includes a Canvas that represents a set of video content recording a historical event, the `navDate` is the datetime of the first moment of the recorded event.

The value _MUST_ be an [XSD dateTime literal][org-w3c-xsd-datetime]. The value _MUST_ have a timezone, and _SHOULD_ be given in UTC with the `Z` timezone indicator, but _MAY_ instead be given as an offset of the form `+hh:mm`.

 * A Collection _MAY_ have the `navDate` property.<br/>
   Clients _MAY_ render `navDate` on a Collection.
 * A Manifest _MAY_ have the `navDate` property.<br/>
   Clients _MAY_ render `navDate` on a Manifest.
 * A Range _MAY_ have the `navDate` property.<br/>
   Clients _MAY_ render `navDate` on a Range.
 * All Container types _MAY_ have the `navDate` property.<br/>
   Clients _MAY_ render `navDate` on Containers.
* Annotations _MAY_ have the `navDate` property.
   Clients _MAY_ render `navDate` on Annotations.   
 * Other types of resource _MUST NOT_ have the `navDate` property.<br/>
   Clients _SHOULD_ ignore `navDate` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "navDate": "2010-01-01T00:00:00Z" }
```

##### navPlace

A geographic location that clients may use for navigation purposes when presenting the resource to the user in a map-based user interface.

The value of the property _MUST_ be a [GeoJSON Feature Collection](link) containing one or more [Features](link).  The value _SHOULD_ be embedded and _MAY_ be a reference. Feature Collections referenced in the `navPlace` property _MUST_ have the `id` and `type` properties and _MUST NOT_ have the `features` property.

*   A Collection _MAY_ have the `navPlace` property.<br/>
   Clients _MAY_ render `navPlace` on a Collection.
*   A Manifest _MAY_ have the `navPlace` property.<br/>
   Clients _MAY_ render `navPlace` on a Manifest.
*   A Range _MAY_ have the `navPlace` property.<br/>
   Clients _MAY_ render `navPlace` on a Range.
* All Container types _MAY_ have the `navPlace` property.<br/>
   Clients _MAY_ render `navPlace` on Containers.
* Annotations _MAY_ have the `navPlace` property.
   Clients _MAY_ render `navPlace` on Annotations.   
*   Other types of resource _MUST NOT_ have the `navPlace` property.<br/>
   Clients _SHOULD_ ignore `navPlace` on other types of resource.


{% include api/code_header.html %}
```json-doc
{
   "navPlace":{
      "id": "http://example.com/feature-collection/1",
      "type": "FeatureCollection",
      "features":[
         {
            "id": "http://example.com/feature/1",
            "type": "Feature",
            "properties":{},
            "geometry":{
               "type": "Point",
               "coordinates":[
                  9.938,
                  51.533
               ]
            }
         }
      ]
   }
}
```


##### placeholderContainer

A single Container that provides additional content for use before the main content of the resource that has the `placeholderContainer` property is rendered, or as an advertisement or stand-in for that content. Examples include images, text and sound standing in for video content before the user initiates playback; or a film poster to attract user attention. The content provided by `placeholderContainer` differs from a thumbnail: a client might use `thumbnail` to summarize and navigate multiple resources, then show content from `placeholderContainer` as part of the initial presentation of a single resource. A placeholder Container is likely to have different dimensions to those of the Container(s) of the resource that has the `placeholderContainer` property. A placeholder Container may be of a different type from the resource that has the `placeholderContainer` property. For example, a `Scene` may have a placeholder Container of type `Canvas`.

Clients _MAY_ display the content of a linked placeholder Container when presenting the resource. When more than one such Container is available, for example if `placeholderContainer` is provided for the currently selected Range and the current Manifest, the client _SHOULD_ pick the one most specific to the content. Publishers _SHOULD NOT_ assume that the placeholder Container will be processed by all clients. Clients _SHOULD_ take care to avoid conflicts between time-based media in the rendered placeholder Container and the content of the resource that has the `placeholderContainer` property.

The value of `placeholderContainer` _MUST_ be a JSON object with the `id` and `type` properties.  The value of `type` _MUST_ be a Container type.  The JSON object _MAY_ have other properties valid for that Container type.

  * A Collection _MAY_ have the `placeholderContainer` property.<br/>
    Clients _MAY_ render `placeholderContainer` on a Collection.
  * A Manifest _MAY_ have the `placeholderContainer` property.<br/>
    Clients _MAY_ render `placeholderContainer` on a Manifest.
  * All Container types _MAY_ have the `placeholderContainer` property.<br/>
    Clients _MAY_ render `placeholderContainer` on Containers.
  * A Range _MAY_ have the `placeholderContainer` property.<br/>
    Clients _MAY_ render `placeholderContainer` on a Range.
  * Other types of resource _MUST NOT_ have the `placeholderContainer` property.<br/>
    Clients _SHOULD_ ignore `placeholderContainer` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "placeholderContainer": {
    "id": "https://example.org/iiif/1/canvas/placeholder",
    "type": "Canvas",
    "height": 1400,
    "width": 1200
  }
}
```

##### accompanyingContainer

A single Container that provides additional content for use while rendering the resource that has the `accompanyingContainer` property. Examples include an image to show while a duration-only Canvas is playing audio; or background audio to play while a user is navigating an image-only Manifest.

Clients _MAY_ display the content of an accompanying Container when presenting the resource. As with `placeholderContainer` above, when more than one accompanying Container is available, the client _SHOULD_ pick the one most specific to the content. Publishers _SHOULD NOT_ assume that the accompanying Container will be processed by all clients. Clients _SHOULD_ take care to avoid conflicts between time-based media in the accompanying Container and the content of the resource that has the `accompanyingContainer` property.

The value of `accompanyingContainer` _MUST_ be a JSON object with the `id` and `type` properties.  The value of `type` _MUST_ be a Container type.  The JSON object _MAY_ have other properties valid for that Container type.

 * A Collection _MAY_ have the `accompanyingContainer` property.<br/>
   Clients _MAY_ render `accompanyingContainer` on a Collection.
 * A Manifest _MAY_ have the `accompanyingContainer` property.<br/>
   Clients _MAY_ render `accompanyingContainer` on a Manifest.
 * All Container types _MAY_ have the `accompanyingContainer` property.<br/>
   Clients _MAY_ render `accompanyingContainer` on Containers.
 * A Range _MAY_ have the `accompanyingContainer` property.<br/>
   Clients _MAY_ render `accompanyingContainer` on a Range.
 * Other types of resource _MUST NOT_ have the `accompanyingContainer` property.<br/>
   Clients _SHOULD_ ignore `accompanyingContainer` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "accompanyingContainer": {
    "id": "https://example.org/iiif/1/timeline/accompany",
    "type": "Timeline",
    "duration": 180.0
  }
}
```



### Technical Properties

##### id

The URI that identifies the resource. If the resource is only available embedded  within another resource (see the [terminology section][prezi30-terminology] for an explanation of "embedded"), such as a Range within a Manifest, then the URI _MAY_ be the URI of the embedding resource with a unique fragment on the end. This is not true for Canvases, which _MUST_ have their own URI without a fragment.

The value _MUST_ be a string, and the value _MUST_ be an HTTP(S) URI for resources defined in this specification. If the resource is retrievable via HTTP(S), then the URI _MUST_ be the URI at which it is published. External resources, such as profiles, _MAY_ have non-HTTP(S) URIs defined by other communities.

The existence of an HTTP(S) URI in the `id` property does not mean that the URI will always be dereferencable.  If the resource with the `id` property is [embedded][prezi30-terminology], it _MAY_ also be dereferenceable. If the resource is referenced (again, see the [terminology section][prezi30-terminology] for an explanation of "referenced"), it _MUST_ be dereferenceable. The [definitions of the Resources][prezi30-resource-structure] give further guidance.

 * All resource types _MUST_ have the `id` property.<br/>
   Clients _MAY_ render `id` on any resource type, and _SHOULD_ render `id` on Collections, Manifests and Canvases.

{% include api/code_header.html %}
``` json-doc
{ "id": "https://example.org/iiif/1/manifest" }
```

##### type

The type or class of the resource. For classes defined for this specification, the value of `type` will be described in the sections below describing each individual class.

For content resources, the value of `type` is drawn from other specifications. Recommendations for common content types such as image, text or audio are given in the table below.

The JSON objects that appear in the value of the `service` property will have many different classes, and can be used to distinguish the sort of service, with specific properties defined in a [registered context document][prezi30-ldce].

The value _MUST_ be a string.

 * All resource types _MUST_ have the `type` property.<br/>
   Clients _MUST_ process, and _MAY_ render, `type` on any resource type.

| Class         | Description                      |
| ------------- | -------------------------------- |
| `Dataset`     | Data not intended to be rendered to humans directly, such as a CSV or RDF |
| `Image`       | Two dimensional visual resources primarily intended to be seen, such as might be rendered with an &lt;img> HTML tag |
| `Model`       | A three dimensional spatial model intended to be visualized, such as might be rendered with a 3d javascript library |
| `Sound`       | Auditory resources primarily intended to be heard, such as might be rendered with an &lt;audio> HTML tag |
| `Text`        | Resources primarily intended to be read |
| `Video`       | Moving images, with or without accompanying audio, such as might be rendered with a &lt;video> HTML tag |
{: .api-table #table-type}

{% include api/code_header.html %}
``` json-doc
{ "type": "Image" }
```

##### format

The specific media type (often called a MIME type) for a content resource, for example `image/jpeg`. This is important for distinguishing different formats of the same overall type of resource, such as distinguishing text in XML from plain text.

Note that this is different to the `formats` property in the [Image API][image-api], which gives the extension to use within that API. It would be inappropriate to use in this case, as `format` can be used with any content resource, not just images.

The value _MUST_ be a string, and it _SHOULD_ be the value of the `Content-Type` header returned when the resource is dereferenced.

 * A content resource _SHOULD_ have the `format` property.<br/>
   Clients _MAY_ render the `format` of any content resource.
 * Other types of resource _MUST NOT_ have the `format` property.<br/>
   Clients _SHOULD_ ignore `format` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "format": "application/xml" }
```

##### language

The language or languages used in the content of this external resource. This property is already available from the Web Annotation model for content resources that are the body or target of an Annotation, however it _MAY_ also be used for resources [referenced][prezi30-terminology] from `homepage`, `rendering`, and `partOf`.

The value _MUST_ be an array of strings. Each item in the array _MUST_ be a valid language code, as described in the [languages section][prezi30-languages].

 * An external resource _SHOULD_ have the `language` property with at least one item.<br/>
   Clients _SHOULD_ process the `language` of external resources.
 * Other types of resource _MUST NOT_ have the `language` property.<br/>
   Clients _SHOULD_ ignore `language` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "language": [ "en" ] }
```

##### profile

A schema or named set of functionality available from the resource. The profile can further clarify the `type` and/or `format` of an external resource or service, allowing clients to customize their handling of the resource that has the `profile` property.

The value _MUST_ be a string, either taken from the [profiles registry][registry-profiles] or a URI.

* Resources [referenced][prezi30-terminology] by the `seeAlso` or `service` properties _SHOULD_ have the `profile` property.<br/>
  Clients _SHOULD_ process the `profile` of a service or external resource.
* Other types of resource _MAY_ have the `profile` property.<br/>
  Clients _MAY_ process the `profile` of other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "profile": "https://example.org/profile/statuary" }
```

##### height

The height of the Canvas or external content resource. For content resources, the value is in pixels. For Canvases, the value does not have a unit. In combination with the width, it conveys an aspect ratio for the space in which content resources are located.

The value _MUST_ be a positive integer.

 * A Canvas _MAY_ have the `height` property. If it has a `height`, it _MUST_ also have a `width`.<br/>
   Clients _MUST_ process `height` on a Canvas.
 * Content resources _SHOULD_ have the `height` property, with the value given in pixels, if appropriate to the resource type.<br/>
   Clients _SHOULD_ process `height` on content resources.
 * Other types of resource _MUST NOT_ have the `height` property.<br/>
   Clients _SHOULD_ ignore `height` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "height": 1800 }
```

##### width

The width of the Canvas or external content resource. For content resources, the value is in pixels. For Canvases, the value does not have a unit. In combination with the height, it conveys an aspect ratio for the space in which content resources are located.

The value _MUST_ be a positive integer.

 * A Canvas _MAY_ have the `width` property. If it has a `width`, it _MUST_ also have a `height`.<br/>
   Clients _MUST_ process `width` on a Canvas.
 * Content resources _SHOULD_ have the `width` property, with the value given in pixels, if appropriate to the resource type.<br/>
   Clients _SHOULD_ process `width` on content resources.
 * Other types of resource _MUST NOT_ have the `width` property.<br/>
   Clients _SHOULD_ ignore `width` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "width": 1200 }
```

##### duration

The duration of the Canvas or external content resource, given in seconds.

The value _MUST_ be a positive floating point number.

 * A Canvas _MAY_ have the `duration` property.<br/>
   Clients _MUST_ process `duration` on a Canvas.
 * Content resources _SHOULD_ have the `duration` property, if appropriate to the resource type.<br/>
   Clients _SHOULD_ process `duration` on content resources.
 * Other types of resource _MUST NOT_ have a `duration`.<br/>
   Clients _SHOULD_ ignore `duration` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "duration": 125.0 }
```

##### viewingDirection

The direction in which a set of Canvases _SHOULD_ be displayed to the user. This specification defines four direction values in the table below. Others may be defined externally [as an extension][prezi30-ldce].

The value _MUST_ be a string.

 * A Collection _MAY_ have the `viewingDirection` property.<br/>
   Clients _SHOULD_ process `viewingDirection` on a Collection.
 * A Manifest _MAY_ have the `viewingDirection` property.<br/>
   Clients _SHOULD_ process `viewingDirection` on a Manifest.
 * A Range _MAY_ have the `viewingDirection` property.<br/>
   Clients _MAY_ process `viewingDirection` on a Range.
 * Other types of resource _MUST NOT_ have the `viewingDirection` property.<br/>
   Clients _SHOULD_ ignore `viewingDirection` on other types of resource.

| Value | Description |
| ----- | ----------- |
| `left-to-right` | The object is displayed from left to right. The default if not specified. |
| `right-to-left` | The object is displayed from right to left. |
| `top-to-bottom` | The object is displayed from the top to the bottom. |
| `bottom-to-top` | The object is displayed from the bottom to the top. |
{: .api-table #table-direction}

{% include api/code_header.html %}
``` json-doc
{ "viewingDirection": "left-to-right" }
```

##### behavior

A set of user experience features that the publisher of the content would prefer the client to use when presenting the resource. This specification defines the values in the table below. Others may be defined externally as an [extension][prezi30-ldce].

In order to determine the behaviors that are governing a particular resource, there are four inheritance rules from resources that reference the current resource:
* Collections inherit behaviors from their referencing Collection.
* Manifests **DO NOT** inherit behaviors from any referencing Collections.
* Canvases inherit behaviors from their referencing Manifest, but **DO NOT** inherit behaviors from any referencing Ranges, as there might be several with different behaviors.
* Ranges inherit behaviors from any referencing Range and referencing Manifest.

Clients should interpret behaviors on a Range only when that Range is selected or is in some other way the context for the user's current interaction with the resources. A Range with the `behavior` value `continuous`, in a Manifest with the `behavior` value `paged`, would mean that the Manifest's Canvases should be rendered in a paged fashion, unless the range is selected to be viewed, and its included Canvases would be rendered in that context only as being virtually stitched together. This might occur, for example, when a physical scroll is cut into pages and bound into a codex with other pages, and the publisher would like to provide the user the experience of the scroll in its original form.

The descriptions of the behavior values have a set of which other values they are disjoint with, meaning that the same resource _MUST NOT_ have both of two or more from that set. In order to determine which is in effect, the client _SHOULD_ follow the inheritance rules above, taking the value from the closest resource. The user interface effects of the possible permutations of non-disjoint behavior values are client dependent, and implementers are advised to look for relevant recipes in the [IIIF cookbook][annex-cookbook].

__Future Clarification Anticipated__<br/>
Further clarifications about the implications of interactions between behavior values should be expected in subsequent minor releases.
{: .warning}

The value _MUST_ be an array of strings.

 * Any resource type _MAY_ have the `behavior` property with at least one item.<br/>
   Clients _SHOULD_ process `behavior` on any resource type.

| Value | Description |
| ----- | ----------- |
|| **Temporal Behaviors** |
| `auto-advance`{: style="white-space:nowrap;"} | Valid on Collections, Manifests, Canvases, and Ranges that include or are Canvases with at least the `duration` dimension. When the client reaches the end of a Canvas, or segment thereof as specified in a Range, with a duration dimension that has this behavior, it _SHOULD_ immediately proceed to the next Canvas or segment and render it. If there is no subsequent Canvas in the current context, then this behavior should be ignored. When applied to a Collection, the client should treat the first Canvas of the next Manifest as following the last Canvas of the previous Manifest, respecting any `start` property specified. Disjoint with `no-auto-advance`. |
| `no-auto-advance`{: style="white-space:nowrap;"} | Valid on Collections, Manifests, Canvases, and Ranges that include or are Canvases with at least the `duration` dimension. When the client reaches the end of a Canvas or segment with a duration dimension that has this behavior, it _MUST NOT_ proceed to the next Canvas, if any. This is a default temporal behavior if not specified. Disjoint with `auto-advance`.|
| `repeat` | Valid on Collections and Manifests, that include Canvases that have at least the `duration` dimension. When the client reaches the end of the duration of the final Canvas in the resource, and the `behavior` value `auto-advance`{: style="white-space:nowrap;"} is also in effect, then the client _SHOULD_ return to the first Canvas, or segment of Canvas, in the resource that has the `behavior` value `repeat` and start playing again. If the `behavior` value `auto-advance` is not in effect, then the client _SHOULD_ render a navigation control for the user to manually return to the first Canvas or segment. Disjoint with `no-repeat`.|
| `no-repeat` | Valid on Collections and Manifests, that include Canvases that have at least the `duration` dimension. When the client reaches the end of the duration of the final Canvas in the resource, the client _MUST NOT_ return to the first Canvas, or segment of Canvas. This is a default temporal behavior if not specified. Disjoint with `repeat`.|
| | **Layout Behaviors** |
| `unordered` | Valid on Collections, Manifests and Ranges. The Canvases included in resources that have this behavior have no inherent order, and user interfaces _SHOULD_ avoid implying an order to the user. Disjoint with `individuals`, `continuous`, and `paged`.|
| `individuals` | Valid on Collections, Manifests, and Ranges. For Collections that have this behavior, each of the included Manifests are distinct objects in the given order. For Manifests and Ranges, the included Canvases are distinct views, and _SHOULD NOT_ be presented in a page-turning interface. This is the default layout behavior if not specified. Disjoint with `unordered`, `continuous`, and `paged`. |
| `continuous` | Valid on Collections, Manifests and Ranges, which include Canvases that have at least `height` and `width` dimensions. Canvases included in resources that have this behavior are partial views and an appropriate rendering might display all of the Canvases virtually stitched together, such as a long scroll split into sections. This behavior has no implication for audio resources. The `viewingDirection` of the Manifest will determine the appropriate arrangement of the Canvases. Disjoint with `unordered`, `individuals` and `paged`. |
| `paged` | Valid on Collections, Manifests and Ranges, which include Canvases that have at least `height` and `width` dimensions. Canvases included in resources that have this behavior represent views that _SHOULD_ be presented in a page-turning interface if one is available. The first canvas is a single view (the first recto) and thus the second canvas likely represents the back of the object in the first canvas. If this is not the case, see the `behavior` value `non-paged`. Disjoint with `unordered`, `individuals`, `continuous`, `facing-pages` and `non-paged`. |
| `facing-pages`{: style="white-space:nowrap;"} | Valid only on Canvases, where the Canvas has at least `height` and `width` dimensions. Canvases that have this behavior, in a Manifest that has the `behavior` value `paged`, _MUST_ be displayed by themselves, as they depict both parts of the opening. If all of the Canvases are like this, then page turning is not possible, so simply use `individuals` instead. Disjoint with `paged` and `non-paged`.|
| `non-paged` | Valid only on Canvases, where the Canvas has at least `height` and `width` dimensions. Canvases that have this behavior _MUST NOT_ be presented in a page turning interface, and _MUST_ be skipped over when determining the page order. This behavior _MUST_ be ignored if the current Manifest does not have the `behavior` value `paged`. Disjoint with `paged` and `facing-pages`. |
| | **Collection Behaviors** |
| `multi-part` | Valid only on Collections. Collections that have this behavior consist of multiple Manifests or Collections which together form part of a logical whole or a contiguous set, such as multi-volume books or a set of journal issues. Clients might render these Collections as a table of contents rather than with thumbnails, or provide viewing interfaces that can easily advance from one member to the next. Disjoint with `together`.|
| `together` | Valid only on Collections. A client _SHOULD_ present all of the child Manifests to the user at once in a separate viewing area with its own controls. Clients _SHOULD_ catch attempts to create too many viewing areas. This behavior _SHOULD NOT_ be interpreted as applying to the members of any child resources. Disjoint with `multi-part`.|
| | **Range Behaviors** |
| `sequence` | Valid only on Ranges, where the Range is [referenced][prezi30-terminology] in the `structures` property of a Manifest. Ranges that have this behavior represent different orderings of the Canvases listed in the `items` property of the Manifest, and user interfaces that interact with this order _SHOULD_ use the order within the selected Range, rather than the default order of `items`. Disjoint with `thumbnail-nav` and `no-nav`.|
| `thumbnail-nav`{: style="white-space:nowrap;"} | Valid only on Ranges. Ranges that have this behavior _MAY_ be used by the client to present an alternative navigation or overview based on thumbnails, such as regular keyframes along a timeline for a video, or sections of a long scroll. Clients _SHOULD NOT_ use them to generate a conventional table of contents. Child Ranges of a Range with this behavior _MUST_ have a suitable `thumbnail` property. Disjoint with `sequence` and `no-nav`.|
| `no-nav` | Valid only on Ranges. Ranges that have this behavior _MUST NOT_ be displayed to the user in a navigation hierarchy. This allows for Ranges to be present that capture unnamed regions with no interesting content, such as the set of blank pages at the beginning of a book, or dead air between parts of a performance, that are still part of the Manifest but do not need to be navigated to directly. Disjoint with `sequence` and `thumbnail-nav`.|
| | **Miscellaneous Behaviors** |
| `hidden` | Valid on Annotation Collections, Annotation Pages, Annotations, Specific Resources and Choices. If this behavior is provided, then the client _SHOULD NOT_ render the resource by default, but allow the user to turn it on and off. This behavior does not inherit, as it is not valid on Collections, Manifests, Ranges or Canvases. |
{: .api-table #table-behavior}

{% include api/code_header.html %}
``` json-doc
{ "behavior": [ "auto-advance", "individuals" ] }
```

##### timeMode

A mode associated with an Annotation that is to be applied to the rendering of any time-based media, or otherwise could be considered to have a duration, used as a body resource of that Annotation. Note that the association of `timeMode` with the Annotation means that different resources in the body cannot have different values. This specification defines the values specified in the table below. Others may be defined externally as an [extension][prezi30-ldce].

The value _MUST_ be a string.

 * An Annotation _MAY_ have the `timeMode` property.<br/>
   Clients _SHOULD_ process `timeMode` on an Annotation.

| Value | Description |
| ----- | ----------- |
| `trim` | (default, if not supplied) If the content resource has a longer duration than the duration of portion of the Canvas it is associated with, then at the end of the Canvas's duration, the playback of the content resource _MUST_ also end. If the content resource has a shorter duration than the duration of the portion of the Canvas it is associated with, then, for video resources, the last frame _SHOULD_ persist on-screen until the end of the Canvas portion's duration. For example, a video of 120 seconds annotated to a Canvas with a duration of 100 seconds would play only the first 100 seconds and drop the last 20 second. |
| `scale` | Fit the duration of content resource to the duration of the portion of the Canvas it is associated with by scaling. For example, a video of 120 seconds annotated to a Canvas with a duration of 60 seconds would be played at double-speed. |
| `loop` | If the content resource is shorter than the `duration` of the Canvas, it _MUST_ be repeated to fill the entire duration. Resources longer than the `duration` _MUST_ be trimmed as described above. For example, if a 20 second duration audio stream is annotated onto a Canvas with duration 30 seconds, it will be played one and a half times. |
{: .api-table #table-timemode}

{% include api/code_header.html %}
``` json-doc
{ "timeMode": "trim" }
```

#### backgroundColor

This property sets the background color behind any painted resources on a spatial resource, such as a Canvas or Scene.

The value _MUST_ be string, which defines an RGB color. It SHOULD be a hex value starting with "#" and is treated in a case-insensitive fashion. If this property is not specified, then the default value is client-dependent.

 * A Canvas _MAY_ have the `backgroundColor` property<br/>
   Clients _SHOULD_ render `backgroundColor` on any resource type.
 * A Scene _MAY_ have the `backgroundColor` property<br/>
   Clients _SHOULD_ render `backgroundColor` on any resource type.
 * Other resources _MUST NOT_ have the `backgroundColor` property.

```json
"backgroundColor": "#FFFFFF"
```

<div style="background: #A0F0A0; padding: 10px; padding-left: 30px; margin-bottom: 10px">
❓Can you set bgColor on a transparent image? An area? Conflict with `style` on a SpecificResource?
</div>



##### near

This property gives the distance from the camera from which objects are visible. Objects closer to the camera than the `near` distance cannot be seen.

The value is a non-negative floating point number. If this property is not specified, then the default value is client-dependent.

* A Camera _MAY_ have the `near` property<br/>
  Clients _SHOULD_ process the `near` property on Cameras.

```json
"near": 1.5
```

##### far

This property gives the distance from the camera after which objects are no longer visible. Objects further from the camera than the `far` distance cannot be seen.

The value is a non-negative floating point number, and _MUST_ be greater than the value for `near` on the same camera. If this property is not specified, then the default value is client-dependent.

* A Camera _MAY_ have the `far` property<br/>
  Clients _SHOULD_ process the `far` property on Cameras.

```json
"far": 200.0
```

##### fieldOfView

_Summary here_

The value _MUST_ be a floating point number greater than 0 and less than 180. If this property is not specified, then the default value is client-dependent.

* A PerspectiveCamera _SHOULD_ have the `fieldOfView` property.<br/>
  Clients _SHOULD_ process the `fieldOfView` property on Cameras.

```json
  "fieldOfView": 50.0
```

##### angle

_Summary here_

The value _MUST_ be a floating point number greater than 0 and less than 90. If this property is not specified, then the default value is client-dependent.

* A SpotLight _SHOULD_ have the `angle` property.<br/>
  Clients _SHOULD_ process the `angle` property on SpotLights.

```json
  "angle": 15.0
```

##### lookAt

_Summary here_

The value _MUST_ be a JSON object, conforming to either a reference to an Annotation with an `id` and a `type` of "Anntoation", or a PointSelector. If this property is not specified, then the default value is null -- the camera or light is not looking at anything.

```json
"lookAt": {
    "type": "PointSelector",
    "x": 3,
    "y": 0,
    "z": -10
}
```

##### color

This property sets the color of a Light.

The value _MUST_ be string, which defines an RGB color. It SHOULD be a hex value starting with "#" and is treated in a case-insensitive fashion. If this property is not specified, then the default value is "#FFFFFF".

 * A Light _SHOULD_ have the `color` property<br/>
   Clients _SHOULD_ render `color` on any resource type.
 * Other resources _MUST NOT_ have the `color` property.

```json
"color": "#FFA0A0"
```

##### intensity

This property sets the strength or brightness of a Light.

The value _MUST_ be a JSON object, that has the `type`, `value` and `unit` properties. All three properties are required. The value of `type` _MUST_ be the string "Value". The value of `value` is a floating point number. The value of `unit` is a string, drawn from a controlled vocabulary of units. If this property is not specified, then the default intensity value is client-dependent.

This specification defines the unit value of "relative" which constrains the value to be a linear scale between 0.0 (no brightness) and 1.0 (as bright as the client will render).

* A Light _SHOULD_ have the `intensity` property.<br/>
  Clients _SHOULD_ process the `intensity` property on Lights.

```json
{
 "intensity": {"type": "Value", "value": 0.5, "unit": "relative"}
}
```

##### Exclude

_Summary here_

_On Annotation, a list of strings drawn from table_

| Value      | Description |
|------------|-------------|
| Audio      | |
| Animations | |
| Cameras    | |
| Lights     | |

```json
"exclude": [ "Audio", "Lights", "Cameras", "Animations" ]
```


##### transform

_Summary here_

The value of this property is an array of JSON objects, each of which is a Transform.

##### x

##### y

##### z


### Linking Properties


##### homepage

A web page that is about the object represented by the resource that has the `homepage` property. The web page is usually published by the organization responsible for the object, and might be generated by a content management system or other cataloging system. The resource _MUST_ be able to be displayed directly to the user. Resources that are related, but not home pages, _MUST_ instead be added into the `metadata` property, with an appropriate `label` or `value` to describe the relationship.

The value of this property _MUST_ be an array of JSON objects, each of which _MUST_ have the `id`, `type`, and `label` properties, _SHOULD_ have a `format` property, and _MAY_ have the `language` property.

 * Any resource type _MAY_ have the `homepage` property.<br/>
   Clients _SHOULD_ render `homepage` on a Collection, Manifest or Canvas, and _MAY_ render `homepage` on other types of resource.

__Model Alignment__<br/>
Please note that this specification has stricter requirements about the JSON pattern used for the `homepage` property than the [Web Annotation Data Model][org-w3c-webanno]. The IIIF requirements are compatible, but the home page of an Agent found might have only a URI, or might be a JSON object with other properties. See the section on [collisions between contexts][prezi30-context-collisions] for more information.
{: .note}

{% include api/code_header.html %}
``` json-doc
{
  "homepage": [
    {
      "id": "https://example.com/info/",
      "type": "Text",
      "label": { "en": [ "Homepage for Example Object" ] },
      "format": "text/html",
      "language": [ "en" ]
    }
  ]
}
```


##### logo

A small image resource that represents the Agent resource it is associated with. The logo _MUST_ be clearly rendered when the resource is displayed or used, without cropping, rotating or otherwise distorting the image. It is _RECOMMENDED_ that a [IIIF Image API][image-api] service be available for this image for other manipulations such as resizing.

When more than one logo is present, the client _SHOULD_ pick only one of them, based on the information in the logo properties. For example, the client could select a logo of appropriate aspect ratio based on the `height` and `width` properties of the available logos. The client _MAY_ decide on the logo by inspecting properties defined as [extensions][prezi30-ldce].

The value of this property _MUST_ be an array of JSON objects, each of which _MUST_ have `id` and `type` properties, and _SHOULD_ have `format`. The value of `type` _MUST_ be "Image".

 * Agent resources _SHOULD_ have the `logo` property.<br/>
   Clients _MUST_ render `logo` on Agent resources.


{% include api/code_header.html %}
``` json-doc
{
  "logo": [
    {
      "id": "https://example.org/img/logo.jpg",
      "type": "Image",
      "format": "image/jpeg",
      "height": 100,
      "width": 120
    }
  ]
}
```

##### rendering

A resource that is an alternative, non-IIIF representation of the resource that has the `rendering` property. Such representations typically cannot be painted onto a single Canvas, as they either include too many views, have incompatible dimensions, or are compound resources requiring additional rendering functionality. The `rendering` resource _MUST_ be able to be displayed directly to a human user, although the presentation may be outside of the IIIF client. The resource _MUST NOT_ have a splash page or other interstitial resource that mediates access to it. If access control is required, then the [IIIF Authentication API][iiif-auth] is _RECOMMENDED_. Examples include a rendering of a book as a PDF or EPUB, a slide deck with images of a building, or a 3D model of a statue.

The value _MUST_ be an array of JSON objects. Each item _MUST_ have the `id`, `type` and `label` properties, and _SHOULD_ have a `format` property.

 * Any resource type _MAY_ have the `rendering` property with at least one item.<br/>
   Clients _SHOULD_ render `rendering` on a Collection, Manifest or Canvas, and _MAY_ render `rendering` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "rendering": [
    {
      "id": "https://example.org/1.pdf",
      "type": "Text",
      "label": { "en": [ "PDF Rendering of Book" ] },
      "format": "application/pdf"
    }
  ]
}
```

##### service

A service that the client might interact with directly and gain additional information or functionality for using the resource that has the `service` property, such as from an Image to the base URI of an associated [IIIF Image API][image-api] service. The service resource _SHOULD_ have additional information associated with it in order to allow the client to determine how to make appropriate use of it. Please see the [Service Registry][registry-services] document for the details of currently known service types.

The value _MUST_ be an array of JSON objects. Each object will have properties depending on the service's definition, but _MUST_ have either the `id` or `@id` and `type` or `@type` properties. Each object _SHOULD_ have a `profile` property.

 * Any resource type _MAY_ have the `service` property with at least one item.<br/>
   Clients _MAY_ process `service` on any resource type, and _SHOULD_ process the IIIF Image API service.

{% include api/code_header.html %}
``` json-doc
{
  "service": [
    {
      "id": "https://example.org/service",
      "type": "ExampleExtensionService",
      "profile": "https://example.org/docs/service"
    }
  ]
}
```

For cross-version consistency, this specification defines the following values for the `type` or `@type` property for backwards compatibility with other IIIF APIs. Future versions of these APIs will define their own types. These `type` values are necessary extensions for compatibility of the older versions.

| Value                | Specification |
| -------------------- | ------------- |
| ImageService1        | [Image API version 1][image11]  |
| ImageService2        | [Image API version 2][image21]  |
| SearchService1       | [Search API version 1][search1] |
| AutoCompleteService1 | [Search API version 1][search1-autocomplete] |
| AuthCookieService1   | [Authentication API version 1][auth1-cookie-service] |
| AuthTokenService1    | [Authentication API version 1][auth1-token-service] |
| AuthLogoutService1   | [Authentication API version 1][auth1-logout-service] |
{: .api-table #table-service-types}

Implementations _SHOULD_ be prepared to recognize the `@id` and `@type` property names used by older specifications, as well as `id` and `type`. Note that the `@context` key _SHOULD NOT_ be present within the `service`, but instead included at the beginning of the document. The example below includes both version 2 and version 3 IIIF Image API services.

{% include api/code_header.html %}
``` json-doc
{
  "service": [
    {
      "@id": "https://example.org/iiif2/image1/identifier",
      "@type": "ImageService2",
      "profile": "http://iiif.io/api/image/2/level2.json"
    },
    {
      "id": "https://example.org/iiif3/image1/identifier",
      "type": "ImageService3",
      "profile": "level2"
    }
  ]
}
```


##### services

A list of one or more service definitions on the top-most resource of the document, that are typically shared by more than one subsequent resource. This allows for these shared services to be collected together in a single place, rather than either having their information duplicated potentially many times throughout the document, or requiring a consuming client to traverse the entire document structure to find the information. The resource that the service applies to _MUST_ still have the `service` property, as described above, where the service resources have at least the `id` and `type` or `@id` and `@type` properties. This allows the client to know that the service applies to that resource. Usage of the `services` property is at the discretion of the publishing system.

A client encountering a `service` property where the definition consists only of an `id` and `type` _SHOULD_ then check the `services` property on the top-most resource for an expanded definition.  If the service is not present in the `services` list, and the client requires more information in order to use the service, then it _SHOULD_ dereference the `id` (or `@id`) of the service in order to retrieve a service description.

The value _MUST_ be an array of JSON objects. Each object _MUST_ a service resource, as described above.

* A Collection _MAY_ have the `services` property, if it is the topmost Collection in a response document.<br/>
  Clients _SHOULD_ process `services` on a Collection.
* A Manifest _MAY_ have the `services` property.<br/>
  Clients _SHOULD_ process `services` on a Manifest.

{% include api/code_header.html %}
``` json-doc
{
  "services": [
    {
      "@id": "https://example.org/iiif/auth/login",
      "@type": "AuthCookieService1",
      "profile": "http://iiif.io/api/auth/1/login",
      "label": "Login to Example Institution",
      "service": [
        {
          "@id": "https://example.org/iiif/auth/token",
          "@type": "AuthTokenService1",
          "profile": "http://iiif.io/api/auth/1/token"          
        }
      ]
    }
  ]
}
```


##### seeAlso

A machine-readable resource such as an XML or RDF description that is related to the current resource that has the `seeAlso` property. Properties of the resource should be given to help the client select between multiple descriptions (if provided), and to make appropriate use of the document. If the relationship between the resource and the document needs to be more specific, then the document should include that relationship rather than the IIIF resource. Other IIIF resources are also valid targets for `seeAlso`, for example to link to a Manifest that describes a related object. The URI of the document _MUST_ identify a single representation of the data in a particular format. For example, if the same data exists in JSON and XML, then separate resources should be added for each representation, with distinct `id` and `format` properties.

The value _MUST_ be an array of JSON objects. Each item _MUST_ have the `id` and `type` properties, and _SHOULD_ have the `label`, `format` and `profile` properties.

 * Any resource type _MAY_ have the `seeAlso` property with at least one item.<br/>
   Clients _MAY_ process `seeAlso` on any resource type.

{% include api/code_header.html %}
``` json-doc
{
  "seeAlso": [
    {
      "id": "https://example.org/library/catalog/book1.xml",
      "type": "Dataset",
      "label": { "en": [ "Bibliographic Description in XML" ] },
      "format": "text/xml",
      "profile": "https://example.org/profiles/bibliographic"
    }
  ]
}
```


#### abouty-field-name-here

Point to a `Dataset` with more semantics than just `seeAlso`


#### 3.3.2. Internal Links

##### partOf

A containing resource that includes the resource that has the `partOf` property. When a client encounters the `partOf` property, it might retrieve the [referenced][prezi30-terminology] containing resource, if it is not [embedded][prezi30-terminology] in the current representation, in order to contribute to the processing of the contained resource. For example, the `partOf` property on a Canvas can be used to reference an external Manifest in order to enable the discovery of further relevant information. Similarly, a Manifest can reference a containing Collection using `partOf` to aid in navigation.

The value _MUST_ be an array of JSON objects. Each item _MUST_ have the `id` and `type` properties, and _SHOULD_ have the `label` property.

 * Any resource type _MAY_ have the `partOf` property with at least one item<br/>
   Clients _MAY_ render `partOf` on any resource type.

{% include api/code_header.html %}
``` json-doc
{ "partOf": [ { "id": "https://example.org/iiif/1", "type": "Manifest" } ] }
```

The resources referred to by the `accompanyingContainer` and `placeholderContainer` properties are `partOf` that referring Container.


##### start

A Canvas, or part of a Canvas, which the client _SHOULD_ show on initialization for the resource that has the `start` property. The reference to part of a Canvas is handled in the same way that Ranges reference parts of Canvases. This property allows the client to begin with the first Canvas that contains interesting content rather than requiring the user to manually navigate to find it.

The value _MUST_ be a JSON object, which _MUST_ have the `id` and `type` properties.  The object _MUST_ be either a Canvas (as in the first example below), or a Specific Resource with a Selector and a `source` property where the value is a Canvas (as in the second example below).

 * A Manifest _MAY_ have the `start` property.<br/>
   Clients _SHOULD_ process `start` on a Manifest.
 * A Range _MAY_ have the `start` property.<br/>
   Clients _SHOULD_ process `start` on a Range.
 * Other types of resource _MUST NOT_ have the `start` property.<br/>
   Clients _SHOULD_ ignore `start` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "start": { "id": "https://example.org/iiif/1/canvas/1", "type": "Canvas" } }
```

{% include api/code_header.html %}
``` json-doc
{
  "start": {
    "id": "https://example.org/iiif/1/canvas-segment/1",
    "type": "SpecificResource",
    "source": "https://example.org/iiif/1/canvas/1",
    "selector": {
      "type": "PointSelector",
      "t": 14.5
    }
  }
}
```

##### supplementary

A link from this Range to an Annotation Collection that includes the `supplementing` Annotations of content resources for the Range. Clients might use this to present additional content to the user from a different Canvas when interacting with the Range, or to jump to the next part of the Range within the same Canvas.  For example, the Range might represent a newspaper article that spans non-sequential pages, and then uses the `supplementary` property to reference an Annotation Collection that consists of the Annotations that record the text, split into Annotation Pages per newspaper page. Alternatively, the Range might represent the parts of a manuscript that have been transcribed or translated, when there are other parts that have yet to be worked on. The Annotation Collection would be the Annotations that transcribe or translate, respectively.

The value _MUST_ be a JSON object, which _MUST_ have the `id` and `type` properties, and the `type` _MUST_ be `AnnotationCollection`.

 * A Range _MAY_ have the `supplementary` property.<br/>
   Clients _MAY_ process `supplementary` on a Range.
 * Other types of resource _MUST NOT_ have the `supplementary` property.<br/>
   Clients _SHOULD_ ignore `supplementary` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{ "supplementary": { "id": "https://example.org/iiif/1/annos/1", "type": "AnnotationCollection" } }
```

### Structural Properties


##### items

Much of the functionality of the IIIF Presentation API is simply recording the order in which child resources occur within a parent resource, such as Collections or Manifests within a parent Collection, or Canvases within a Manifest. All of these situations are covered with a single property, `items`.

The value _MUST_ be an array of JSON objects. Each item _MUST_ have the `id` and `type` properties. The items will be resources of different types, as described below.

 * A Collection _MUST_ have the `items` property. Each item _MUST_ be either a Collection or a Manifest.<br/>
   Clients _MUST_ process `items` on a Collection.
 * A Manifest _MUST_ have the `items` property with at least one item. Each item _MUST_ be a Canvas.<br/>
   Clients _MUST_ process `items` on a Manifest.
 * A Canvas _SHOULD_ have the `items` property with at least one item. Each item _MUST_ be an Annotation Page.<br/>
   Clients _MUST_ process `items` on a Canvas.
 * An Annotation Page _SHOULD_ have the `items` property with at least one item. Each item _MUST_ be an Annotation.<br/>
   Clients _MUST_ process `items` on an Annotation Page.
 * A Range _MUST_ have the `items` property with at least one item. Each item _MUST_ be a Range, a Canvas or a Specific Resource where the source is a Canvas.<br/>
   Clients _SHOULD_ process `items` on a Range.
 * Other types of resource _MUST NOT_ have the `items` property.<br/>
   Clients _SHOULD_ ignore `items` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "items": [
    {
      "id": "https://example.org/iiif/manifest1",
      "type": "Manifest"
    },
    {
      "id": "https://example.org/iiif/collection1",
      "type": "Collection"
    }
    // ...
  ]
}
```

##### structures

The structure of an object represented as a Manifest can be described using a hierarchy of Ranges. Ranges can be used to describe the "table of contents" of the object or other structures that the user can interact with beyond the order given by the `items` property of the Manifest. The hierarchy is built by nesting the child Range resources in the `items` array of the higher level Range. The top level Ranges of these hierarchies are given in the `structures` property.

The value _MUST_ be an array of JSON objects. Each item _MUST_ have the `id` and `type` properties, and the `type` _MUST_ be `Range`.

 * A Manifest _MAY_ have the `structures` property.<br/>
   Clients _SHOULD_ process `structures` on a Manifest. The first hierarchy _SHOULD_ be presented to the user by default, and further hierarchies _SHOULD_ be able to be selected as alternative structures by the user.
 * Other types of resource _MUST NOT_ have the `structures` property.<br/>
   Clients _SHOULD_ ignore `structures` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "structures": [
    {
      "id": "https://example.org/iiif/range/1",
      "type": "Range",
      "items": [ { ... } ]
    }
  ]
}
```

##### annotations

An ordered list of Annotation Pages that contain commentary or other Annotations about this resource, separate from the Annotations that are used to paint content on to a Canvas. The `motivation` of the Annotations _MUST NOT_ be `painting`, and the target of the Annotations _MUST_ include this resource or part of it.

The value _MUST_ be an array of JSON objects. Each item _MUST_ have at least the `id` and `type` properties.

 * A Collection _MAY_ have the `annotations` property with at least one item.<br/>
   Clients _SHOULD_ process `annotations` on a Collection.
 * A Manifest _MAY_ have the `annotations` property with at least one item.<br/>
   Clients _SHOULD_ process `annotations` on a Manifest,.
 * A Canvas _MAY_ have the `annotations` property with at least one item.<br/>
   Clients _SHOULD_ process `annotations` on a Canvas.
 * A Range _MAY_ have the `annotations` property with at least one item.<br/>
   Clients _SHOULD_ process `annotations` on a Range.
 * A content resource _MAY_ have the `annotations` property with at least one item.<br/>
   Clients _SHOULD_ process `annotations` on a content resource.
 * Other types of resource _MUST NOT_ have the `annotations` property.<br/>
   Clients _SHOULD_ ignore `annotations` on other types of resource.

{% include api/code_header.html %}
``` json-doc
{
  "annotations": [
    {
      "id": "https://example.org/iiif/annotationPage/1",
      "type": "AnnotationPage",
      "items": [ { ... } ]
    }
  ]
}
```

### 3.5. Values

##### Values for motivation

This specification defines two values for the Web Annotation property of `motivation`, or `purpose` when used on a Specific Resource or Textual Body.

While any resource _MAY_ be the `target` of an Annotation, this specification defines only motivations for Annotations that target Canvases. These motivations allow clients to determine how the Annotation should be rendered, by distinguishing between Annotations that provide the content of the Canvas, from ones with externally defined motivations which are typically comments about the Canvas.

Additional motivations may be added to the Annotation to further clarify the intent, drawn from [extensions][prezi30-ldce] or other sources. Clients _MUST_ ignore motivation values that they do not understand. Other motivation values given in the Web Annotation specification _SHOULD_ be used where appropriate, and examples are given in the [Presentation API Cookbook][annex-cookbook].

| Value | Description |
| ----- | ----------- |
| `painting` | Resources associated with a Canvas by an Annotation that has the `motivation` value `painting`  _MUST_ be presented to the user as the representation of the Canvas. The content can be thought of as being _of_ the Canvas. The use of this motivation with target resources other than Canvases is undefined. For example, an Annotation that has the `motivation` value `painting`, a body of an Image and the target of the Canvas is an instruction to present that Image as (part of) the visual representation of the Canvas. Similarly, a textual body is to be presented as (part of) the visual representation of the Canvas and not positioned in some other part of the user interface.|
| `supplementing` | Resources associated with a Canvas by an Annotation that has the `motivation` value `supplementing`  _MAY_ be presented to the user as part of the representation of the Canvas, or _MAY_ be presented in a different part of the user interface. The content can be thought of as being _from_ the Canvas. The use of this motivation with target resources other than Canvases is undefined. For example, an Annotation that has the `motivation` value `supplementing`, a body of an Image and the target of part of the Canvas is an instruction to present that Image to the user either in the Canvas's rendering area or somewhere associated with it, and could be used to present an easier to read representation of a diagram. Similarly, a textual body is to be presented either in the targeted region of the Canvas or otherwise associated with it, and might be OCR, a manual transcription or a translation of handwritten text, or captions for what is being said in a Canvas with audio content. |
{: .api-table #table-motivations}




The top level resource in the response _MUST_ have the `@context` property, and it _SHOULD_ appear as the very first key/value pair of the JSON representation. This tells Linked Data processors how to interpret the document. The IIIF Presentation API context, below, _MUST_ occur once per response in the top-most resource, and thus _MUST NOT_ appear within [embedded][prezi30-terminology] resources. For example, when embedding a Canvas within a Manifest, the Canvas will not have the `@context` property.

The value of the `@context` property _MUST_ be either the URI `http://iiif.io/api/presentation/{{ page.major }}/context.json` or a JSON array with the URI `http://iiif.io/api/presentation/{{ page.major }}/context.json` as the last item. Further contexts, such as those for local or [registered extensions][registry], _MUST_ be added at the beginning of the array.

{% include api/code_header.html %}
``` json-doc
{
  "@context": "http://iiif.io/api/presentation/{{ page.major }}/context.json"
}
```

Any additional properties beyond those defined in this specification or the Web Annotation Data Model _SHOULD_ be mapped to RDF predicates using further context documents. These extensions _SHOULD_ be added to the top level `@context` property, and _MUST_ be added before the above context. The JSON-LD 1.1 functionality of predicate specific context definitions, known as [scoped contexts][org-w3c-json-ld-scoped-contexts], _MUST_ be used to minimize cross-extension collisions. Extensions intended for community use _SHOULD_ be [registered in the extensions registry][registry], but registration is not mandatory.

{% include api/code_header.html %}
``` json-doc
{
  "@context": [
    "http://example.org/extension/context.json",
    "http://iiif.io/api/presentation/{{ page.major }}/context.json"
  ]
}
```

The JSON representation _MUST NOT_ include the `@graph` key at the top level. This key might be created when serializing directly from RDF data using the JSON-LD 1.0 compaction algorithm. Instead, JSON-LD framing and/or custom code should be used to ensure the structure of the document is as defined by this specification.

### 4.7. Term Collisions between Contexts

There are some common terms used in more than one JSON-LD context document. Every attempt has been made to minimize these collisions, but some are inevitable. In order to know which specification is in effect at any given point, the class of the resource that has the property is the primary governing factor. Thus properties on Annotation based resources use the context from the [Web Annotation Data Model][org-w3c-webanno], whereas properties on classes defined by this specification use the IIIF Presentation API context's definition.

There is one property that is in direct conflict - the `label` property is defined by both and is available for every resource. The use of `label` in IIIF follows modern best practices for internationalization by allowing the language to be associated with the value using the language map construction [described above][prezi30-languages]. The Web Annotation Data Model uses it only for [Annotation Collections][prezi30-annocoll], and mandates the format is a string. For this property, the API overrides the definition from the Annotation model to ensure that labels can consistently be represented in multiple languages.

The following properties are defined by both, and the IIIF representation is more specific than the Web Annotation Data Model but are not in conflict, or are never used on the same resource:

* `homepage`: In IIIF the home page of a resource is represented as a JSON object, whereas in the Web Annotation Data Model it can also be a string.
* `type`: In IIIF the type is singular, whereas in the Web Annotation Data Model there can be more than one type.
* `format`: In IIIF the format of a resource is also singular, whereas in the Web Annotation Data Model there can be more than one format.
* `language`: In IIIF the `language` property always takes an array, whereas in the Web Annotation Data Model it can be a single string.
* `start`: The `start` property is used on a Manifest to refer to the start Canvas or part of a Canvas and thus is a JSON object, whereas in the Web Annotation Data Model it is used on a TextPositionSelector to give the start offset into the textual content and is thus an integer.

The `rights`, `partOf`, and `items` properties are defined by both in the same way.

### 4.8. Keyword Mappings

The JSON-LD keywords `@id`, `@type` and `@none` are mapped to `id`, `type` and `none` by the Presentation API [linked data context][prezi30-ldce]. Thus in content conforming to this version of the Presentation API, the only JSON key beginning with `@` will be `@context`. However, the content may include data conforming to older specifications or external specifications that use keywords beginning with `@`. Clients should expect to encounter both syntaxes.

