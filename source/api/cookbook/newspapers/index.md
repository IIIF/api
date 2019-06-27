---
title: Recipe - Newspapers
layout: spec
tags: [annex, service, services, specifications]
cssversion: 2
---

This is a recipe from the [Presentation API Cookbook][annex-cookbook].


# Newspapers

## Use Case

Newspapers can be described via the IIIF Presentation API in ways that support display, navigation, relationships with OCR and other objects, and search. The [IIIF Image API][image-api] provides the foundation for sharing newspaper images. This recipe describes patterns agreed by the [IIIF Newspapers Community Group][groups-newspapers] to ease implementation and promote interoperability. These patterns include:

  1. Want to support browse through newspapers by date? Use the [`navDate`][prezi30-navdate] property
  2. Want to provide relationship to text files of OCR, ALTO, or other associated text? Use the [`seeAlso`][prezi30-seealso] property
  3. Want to provide viewer-available OCR text associated with newspaper images? Use [Web Annotations][prezi30-anno]
  4. Want to support articles, illustrations, and other sections of a page? Use [Range][prezi30-range] resources
  5. Want to search through text and annotations associated with newspaper images? Implement the [IIIF Search API][search-api] (Note: some IIIF viewers and software may have an annotation server and this option ready-to-go.)
  6. Need to restrict access to images, versions, or reRecommendations? Implement [IIIF Authentication API][auth1] with your local authentication service

## Implementation notes

This scope of this guide provides examples for newspaper implementations in the presentation API to especially enhance access to newspaper content, representing the 6 use cases above. While the [IIIF Image API][image-api] is essential for transfer of image pixels, the [IIIF Presentation API][prezi-api] provides the ability **to indicate structure and viewing order** for complex objects and **supports an annotation layer that is integral for OCR text**.

The guidance below provides an on-ramp for IIIF compatibility for newspapers, highlighting various levels of compliance with the IIIF specifications. Each pattern provides a use-case and recommendations with example excepts.

### Newspaper structure mapped to IIIF

| --- | --- | --- |
| Newspaper Level | IIIF Resource | Notes |
| --- | --- | --- |
| Summary Title / Collection Title / Curated Title / Collection | Collection | Locally defined for user access and to address title changes per serials cataloging |
| Title | Collection | Usually the masthead title |
| Volume | Collection | Locally defined as necessary; often more useful for provenance than user interaction and presentation |
| Issue | Manifest | [`navDate`][prezi30-navdate] recommended for presentation browsing experience |
| Edition | Manifest | [`navDate`][prezi30-navdate] recommended for presentation browsing experience |
| Section | Range | |
| Page | Canvas | |
| Page Text (OCR) | Annotation Page | See [Annotation Page][prezi30-annopage] and [Annotation][prezi30-anno], also [Annotation Collection][prezi30-annocoll] for issue or article level OCR |
| Article | Range | | 
| Illustration | Range | |
| Supplement | Manifest or Range | Locally defined |
| --- | --- | --- |

*Summary Title / Collection Title / Curated Title / Collection* - Local aggregation often used to group like titles for user access and avoid the trappings of succeeding, preceding, and title variants in serials cataloging that can make using digital newspapers disorienting. Note: not equivalent to a Uniform Title.

*Title* - A collection of newspaper issues that are grouped together to form a single publication. Newspapers can change names and publishers but this grouping would link issues into a single publication. Traditionally linked to the $245 field in a MARC catalog record.

*Volume* - A collection of issues which are gathered together, typically in physical form. This historically has been used for issues that are published in a particular year. Note date based volumes like collections of issues published in a year could be created by a viewer using the [`navDate`][prezi30-navdate] for an issue, so a volume designation may not be necessary or only serve provenance purposes. Note: incorrect volumes may or may not be corrected in metadata.

*Issue* - The collection of pages that were published at a particular issuance. Multiple issues of the same Newspaper can be published on the same date. Note: incorrect issues may or may not be corrected in metadata. Some implementations may treat supplements as issues published on the same date as the issue it is associated with.

*Edition* - The textual label of the edition on the piece. Editions vary widely by newspaper and region and may include examples such as: "Late Edition", "Morning Edition", "Special Edition", "Weekend Early Edition", "East Side", and "West Side". Use the [`navDate`][prezi30-navdate] for presentation flow and edition order (e.g. from morning to late editions).

*Section* - A section within a newspaper issue, for example the sports section or supplement included in the newspaper.

*Page* - A page, insert, foldout or other "piece" of a newspaper that is digitized as a single image. "Pages" may link to "Page text" or other annotations.

*Page text* - The text contained within a page usually generated by running optical character recognition software on a newspaper image. This can have coordinates associated with the text to allow a bounding box to be placed on the image where the text appears. Page text can be available at multiple granularities including article, paragraph, line, word and character. The page text may be provided as an [Annotation Page][prezi30-annopage], or as a [`seeAlso`][prezi30-seealso] link to an ALTO file. Examples are provided below. See *FIXME - Text Granularity Extensions for guidancec on different levels of text for the same annotation*.

*Articles and Illustrations* - A collection of text areas on a page that are related. Examples include News article, advertising, family notices, cartoons etc. In the current model articles can cross pages but not issues. Articles have text and coordinates which highlight the areas of a page which relate to an article. Articles can have metadata like title, author or type.

*Supplements* - Supplements come in a variety of forms for newspapers. Local practice and a particular instance will determine if supplements should be treated as their own issue and a manifest or a range within an issue.

### `navDate` for Issue Date and Edition Order

*Use case:* I want to browse newspapers published between certain dates. I want to browse through issues of a newspaper in chronological order.

*Recommendation:* Newspapers should provide a `navDate` property in the issue level Manifest. See [`navDate`][prezi30-navdate] and the example below:

```
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/3/context.json"
  ],
  "id": "http://dams.llgc.org.uk/iiif/newspaper/issue/3100021/manifest.json",
  "type": "Manifest",
  "label": { "en": [ "Potter's electric news (1859-01-05)" ] },
  "navDate": "1859-01-05T00:00:00Z", 
  "items": [
    ...
  ]
}
```

IIIF Collections for newspaper titles may also have a `navDate` in the Manifest section, for example:

``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/3/context.json"
  ],
  "id": "http://dams.llgc.org.uk/iiif/newspaper/collection.json",
  "type": "Collection",
  "label": { "en": [ "Potter's electric news" ] },
  "navDate": "1850-01-01T00:00:00Z",
  "items": [
    ...
  ]
}
```

For Editions, a temporal value can be inserted to enforce navigation order. `navDate` is, by definition, not an assertion of when an issue was published, therefore, you can use a 06:00 timestamp for a morning edition and a 17:00 for an evening edition to provide browse order.

### Linking to Text

*Use case:* I would like to be able to link to OCR for a Newspaper page. The OCR may contain information not contained in Annotations (e.g. OCR confidence in ALTO).

*Recommendation:* It is possible to link OCR documents to a IIIF canvas by adding a [`seeAlso`][prezi30-seealso] property on the appropriate [Canvas][prezi30-canvas]. Examples for ALTO, hOCR, and plain text:

ALTO:

``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/3/context.json"
  ],
  ...
  "seeAlso": {
     "id": "http://wellcomelibrary.org/service/alto/b19956435/0?image=0",
     "type": "Text",
     "format": "application/xml",
     "profile": "http://www.loc.gov/standards/alto/",
     "label": { "en": [ "ALTO XML" ] }
  }
}
```

hOCR:

``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/3/context.json"
  ],
  ...
  "seeAlso": [ {
    "id": "https://ocr.lib.ncsu.edu/ocr/nu/nubian-message-2003-04-01_0002/nubian-message-2003-04-01_0002.hocr",
    "type": "Text",
    "format": "text/vnd.hocr+html",
    "profile": "https://github.com/kba/hocr-spec/blob/master/hocr-spec.md",
    "label": { "en": [ "hOCR" ] }
  }
}
```

Plain text:

``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/3/context.json"
  ],
  ...
  "seeAlso": [ {
    "id": "https://ocr.lib.ncsu.edu/ocr/nu/nubian-message-2003-04-01_0002/nubian-message-2003-04-01_0002.txt",
    "type": "Text",
    "format": "text/plain",
    "label": { "en": [ "plain text OCR" ] }
  }
}
```

### Providing Text as Annotations

*Use case:* I want text associated with areas of an image, including OCR and transcription.

*Recommendation:* Use Annotation Pages of Annotations. The following example is a page of word-level annotation:

``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/3/context.json"
  ],
  "id": "http://dams.llgc.org.uk/iiif/4342443/annotation/list/ART8.json",
  "type": "AnnotationPage",
  "resources": [
    {
      "id": "http://dams.llgc.org.uk/iiif/4342443/annotation/2003468828629",
      "type": "Annotation",
      "motivation": "painting",
      "body": {
         "type": "TextualBody",
         "value": "SIEraOROLlOIO,At"
      },
      "target": "http://dams.llgc.org.uk/iiif/4342439/canvas/4342443#xywh=2003,4688,286,29"
    },
    {
      "id":"http://dams.llgc.org.uk/iiif/4342443/annotation/2308468424928",
      "type":"Annotation",
      "motivation":"painting",
      "body": {
        "type": "TextualBody",
        "value": "OBSERVATIONS"
      },
      "target": {
        "type": "SpecificResource",
        "source": "http://dams.llgc.org.uk/iiif/4342439/canvas/4342443",
        "selector": {
          "type": "FragmentSelector",
          "value": "xywh=588,2844,9951,10412"
        }
      }
    },
```

### Giving access to OCR text as paragraphs, lines and words

*Use case:* I would like to share multiple versions of the same annotation list with different specificities so for example I might have:
  * a word level annotation list for harvesting by Europeana
  * a line level annotation list for use in Mirador
  * a paragraph annotation list for OCR correction.
I would like to be able to link to these options to allow the client to decide which ones they want to use.

*Recommendation:* FIXME -- need extension to implement outputs of Text Granularity Working Group, see <https://github.com/IIIF/api/issues/758>.

### Encoding Newspaper Articles

*Use case:* I would like to display the articles contained in a newspaper page including any OCR text associated with that article.

*Recommendation:* Articles should be modeled by adding a Range to the issue Manifest. The `items` list  of the range should include all SpecificResources representing areas of the Canvas that are part of this article. The `supplementing` property is used to link to the Annotation Collection for the article's OCR annotations.

``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/3/context.json"
  ],
  "id": "http://dams.llgc.org.uk/iiif/newspapers/3100020.json",
  "type": "Manifest",
  ...
  "structures": [
    { 
      "id": "http://dams.llgc.org.uk/iiif/3100021/article/ART1",
      "type": "Range",
      "label": { "en": [ "Rousing the Bees" ] },
      "items": [
        {
          "type": "SpecificResource",
          "source": "http://dams.llgc.org.uk/iiif/3100021/canvas/3100022",
          "selector": {
            "type": "FragmentSelector",
            "value": "xywh=588,2844,9951,10412"
          }
        },
        {
          "type": "SpecificResource",
          "source": "http://dams.llgc.org.uk/iiif/3100021/canvas/3100022",
            "selector": {
            "type": "FragmentSelector",
            "value": "xywh=12588,5600,10256,20400"
          }
        }
      ],
      "supplementary": {
        "id": "http://dams.llgc.org.uk/iiif/3100021/annocoll/article1.json",
        "type": "AnnotationCollection",
        "label": { "en": [ "Rousing the Bees - OCR Article Text" ] }
      }
    }
  ]
}
```

Canvases can link to the annotations that are contained in page by:

``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/3/context.json"
  ],
  ...
  "otherContent": [  FIXME -- UPDATE FOR 3.0
    {
       "id": "http://dams.llgc.org.uk/iiif/3100022/annotation/list/ART1.json",
       "type": "AnnotationList",
       "label": { "en": [ "Rousing the Bees" ] },
       "within": {
          "id": "http://dams.llgc.org.uk/iiif/3100021/annotation/layer/ART1.json",
          "type": "sc:Layer",
          "label": { "en": [ "OCR Article Text" ] }
       }
    },
    ...
  ]
}
```

### Linking to article text that crosses pages or appears in different sections on a single page

*Use case:* Some of my newspaper articles span across pages and I would like to reflect this using IIIF.

*Recommendation:* Use a Range within your structures to represent the aritcle. In the `items` property list out each of the canvas fragments as a SpecificResource that belong to the article. The following is an example if the article split across two pages, with an associated AnnotationCollection for the article's OCR:

``` json-doc
{
  "@context": [
    "http://www.w3.org/ns/anno.jsonld",
    "http://iiif.io/api/presentation/3/context.json"
  ],
  ...
  "structures": [
    { 
      "id": "http://dams.llgc.org.uk/iiif/3100021/article/ART1",
      "type": "Range",
      "label": { "en": [ "Letters to the Editor" ] },
      "items": [
        {
          "type": "SpecificResource",
          "source": "http://dams.llgc.org.uk/iiif/3100021/canvas/page1",
            "selector": {
            "type": "FragmentSelector",
            "value": "xywh=588,2844,9951,20412"
          }
        },
        {
          "type": "SpecificResource",
          "source": "http://dams.llgc.org.uk/iiif/3100021/canvas/page2",
          "selector": {
            "type": "FragmentSelector",
            "value": "xywh=0,0,100,100"
          }
        }
      ],
      "supplementary": {
        "id": "http://dams.llgc.org.uk/iiif/3100021/annocoll/article1.json",
        "type": "AnnotationCollection",
        "label": { "en": [ "OCR Article Text" ] }
      }
    }
  ]
  ...
}
```

## Restrictions

FIXME -- When is this pattern is usable / not usable? Is it deprecated? If it uses multiple specifications, which versions are needed, etc.? (Not present if not needed.)

## Example

FIXME - Need to make a complete working example demonstrating features above.

# Related recipes

  * FIXME - Provide a bulleted list of related recipes and why they are relevant.

{% include acronyms.md %}
{% include links.md %}

